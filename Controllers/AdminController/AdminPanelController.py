from PySide6.QtWidgets import QWidget, QMessageBox, QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from Controllers.BaseFileController import BaseFileController

from Views.Admin.AdminPanelView import AdminPanelView
from database import Database

class AdminPanelController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        self.sys_user_id = sys_user_id
        self.user_role = user_role
        self.stack = stack


        
        # Initialize the view
        self.view = AdminPanelView(self)
        

        self.admin_panel_screen = self.load_ui("Resources/UIs/AdminPages/AdminPanel/adminpanel.ui")
        # Setup the view
        self.view.setup_admin_panel_ui(self.admin_panel_screen)
        self.admin_panel_screen.setWindowTitle("Admin Panel - MaPro")

        self.set_current_user_id()
    
    def set_current_user_id(self):
        """Set the current user ID for the dashboard."""
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("Set app.current_user_id = %s", (self.sys_user_id,))
            connection.commit()
            print(f"Current user ID set to: {self.sys_user_id}")
        except Exception as e:
            print(f"Error setting current user ID: {e}")
            connection.close()

    def goto_activity_logs(self):
        print("-- Navigating to Activity Logs")
        if not hasattr(self, 'activity_logs'):
            from Controllers.AdminController.ActivityLogsController import ActivityLogsController
            self.activity_logs = ActivityLogsController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.activity_logs.activity_logs_screen)
        self.stack.setCurrentWidget(self.activity_logs.activity_logs_screen)

    def goto_manage_accounts(self):
        print("-- Navigating to Manage Accounts")
        if not hasattr(self, 'manage_accounts'):
            from Controllers.AdminController.ManageAccountsController import ManageAccountsController
            self.manage_accounts = ManageAccountsController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.manage_accounts.admin_manage_accounts_screen)
        self.stack.setCurrentWidget(self.manage_accounts.admin_manage_accounts_screen)

    def goto_admin_controls(self):
        print("-- Navigating to Admin Controls")
        if not hasattr(self, 'admin_controls'):
            from Controllers.AdminController.AdminControlsController import AdminControlsController
            self.admin_controls = AdminControlsController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_controls.admin_controls_screen)
        self.stack.setCurrentWidget(self.admin_controls.admin_controls_screen)
    
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

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions_panel'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)
        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)
        self.stack.setCurrentWidget(self.history_panel.history_screen)


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
