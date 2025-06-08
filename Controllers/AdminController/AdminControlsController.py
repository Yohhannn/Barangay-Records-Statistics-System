from PySide6.QtWidgets import QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class AdminControlsController(QWidget):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__()
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        self.sys_user_id = sys_user_id
        self.user_role = user_role
        self.stack = stack

        loader = QUiLoader()
        file = QFile("Resources/UIs/AdminPages/AdminPanel/AdminControls/admincontrols.ui")
        file.open(QFile.ReadOnly)
        self.admin_controls_screen = loader.load(file, None)
        file.close()