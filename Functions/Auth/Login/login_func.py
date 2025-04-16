from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from Functions.Main.Dashboard.dashboard_func import dashboard_func
from database import Database
from Utils.utils_corner import applyRoundedCorners


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.login_screen = self.load_ui("UI/AuthPages/login.ui")
        self.setCentralWidget(self.login_screen)

        self.SUPER_ADMIN_ID = 1
        self.SUPER_ADMIN_PIN = "123"

        self.setFixedSize(1080, 720)
        self.setWindowTitle("MaPro - Marigondon Records & Statistics System")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_auth.ico"))

        self.setup_images()
        self.setup_rounded_corners()
        self.setup_event_handlers()

    def load_ui(self, ui_path):
        file = QFile(ui_path)
        if not file.open(QFile.ReadOnly):
            raise IOError(f"Cannot open {ui_path}: {file.errorString()}")
        ui = self.loader.load(file, None)
        file.close()
        return ui

    def setup_images(self):
        self.login_screen.login_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        self.login_screen.login_imagePattern.setPixmap(QPixmap("Assets/Images/img_newloginpattern.png"))
        self.login_screen.login_imageAppIcon.setPixmap(QPixmap("Assets/Images/img_mainappicon.png"))

    def setup_rounded_corners(self):
        applyRoundedCorners(
            self.login_screen.login_imagePattern,
            radius_top_left=20,
            radius_bottom_left=20,
            radius_top_right=0,
            radius_bottom_right=0,
        )

    def setup_event_handlers(self):
        self.login_screen.login_buttonLogin.clicked.connect(self.handle_login)
        self.login_screen.login_fieldPin.returnPressed.connect(self.handle_login)
        self.login_screen.login_fieldEmp_id.returnPressed.connect(self.handle_login)

    def handle_login(self):
        user_id = self.login_screen.login_fieldEmp_id.text().strip()
        user_pin = self.login_screen.login_fieldPin.text().strip()

        if not self.validate_inputs(user_id, user_pin):
            return

        if self.check_super_admin(user_id, user_pin):
            self.grant_access("admin")
            return

        self.authenticate_regular_user(user_id, user_pin)

    def validate_inputs(self, user_id, user_pin):
        if not user_id and not user_pin:
            QMessageBox.warning(self, "Login Error", "Employee ID and PIN are required!")
            return False
        if not user_id:
            QMessageBox.warning(self, "Login Error", "Employee ID is required!")
            return False
        if not user_pin:
            QMessageBox.warning(self, "Login Error", "PIN is required!")
            return False
        if not user_id.isdigit():
            QMessageBox.warning(self, "Login Error", "Invalid Employee ID! It must be numeric.")
            return False
        if not user_pin.isdigit():
            QMessageBox.warning(self, "Login Error", "Invalid PIN! It must be numeric.")
            return False
        return True

    def check_super_admin(self, user_id, user_pin):
        try:
            return (int(user_id) == self.SUPER_ADMIN_ID and
                    user_pin == self.SUPER_ADMIN_PIN)
        except ValueError:
            return False

    def authenticate_regular_user(self, user_id, user_pin):
        print(f"-- Login Attempt\nSystem User ID: {user_id}\nSystem User PIN: {user_pin}")

        try:
            connection = Database()
            cursor = connection.cursor

            query = """
            SELECT SYS_USER_FIRSTNAME 
            FROM SYSTEM_ACCOUNT 
            WHERE SYS_USER_ID = %s AND SYS_USER_PIN = %s
            """
            cursor.execute(query, (user_id, user_pin))
            result = cursor.fetchone()

            if result:
                self.grant_access(result[0])
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials")
                self.clear_fields()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error occurred while authenticating: {str(e)}")
        finally:
            if 'connection' in locals():
                connection.close()

    def grant_access(self, first_name):
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))
        QMessageBox.information(self, "Success", "Login successful!")
        dashboard_func(self, first_name).show()
        self.close()

    def clear_fields(self):
        self.login_screen.login_fieldEmp_id.clear()
        self.login_screen.login_fieldPin.clear()