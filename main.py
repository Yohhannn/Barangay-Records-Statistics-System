import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QPushButton
from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtCore import QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from Utils.utils_corner import applyRoundedCorners
from Utils.utils_datetime import update_date_label
from Utils.utils_realtime import update_time_label
from Utils.util_popup import load_popup

from database import Database

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

        # only here for debugging purposes
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
        if employee:
            QMessageBox.information(self, "Success", "Login successful!")
            self.main_window = MainWindow(self)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

        self.login_screen.login_fieldEmp_id.clear()
        self.login_screen.login_fieldPin.clear()

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

    # ===============================================================================================
    def setup_dashboard_ui(self):
        """Setup the dashboard UI layout and connect buttons."""
        self.setFixedSize(1350, 850)  # Set size for dashboard screen
        self.setWindowTitle("Dashboard - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/Icons/icon_main.png"))

        if not self.dashboard_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.dashboard_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.dashboard_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.dashboard_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.dashboard_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.dashboard_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.dashboard_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.dashboard_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.dashboard_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Set the rest of the icons to the page.
            self.dashboard_screen.acc_buttonYourAccount.setIcon(QIcon('Assets/Icons/icon_myprofile.svg'))

            # Update date label
            update_date_label(self.dashboard_screen.label_dateDashboard)

            # Set up and start the timer for real-time time updates
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: update_time_label(self.dashboard_screen.label_timeDashboard))
            self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

            # Connect navbar buttons
            self.dashboard_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.dashboard_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.dashboard_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.dashboard_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.dashboard_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.dashboard_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.dashboard_initialized = True

            # Connect the button to the popup method
            self.dashboard_screen.acc_buttonYourAccount.clicked.connect(self.show_account_popup)

    def show_account_popup(self):
        print("-- Navigating to Dashboard > Your Account")
        popup = load_popup("UI/PopUp/youraccount.ui", self)
        popup.setWindowTitle("Your Account")  # Optional title
        popup.setWindowModality(Qt.ApplicationModal)  # Make it modal

        # Find the "Admin Override" button inside the popup UI
        admin_override_button = popup.findChild(QPushButton, "employeeaccount_buttonAdminOverride")

        if admin_override_button:
            admin_override_button.clicked.connect(lambda: self.show_admin_override_popup(popup))

        popup.show()

    def show_admin_override_popup(self, first_popup):
        print("-- Navigating to Dashboard > Your Account > Admin Override")
        first_popup.close()  # Close the first popup
        admin_popup = load_popup("UI/PopUp/adminoverride.ui", self)
        admin_popup.setWindowTitle("Admin Override")
        admin_popup.setWindowModality(Qt.ApplicationModal)  # Modal type para dili ma click ang other window na nag open.

        # Find the "Return to Your Account" button inside the Admin Override popup
        return_button = admin_popup.findChild(QPushButton, "btn_return_to_youraccount")

        if return_button:
            print("-- Found 'Return to Your Account' button")
            return_button.clicked.connect(lambda: self.return_to_account_popup(admin_popup))
        else:
            print("-- Error: 'Return to Your Account' button not found!")

        admin_popup.show()

    def return_to_account_popup(self, current_popup):
        print("-- Returning to Dashboard > Your Account")
        current_popup.close()  # Close the current popup
        self.show_account_popup()  # Reopen the 'Your Account' popup

    # ===============================================================================================

    def setup_citizen_profile_ui(self):
        """Setup the citizen profile UI layout."""
        self.setFixedSize(1350, 850)  # Set size for citizen profile screen
        self.setWindowTitle("Citizen Profiles - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/Icons/icon_main.png"))

        if not self.citizen_profile_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.citizen_profile_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.citizen_profile_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.citizen_profile_screen.nav_buttonCitizenProfiles.setIcon(QIcon(
                'Assets/Icons/icon_citizenprofiles.svg'))
            self.citizen_profile_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.citizen_profile_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.citizen_profile_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.citizen_profile_screen.nav_buttonAdminOverview.setIcon(QIcon(
                'Assets/Icons/icon_adminoverview_off.svg'))
            self.citizen_profile_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.citizen_profile_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.citizen_profile_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.citizen_profile_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.citizen_profile_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.citizen_profile_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.citizen_profile_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.citizen_profile_initialized = True

    # ===============================================================================================

    def setup_statistics_ui(self):
        """Setup the statistics UI layout."""
        self.setFixedSize(1350, 850)  # Set size for statistics screen
        self.setWindowTitle("Statistics - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/Icons/icon_main.png"))

        if not self.statistics_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.statistics_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.statistics_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.statistics_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.statistics_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.statistics_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.statistics_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.statistics_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.statistics_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.statistics_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.statistics_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.statistics_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.statistics_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.statistics_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.statistics_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.statistics_initialized = True

    # ===============================================================================================

    def setup_business_ui(self):
        """Setup the business UI layout."""
        self.setFixedSize(1350, 850)  # Set size for business screen
        self.setWindowTitle("Business - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/Icons/icon_main.png"))

        if not self.business_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.business_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.business_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.business_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.business_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.business_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.business_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.business_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.business_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.business_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.business_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.business_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.business_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.business_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.business_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.business_initialized = True

    # ===============================================================================================

    def setup_schedules_ui(self):
        """Setup the schedules UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("Schedules - Marigondon Barangay Profiling System")
        self.setWindowIcon(QIcon("Assets/Icons/icon_main.png"))

        if not self.schedules_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.schedules_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.schedules_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.schedules_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.schedules_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.schedules_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.schedules_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.schedules_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.schedules_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.schedules_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.schedules_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.schedules_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.schedules_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.schedules_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.schedules_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.schedules_initialized = True

    # ===============================================================================================

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