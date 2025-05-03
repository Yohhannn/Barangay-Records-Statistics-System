from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QApplication

from Controllers.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class history_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.history_screen = self.load_ui("Views/MainPages/historyrecords.ui")
        self.setup_history_ui()
        self.center_on_screen()

    def setup_history_ui(self):
        """Setup the History Records Views layout."""
        self.setFixedSize(1350, 850)  # Set size for business screen
        self.setWindowTitle("MaPro: History Records")
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

        # SET NAVIGATION MAIN ASSETS
        self.history_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/logo_brgyClear.png"))
        self.history_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/icon_dashboard.svg'))
        self.history_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/icon_citizenpanel.svg'))
        self.history_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/icon_statistics.svg'))
        self.history_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/icon_institutions.svg'))
        self.history_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/icon_transaction.svg'))
        self.history_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/icon_historyrecord.svg'))

        # SET NAVIGATION ADMIN ASSETS
        self.history_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/icon_adminoverview_off.svg'))
        self.history_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/icon_activitylogs_off.svg'))
        self.history_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/icon_isLocked.svg'))

        # SET MAIN HISTORY RECORDS SCREEN ASSETS
        self.history_screen.hisrec_Button_CitizenHistory.setIcon(QIcon('Resources/Images/img_history_citizen.png'))
        self.history_screen.hisrec_Button_MedicalHistory.setIcon(QIcon('Resources/Images/img_history_medical.png'))
        self.history_screen.hisrec_Button_SettlementHistory.setIcon(QIcon('Resources/Images/img_history_settlement.png'))

        # SUBPAGES : NAVIGATIONAL BUTTONS --> GOTO
        self.history_screen.hisrec_Button_CitizenHistory.clicked.connect(self.goto_citizen_history_panel)
        self.history_screen.hisrec_Button_MedicalHistory.clicked.connect(self.goto_medical_history_panel)
        self.history_screen.hisrec_Button_SettlementHistory.clicked.connect(self.goto_settlement_history_panel)

        # NAVIGATIONAL BUTTONS --> GOTO
        self.history_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard_panel)
        self.history_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        self.history_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics_panel)
        self.history_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)
        self.history_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions_panel)
        # self.history_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_panel)
        self.history_screen.logout_buttonLogout.clicked.connect(self.logout)

    # GOTO NAVIGATIONS ================================
    def goto_dashboard_panel(self):
        """Return to dashboard screen"""
        print("-- Navigating to Dashboard")
        self.stack.setCurrentIndex(0)
        self.setWindowTitle("MaPro: Dashboard")

    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.MainController.Citizen_Panel.citizen_func import citizen_func
            self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.MainController.Statistics.statistics_func import statistics_func
            self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Controllers.MainController.Institutions.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions'):
            from Controllers.MainController.Transactions.transaction_func import transaction_func
            self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
        self.setWindowTitle("MaPro: Transactions")

    # SUBPAGES : GOTO ================

    def goto_citizen_history_panel(self):
        """Handle navigation to Citizen History Panel screen."""
        print("-- Navigating to Citizen History")
        if not hasattr(self, 'citizen_history'):
            from Controllers.MainController.History_Records.Citizen_History.citizen_history_func import citizen_history_func
            self.citizen_history_panel = citizen_history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_history_panel.hist_citizen_history_screen)

        self.stack.setCurrentWidget(self.citizen_history_panel.hist_citizen_history_screen)

    def goto_medical_history_panel(self):
        """Handle navigation to Medical History Panel screen."""
        print("-- Navigating to Medical History")
        if not hasattr(self, 'medical_history'):
            from Controllers.MainController.History_Records.Medical_History.medical_history_func import medical_history_func
            self.medical_history_panel = medical_history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.medical_history_panel.hist_medical_history_screen)

        self.stack.setCurrentWidget(self.medical_history_panel.hist_medical_history_screen)

    def goto_settlement_history_panel(self):
        """Handle navigation to Settlement History Panel screen."""
        print("-- Navigating to Settlement History")
        if not hasattr(self, 'settlement_history'):
            from Controllers.MainController.History_Records.Settlement_History.settlement_history_func import settlement_history_func
            self.settlement_history_panel = settlement_history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.settlement_history_panel.hist_settlement_history_screen)

        self.stack.setCurrentWidget(self.settlement_history_panel.hist_settlement_history_screen)

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



