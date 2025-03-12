import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from menu_func.dashboard_func import MainWindow
from database import Database
from Utils.utils_corner import applyRoundedCorners

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.login_screen = self.load_ui("UI/login.ui")
        self.setCentralWidget(self.login_screen)

        # Set up login UI
        self.setFixedSize(1080, 720)
        self.setWindowTitle("Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/Icons/icon_main.png"))

        # Set images
        self.login_screen.login_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgy.png"))
        self.login_screen.login_imagePattern.setPixmap(QPixmap("Assets/Images/image_pattern.png"))
        applyRoundedCorners(
            self.login_screen.login_imagePattern,
            radius_top_left=20,
            radius_bottom_left=20,
            radius_top_right=0,
            radius_bottom_right=0,
        )

        # Connect login button
        self.login_screen.login_buttonLogin.clicked.connect(self.login_button_clicked)

    def load_ui(self, ui_path):
        """Utility function to load a .ui file."""
        file = QFile(ui_path)
        file.open(QFile.ReadOnly)
        ui = self.loader.load(file, None)
        file.close()
        return ui

    def login_button_clicked(self):
        """Handle login button click."""
        print("-- Login Attempt")
        print("Employee ID:", self.login_screen.login_fieldEmp_id.text(),
              " PIN:", self.login_screen.login_fieldPin.text())

        emp_id = self.login_screen.login_fieldEmp_id.text()
        emp_pin = self.login_screen.login_fieldPin.text()

        connection = Database()
        cursor = connection.cursor
        try:
            cursor.execute("SELECT * FROM employee WHERE emp_id = %s AND emp_pin = %s", (emp_id, emp_pin))
            employee = cursor.fetchone()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error occurred while fetching data: {e}")
        finally:
            connection.close()

        # Open Main Application (Dashboard + Citizen Profiles and other .ui)
        if emp_id == "123" and emp_pin == "123":
            main_window = MainWindow(self)  # Pass self as login_window
            main_window.show()
            self.close()
        elif employee:
            QMessageBox.information(self, "Success", "Login successful!")
            main_window = MainWindow(self)  # Pass self as login_window
            main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

        self.login_screen.login_fieldEmp_id.clear()
        self.login_screen.login_fieldPin.clear()

# Ensure QApplication is only created in the main script
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
