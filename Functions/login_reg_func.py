import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from Functions.dashboard_func import MainWindow
from database import Database
from Utils.utils_corner import applyRoundedCorners

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.login_screen = self.load_ui("UI/AuthPages/login.ui")
        self.setCentralWidget(self.login_screen)

        # Set up login UI
        self.setFixedSize(1080, 720)
        self.setWindowTitle("MaPro - Marigondon Records & Statistics System")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_auth.ico"))

        # Set images
        self.login_screen.login_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        self.login_screen.login_imagePattern.setPixmap(QPixmap("Assets/Images/img_newloginpattern.png"))
        self.login_screen.login_imageAppIcon.setPixmap(QPixmap("Assets/Images/img_mainappicon.png"))

        applyRoundedCorners(
            self.login_screen.login_imagePattern,
            radius_top_left=20,
            radius_bottom_left=20,
            radius_top_right=0,
            radius_bottom_right=0,
        )

        # Connect login button
        self.login_screen.login_buttonLogin.clicked.connect(self.login_button_clicked)
        self.login_screen.login_fieldPin.returnPressed.connect(self.login_button_clicked) # Pin Field : Enter to Login
        self.login_screen.login_fieldEmp_id.returnPressed.connect(self.login_button_clicked) # Emp_ID Field : Enter to Login

    def load_ui(self, ui_path):
        """Utility function to load a .ui file."""
        file = QFile(ui_path)
        file.open(QFile.ReadOnly)
        ui = self.loader.load(file, None)
        file.close()
        return ui

    def login_button_clicked(self):
        """Handle login button click."""

        # Get input values and strip whitespace
        emp_id = self.login_screen.login_fieldEmp_id.text().strip()
        emp_pin = self.login_screen.login_fieldPin.text().strip()

        # Check if either field is empty and show appropriate message
        # Check if either field contains only numeric characters
        if not emp_id and not emp_pin:
            QMessageBox.warning(self, "Login Error", "Employee ID and PIN are required!")
            return
        elif not emp_id:
            QMessageBox.warning(self, "Login Error", "Employee ID is required!")
            return
        elif not emp_id.isdigit():
            QMessageBox.warning(self, "Login Error", "Invalid Employee ID! It must be numeric.")
            return
        elif not emp_pin:
            QMessageBox.warning(self, "Login Error", "PIN is required!")
            return
        elif not emp_pin.isdigit():
            QMessageBox.warning(self, "Login Error", "Invalid PIN! It must be numeric.")
            return

        print("-- Login Attempt")
        print("Employee ID:", self.login_screen.login_fieldEmp_id.text(),
              " PIN:", self.login_screen.login_fieldPin.text())

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
        if employee:
            self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico")) # Will set the Application Icon as Active.
            QMessageBox.information(self, "Success", "Login successful!")
            emp_first_name = employee[2]
            self.main_window = MainWindow(self, emp_first_name)
            self.main_window.show()
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
