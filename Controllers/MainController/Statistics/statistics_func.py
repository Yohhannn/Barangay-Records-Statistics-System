from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtWidgets import QMessageBox, QApplication

from Controllers.base_file_func import base_file_func

class statistics_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.statistics_screen = self.load_ui("Views/MainPages/statistics.ui")
        self.setup_statistics_ui()
        self.center_on_screen()

    def setup_statistics_ui(self):
        """Setup the statistics Views layout."""
        self.setFixedSize(1350, 850)  # Set size for statistics screen
        self.setWindowTitle("MaPro: Statistics")
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

        # SET NAVIGATION MAIN ASSETS
        self.statistics_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/logo_brgyClear.png"))
        self.statistics_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/icon_dashboard.svg'))
        self.statistics_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/icon_citizenpanel.svg'))
        self.statistics_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/icon_statistics.svg'))
        self.statistics_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/icon_institutions.svg'))
        self.statistics_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/icon_transaction.svg'))
        self.statistics_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/icon_historyrecord_closed.svg'))

        # SET NAVIGATION ADMIN ASSETS
        self.statistics_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/icon_adminoverview_off.svg'))
        self.statistics_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/icon_activitylogs_off.svg'))
        self.statistics_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/icon_isLocked.svg'))

        # SET MAIN STATISTICS SCREEN ASSETS
        self.statistics_screen.statistics_ButtonDemographic.setIcon(QIcon('Resources/Images/img_demographic.png'))
        self.statistics_screen.statistics_ButtonNeighborhood.setIcon(QIcon('Resources/Images/img_neighborhood.png'))
        # self.statistics_screen.statistics_ButtonGeographic.setIcon(QIcon('Resources/Images/img_geographic.png'))        -- Renamed Geographic into Neighborhood
        self.statistics_screen.statistics_ButtonHousehold.setIcon(QIcon('Resources/Images/img_household.png'))
        self.statistics_screen.statistics_ButtonEducation.setIcon(QIcon('Resources/Images/img_education.png'))
        self.statistics_screen.statistics_ButtonEmployment.setIcon(QIcon('Resources/Images/img_employment.png'))
        # self.statistics_screen.statistics_ButtonSocioEconomic.setIcon(QIcon('Resources/Images/img_socioeconomic.png'))  -- Removed SocioEconomic Replaced into Education
        # self.statistics_screen.statistics_ButtonVoters.setIcon(QIcon('Resources/Images/img_voters.png'))                -- Removed Voters Replaced into Employment
        self.statistics_screen.statistics_ButtonHealth.setIcon(QIcon('Resources/Images/img_health.png'))
        self.statistics_screen.statistics_ButtonBusiness.setIcon(QIcon('Resources/Images/img_business.png'))
        # self.statistics_screen.statistics_ButtonJobs.setIcon(QIcon('Resources/Images/img_jobs.png'))                    -- Removed Jobs Replaced into Business
        self.statistics_screen.statistics_ButtonInfrastructures.setIcon(QIcon('Resources/Images/img_infrastructure.png'))
        # self.statistics_screen.statistics_ButtonGroups.setIcon(QIcon('Resources/Images/img_groups.png'))                -- Removed Groups Replaced into Infrastructure

        # SUBPAGES: NAVIGATIONAL BUTTONS --> GOTO
        self.statistics_screen.statistics_ButtonDemographic.clicked.connect(self.goto_demographics_panel)
        self.statistics_screen.statistics_ButtonNeighborhood.clicked.connect(self.goto_neighborhood_panel)
        # self.statistics_screen.statistics_ButtonGeographic.clicked.connect(self.goto_geographics_panel)
        self.statistics_screen.statistics_ButtonHousehold.clicked.connect(self.goto_household_panel)
        self.statistics_screen.statistics_ButtonEducation.clicked.connect(self.goto_education_panel)
        self.statistics_screen.statistics_ButtonEmployment.clicked.connect(self.goto_employment_panel)
        # self.statistics_screen.statistics_ButtonSocioEconomic.clicked.connect(self.goto_socioeconomic_panel)
        # self.statistics_screen.statistics_ButtonVoters.clicked.connect(self.goto_voters_panel)
        self.statistics_screen.statistics_ButtonHealth.clicked.connect(self.goto_health_panel)
        self.statistics_screen.statistics_ButtonBusiness.clicked.connect(self.goto_business_panel)
        # self.statistics_screen.statistics_ButtonJobs.clicked.connect(self.goto_jobs_panel)
        self.statistics_screen.statistics_ButtonInfrastructures.clicked.connect(self.goto_infrastructures_panel)
        # self.statistics_screen.statistics_ButtonGroups.clicked.connect(self.goto_groups_panel)

        # NAVIGATIONAL BUTTONS --> GOTO
        self.statistics_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard_panel)
        self.statistics_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        # self.statistics_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics_panel)
        self.statistics_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)
        self.statistics_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions_panel)
        self.statistics_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_panel)
        self.statistics_screen.logout_buttonLogout.clicked.connect(self.logout)

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

    # def goto_statistics_panel(self):
    #     """Handle navigation to Statistics Panel screen."""
    #     print("-- Navigating to Statistics")
    #     if not hasattr(self, 'statistics_panel'):
    #         from Controllers.MainController.Statistics.statistics_func import statistics_func
    #         self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.statistics_panel.statistics_screen)
    #
    #     self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
    #     self.setWindowTitle("MaPro: Statistics")

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

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.MainController.History_Records.history_func import history_func
            self.history_panel = history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)
        self.setWindowTitle("MaPro: History Records")

    # SUBPAGES : GOTO NAVIGATIONS ================================

    def goto_demographics_panel(self):
        """Handle navigation to Demographics Panel screen."""
        print("-- Navigating to Statistics > Demographics")
        if not hasattr(self, 'demographic'):
            from Controllers.MainController.Statistics.Demographics.demographics_func import demographics_func
            self.demo_panel = demographics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.demo_panel.stat_demo_screen)

        self.stack.setCurrentWidget(self.demo_panel.stat_demo_screen)
        self.setWindowTitle("MaPro: Demographics")

    def goto_neighborhood_panel(self):
        """Handle navigation to Neighborhood Panel screen."""
        print("-- Navigating to Statistics > Neighborhood")
        if not hasattr(self, 'neighborhood'):
            from Controllers.MainController.Statistics.Neighborhood.neighborhood_func import neighborhood_func
            self.neighborhood_panel = neighborhood_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.neighborhood_panel.stat_neighborhood_screen)

        self.stack.setCurrentWidget(self.neighborhood_panel.stat_neighborhood_screen)
        self.setWindowTitle("MaPro: Neighborhood")

    # def goto_geographics_panel(self):
    #     """Handle navigation to Geographics Panel screen."""
    #     print("-- Navigating to Statistics > Geographics")
    #     if not hasattr(self, 'geographic'):
    #         from Controllers.MainController.Statistics.Geographics.geographics_func import geographics_func
    #         self.geo_panel = geographics_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.geo_panel.stat_geo_screen)
    #
    #     self.stack.setCurrentWidget(self.geo_panel.stat_geo_screen)
    #     self.setWindowTitle("MaPro: Geographics")

    def goto_household_panel(self):
        """Handle navigation to Household Panel screen."""
        print("-- Navigating to Statistics > Household")
        if not hasattr(self, 'household'):
            from Controllers.MainController.Statistics.Household.household_func import household_func
            self.household_panel = household_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.household_panel.stat_household_screen)

        self.stack.setCurrentWidget(self.household_panel.stat_household_screen)
        self.setWindowTitle("MaPro: Household")

    # def goto_socioeconomic_panel(self):
    #     """Handle navigation to SocioEconomic Panel screen."""
    #     print("-- Navigating to Statistics > SocioEconomic")
    #     if not hasattr(self, 'socioeconomic'):
    #         from Controllers.MainController.Statistics.SocioEconomic.socioeconomic_func import socioeconomic_func
    #         self.socioeconomic_panel = socioeconomic_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.socioeconomic_panel.stat_socioeconomic_screen)
    #
    #     self.stack.setCurrentWidget(self.socioeconomic_panel.stat_socioeconomic_screen)
    #     self.setWindowTitle("MaPro: SocioEconomic")

    def goto_education_panel(self):
        """Handle navigation to Education Panel screen."""
        print("-- Navigating to Statistics > Education")
        if not hasattr(self, 'education'):
            from Controllers.MainController.Statistics.Education.education_func import education_func
            self.education_panel = education_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.education_panel.stat_edu_screen)

        self.stack.setCurrentWidget(self.education_panel.stat_edu_screen)
        self.setWindowTitle("MaPro: Education")

    def goto_employment_panel(self):
        """Handle navigation to Employment Panel screen."""
        print("-- Navigating to Statistics > Employment")
        if not hasattr(self, 'employment'):
            from Controllers.MainController.Statistics.Employment.employment_func import employment_func
            self.employment_panel = employment_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.employment_panel.stat_emp_screen)

        self.stack.setCurrentWidget(self.employment_panel.stat_emp_screen)
        self.setWindowTitle("MaPro: Employment")

    # def goto_voters_panel(self):
    #     """Handle navigation to Voters Panel screen."""
    #     print("-- Navigating to Statistics > Voters")
    #     if not hasattr(self, 'voters'):
    #         from Controllers.MainController.Statistics.Voters.voters_func import voters_func
    #         self.voters_panel = voters_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.voters_panel.stat_voters_screen)
    #
    #     self.stack.setCurrentWidget(self.voters_panel.stat_voters_screen)
    #     self.setWindowTitle("MaPro: Voters")

    def goto_health_panel(self):
        """Handle navigation to Health Panel screen."""
        print("-- Navigating to Statistics > Health")
        if not hasattr(self, 'health'):
            from Controllers.MainController.Statistics.Health.health_func import health_func
            self.health_panel = health_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.health_panel.stat_health_screen)

        self.stack.setCurrentWidget(self.health_panel.stat_health_screen)
        self.setWindowTitle("MaPro: Health")

    def goto_business_panel(self):
        """Handle navigation to Business Panel screen."""
        print("-- Navigating to Statistics > Business")
        if not hasattr(self, 'business_stat'):
            from Controllers.MainController.Statistics.Business.business_func import business_func
            self.business_panel = business_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.business_panel.stat_business_screen)

        self.stack.setCurrentWidget(self.business_panel.stat_business_screen)
        self.setWindowTitle("MaPro: Business")

    # def goto_jobs_panel(self):
    #     """Handle navigation to Jobs Panel screen."""
    #     print("-- Navigating to Statistics > Jobs")
    #     if not hasattr(self, 'jobs'):
    #         from Controllers.MainController.Statistics.Jobs.jobs_func import jobs_func
    #         self.jobs_panel = jobs_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.jobs_panel.stat_jobs_screen)
    #
    #     self.stack.setCurrentWidget(self.jobs_panel.stat_jobs_screen)
    #     self.setWindowTitle("MaPro: Jobs")

    def goto_infrastructures_panel(self):
        """Handle navigation to Infrastructure Panel screen."""
        print("-- Navigating to Statistics > Infrastructure")
        if not hasattr(self, 'infra'):
            from Controllers.MainController.Statistics.Infrastructure.infrastructure_func import infrastructure_func
            self.infra_panel = infrastructure_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.infra_panel.stat_infra_screen)

        self.stack.setCurrentWidget(self.infra_panel.stat_infra_screen)
        self.setWindowTitle("MaPro: Infrastructure")

    # def goto_groups_panel(self):
    #     """Handle navigation to Groups Panel screen."""
    #     print("-- Navigating to Statistics > Groups")
    #     if not hasattr(self, 'groups'):
    #         from Controllers.MainController.Statistics.Groups.groups_func import groups_func
    #         self.groups_panel = groups_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.groups_panel.stat_groups_screen)
    #
    #     self.stack.setCurrentWidget(self.groups_panel.stat_groups_screen)
    #     self.setWindowTitle("MaPro: Groups")

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
