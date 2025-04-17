from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QApplication

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class transaction_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.transactions_screen = self.load_ui("UI/MainPages/transactions.ui")
        self.setup_ui()
        self.center_on_screen()

    def setup_ui(self):
        """Setup the Transactions UI layout."""
        self.setFixedSize(1350, 850)  # Set size for business screen
        self.setWindowTitle("MaPro: Transactions")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        # SET NAVIGATION MAIN ASSETS
        self.transactions_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        self.transactions_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
        self.transactions_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
        self.transactions_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
        self.transactions_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
        self.transactions_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
        self.transactions_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

        # SET NAVIGATION ADMIN ASSETS
        self.transactions_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
        self.transactions_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
        self.transactions_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

        # NAVIGATIONAL BUTTONS --> GOTO
        self.transactions_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard_panel)
        self.transactions_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        self.transactions_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics_panel)
        self.transactions_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)
        # self.transactions_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions_panel)
        self.transactions_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_panel)
        self.transactions_screen.logout_buttonLogout.clicked.connect(self.logout)

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
            from Functions.Main.Citizen_Panel.citizen_func import citizen_func
            self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Functions.Main.Statistics.statistics_func import statistics_func
            self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Functions.Main.Institutions.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")

    # def goto_transactions_panel(self):
    #     """Handle navigation to Transactions Panel screen."""
    #     print("-- Navigating to Transactions")
    #     if not hasattr(self, 'transactions'):
    #         from Functions.Main.Transactions.transaction_func import transaction_func
    #         self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.transactions_panel.transactions_screen)
    #
    #     self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
    #     self.setWindowTitle("MaPro: Transactions")

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Functions.Main.History_Records.history_func import history_func
            self.history_panel = history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)
        self.setWindowTitle("MaPro: History Records")

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
