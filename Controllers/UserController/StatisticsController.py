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
            from Controllers.UserController.Statistics.Demographics.DemographicsController import DemographicsController
            self.view = DemographicsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.view.view)

        self.stack.setCurrentWidget(self.view.view)
        self.setWindowTitle("MaPro: Demographics")

    def goto_neighborhood_panel(self):
        """Handle navigation to Neighborhood Panel screen."""
        print("-- Navigating to Statistics > Neighborhood")
        if not hasattr(self, 'neighborhood'):
            from Controllers.UserController.Statistics.Neighborhood.NeighborhoodController import NeighborhoodController
            self.neighborhood_panel = NeighborhoodController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.neighborhood_panel.view)

        self.stack.setCurrentWidget(self.neighborhood_panel.view)
        self.setWindowTitle("MaPro: Neighborhood")

    def goto_household_panel(self):
        """Handle navigation to Household Panel screen."""
        print("-- Navigating to Statistics > Household")
        if not hasattr(self, 'household'):
            from Controllers.UserController.Statistics.Household.household_func import household_func
            self.household_panel = household_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.household_panel.stat_household_screen)

        self.stack.setCurrentWidget(self.household_panel.stat_household_screen)
        self.setWindowTitle("MaPro: Household")

    def goto_education_panel(self):
        """Handle navigation to Education Panel screen."""
        print("-- Navigating to Statistics > Education")
        if not hasattr(self, 'education'):
            from Controllers.UserController.Statistics.Education.education_func import education_func
            self.education_panel = education_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.education_panel.stat_edu_screen)

        self.stack.setCurrentWidget(self.education_panel.stat_edu_screen)
        self.setWindowTitle("MaPro: Education")

    def goto_employment_panel(self):
        """Handle navigation to Employment Panel screen."""
        print("-- Navigating to Statistics > Employment")
        if not hasattr(self, 'employment'):
            from Controllers.UserController.Statistics.Employment.employment_func import employment_func
            self.employment_panel = employment_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.employment_panel.stat_emp_screen)

        self.stack.setCurrentWidget(self.employment_panel.stat_emp_screen)
        self.setWindowTitle("MaPro: Employment")

    def goto_health_panel(self):
        """Handle navigation to Health Panel screen."""
        print("-- Navigating to Statistics > Health")
        if not hasattr(self, 'health'):
            from Controllers.UserController.Statistics.Health.health_func import health_func
            self.health_panel = health_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.health_panel.stat_health_screen)

        self.stack.setCurrentWidget(self.health_panel.stat_health_screen)
        self.setWindowTitle("MaPro: Health")

    def goto_business_panel(self):
        """Handle navigation to Business Panel screen."""
        print("-- Navigating to Statistics > Business")
        if not hasattr(self, 'business_stat'):
            from Controllers.UserController.Statistics.Business.business_func import business_func
            self.business_panel = business_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.business_panel.stat_business_screen)

        self.stack.setCurrentWidget(self.business_panel.stat_business_screen)
        self.setWindowTitle("MaPro: Business")

    def goto_infrastructures_panel(self):
        """Handle navigation to Infrastructure Panel screen."""
        print("-- Navigating to Statistics > Infrastructure")
        if not hasattr(self, 'infra'):
            from Controllers.UserController.Statistics.Infrastructure.infrastructure_func import infrastructure_func
            self.infra_panel = infrastructure_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.infra_panel.stat_infra_screen)

        self.stack.setCurrentWidget(self.infra_panel.stat_infra_screen)
        self.setWindowTitle("MaPro: Infrastructure")

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
