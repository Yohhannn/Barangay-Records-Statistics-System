import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QPushButton, QFileDialog, QLabel, \
    QButtonGroup, QRadioButton
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer

from Functions.base_file_func import base_file_func
from Functions.institution_functions.institution_func import institutions_func
from Utils.utils_datetime import update_date_label
from Utils.utils_realtime import update_time_label
from Utils.util_popup import load_popup


class dashboard_func(base_file_func):
    def __init__(self, login_window, emp_first_name):
        super().__init__(login_window, emp_first_name)
        self.dashboard_screen = self.load_ui("UI/MainPages/dashboard.ui")
        self.stack.addWidget(self.dashboard_screen)
        self.setup_ui()
        self.stack.setCurrentIndex(0)
        self.center_on_screen()

    def setup_ui(self):
        """Setup the dashboard UI layout and connect buttons."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Dashboard")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        # Set images and icons for the navbar
        self.dashboard_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        self.dashboard_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
        self.dashboard_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
        self.dashboard_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
        self.dashboard_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
        self.dashboard_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
        self.dashboard_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

        self.dashboard_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
        self.dashboard_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
        self.dashboard_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

        self.dashboard_screen.dashboard_buttonAboutSoftware.setIcon(QIcon('Assets/Icons/icon_aboutsoftware.svg'))
        self.dashboard_screen.dashboard_buttonBarangayInfo.setIcon(QIcon('Assets/Icons/icon_brgyinfo.svg'))
        self.dashboard_screen.dashboard_buttonViewEmployees.setIcon(QIcon('Assets/Icons/icon_viewemplist.svg'))

        # Set the rest of the icons to the page
        self.dashboard_screen.acc_buttonYourAccount.setIcon(QIcon('Assets/Icons/icon_myprofile.svg'))

        # Update date label
        update_date_label(self.dashboard_screen.label_dateDashboard)

        # Welcome Message Display Name
        self.dashboard_screen.title_employeeFirstNameDashboard.setText(self.emp_first_name)

        # Set up and start the timer for real-time time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: update_time_label(self.dashboard_screen.label_timeDashboard))
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        self.dashboard_screen.label_UpdateVersion.setText("V2.8.2 - Alpha")

        # Connect the button to the popup method
        self.dashboard_screen.acc_buttonYourAccount.clicked.connect(self.show_account_popup)
        self.dashboard_screen.dashboard_buttonViewEmployees.clicked.connect(self.show_employee_popup)
        self.dashboard_screen.dashboard_buttonBarangayInfo.clicked.connect(self.show_barangayinfo_popup)
        self.dashboard_screen.dashboard_buttonAboutSoftware.clicked.connect(self.show_aboutsoftware_popup)

        # CATEGORY BUTTONS
        self.dashboard_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        self.dashboard_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics_panel)
        self.dashboard_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)

    def goto_citizen_panel(self):
        """Handle navigation to citizen panel screen."""
        if not hasattr(self, 'citizen_panel'):
            from Functions.citizen_functions.citizen_func import citizen_func
            self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")

    def goto_statistics_panel(self):
        """Handle navigation to citizen panel screen."""
        if not hasattr(self, 'statistics_panel'):
            from Functions.statistic_functions.statistics_func import statistics_func
            self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")

    def goto_institutions_panel(self):
        """Handle navigation to citizen panel screen."""
        if not hasattr(self, 'insitutions'):
            from Functions.institution_functions.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")


    def show_employee_popup(self):
        print("-- Navigating to Dashboard > List of Employees")
        popup = load_popup("UI/PopUp/Screen_Dashboard/listofemployees.ui", self)
        popup.setWindowTitle("List of Employees")
        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    def show_barangayinfo_popup(self):
        print("-- Navigating to Dashboard > Barangay Info")
        popup = load_popup("UI/PopUp/Screen_Dashboard/barangayinfo.ui", self)
        popup.setWindowTitle("Barangay Information")
        popup.brgyinfo_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    def show_aboutsoftware_popup(self):
        print("-- Navigating to Dashboard > About Software")
        popup = load_popup("UI/PopUp/Screen_Dashboard/aboutsoftware.ui", self)
        popup.setWindowTitle("About the Software")
        popup.aboutsoftwareinfo_imageRavenLabs.setPixmap(QPixmap("Assets/AppIcons/icon_ravenlabs.png"))
        popup.aboutsoftwareinfo_imageCTULOGO.setPixmap(QPixmap("Assets/Images/img_ctulogo.png"))
        popup.aboutsoftwareinfo_imageLogo.setPixmap(QPixmap("Assets/Images/img_mainappicon.png"))
        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    def show_account_popup(self):
        print("-- Navigating to Dashboard > Your Account")
        popup = load_popup("UI/PopUp/Screen_Dashboard/youraccount.ui", self)
        popup.setWindowTitle("Your Account")
        popup.setWindowModality(Qt.ApplicationModal)

        admin_override_button = popup.findChild(QPushButton, "employeeaccount_buttonAdminOverride")
        if admin_override_button:
            admin_override_button.clicked.connect(lambda: self.show_admin_override_popup(popup))

        popup.show()

    def show_admin_override_popup(self, first_popup):
        print("-- Navigating to Dashboard > Your Account > Admin Override")
        first_popup.close()
        admin_popup = load_popup("UI/PopUp/Screen_Dashboard/adminoverride.ui", self)
        admin_popup.setWindowTitle("Admin Override")
        admin_popup.setWindowModality(Qt.ApplicationModal)
        admin_popup.btn_return_to_youraccount.setIcon(QIcon('Assets/Icons/icon_return_light.svg'))

        return_button = admin_popup.findChild(QPushButton, "btn_return_to_youraccount")
        if return_button:
            print("-- Found 'Return to Your Account' button")
            return_button.clicked.connect(lambda: self.return_to_account_popup(admin_popup))
        else:
            print("-- Error: 'Return to Your Account' button not found!")

        admin_popup.show()

    def return_to_account_popup(self, current_popup):
        print("-- Returning to Dashboard > Your Account")
        current_popup.close()
        self.show_account_popup()