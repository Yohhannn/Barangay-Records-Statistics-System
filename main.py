import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
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
        self.setWindowIcon(QIcon("Assets/icon_main.png"))

        # Set images
        self.login_screen.login_imageLogo.setPixmap(QPixmap("Assets/logo_brgy.png"))
        self.login_screen.login_imagePattern.setPixmap(QPixmap("Assets/image_pattern.png"))
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

        # Joe insert validation logic here.

        # Open Main Application (Dashboard + Citizen Profiles and other .ui)
        self.main_window = MainWindow(self)
        self.main_window.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window

        # Initialize QStackedWidget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Load the UI files
        self.loader = QUiLoader()
        self.dashboard_screen = self.load_ui("UI/dashboard.ui")
        self.citizen_profile_screen = self.load_ui("UI/citizenprofile.ui")
        self.statistics_screen = self.load_ui("UI/statistics.ui")
        self.business_screen = self.load_ui("UI/business.ui")
        self.schedules_screen = self.load_ui("UI/schedule.ui")


        # Add the screens to the stack
        self.stack.addWidget(self.dashboard_screen)  # Index 0
        self.stack.addWidget(self.citizen_profile_screen)  # Index 1
        self.stack.addWidget(self.statistics_screen)  # Index 2
        self.stack.addWidget(self.business_screen)  # Index 3
        self.stack.addWidget(self.schedules_screen)  # Index 4

        # Flags to track signal initialization
        self.dashboard_initialized = False
        self.citizen_profile_initialized = False
        self.statistics_initialized = False
        self.business_initialized = False
        self.schedules_initialized = False

        # Setup initial screen
        self.setup_dashboard_ui()
        self.stack.setCurrentIndex(0)  # Show dashboard by default

    def load_ui(self, ui_path):
        """Utility function to load a .ui file."""
        file = QFile(ui_path)
        file.open(QFile.ReadOnly)
        ui = self.loader.load(file, None)
        file.close()
        return ui

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
            self.dashboard_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.dashboard_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.dashboard_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.dashboard_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.dashboard_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

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
            self.citizen_profile_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.citizen_profile_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.citizen_profile_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.citizen_profile_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.citizen_profile_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.citizen_profile_initialized = True

    def setup_statistics_ui(self):
        """Setup the statistics UI layout."""
        self.setFixedSize(1350, 850)  # Set size for statistics screen
        self.setWindowTitle("Statistics - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/icon_main.png"))

        if not self.statistics_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.statistics_screen.nav_imageLogo.setPixmap(QPixmap("Assets/logo_brgyClear.png"))
            self.statistics_screen.nav_buttonDashboard.setIcon(QIcon('Assets/icon_dashboard.svg'))
            self.statistics_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/icon_citizenprofiles.svg'))
            self.statistics_screen.nav_buttonStatistics.setIcon(QIcon('Assets/icon_statistics.svg'))
            self.statistics_screen.nav_buttonBusiness.setIcon(QIcon('Assets/icon_business.svg'))
            self.statistics_screen.nav_buttonSchedules.setIcon(QIcon('Assets/icon_schedule.svg'))
            self.statistics_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/icon_adminoverview_off.svg'))
            self.statistics_screen.nav_isLocked.setIcon(QIcon('Assets/icon_isLocked.svg'))

            # Connect navbar buttons
            self.statistics_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.statistics_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.statistics_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.statistics_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.statistics_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.statistics_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.statistics_initialized = True

    def setup_business_ui(self):
        """Setup the business UI layout."""
        self.setFixedSize(1350, 850)  # Set size for business screen
        self.setWindowTitle("Business - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/icon_main.png"))

        if not self.business_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.business_screen.nav_imageLogo.setPixmap(QPixmap("Assets/logo_brgyClear.png"))
            self.business_screen.nav_buttonDashboard.setIcon(QIcon('Assets/icon_dashboard.svg'))
            self.business_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/icon_citizenprofiles.svg'))
            self.business_screen.nav_buttonStatistics.setIcon(QIcon('Assets/icon_statistics.svg'))
            self.business_screen.nav_buttonBusiness.setIcon(QIcon('Assets/icon_business.svg'))
            self.business_screen.nav_buttonSchedules.setIcon(QIcon('Assets/icon_schedule.svg'))
            self.business_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/icon_adminoverview_off.svg'))
            self.business_screen.nav_isLocked.setIcon(QIcon('Assets/icon_isLocked.svg'))

            # Connect navbar buttons
            self.business_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.business_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.business_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.business_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.business_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.business_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.business_initialized = True

    def setup_schedules_ui(self):
        """Setup the schedules UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("Schedules - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/icon_main.png"))

        if not self.schedules_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.schedules_screen.nav_imageLogo.setPixmap(QPixmap("Assets/logo_brgyClear.png"))
            self.schedules_screen.nav_buttonDashboard.setIcon(QIcon('Assets/icon_dashboard.svg'))
            self.schedules_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/icon_citizenprofiles.svg'))
            self.schedules_screen.nav_buttonStatistics.setIcon(QIcon('Assets/icon_statistics.svg'))
            self.schedules_screen.nav_buttonBusiness.setIcon(QIcon('Assets/icon_business.svg'))
            self.schedules_screen.nav_buttonSchedules.setIcon(QIcon('Assets/icon_schedule.svg'))
            self.schedules_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/icon_adminoverview_off.svg'))
            self.schedules_screen.nav_isLocked.setIcon(QIcon('Assets/icon_isLocked.svg'))

            # Connect navbar buttons
            self.schedules_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.schedules_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.schedules_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.schedules_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.schedules_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.schedules_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.schedules_initialized = True

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
            self.login_window.show()  # Show the login window again
            self.close()

    def goto_dashboard(self):
        """Handle navigation to dashboard screen."""
        print("-- Navigating to Dashboard")
        self.setup_dashboard_ui()  # Ensure dashboard is set up
        self.stack.setCurrentIndex(0)  # Switch to dashboard screen

    def goto_citizen_profiles(self):
        """Handle navigation to citizen profiles screen."""
        print("-- Navigating to Citizen Profiles")
        self.setup_citizen_profile_ui()  # Ensure citizen profile is set up
        self.stack.setCurrentIndex(1)  # Switch to citizen profile screen

    def goto_statistics(self):
        """Handle navigation to statistics screen."""
        print("-- Navigating to Statistics")
        self.setup_statistics_ui()  # Ensure statistics is set up
        self.stack.setCurrentIndex(2)  # Switch to statistics screen

    def goto_business(self):
        """Handle navigation to business screen."""
        print("-- Navigating to Business")
        self.setup_business_ui()  # Ensure business is set up
        self.stack.setCurrentIndex(3)  # Switch to business screen

    def goto_schedules(self):
        """Handle navigation to schedules screen."""
        print("-- Navigating to Schedules")
        self.setup_schedules_ui()  # Ensure schedules is set up
        self.stack.setCurrentIndex(4)  # Switch to schedules screen


# Main Program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())


# FUCNTION 1
# FUCNTION 2