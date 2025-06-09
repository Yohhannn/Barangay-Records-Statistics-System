from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMessageBox, QApplication

class InstitutionsView:
    def __init__(self, controller):
        self.controller = controller
        self.popup = None
        self.inistitutions_screen = None


    def setup_institutions_ui(self, ui_screen):
        self.inistitutions_screen = ui_screen
        """Setup the institutions Views layout."""
        ui_screen.setFixedSize(1350, 850)  # Set size for business screen
        ui_screen.setWindowTitle("MaPro: Institutions")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set images and icons for the navbar
        ui_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))

        ui_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/General_Icons/icon_dashboard.svg'))
        ui_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_citizenpanel.svg'))
        ui_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/General_Icons/icon_statistics.svg'))
        ui_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/General_Icons/icon_institutions.svg'))
        ui_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/General_Icons/icon_transaction.svg'))
        ui_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/General_Icons/icon_historyrecord_closed.svg'))

        ui_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_adminoverview_on.svg'))
        ui_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/General_Icons/icon_activitylogs_on.svg'))
        ui_screen.nav_buttonTrashBin.setIcon(QIcon('Resources/Icons/General_Icons/icon_trash_bin.svg'))
        # ui_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/General_Icons/icon_isLocked.svg'))

        ui_screen.inst_ButtonCategory_Business.setIcon(QIcon('Resources/Images/General_Images/img_category_business.png'))
        ui_screen.inst_ButtonCategory_Infrastructure.setIcon(QIcon('Resources/Images/General_Images/img_category_infrastructure.png'))

        # SUBPAGES : NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.inst_ButtonCategory_Business.clicked.connect(self.controller.goto_business_panel)
        ui_screen.inst_ButtonCategory_Infrastructure.clicked.connect(self.controller.goto_infrastructure_panel)

        # NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.nav_buttonDashboard.clicked.connect(self.controller.goto_dashboard_panel)
        ui_screen.nav_buttonCitizenPanel.clicked.connect(self.controller.goto_citizen_panel)
        ui_screen.nav_buttonStatistics.clicked.connect(self.controller.goto_statistics_panel)
        # ui_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)
        ui_screen.nav_buttonTransactions.clicked.connect(self.controller.goto_transactions_panel)
        ui_screen.nav_buttonHistoryRecords.clicked.connect(self.controller.goto_history_panel)
        ui_screen.logout_buttonLogout.clicked.connect(self.controller.logout)
        ui_screen.nav_buttonAdminPanel.clicked.connect(self.controller.goto_admin_panel)
        ui_screen.nav_buttonActivityLogs.clicked.connect(self.controller.goto_activity_logs)
        ui_screen.nav_buttonTrashBin.clicked.connect(self.controller.goto_trashbin_panel)



