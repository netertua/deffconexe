import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QAction, QMenuBar, QMessageBox
)
from PySide6.QtGui import QIcon

# Her pencere ayrı modülde
from llm_manager import LLMManagerWindow
from agent_manager import AgentManagerWindow
from gui_designer import GUIDesignerWindow
from build_system import BuildSystemWindow
from memory_manager import MemoryWindow
from internet_scraper import InternetScraperWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM GUI System - Full Integration")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("ui/icons/app.png"))

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        # LLM Menu
        llm_menu = menubar.addMenu("LLM")
        open_llm_mgr = QAction("LLM Manager", self)
        open_llm_mgr.triggered.connect(self.open_llm_manager)
        llm_menu.addAction(open_llm_mgr)

        # Agent Menu
        agent_menu = menubar.addMenu("Agents")
        open_agent_mgr = QAction("Agent Manager", self)
        open_agent_mgr.triggered.connect(self.open_agent_manager)
        agent_menu.addAction(open_agent_mgr)

        # Build Menu
        build_menu = menubar.addMenu("Build")
        open_build = QAction("Build System", self)
        open_build.triggered.connect(self.open_build_window)
        build_menu.addAction(open_build)

        # GUI Designer
        gui_menu = menubar.addMenu("GUI")
        open_gui_designer = QAction("Visual GUI Designer", self)
        open_gui_designer.triggered.connect(self.open_gui_designer)
        gui_menu.addAction(open_gui_designer)

        # Memory Menu
        mem_menu = menubar.addMenu("Memory")
        open_memory = QAction("Memory System", self)
        open_memory.triggered.connect(self.open_memory_window)
        mem_menu.addAction(open_memory)

        # Internet Tools
        web_menu = menubar.addMenu("Internet")
        open_browser = QAction("GitHub / Scraper", self)
        open_browser.triggered.connect(self.open_internet_scraper)
        web_menu.addAction(open_browser)

    # Her pencere bir sekme olarak açılır
    def open_llm_manager(self):
        llm_tab = LLMManagerWindow()
        self.tabs.addTab(llm_tab, "LLM Manager")

    def open_agent_manager(self):
        agent_tab = AgentManagerWindow()
        self.tabs.addTab(agent_tab, "Agent Manager")

    def open_build_window(self):
        build_tab = BuildSystemWindow()
        self.tabs.addTab(build_tab, "Build System")

    def open_gui_designer(self):
        gui_tab = GUIDesignerWindow()
        self.tabs.addTab(gui_tab, "GUI Designer")

    def open_memory_window(self):
        memory_tab = MemoryWindow()
        self.tabs.addTab(memory_tab, "Memory")

    def open_internet_scraper(self):
        scraper_tab = InternetScraperWindow()
        self.tabs.addTab(scraper_tab, "Internet Tools")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
