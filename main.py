import sys
from PySide6.QtWidgets import QApplication

from menu_func.login_reg_func import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
