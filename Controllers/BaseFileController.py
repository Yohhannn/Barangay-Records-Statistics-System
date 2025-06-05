from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class BaseFileController(QMainWindow):
    def __init__(self, login_window, emp_first_name, sys_user_id):
        super().__init__()
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        self.sys_user_id = sys_user_id
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.loader = QUiLoader()

    def center_on_screen(self):
        """Center the window on the primary screen"""
        screen = QApplication.primaryScreen().availableGeometry()
        window_size = self.frameGeometry()
        self.move(
            (screen.width() - window_size.width()) // 2,
            (screen.height() - window_size.height()) // 2
        )

    def load_ui(self, ui_path):
        """Load a UI file from the given path"""
        file = QFile(ui_path)
        if not file.exists():
            print(f"Error: UI file not found: {ui_path}")
            return None
        if not file.open(QFile.ReadOnly):
            print(f"Error: Cannot open {ui_path}: {file.errorString()}")
            return None
        ui = self.loader.load(file, None)
        file.close()
        return ui

    def show(self):
        """Override show method to center the window"""
        super().show()
        self.center_on_screen()