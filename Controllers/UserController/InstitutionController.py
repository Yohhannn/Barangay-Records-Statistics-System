from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMessageBox, QApplication
from psycopg2.errorcodes import INAPPROPRIATE_ISOLATION_LEVEL_FOR_BRANCH_TRANSACTION

from Controllers.BaseFileController import BaseFileController
from Models.InstitutionModel import InstitutionsModel
from Views.InstitutionView import InstitutionsView


class InstitutionsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.stack = stack
        self.model = InstitutionsModel()
        self.view = InstitutionsView(self)

        self.institutions_screen = self.load_ui("Resources/UIs/MainPages/institutions.ui")
        self.view.setup_institutions_ui(self.institutions_screen)
        self.center_on_screen()


    # GOTO NAVIGATIONS ================================
    def goto_dashboard_panel(self):
        """Return to dashboard screen"""
        print("-- Navigating to Dashboard")
        self.stack.setCurrentIndex(0)
    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.UserController.StatisticsController import StatisticsController
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions_panel'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)
    # def goto_dashboard_panel(self):
    #     """Return to dashboard screen"""
    #     print("-- Navigating to Dashboard")
    #     self.stack.setCurrentIndex(0)
    #     self.setWindowTitle("MaPro: Dashboard")
    #
    # def goto_citizen_panel(self):
    #     """Handle navigation to Citizen Panel screen."""
    #     print("-- Navigating to Citizen Panel")
    #     if not hasattr(self, 'citizen_panel'):
    #         from Controllers.Categories.citizen_func import citizen_func
    #         self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.citizen_panel.citizen_panel_screen)
    #
    #     self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
    #     self.setWindowTitle("MaPro: Citizen Panel")
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
    #     self.setWindowTitle("MaPro: Statistics")
    #
    # # def goto_institutions_panel(self):
    # #     """Handle navigation to Institutions Panel screen."""
    # #     print("-- Navigating to Institutions")
    # #     if not hasattr(self, 'institutions'):
    # #         from Controllers.Categories.institution_func import institutions_func
    # #         self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
    # #         self.stack.addWidget(self.institutions_panel.institutions_screen)
    # #
    # #     self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
    # #     self.setWindowTitle("MaPro: Institutions")
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
    #     self.setWindowTitle("MaPro: Transactions")
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
    #     self.setWindowTitle("MaPro: History Records")

    # SUB PAGES : GOTO =============
    def goto_business_panel(self):
        """Handle navigation to Business Panel screen."""
        print("-- Navigating to Business Panel")
        if not hasattr(self, 'business'):
            from Controllers.UserController.Institutions.BusinessController import BusinessController
            self.business_panel = BusinessController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.business_panel.inst_business_screen)

        self.stack.setCurrentWidget(self.business_panel.inst_business_screen)
        self.setWindowTitle("MaPro: Business")

    def goto_infrastructure_panel(self):
        """Handle navigation to Infrastructure Panel screen."""
        print("-- Navigating to Infrastructure Panel")
        if not hasattr(self, 'infrastructure'):
            from Controllers.UserController.Institutions.InfrastructureController import InfrastructureController
            self.infra_panel = InfrastructureController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.infra_panel.inst_infrastructure_screen)

        self.stack.setCurrentWidget(self.infra_panel.inst_infrastructure_screen)
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


