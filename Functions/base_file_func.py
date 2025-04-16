from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class base_file_func(QMainWindow):
    def __init__(self, login_window, emp_first_name):
        super().__init__()
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.loader = QUiLoader()

    def center_on_screen(self):
        center_point = QApplication.primaryScreen().availableGeometry().center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def load_ui(self, ui_path):
        file = QFile(ui_path)
        if not file.exists():
            print(f"Error: UI file not found: {ui_path}")
            return None
        file.open(QFile.ReadOnly)
        ui = self.loader.load(file, None)
        file.close()
        return ui


