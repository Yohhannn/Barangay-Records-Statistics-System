from PySide6.QtWidgets import QMessageBox, QApplication

from Controllers.BaseFileController import BaseFileController
from Models.HistoryModel import HistoryModel
from Views.HistoryRecordsView import HistoryRecordsView


class HistoryRecordsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)

        # INITIALIZE OBJECTS NEEDED
        self.stack = stack
        self.model = HistoryModel()
        self.view = HistoryRecordsView(self)

        self.history_screen = self.load_ui("Resources/UIs/MainPages/historyrecords.ui")

        self.view.setup_history_ui(self.history_screen)
        self.center_on_screen()

        self.login_window = login_window
        self.emp_first_name = emp_first_name


#### GOTO
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

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions_panel'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)


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

    # SUBPAGES : GOTO ================

    def goto_citizen_history_panel(self):
        """Handle navigation to Citizen History Panel screen."""
        print("-- Navigating to Citizen History")
        if not hasattr(self, 'citizen_history'):
            from Controllers.UserController.HistoryRecords.CitizenHistoryController import CitizenHistoryController
            self.citizen_history_panel = CitizenHistoryController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.citizen_history_panel.hist_citizen_history_screen)

        self.stack.setCurrentWidget(self.citizen_history_panel.hist_citizen_history_screen)

    def goto_medical_history_panel(self):
        """Handle navigation to Medical History Panel screen."""
        print("-- Navigating to Medical History")
        if not hasattr(self, 'medical_history'):
            from Controllers.UserController.HistoryRecords.MedicalHistoryController import MedicalHistoryController
            self.medical_history_panel = MedicalHistoryController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.medical_history_panel.hist_medical_history_screen)

        self.stack.setCurrentWidget(self.medical_history_panel.hist_medical_history_screen)

    def goto_settlement_history_panel(self):
        """Handle navigation to Settlement History Panel screen."""
        print("-- Navigating to Settlement History")
        if not hasattr(self, 'settlement_history'):
            from Controllers.UserController.HistoryRecords.SettlementHistoryController import SettlementHistoryController
            self.settlement_history_panel = SettlementHistoryController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.settlement_history_panel.hist_settlement_history_screen)

        self.stack.setCurrentWidget(self.settlement_history_panel.hist_settlement_history_screen)


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

