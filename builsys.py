import os
import subprocess
import threading
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTextEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Signal, QObject

class BuildWorker(QObject):
    progress_signal = Signal(int)        # Yüzde olarak ilerleme
    log_signal = Signal(str)             # Build loglarını iletmek için
    finished_signal = Signal(bool)       # Build bittiğinde True gönderir

    def __init__(self, source_path: str, output_path: str):
        super().__init__()
        self.source_path = source_path
        self.output_path = output_path

    def run(self):
        """
        PyInstaller ile build komutunu çalıştırır.
        stdout ve stderr çıktısını toplayıp GUI'ye gönderir.
        """
        command = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            f"--distpath={self.output_path}",
            self.source_path
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in process.stdout:
            line = line.strip()
            self.log_signal.emit(line)
            # İlerleme tespiti (basit bir örnek)
            if "Building EXE" in line:
                self.progress_signal.emit(60)
            elif "completed successfully" in line:
                self.progress_signal.emit(100)

        process.wait()
        success = (process.returncode == 0)
        self.finished_signal.emit(success)


class BuildSystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Build Sistemi")

        self.layout = QVBoxLayout()

        self.label_source = QLabel("Kaynak .py dosyası:")
        self.layout.addWidget(self.label_source)

        self.btn_select_source = QPushButton("Dosya Seç")
        self.btn_select_source.clicked.connect(self.select_source_file)
        self.layout.addWidget(self.btn_select_source)

        self.label_output = QLabel("Çıktı Klasörü:")
        self.layout.addWidget(self.label_output)

        self.btn_select_output = QPushButton("Klasör Seç")
        self.btn_select_output.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.btn_select_output)

        self.btn_build = QPushButton("Build Başlat")
        self.btn_build.clicked.connect(self.start_build)
        self.layout.addWidget(self.btn_build)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)

        self.source_path = None
        self.output_path = None
        self.build_thread = None
        self.build_worker = None

    def select_source_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Kaynak Python Dosyasını Seç", "", "Python Files (*.py)")
        if file_path:
            self.source_path = file_path
            self.label_source.setText(f"Kaynak .py dosyası: {file_path}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Çıktı Klasörü Seç")
        if folder:
            self.output_path = folder
            self.label_output.setText(f"Çıktı Klasörü: {folder}")

    def start_build(self):
        if not self.source_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen kaynak .py dosyasını seçin!")
            return
        if not self.output_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen çıktı klasörünü seçin!")
            return

        self.progress_bar.setValue(0)
        self.log_output.clear()
        self.btn_build.setEnabled(False)

        self.build_worker = BuildWorker(self.source_path, self.output_path)
        self.build_worker.progress_signal.connect(self.update_progress)
        self.build_worker.log_signal.connect(self.append_log)
        self.build_worker.finished_signal.connect(self.build_finished)

        self.build_thread = threading.Thread(target=self.build_worker.run, daemon=True)
        self.build_thread.start()

    def update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def append_log(self, text: str):
        self.log_output.append(text)

    def build_finished(self, success: bool):
        self.btn_build.setEnabled(True)
        if success:
            QMessageBox.information(self, "Build Başarılı", "Build işlemi başarıyla tamamlandı!")
        else:
            QMessageBox.critical(self, "Build Hatası", "Build sırasında hata oluştu!")

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = BuildSystemWidget()
    w.show()
    sys.exit(app.exec())
