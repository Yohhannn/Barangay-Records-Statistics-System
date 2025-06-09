from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QApplication, QTableWidgetItem, QHeaderView
from PySide6.QtUiTools import QUiLoader

from Controllers.BaseFileController import BaseFileController
from Views.Admin.AdminActivityLogsView import AdminActivityLogsView
from Models.AdminModels.ActivityLogsModel import ActivityLogsModel


class ActivityLogsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        self.sys_user_id = sys_user_id
        self.user_role = user_role
        self.stack = stack

        self.model = ActivityLogsModel()
        self.view = AdminActivityLogsView(self)
        # Initialize the view
        self.activity_logs_screen = self.load_ui("Resources/UIs/AdminPages/ActivityLogs/activitylogs.ui")
        # Setup the view
        self.view.setup_activity_logs_ui(self.activity_logs_screen)
        self.activity_logs_screen.setWindowTitle("Activity Logs - MaPro")

        self._refresh()


    def populate_activity_logs_table(self):
        try:
            result = self.model.get_activity_logs()
            if not result or not result['data']:
                return
            self.model.account_rows = result['data']
            self._populate_table(
                self.view.activity_logs_screen.table_logs_create,
                result['columns'],
                result['data']
            )
        except Exception as e:
            self.show_error_message("System Account Data Error", "Could not load system user accounts.")
            print(f"Error loading system user accounts: {e}")

    def _refresh(self):
        try:
            self.populate_activity_logs_table()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Manage Accounts Error",
                "Error refreshing Manage Accounts",
                QMessageBox.Ok
            )
            print(f"Error refreshing Manage Accounts: {e}")


    def show_error_message(self, title, message):
        QMessageBox.critical(
            self,
            title,
            message,
            QMessageBox.Ok
        )

    def _populate_table(self, table, headers, data):
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setForeground(Qt.black)
                if col_idx > 0:
                    item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def goto_admin_panel(self):
        print("-- Navigating to Admin Panel")
        if not hasattr(self, 'admin_panel'):
            from Controllers.AdminController.AdminPanelController import AdminPanelController
            self.admin_panel = AdminPanelController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_panel.admin_panel_screen)
        self.stack.setCurrentWidget(self.admin_panel.admin_panel_screen)

    def goto_manage_accounts(self):
        print("-- Navigating to Manage Accounts")
        if not hasattr(self, 'manage_accounts'):
            from Controllers.AdminController.ManageAccountsController import ManageAccountsController
            self.manage_accounts = ManageAccountsController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.manage_accounts.manage_accounts_screen)
        self.stack.setCurrentWidget(self.manage_accounts.manage_accounts_screen)

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
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                        self.user_role, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)
        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.UserController.StatisticsController import StatisticsController
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                         self.user_role, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)
        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                             self.user_role, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)
        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions_panel'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                            self.user_role, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)
        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                          self.user_role, self.stack)
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