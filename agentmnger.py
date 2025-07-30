from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QComboBox, QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt

class Agent:
    def __init__(self, name, role, linked_llm):
        self.name = name
        self.role = role  # Ör: "Build", "Memory", "Optimizer", "Scraper", "GUI Designer"
        self.linked_llm = linked_llm  # "Main", "Refiner", "Supervisor"

    def __str__(self):
        return f"{self.name} [{self.role}] (LLM: {self.linked_llm})"


class AgentManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agent Manager")
        self.agents = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Agent list
        self.agent_list_widget = QListWidget()
        main_layout.addWidget(QLabel("Agent Listesi:"))
        main_layout.addWidget(self.agent_list_widget)

        # Add new agent section
        add_group = QGroupBox("Yeni Agent Ekle")
        add_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Agent Adı")

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Build", "Memory", "Optimizer", "Scraper", "GUI Designer"])

        self.llm_combo = QComboBox()
        self.llm_combo.addItems(["Main", "Refiner", "Supervisor"])

        self.add_btn = QPushButton("Agent Ekle")
        self.add_btn.clicked.connect(self.add_agent)

        add_layout.addWidget(QLabel("İsim:"))
        add_layout.addWidget(self.name_input)
        add_layout.addWidget(QLabel("Görev:"))
        add_layout.addWidget(self.role_combo)
        add_layout.addWidget(QLabel("LLM Bağlantısı:"))
        add_layout.addWidget(self.llm_combo)
        add_layout.addWidget(self.add_btn)
        add_group.setLayout(add_layout)
        main_layout.addWidget(add_group)

        # Remove agent button
        self.remove_btn = QPushButton("Seçili Agentı Sil")
        self.remove_btn.clicked.connect(self.remove_selected_agent)
        main_layout.addWidget(self.remove_btn)

        self.setLayout(main_layout)

    def add_agent(self):
        name = self.name_input.text().strip()
        role = self.role_combo.currentText()
        linked_llm = self.llm_combo.currentText()

        if not name:
            QMessageBox.warning(self, "Hata", "Lütfen agent adı girin!")
            return

        # Check for duplicate agent name
        for agent in self.agents:
            if agent.name == name:
                QMessageBox.warning(self, "Hata", "Bu isimde bir agent zaten var!")
                return

        new_agent = Agent(name, role, linked_llm)
        self.agents.append(new_agent)
        self.refresh_agent_list()
        self.name_input.clear()

    def refresh_agent_list(self):
        self.agent_list_widget.clear()
        for agent in self.agents:
            item = QListWidgetItem(str(agent))
            self.agent_list_widget.addItem(item)

    def remove_selected_agent(self):
        selected_items = self.agent_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için bir agent seçin!")
            return
        for item in selected_items:
            idx = self.agent_list_widget.row(item)
            del self.agents[idx]
        self.refresh_agent_list()

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AgentManagerWindow()
    window.show()
    sys.exit(app.exec())
