from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMessageBox, QApplication

from Controllers.BaseFileController import BaseFileController


class history_func(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.history_screen = self.load_ui("Resources/UIs/MainPages/historyrecords.ui")
        self.setup_history_ui()
        self.center_on_screen()


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
            from Controllers.Categories.citizen_func import citizen_func
            self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.Categories.statistics_func import statistics_func
            self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Controllers.Categories.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions'):
            from Controllers.Categories.transaction_func import transaction_func
            self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
        self.setWindowTitle("MaPro: Transactions")

    # SUBPAGES : GOTO ================

    def goto_citizen_history_panel(self):
        """Handle navigation to Citizen History Panel screen."""
        print("-- Navigating to Citizen History")
        if not hasattr(self, 'citizen_history'):
            from Controllers.Categories.Citizen_History.CitizenHistoryController import citizen_history_func
            self.citizen_history_panel = citizen_history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_history_panel.hist_citizen_history_screen)

        self.stack.setCurrentWidget(self.citizen_history_panel.hist_citizen_history_screen)

    def goto_medical_history_panel(self):
        """Handle navigation to Medical History Panel screen."""
        print("-- Navigating to Medical History")
        if not hasattr(self, 'medical_history'):
            from Controllers.Categories.Medical_History.medical_history_func import medical_history_func
            self.medical_history_panel = medical_history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.medical_history_panel.hist_medical_history_screen)

        self.stack.setCurrentWidget(self.medical_history_panel.hist_medical_history_screen)

    def goto_settlement_history_panel(self):
        """Handle navigation to Settlement History Panel screen."""
        print("-- Navigating to Settlement History")
        if not hasattr(self, 'settlement_history'):
            from Controllers.Categories.Settlement_History.settlement_history_func import settlement_history_func
            self.settlement_history_panel = settlement_history_func(self.login_window, self.emp_first_name, self.stack)
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



