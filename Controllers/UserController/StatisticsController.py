from PySide6.QtWidgets import QMessageBox, QApplication, QPushButton, QFrame


from Controllers.BaseFileController import BaseFileController
from Views.StatisticsView import StatisticsView
from Models.StatisticsModel import StatisticsModel


class StatisticsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)

        # INITIALIZE OBJECTS NEEDED
        self.stack = stack
        self.model = StatisticsModel()
        self.view = StatisticsView(self)
        self.user_role = user_role


        self.statistics_screen = self.load_ui("Resources/UIs/MainPages/statistics.ui")
        self.view.setup_statistics_ui(self.statistics_screen)
        self.center_on_screen()


        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        

        admin_buttons = [
            self.statistics_screen.findChild(QPushButton, "nav_buttonAdminPanel"),
            self.statistics_screen.findChild(QPushButton, "nav_buttonActivityLogs"),
        ]
        admin_frame = self.statistics_screen.findChild(QFrame, "baseNavFramesub2")  

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

    def goto_activity_logs(self):
        print("-- Navigating to Activity Logs")
        if not hasattr(self, 'activity_logs'):
            from Controllers.AdminController.ActivityLogsController import ActivityLogsController
            self.activity_logs = ActivityLogsController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.activity_logs.activity_logs_screen)
        self.stack.setCurrentWidget(self.activity_logs.activity_logs_screen)

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


    # SUBPAGES : GOTO NAVIGATIONS ================================

    def goto_demographics_panel(self):
        """Handle navigation to Demographics Panel screen."""
        print("-- Navigating to Statistics > Demographics")
        if not hasattr(self, 'demographic'):
            from Controllers.UserController.Statistics.Demographics.DemographicsController import DemographicsController
            self.view = DemographicsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.view.view)

        self.stack.setCurrentWidget(self.view.view)
        self.setWindowTitle("MaPro: Demographics")

    def goto_neighborhood_panel(self):
        """Handle navigation to Neighborhood Panel screen."""
        print("-- Navigating to Statistics > Neighborhood")
        if not hasattr(self, 'neighborhood'):
            from Controllers.UserController.Statistics.Neighborhood.NeighborhoodController import NeighborhoodController
            self.neighborhood_panel = NeighborhoodController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.neighborhood_panel.view)

        self.stack.setCurrentWidget(self.neighborhood_panel.view)
        self.setWindowTitle("MaPro: Neighborhood")

    def goto_household_panel(self):
        """Handle navigation to Household Panel screen."""
        print("-- Navigating to Statistics > Household")
        if not hasattr(self, 'household'):
            from Controllers.UserController.Statistics.Household.HouseholdController import HouseholdController
            self.household_panel = HouseholdController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.household_panel.view)

        self.stack.setCurrentWidget(self.household_panel.view)
        self.setWindowTitle("MaPro: Household")

    def goto_education_panel(self):
        """Handle navigation to Education Panel screen."""
        print("-- Navigating to Statistics > Education")
        if not hasattr(self, 'education'):
            from Controllers.UserController.Statistics.Education.EducationController import EducationController
            self.education_panel = EducationController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.education_panel.view)

        self.stack.setCurrentWidget(self.education_panel.view)
        self.setWindowTitle("MaPro: Education")

    def goto_employment_panel(self):
        """Handle navigation to Employment Panel screen."""
        print("-- Navigating to Statistics > Employment")
        if not hasattr(self, 'employment'):
            from Controllers.UserController.Statistics.Employment.EmploymentController import EmploymentController
            self.employment_panel = EmploymentController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.employment_panel.view)

        self.stack.setCurrentWidget(self.employment_panel.view)
        self.setWindowTitle("MaPro: Employment")

    def goto_health_panel(self):
        """Handle navigation to Health Panel screen."""
        print("-- Navigating to Statistics > Health")
        if not hasattr(self, 'health'):
            from Controllers.UserController.Statistics.Health.HealthController import HealthController
            self.health_panel = HealthController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.health_panel.view)

        self.stack.setCurrentWidget(self.health_panel.view)
        self.setWindowTitle("MaPro: Health")

    def goto_business_panel(self):
        """Handle navigation to Business Panel screen."""
        print("-- Navigating to Statistics > Business")
        if not hasattr(self, 'business_stat'):
            from Controllers.UserController.Statistics.Business.BusinessController import BusinessController
            self.business_panel = BusinessController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.business_panel.view)

        self.stack.setCurrentWidget(self.business_panel.view)
        self.setWindowTitle("MaPro: Business")

    def goto_infrastructures_panel(self):
        """Handle navigation to Infrastructure Panel screen."""
        print("-- Navigating to Statistics > Infrastructure")
        if not hasattr(self, 'infra'):
            from Controllers.UserController.Statistics.Infrastructure.InfrastructureController import InfrastructureController
            self.infra_panel = InfrastructureController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.infra_panel.view)

        self.stack.setCurrentWidget(self.infra_panel.view)
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
