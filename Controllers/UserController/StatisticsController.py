from PySide6.QtWidgets import QMessageBox, QApplication


from Controllers.BaseFileController import BaseFileController
from Views.StatisticsView import StatisticsView
from Models.StatisticsModel import StatisticsModel


class StatisticsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)

        # INITIALIZE OBJECTS NEEDED
        self.stack = stack
        self.model = StatisticsModel()
        self.view = StatisticsView(self)


        self.statistics_screen = self.load_ui("Resources/UIs/MainPages/statistics.ui")
        self.view.setup_statistics_ui(self.statistics_screen)
        self.center_on_screen()


        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name




    def goto_dashboard_panel(self):
        """Return to dashboard screen"""
        print("-- Navigating to Dashboard")
        self.stack.setCurrentIndex(0)
    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions_panel'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)
    # def goto_dashboard_panel(self):
    #     """Return to dashboard screen"""
    #     print("-- Navigating to Dashboard")
    #     self.stack.setCurrentIndex(0)
    #
    # def goto_citizen_panel(self):
    #     """Handle navigation to Citizen Panel screen."""
    #     print("-- Navigating to Citizen Panel")
    #     if not hasattr(self, 'citizen_panel'):
    #         from Controllers.UserController.CitizenPanelController import CitizenPanelController
    #         self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.citizen_panel.citizen_panel_screen)
    #
    #     self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
    #
    #
    # def goto_statistics_panel(self):
    #     """Handle navigation to Statistics Panel screen."""
    #     print("-- Navigating to Statistics")
    #     if not hasattr(self, 'statistics_panel'):
    #         from Controllers.Categories.statistics_func import statistics_func
    #         self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.statistics_panel.statistics_screen)
    #
    #     self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
    #
    # def goto_institutions_panel(self):
    #     """Handle navigation to Institutions Panel screen."""
    #     print("-- Navigating to Institutions")
    #     if not hasattr(self, 'institutions'):
    #         from Controllers.Categories.institution_func import institutions_func
    #         self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.institutions_panel.institutions_screen)
    #
    #     self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
    #
    # def goto_transactions_panel(self):
    #     """Handle navigation to Transactions Panel screen."""
    #     print("-- Navigating to Transactions")
    #     if not hasattr(self, 'transactions'):
    #         from Controllers.Categories.transaction_func import transaction_func
    #         self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.transactions_panel.transactions_screen)
    #
    #     self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
    #
    # def goto_history_panel(self):
    #     """Handle navigation to History Records Panel screen."""
    #     print("-- Navigating to History Records")
    #     if not hasattr(self, 'history'):
    #         from Controllers.Categories.history_func import history_func
    #         self.history_panel = history_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.history_panel.history_screen)
    #
    #     self.stack.setCurrentWidget(self.history_panel.history_screen)








    # SUBPAGES : GOTO NAVIGATIONS ================================

    def goto_demographics_panel(self):
        """Handle navigation to Demographics Panel screen."""
        print("-- Navigating to Statistics > Demographics")
        if not hasattr(self, 'demographic'):
            from Controllers.UserController.Statistics.demographics_func import demographics_func
            self.demo_panel = demographics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.demo_panel.stat_demo_screen)

        self.stack.setCurrentWidget(self.demo_panel.stat_demo_screen)
        self.setWindowTitle("MaPro: Demographics")

    def goto_geographics_panel(self):
        """Handle navigation to Geographics Panel screen."""
        print("-- Navigating to Statistics > Geographics")
        if not hasattr(self, 'geographic'):
            from Controllers.UserController.Statistics.geographics_func import geographics_func
            self.geo_panel = geographics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.geo_panel.stat_geo_screen)

        self.stack.setCurrentWidget(self.geo_panel.stat_geo_screen)
        self.setWindowTitle("MaPro: Geographics")

    def goto_household_panel(self):
        """Handle navigation to Household Panel screen."""
        print("-- Navigating to Statistics > Household")
        if not hasattr(self, 'household'):
            from Controllers.UserController.Statistics.household_func import household_func
            self.household_panel = household_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.household_panel.stat_household_screen)

        self.stack.setCurrentWidget(self.household_panel.stat_household_screen)
        self.setWindowTitle("MaPro: Household")

    def goto_socioeconomic_panel(self):
        """Handle navigation to SocioEconomic Panel screen."""
        print("-- Navigating to Statistics > SocioEconomic")
        if not hasattr(self, 'socioeconomic'):
            from Controllers.UserController.Statistics.socioeconomic_func import socioeconomic_func
            self.socioeconomic_panel = socioeconomic_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.socioeconomic_panel.stat_socioeconomic_screen)

        self.stack.setCurrentWidget(self.socioeconomic_panel.stat_socioeconomic_screen)
        self.setWindowTitle("MaPro: SocioEconomic")

    def goto_voters_panel(self):
        """Handle navigation to Voters Panel screen."""
        print("-- Navigating to Statistics > Voters")
        if not hasattr(self, 'voters'):
            from Controllers.UserController.Statistics.voters_func import voters_func
            self.voters_panel = voters_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.voters_panel.stat_voters_screen)

        self.stack.setCurrentWidget(self.voters_panel.stat_voters_screen)
        self.setWindowTitle("MaPro: Voters")

    def goto_health_panel(self):
        """Handle navigation to Health Panel screen."""
        print("-- Navigating to Statistics > Health")
        if not hasattr(self, 'health'):
            from Controllers.UserController.Statistics.health_func import health_func
            self.health_panel = health_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.health_panel.stat_health_screen)

        self.stack.setCurrentWidget(self.health_panel.stat_health_screen)
        self.setWindowTitle("MaPro: Health")

    def goto_jobs_panel(self):
        """Handle navigation to Jobs Panel screen."""
        print("-- Navigating to Statistics > Jobs")
        if not hasattr(self, 'jobs'):
            from Controllers.UserController.Statistics.jobs_func import jobs_func
            self.jobs_panel = jobs_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.jobs_panel.stat_jobs_screen)

        self.stack.setCurrentWidget(self.jobs_panel.stat_jobs_screen)
        self.setWindowTitle("MaPro: Jobs")

    def goto_groups_panel(self):
        """Handle navigation to Groups Panel screen."""
        print("-- Navigating to Statistics > Groups")
        if not hasattr(self, 'groups'):
            from Controllers.UserController.Statistics.groups_func import groups_func
            self.groups_panel = groups_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.groups_panel.stat_groups_screen)

        self.stack.setCurrentWidget(self.groups_panel.stat_groups_screen)
        self.setWindowTitle("MaPro: Groups")

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
