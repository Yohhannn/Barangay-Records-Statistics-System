from PySide6.QtGui import QPixmap, QIcon, Qt


class TransactionView:
    def __init__(self, controller):
        self.controller = controller
        self.popup = None
        self.transaction_screen = None

    def setup_transaction_ui(self, ui_screen):
        """Setup the Transactions Views layout."""
        ui_screen.setFixedSize(1350, 850)  # Set size for business screen
        ui_screen.setWindowTitle("MaPro: Transactions")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # SET NAVIGATION MAIN ASSETS
        ui_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))

        ui_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/General_Icons/icon_dashboard.svg'))
        ui_screen.nav_buttonCitizenPanel.setIcon(
            QIcon('Resources/Icons/General_Icons/icon_citizenpanel.svg'))
        ui_screen.nav_buttonStatistics.setIcon(
            QIcon('Resources/Icons/General_Icons/icon_statistics.svg'))
        ui_screen.nav_buttonInstitutions.setIcon(
            QIcon('Resources/Icons/General_Icons/icon_institutions.svg'))
        ui_screen.nav_buttonTransactions.setIcon(
            QIcon('Resources/Icons/General_Icons/icon_transaction.svg'))
        ui_screen.nav_buttonHistoryRecords.setIcon(
            QIcon('Resources/Icons/General_Icons/icon_historyrecord_closed.svg'))

        # SET NAVIGATION ADMIN ASSETS
        ui_screen.nav_buttonAdminPanel.setIcon(
            QIcon('Resources/Icons/General_Icons/icon_adminoverview_off.svg'))
        ui_screen.nav_buttonActivityLogs.setIcon(
            QIcon('Resources/Icons/General_Icons/icon_activitylogs_off.svg'))
        ui_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/General_Icons/icon_isLocked.svg'))

        # SET MAIN TRANSACTION PAGES ASSETS
        ui_screen.trans_ButtonCategory_Services.setIcon(
            QIcon('Resources/Images/General_Images/img_transaction_papers.png'))

        # SUBPAGES : SERVICES --> GOTO
        ui_screen.trans_ButtonCategory_Services.clicked.connect(self.controller.goto_services_panel)

        # NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.nav_buttonDashboard.clicked.connect(self.controller.goto_dashboard_panel)
        ui_screen.nav_buttonCitizenPanel.clicked.connect(self.controller.goto_citizen_panel)
        ui_screen.nav_buttonStatistics.clicked.connect(self.controller.goto_statistics_panel)
        ui_screen.nav_buttonInstitutions.clicked.connect(self.controller.goto_institutions_panel)
        # ui_screen.nav_buttonTransactions.clicked.connect(self.controller.goto_transactions_panel)
        ui_screen.nav_buttonHistoryRecords.clicked.connect(self.controller.goto_history_panel)
        ui_screen.logout_buttonLogout.clicked.connect(self.controller.logout)
        ui_screen.nav_buttonAdminPanel.clicked.connect(self.controller.goto_admin_panel)
        ui_screen.nav_buttonActivityLogs.clicked.connect(self.controller.goto_activity_logs)
