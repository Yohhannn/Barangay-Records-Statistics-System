from PySide6.QtGui import QPixmap, QIcon, Qt

class CitizenPanelView:
    def __init__(self, controller):
        self.controller = controller
        self.popup = None
        self.profile_screen = None
        self.cp_profile_screen = None
    def setup_citizen_panel_ui(self, ui_screen):
        self.profile_screen = ui_screen

        # SET NAVIGATION MAIN ASSETS
        ui_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))

        ui_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/General_Icons/icon_dashboard.svg'))
        ui_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_citizenpanel.svg'))
        ui_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/General_Icons/icon_statistics.svg'))
        ui_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/General_Icons/icon_institutions.svg'))
        ui_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/General_Icons/icon_transaction.svg'))
        ui_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/General_Icons/icon_historyrecord_closed.svg'))

        # SET NAVIGATION ADMIN ASSETS
        ui_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_adminoverview_on.svg'))
        ui_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/General_Icons/icon_activitylogs_on.svg'))
        ui_screen.nav_buttonTrashBin.setIcon(QIcon('Resources/Icons/General_Icons/icon_trash_bin.svg'))
        # ui_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/General_Icons/icon_isLocked.svg'))

        # SET MAIN CITIZEN PANEL SCREEN ASSETS
        ui_screen.CP_ButtonCategory_Household.setIcon(QIcon('Resources/Images/General_Images/img_CP_household.png'))
        ui_screen.CP_ButtonCategory_CitizenProfile.setIcon(QIcon('Resources/Images/General_Images/img_CP_citizenprofile.png'))

        # SUB PAGES : NAVIGATIONAL BUTTONS --> GOTO
        # ui_screen.CP_ButtonCategory_Household.clicked.connect(cp_profile_screengoto_household_panel)
   #     ui_screen.CP_ButtonCategory_CitizenProfile.clicked.connect(cp_profile_screengoto_citizenprofile_panel)



        # NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.nav_buttonDashboard.clicked.connect(self.controller.goto_dashboard_panel)
        ui_screen.nav_buttonStatistics.clicked.connect(self.controller.goto_statistics_panel)
        ui_screen.nav_buttonInstitutions.clicked.connect(self.controller.goto_institutions_panel)
        ui_screen.nav_buttonTransactions.clicked.connect(self.controller.goto_transactions_panel)
        ui_screen.nav_buttonHistoryRecords.clicked.connect(self.controller.goto_history_panel)
        ui_screen.logout_buttonLogout.clicked.connect(self.controller.logout)
        ui_screen.nav_buttonAdminPanel.clicked.connect(self.controller.goto_admin_panel)
        ui_screen.nav_buttonActivityLogs.clicked.connect(self.controller.goto_activity_logs)
        ui_screen.nav_buttonTrashBin.clicked.connect(self.controller.goto_trashbin_panel)


        # SUB PAGES : NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.CP_ButtonCategory_Household.clicked.connect(self.controller.goto_household_sub_panel)
        ui_screen.CP_ButtonCategory_CitizenProfile.clicked.connect(self.controller.goto_citizen_profile_sub_panel)



