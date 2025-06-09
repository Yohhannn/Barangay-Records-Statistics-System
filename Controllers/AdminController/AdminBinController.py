from PySide6.QtWidgets import QMessageBox, QApplication, QPushButton, QFrame
from PySide6.QtGui import QPixmap, QIcon, Qt
from Controllers.BaseFileController import BaseFileController
# from Models.HistoryModel import HistoryModel
# from Views.HistoryRecordsView import HistoryRecordsView


class AdminBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)

        # INITIALIZE OBJECTS NEEDED
        self.stack = stack
        # self.model = HistoryModel()
        # self.view = HistoryRecordsView(self)
        self.user_role = user_role

        self.trashbin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/trashbin.ui")

        self.setup_trashbin_ui(self.trashbin_screen)
        self.center_on_screen()

        self.login_window = login_window
        self.emp_first_name = emp_first_name



    def setup_trashbin_ui(self, ui_screen):
        self.history_screen = ui_screen
        """Setup the History Records Views layout."""
        ui_screen.setFixedSize(1350, 850)  # Set size for business screen
        ui_screen.setWindowTitle("MaPro: History Records")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # SET NAVIGATION MAIN ASSETS
        ui_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))

        ui_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/General_Icons/icon_dashboard.svg'))
        ui_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_citizenpanel.svg'))
        ui_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/General_Icons/icon_statistics.svg'))
        ui_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/General_Icons/icon_institutions.svg'))
        ui_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/General_Icons/icon_transaction.svg'))
        ui_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/General_Icons/icon_historyrecord.svg'))

        # SET NAVIGATION ADMIN ASSETS
        ui_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_adminoverview_on.svg'))
        ui_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/General_Icons/icon_activitylogs_on.svg'))
        ui_screen.nav_buttonTrashBin.setIcon(QIcon('Resources/Icons/General_Icons/icon_trash_bin.svg'))
        # ui_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/General_Icons/icon_isLocked.svg'))

        # NAVIGATIONAL BUTTONS --> GOTO
        ui_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard_panel)
        ui_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        ui_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics_panel)
        ui_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)
        ui_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions_panel)
        ui_screen.nav_buttonAdminPanel.clicked.connect(self.goto_admin_panel)
        ui_screen.nav_buttonActivityLogs.clicked.connect(self.goto_activity_logs)
        ui_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_panel)
        ui_screen.logout_buttonLogout.clicked.connect(self.logout)
        ui_screen.trashbin_btn_citizens.clicked.connect(self.goto_citizin_bin)
        ui_screen.trashbin_btn_household.clicked.connect(self.goto_household_bin)
        ui_screen.trashbin_btn_business.clicked.connect(self.goto_business_bin)
        ui_screen.trashbin_btn_infra.clicked.connect(self.goto_infrastructure_bin)
        ui_screen.trashbin_btn_services.clicked.connect(self.goto_transaction_bin)
        ui_screen.trashbin_btn_ctzhist.clicked.connect(self.goto_citizen_history_bin)
        ui_screen.trashbin_btn_medhist.clicked.connect(self.goto_medical_history_bin)
        ui_screen.trashbin_btn_setthist.clicked.connect(self.goto_settlement_history_bin)


    def goto_dashboard_panel(self):
        """Return to dashboard screen"""
        print("-- Navigating to Dashboard")
        self.stack.setCurrentIndex(0)

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

    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                        self.user_role, self.stack)
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
            self.citizen_history_panel = CitizenHistoryController(self.login_window, self.emp_first_name,
                                                                  self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.citizen_history_panel.hist_citizen_history_screen)

        self.stack.setCurrentWidget(self.citizen_history_panel.hist_citizen_history_screen)

    def goto_medical_history_panel(self):
        """Handle navigation to Medical History Panel screen."""
        print("-- Navigating to Medical History")
        if not hasattr(self, 'medical_history'):
            from Controllers.UserController.HistoryRecords.MedicalHistoryController import MedicalHistoryController
            self.medical_history_panel = MedicalHistoryController(self.login_window, self.emp_first_name,
                                                                  self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.medical_history_panel.hist_medical_history_screen)

        self.stack.setCurrentWidget(self.medical_history_panel.hist_medical_history_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        # self.load_account_info()
        # self.load_recent_citizens_data()
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)


    def goto_settlement_history_panel(self):
        """Handle navigation to Settlement History Panel screen."""
        print("-- Navigating to Settlement History")
        if not hasattr(self, 'settlement_history'):
            from Controllers.UserController.HistoryRecords.SettlementHistoryController import \
                SettlementHistoryController
            self.settlement_history_panel = SettlementHistoryController(self.login_window, self.emp_first_name,
                                                                        self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.settlement_history_panel.hist_settlement_history_screen)

        self.stack.setCurrentWidget(self.settlement_history_panel.hist_settlement_history_screen)

    def goto_citizin_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to Citizen Bin")
        if not hasattr(self, 'citizenbin'):
            from Controllers.AdminController.AdminBin.CitizenBinController import CitizenBinController
            self.citizen_bin = CitizenBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.citizen_bin.cp_citizenbin_screen)

        self.stack.setCurrentWidget(self.citizen_bin.cp_citizenbin_screen)


    def goto_household_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to Household Bin")
        if not hasattr(self, 'householdbin'):
            from Controllers.AdminController.AdminBin.HouseholdBinController import HouseholdBinController
            self.household_bin = HouseholdBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.household_bin.cp_householdbin_screen)

        self.stack.setCurrentWidget(self.household_bin.cp_householdbin_screen)


    def goto_business_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to business Bin")
        if not hasattr(self, 'businessbin'):
            from Controllers.AdminController.AdminBin.BusinessBinController import BusinessBinController
            self.business_bin = BusinessBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.business_bin.inst_businessbin_screen)

        self.stack.setCurrentWidget(self.business_bin.inst_businessbin_screen)

    def goto_infrastructure_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to Infra Bin")
        if not hasattr(self, 'infrabin'):
            from Controllers.AdminController.AdminBin.InfrastructureBinController import InfrastructureBinController
            self.infrastructure_bin = InfrastructureBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.infrastructure_bin.inst_infrastructurebin_screen)

        self.stack.setCurrentWidget(self.infrastructure_bin.inst_infrastructurebin_screen)



    def goto_transaction_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to transaction Bin")
        if not hasattr(self, 'transactionbin'):
            from Controllers.AdminController.AdminBin.ServicesBinController import ServicesBinController
            self.services_bin = ServicesBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.services_bin.trans_servicesbin_screen)

        self.stack.setCurrentWidget(self.services_bin.trans_servicesbin_screen)



    def goto_citizen_history_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to transaction Bin")
        if not hasattr(self, 'medicalbin'):
            from Controllers.AdminController.AdminBin.CitizenHistoryBinController import CitizenHistoryBinController
            self.citizen_bin_history = CitizenHistoryBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.citizen_bin_history.hist_citizen_history_bin_screen)

        self.stack.setCurrentWidget(self.citizen_bin_history.hist_citizen_history_bin_screen)

    def goto_medical_history_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to medical Bin")
        if not hasattr(self, 'medicalbin'):
            from Controllers.AdminController.AdminBin.MedicalHistoryBinController import MedicalHistoryBinController
            self.medical_bin_history = MedicalHistoryBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.medical_bin_history.hist_medical_history_bin_screen)

        self.stack.setCurrentWidget(self.medical_bin_history.hist_medical_history_bin_screen)

    def goto_settlement_history_bin(self):
        """Handle navigation to Citizen Profile Panel screen."""
        print("-- Navigating to settlement Bin")
        if not hasattr(self, 'settlementbin'):
            from Controllers.AdminController.AdminBin.SettlementHistoryBinController import SettlementHistoryBinController
            self.settlement_bin_history = SettlementHistoryBinController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.settlement_bin_history.hist_settlement_history_bin_screen)

        self.stack.setCurrentWidget(self.settlement_bin_history.hist_settlement_history_bin_screen)
