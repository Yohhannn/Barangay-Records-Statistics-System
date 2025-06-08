from PySide6.QtGui import QPixmap, QIcon, Qt
from Utils.util_popup import load_popup
from PySide6.QtWidgets import QMessageBox

class StatisticsView:
    def __init__(self, controller):
        self.controller = controller

        self.popup = None

        self.statistics_screen = None


    def setup_statistics_ui(self, ui_screen):
        self.statistics_screen = ui_screen
        """Setup the statistics Views layout."""
        ui_screen.setFixedSize(1350, 850)  # Set size for statistics screen
        ui_screen.setWindowTitle("MaPro: Statistics")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

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

        # SET MAIN STATISTICS SCREEN ASSETS
        ui_screen.statistics_ButtonDemographic.setIcon(QIcon('Resources/Images/General_Images/img_demographic.png'))
        ui_screen.statistics_ButtonNeighborhood.setIcon(QIcon('Resources/Images/General_Images/img_neighborhood.png'))
        # self.statistics_screen.statistics_ButtonGeographic.setIcon(QIcon('Resources/Images/img_geographic.png'))        -- Renamed Geographic into Neighborhood
        ui_screen.statistics_ButtonHousehold.setIcon(QIcon('Resources/Images/General_Images/img_household.png'))
        ui_screen.statistics_ButtonEducation.setIcon(QIcon('Resources/Images/General_Images/img_education.png'))
        ui_screen.statistics_ButtonEmployment.setIcon(QIcon('Resources/Images/General_Images/img_employment.png'))
        # self.statistics_screen.statistics_ButtonSocioEconomic.setIcon(QIcon('Resources/Images/img_socioeconomic.png'))  -- Removed SocioEconomic Replaced into Education
        # self.statistics_screen.statistics_ButtonVoters.setIcon(QIcon('Resources/Images/img_voters.png'))                -- Removed Voters Replaced into Employment
        ui_screen.statistics_ButtonHealth.setIcon(QIcon('Resources/Images/General_Images/img_health.png'))
        ui_screen.statistics_ButtonBusiness.setIcon(QIcon('Resources/Images/General_Images/img_business.png'))
        # self.statistics_screen.statistics_ButtonJobs.setIcon(QIcon('Resources/Images/img_jobs.png'))                    -- Removed Jobs Replaced into Business
        ui_screen.statistics_ButtonInfrastructures.setIcon(
            QIcon('Resources/Images/General_Images/img_infrastructure.png'))
        # self.statistics_screen.statistics_ButtonGroups.setIcon(QIcon('Resources/Images/img_groups.png'))                -- Removed Groups Replaced into Infrastructure

        # SUBPAGES: NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.statistics_ButtonDemographic.clicked.connect(self.controller.goto_demographics_panel)
        ui_screen.statistics_ButtonNeighborhood.clicked.connect(self.controller.goto_neighborhood_panel)
        ui_screen.statistics_ButtonHousehold.clicked.connect(self.controller.goto_household_panel)
        ui_screen.statistics_ButtonEducation.clicked.connect(self.controller.goto_education_panel)
        ui_screen.statistics_ButtonEmployment.clicked.connect(self.controller.goto_employment_panel)
        ui_screen.statistics_ButtonHealth.clicked.connect(self.controller.goto_health_panel)
        ui_screen.statistics_ButtonBusiness.clicked.connect(self.controller.goto_business_panel)
        ui_screen.statistics_ButtonInfrastructures.clicked.connect(self.controller.goto_infrastructures_panel)

        # NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.nav_buttonDashboard.clicked.connect(self.controller.goto_dashboard_panel)
        ui_screen.nav_buttonCitizenPanel.clicked.connect(self.controller.goto_citizen_panel)
        ui_screen.nav_buttonInstitutions.clicked.connect(self.controller.goto_institutions_panel)
        ui_screen.nav_buttonTransactions.clicked.connect(self.controller.goto_transactions_panel)
        ui_screen.nav_buttonHistoryRecords.clicked.connect(self.controller.goto_history_panel)
        ui_screen.logout_buttonLogout.clicked.connect(self.controller.logout)
        ui_screen.nav_buttonAdminPanel.clicked.connect(self.controller.goto_admin_panel)
        ui_screen.nav_buttonActivityLogs.clicked.connect(self.controller.goto_activity_logs)


