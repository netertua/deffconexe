from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QComboBox, QLineEdit, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt

class SingleLLMWidget(QWidget):
    def __init__(self, llm_name):
        super().__init__()
        self.llm_name = llm_name
        self.init_ui()

        self.conversation_history = []  # (prompt, response) pairs
        self.prompt_preprocessing_text = ""

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(f"<b>{self.llm_name} LLM Settings</b>")
        layout.addWidget(title)

        # Host input
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.host_input = QLineEdit("http://localhost")
        host_layout.addWidget(self.host_input)
        layout.addLayout(host_layout)

        # Port input
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit("11434")
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)

        # Role input (e.g., main, refiner, supervisor)
        role_layout = QHBoxLayout()
        role_layout.addWidget(QLabel("Role:"))
        self.role_input = QLineEdit(self.llm_name.lower())
        role_layout.addWidget(self.role_input)
        layout.addLayout(role_layout)

        # Prompt Preprocessing
        pp_group = QGroupBox("Prompt Preprocessing (Her sorgu öncesi uygulanır)")
        pp_layout = QVBoxLayout()
        self.pp_textedit = QTextEdit()
        self.pp_textedit.setPlaceholderText("Buraya sorgudan önce eklenecek metni yaz...")
        pp_layout.addWidget(self.pp_textedit)
        pp_group.setLayout(pp_layout)
        layout.addWidget(pp_group)

        # Conversation history (readonly)
        hist_group = QGroupBox("Konuşma Geçmişi")
        hist_layout = QVBoxLayout()
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        hist_layout.addWidget(self.history_text)

        clear_btn = QPushButton("Konuşma Geçmişini Sıfırla")
        clear_btn.clicked.connect(self.clear_history)
        hist_layout.addWidget(clear_btn)

        hist_group.setLayout(hist_layout)
        layout.addWidget(hist_group)

        self.setLayout(layout)

    def clear_history(self):
        self.conversation_history.clear()
        self.history_text.clear()

    def get_settings(self):
        return {
            "host": self.host_input.text(),
            "port": self.port_input.text(),
            "role": self.role_input.text(),
            "prompt_preprocessing": self.pp_textedit.toPlainText()
        }

    def add_to_history(self, prompt, response):
        self.conversation_history.append((prompt, response))
        self.history_text.append(f">>> {prompt}\n{response}\n")

class LLMManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM Manager - 3 LLM Control")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.llm_main = SingleLLMWidget("Main")
        self.llm_refiner = SingleLLMWidget("Refiner")
        self.llm_supervisor = SingleLLMWidget("Supervisor")

        layout.addWidget(self.llm_main)
        layout.addWidget(self.llm_refiner)
        layout.addWidget(self.llm_supervisor)

        # Test button for demonstration: Show all settings
        test_btn = QPushButton("LLM Ayarlarını Göster")
        test_btn.clicked.connect(self.show_all_settings)
        layout.addWidget(test_btn)

        self.setLayout(layout)

    def show_all_settings(self):
        main_settings = self.llm_main.get_settings()
        refiner_settings = self.llm_refiner.get_settings()
        supervisor_settings = self.llm_supervisor.get_settings()

        msg = (
            f"Main LLM:\n{main_settings}\n\n"
            f"Refiner LLM:\n{refiner_settings}\n\n"
            f"Supervisor LLM:\n{supervisor_settings}"
        )
        QMessageBox.information(self, "LLM Ayarları", msg)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LLMManagerWindow()
    window.show()
    sys.exit(app.exec())
