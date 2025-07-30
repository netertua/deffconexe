from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QListWidget, QMessageBox, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt

class GuiDesignerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual GUI Designer")
        self.setMinimumSize(600, 400)

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Sol: widget paleti
        self.widget_palette = QListWidget()
        self.widget_palette.addItems(["QPushButton", "QLabel", "QLineEdit", "QComboBox"])
        self.main_layout.addWidget(self.widget_palette, 1)

        # Orta: tasarım alanı (basit çerçeve)
        self.design_area = QFrame()
        self.design_area.setFrameShape(QFrame.Box)
        self.design_area.setMinimumSize(400, 400)
        self.design_area.setLayout(QVBoxLayout())
        self.main_layout.addWidget(self.design_area, 3)

        # Sağ: özellikler ve kod üretme
        self.prop_layout = QVBoxLayout()

        self.btn_add_widget = QPushButton("Seçili Widget Ekle")
        self.btn_add_widget.clicked.connect(self.add_widget_to_design)
        self.prop_layout.addWidget(self.btn_add_widget)

        self.btn_generate_code = QPushButton("Tasarımdan Kod Üret")
        self.btn_generate_code.clicked.connect(self.generate_code)
        self.prop_layout.addWidget(self.btn_generate_code)

        self.code_output = QLabel("Oluşan Kod Gösterimi (konsol veya ayrı pencereye eklenebilir)")
        self.prop_layout.addWidget(self.code_output)

        self.main_layout.addLayout(self.prop_layout, 2)

        self.widgets_in_design = []

    def add_widget_to_design(self):
        current_item = self.widget_palette.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir widget seçin!")
            return
        widget_type = current_item.text()

        if widget_type == "QPushButton":
            w = QPushButton("Yeni Buton")
        elif widget_type == "QLabel":
            w = QLabel("Yeni Label")
        elif widget_type == "QLineEdit":
            w = QLineEdit()
        elif widget_type == "QComboBox":
            w = QComboBox()
            w.addItems(["Seçenek 1", "Seçenek 2"])
        else:
            QMessageBox.warning(self, "Uyarı", "Desteklenmeyen widget!")
            return

        self.design_area.layout().addWidget(w)
        self.widgets_in_design.append((widget_type, w))
    
    def generate_code(self):
        # Basit örnek: sadece widget tiplerini ve default isimleri yazdırır
        code_lines = [
            "from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox",
            "app = QApplication([])",
            "window = QWidget()",
            "layout = QVBoxLayout()",
            "window.setLayout(layout)"
        ]

        for idx, (wtype, widget) in enumerate(self.widgets_in_design):
            name = f"widget_{idx}"
            if wtype == "QPushButton":
                code_lines.append(f"{name} = QPushButton('{widget.text()}')")
            elif wtype == "QLabel":
                code_lines.append(f"{name} = QLabel('{widget.text()}')")
            elif wtype == "QLineEdit":
                code_lines.append(f"{name} = QLineEdit()")
            elif wtype == "QComboBox":
                code_lines.append(f"{name} = QComboBox()")
                # Örnek olarak sabit 2 seçenek
                code_lines.append(f"{name}.addItems(['Seçenek 1', 'Seçenek 2'])")
            code_lines.append(f"layout.addWidget({name})")

        code_lines.append("window.show()")
        code_lines.append("app.exec()")

        code_str = "\n".join(code_lines)
        self.code_output.setText(f"<pre>{code_str}</pre>")
        print(code_str)  # İstersen dosyaya yazdırma eklenebilir

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    designer = GuiDesignerWidget()
    designer.show()
    sys.exit(app.exec())
