import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from Utils.utils_corner import applyRoundedCorners


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize QStackedWidget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Load the UI files
        self.loader = QUiLoader()
        self.login_screen = self.load_ui("UI/login.ui")
        self.dashboard_screen = self.load_ui("UI/dashboard.ui")
        self.citizen_profile_screen = self.load_ui("UI/citizenprofile.ui")

        # Add the screens to the stack
        self.stack.addWidget(self.login_screen)  # Index 0
        self.stack.addWidget(self.dashboard_screen)  # Index 1
        self.stack.addWidget(self.citizen_profile_screen)  # Index 2

        # Flags to track signal initialization
        self.login_initialized = False
        self.dashboard_initialized = False
        self.citizen_profile_initialized = False

        # Setup initial screen
        self.setup_login_ui()
        self.stack.setCurrentIndex(0)  # Show login screen

    def load_ui(self, ui_path):
        """Utility function to load a .ui file."""
        file = QFile(ui_path)
        file.open(QFile.ReadOnly)
        ui = self.loader.load(file, None)
        file.close()
        return ui

    def setup_login_ui(self):
        """Setup the login UI layout and connect buttons."""
        self.setFixedSize(1080, 720)  # Set size for login screen
        self.setWindowTitle("Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/icon_main.png"))

        # Set images
        self.login_screen.login_imageLogo.setPixmap(QPixmap("Assets/logo_brgy.png"))
        self.login_screen.login_imagePattern.setPixmap(QPixmap("Assets/image_pattern.png"))

        # Apply rounded corners
        applyRoundedCorners(
            self.login_screen.login_imagePattern,
            radius_top_left=20,
            radius_bottom_left=20,
            radius_top_right=0,
            radius_bottom_right=0,
        )

        if not self.login_initialized:  # Ensure connection is made only once
            # Connect login button
            self.login_screen.login_buttonLogin.clicked.connect(self.login_button_clicked)
            self.login_initialized = True

    def setup_dashboard_ui(self):
        """Setup the dashboard UI layout and connect buttons."""
        self.setFixedSize(1350, 850)  # Set size for dashboard screen
        self.setWindowTitle("Dashboard - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/icon_main.png"))

        if not self.dashboard_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.dashboard_screen.nav_imageLogo.setPixmap(QPixmap("Assets/logo_brgyClear.png"))
            self.dashboard_screen.nav_buttonDashboard.setIcon(QIcon('Assets/icon_dashboard.svg'))
            self.dashboard_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/icon_citizenprofiles.svg'))
            self.dashboard_screen.nav_buttonStatistics.setIcon(QIcon('Assets/icon_statistics.svg'))
            self.dashboard_screen.nav_buttonBusiness.setIcon(QIcon('Assets/icon_business.svg'))
            self.dashboard_screen.nav_buttonSchedules.setIcon(QIcon('Assets/icon_schedule.svg'))
            self.dashboard_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/icon_adminoverview_off.svg'))
            self.dashboard_screen.nav_isLocked.setIcon(QIcon('Assets/icon_isLocked.svg'))

            # Connect navbar buttons
            self.dashboard_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)

            # Connect logout button
            self.dashboard_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.dashboard_initialized = True

    def setup_citizen_profile_ui(self):
        """Setup the citizen profile UI layout."""
        self.setFixedSize(1350, 850)  # Set size for citizen profile screen
        self.setWindowTitle("Citizen Profiles - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/icon_main.png"))

        if not self.citizen_profile_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.citizen_profile_screen.nav_imageLogo.setPixmap(QPixmap("Assets/logo_brgyClear.png"))
            self.citizen_profile_screen.nav_buttonDashboard.setIcon(QIcon('Assets/icon_dashboard.svg'))
            self.citizen_profile_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/icon_citizenprofiles.svg'))
            self.citizen_profile_screen.nav_buttonStatistics.setIcon(QIcon('Assets/icon_statistics.svg'))
            self.citizen_profile_screen.nav_buttonBusiness.setIcon(QIcon('Assets/icon_business.svg'))
            self.citizen_profile_screen.nav_buttonSchedules.setIcon(QIcon('Assets/icon_schedule.svg'))
            self.citizen_profile_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/icon_adminoverview_off.svg'))
            self.citizen_profile_screen.nav_isLocked.setIcon(QIcon('Assets/icon_isLocked.svg'))

            # Connect navbar buttons
            self.citizen_profile_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)

            # Connect logout button
            self.citizen_profile_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.citizen_profile_initialized = True

    def login_button_clicked(self):
        """Handle login button click."""
        print("-- Login Attempt")
        print("Employee ID:", self.login_screen.login_fieldEmp_id.text(),
              " PIN:", self.login_screen.login_fieldPin.text())

        # Insert validation logic here if needed.

        # Switch to dashboard UI
        self.setup_dashboard_ui()  # Ensure dashboard is set up
        self.stack.setCurrentIndex(1)  # Switch to dashboard screen

    def logout_button_clicked(self):
        """Handle logout button click."""
        confirmation = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            print("-- Logout Confirmed")
            self.setup_login_ui()  # Ensure login is set up again
            self.stack.setCurrentIndex(0)  # Switch to login screen
        else:
            print("-- Logout Canceled")

    def goto_dashboard(self):
        """Handle navigation to dashboard screen."""
        print("-- Navigating to Dashboard")
        self.setup_dashboard_ui()  # Ensure dashboard is set up
        self.stack.setCurrentIndex(1)  # Switch to dashboard screen

    def goto_citizen_profiles(self):
        """Handle navigation to citizen profiles screen."""
        print("-- Navigating to Citizen Profiles")
        self.setup_citizen_profile_ui()  # Ensure citizen profile is set up
        self.stack.setCurrentIndex(2)  # Switch to citizen profile screen


# Main Program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
