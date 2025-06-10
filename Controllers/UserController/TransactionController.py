from PySide6.QtWidgets import QMessageBox, QApplication, QPushButton, QFrame

from Controllers.BaseFileController import BaseFileController
from Models.CitizenModel import CitizenModel
from Models.TransactionModel import TransactionModel
from Views.CitizenPanelView import CitizenPanelView
from Views.TransactionView import TransactionView


class TransactionController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)

        # INITIALIZE OBJECTS NEEDED
        self.stack = stack
        self.model = TransactionModel()
        self.view = TransactionView(self)
        self.user_role = user_role


        # CALL OBJECT FOR METHOD IMPLEMENTATION
        self.transactions_screen = self.load_ui("Resources/UIs/MainPages/transactions.ui")

    #    self.cp_profile_screen = self.load_ui("Resources/UIs/MainPages/CitizenPanelPages/cp_citizenprofile.ui")
        self.view.setup_transaction_ui(self.transactions_screen)
        # self.view.setup_citizen_panel_ui(self.cp_profile_screen)
        self.center_on_screen()
        self.citizen_data = {}
        # self.part1_popup = None
        # self.part2_popup = None
        # self.part3_popup = None

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        
        admin_buttons = [
            self.transactions_screen.findChild(QPushButton, "nav_buttonAdminPanel"),
            self.transactions_screen.findChild(QPushButton, "nav_buttonActivityLogs"),
        ]
        admin_frame = self.transactions_screen.findChild(QFrame, "baseNavFramesub2")  

        if self.user_role in ['Admin', 'Super Admin']:
            print("Should show admin buttons")
            for btn in admin_buttons:
                if btn:
                    btn.setVisible(True)
                    btn.setEnabled(True)
            if admin_frame:
                admin_frame.setVisible(True)
        else:
            print("Should hide admin buttons")
            for btn in admin_buttons:
                if btn:
                    btn.setVisible(False)
                    btn.setEnabled(False)
            if admin_frame:
                admin_frame.setVisible(False)

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
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
    
    def goto_admin_panel(self):
        print("-- Navigating to Admin Panel")
        if not hasattr(self, 'admin_panel'):
            from Controllers.AdminController.AdminPanelController import AdminPanelController
            self.admin_panel = AdminPanelController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_panel.admin_panel_screen)
        self.stack.setCurrentWidget(self.admin_panel.admin_panel_screen)


    def goto_trashbin_panel(self):
        print("-- Navigating to AdmiTrashhbin Panel")

        if not hasattr(self, 'trashbin_panel'):
            from Controllers.AdminController.AdminBinController import AdminBinController
            self.trashbin_panel = AdminBinController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.trashbin_panel.trashbin_screen)
        self.stack.setCurrentWidget(self.trashbin_panel.trashbin_screen)

    def goto_activity_logs(self):
        print("-- Navigating to Activity Logs")
        if not hasattr(self, 'activity_logs'):
            from Controllers.AdminController.ActivityLogsController import ActivityLogsController
            self.activity_logs = ActivityLogsController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.activity_logs.activity_logs_screen)
        self.stack.setCurrentWidget(self.activity_logs.activity_logs_screen)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.UserController.StatisticsController import StatisticsController
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
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
    # def goto_institutions_panel(self):
    #     """Handle navigation to Institutions Panel screen."""
    #     print("-- Navigating to Institutions")
    #     if not hasattr(self, 'institutions'):
    #         from Controllers.Categories.institution_func import institutions_func
    #         self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
    #         self.stack.addWidget(self.institutions_panel.institutions_screen)
    #
    #     self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
    #     self.setWindowTitle("MaPro: Institutions")
    #
    # # def goto_transactions_panel(self):
    # #     """Handle navigation to Transactions Panel screen."""
    # #     print("-- Navigating to Transactions")
    # #     if not hasattr(self, 'transactions'):
    # #         from Controllers.MainController.Transactions.transaction_func import transaction_func
    # #         self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
    # #         self.stack.addWidget(self.transactions_panel.transactions_screen)
    # #
    # #     self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
    # #     self.setWindowTitle("MaPro: Transactions")
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
    #
    # SUBPAGES : GOTO ===========
    def goto_services_panel(self):
        """Handle navigation to Services Panel screen."""
        self.setWindowTitle("MaPro: Services")
        print("-- Navigating to Services")
        if not hasattr(self, 'services'):
            from Controllers.UserController.Transactions.ServicesController import ServiceController
            self.services_panel = ServiceController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.services_panel.trans_services_screen)

        self.stack.setCurrentWidget(self.services_panel.trans_services_screen)


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
