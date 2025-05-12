from PySide6.QtGui import QPixmap, QIcon, Qt


class HistoryRecordsView:
    def __init__(self, controller):
        self.controller = controller
        self.popup = None
        self.history_screen = None


    def setup_history_ui(self, ui_screen):
        self.history_screen = ui_screen
        """Setup the History Records Views layout."""
        ui_screen.setFixedSize(1350, 850)  # Set size for business screen
        ui_screen.setWindowTitle("MaPro: History Records")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # SET NAVIGATION MAIN ASSETS
        ui_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))

        ui_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/General_Icons/icon_dashboard.svg'))
        ui_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_citizenpanel.svg'))
        ui_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/General_Icons/icon_statistics.svg'))
        ui_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/General_Icons/icon_institutions.svg'))
        ui_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/General_Icons/icon_transaction.svg'))
        ui_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/General_Icons/icon_historyrecord.svg'))

        # SET NAVIGATION ADMIN ASSETS
        ui_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_adminoverview_off.svg'))
        ui_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/General_Icons/icon_activitylogs_off.svg'))
        ui_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/General_Icons/icon_isLocked.svg'))

        # SET MAIN HISTORY RECORDS SCREEN ASSETS
        ui_screen.hisrec_Button_CitizenHistory.setIcon(QIcon('Resources/Images/General_Images/img_history_citizen.png'))
        ui_screen.hisrec_Button_MedicalHistory.setIcon(QIcon('Resources/Images/General_Images/img_history_medical.png'))
        ui_screen.hisrec_Button_SettlementHistory.setIcon(QIcon('Resources/Images/General_Images/img_history_settlement.png'))

        # SUBPAGES : NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.hisrec_Button_CitizenHistory.clicked.connect(self.controller.goto_citizen_history_panel)
        ui_screen.hisrec_Button_MedicalHistory.clicked.connect(self.controller.goto_medical_history_panel)
        ui_screen.hisrec_Button_SettlementHistory.clicked.connect(self.controller.goto_settlement_history_panel)

        # NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.nav_buttonDashboard.clicked.connect(self.controller.goto_dashboard_panel)
        ui_screen.nav_buttonCitizenPanel.clicked.connect(self.controller.goto_citizen_panel)
        ui_screen.nav_buttonStatistics.clicked.connect(self.controller.goto_statistics_panel)
        ui_screen.nav_buttonInstitutions.clicked.connect(self.controller.goto_institutions_panel)
        ui_screen.nav_buttonTransactions.clicked.connect(self.controller.goto_transactions_panel)
        # self.nav_buttonHistoryRecords.clicked.connect(self.goto_history_panel)
        ui_screen.logout_buttonLogout.clicked.connect(self.controller.logout)