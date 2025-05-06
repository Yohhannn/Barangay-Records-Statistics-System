import cv2
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QLabel, QButtonGroup, QRadioButton, QApplication
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer

from Controllers.MainController.Citizen_Panel.Household.household_controller import HouseholdController
from Controllers.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class citizen_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.citizen_panel_screen = self.load_ui("Views/MainPages/citizenpanel.ui")
        self.setup_citizen_panel_ui()
        self.center_on_screen()

    def setup_citizen_panel_ui(self):
        """Setup the citizen panel Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

        # SET NAVIGATION MAIN ASSETS
        self.citizen_panel_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/logo_brgyClear.png"))
        self.citizen_panel_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/icon_dashboard.svg'))
        self.citizen_panel_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/icon_citizenpanel.svg'))
        self.citizen_panel_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/icon_statistics.svg'))
        self.citizen_panel_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/icon_institutions.svg'))
        self.citizen_panel_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/icon_transaction.svg'))
        self.citizen_panel_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/icon_historyrecord_closed.svg'))

        # SET NAVIGATION ADMIN ASSETS
        self.citizen_panel_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/icon_adminoverview_off.svg'))
        self.citizen_panel_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/icon_activitylogs_off.svg'))
        self.citizen_panel_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/icon_isLocked.svg'))

        # SET MAIN CITIZEN PANEL SCREEN ASSETS
        self.citizen_panel_screen.CP_ButtonCategory_Household.setIcon(QIcon('Resources/Images/img_CP_household.png'))
        self.citizen_panel_screen.CP_ButtonCategory_CitizenProfile.setIcon(QIcon('Resources/Images/img_CP_citizenprofile.png'))

        # SUB PAGES : NAVIGATIONAL BUTTONS --> GOTO
        self.citizen_panel_screen.CP_ButtonCategory_Household.clicked.connect(self.goto_household_panel)
        self.citizen_panel_screen.CP_ButtonCategory_CitizenProfile.clicked.connect(self.goto_citizenprofile_panel)

        # NAVIGATIONAL BUTTONS --> GOTO
        self.citizen_panel_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard_panel)
        # self.citizen_panel_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        self.citizen_panel_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics_panel)
        self.citizen_panel_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)
        self.citizen_panel_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions_panel)
        self.citizen_panel_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_panel)
        self.citizen_panel_screen.logout_buttonLogout.clicked.connect(self.logout)

    # GOTO NAVIGATIONS ================================
    def goto_dashboard_panel(self):
        """Return to dashboard screen"""
        print("-- Navigating to Dashboard")
        self.stack.setCurrentIndex(0)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.MainController.Statistics.statistics_func import statistics_func
            self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Controllers.MainController.Institutions.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions'):
            from Controllers.MainController.Transactions.transaction_func import transaction_func
            self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.MainController.History_Records.history_func import history_func
            self.history_panel = history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)

    # SUBPAGES : GOTO =================
    def goto_citizenprofile_panel(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to Citizen Profile")
        if not hasattr(self, 'citizenprofile'):
            from Controllers.MainController.Citizen_Panel.Citizen_Profile.citizen_profile_func import citizen_profile_func
            self.profile_panel = citizen_profile_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.profile_panel.cp_profile_screen)

        self.stack.setCurrentWidget(self.profile_panel.cp_profile_screen)

    def goto_household_panel(self):
        """Handle navigation to Household Panel screen."""
        print("-- Navigating to Household")
        if not hasattr(self, 'household'):
            from Controllers.MainController.Citizen_Panel.Household.household_controller import HouseholdController
            self.household_panel = HouseholdController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.household_panel.cp_household_screen)

        self.stack.setCurrentWidget(self.household_panel.cp_household_screen)

    def logout(self):
        confirmation = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            QApplication.closeAllWindows()

            self.login_window.show()
            self.login_window.clear_fields()


    # SCREEN POPUPS ================================
    # def show_filter_popup(self):
    #     print("-- Navigating to Profile List > Filter Options")
    #     popup = load_popup("Views/PopUp/Screen_CitizenProfiles/filteroptions.ui", self)
    #     popup.setWindowModality(Qt.ApplicationModal)
    #     popup.show()

