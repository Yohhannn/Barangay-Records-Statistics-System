# from PySide6.QtGui import QPixmap, QIcon
# from PySide6.QtWidgets import QMessageBox, QApplication
#
# from Controllers.BaseFileController import BaseFileController
#
#
# class institutions_func(BaseFileController):
#     def __init__(self, login_window, emp_first_name, stack):
#         super().__init__(login_window, emp_first_name)
#         self.stack = stack
#         self.institutions_screen = self.load_ui("Resources/UIs/MainPages/institutions.ui")
#         self.setup_ui()
#         self.center_on_screen()
#
#     def setup_ui(self):
#         """Setup the institutions Views layout."""
#         self.setFixedSize(1350, 850)  # Set size for business screen
#         self.setWindowTitle("MaPro: Institutions")
#         self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
#
#         # Set images and icons for the navbar
#         self.institutions_screen.nav_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))
#
#         self.institutions_screen.nav_buttonDashboard.setIcon(QIcon('Resources/Icons/General_Icons/icon_dashboard.svg'))
#         self.institutions_screen.nav_buttonCitizenPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_citizenpanel.svg'))
#         self.institutions_screen.nav_buttonStatistics.setIcon(QIcon('Resources/Icons/General_Icons/icon_statistics.svg'))
#         self.institutions_screen.nav_buttonInstitutions.setIcon(QIcon('Resources/Icons/General_Icons/icon_institutions.svg'))
#         self.institutions_screen.nav_buttonTransactions.setIcon(QIcon('Resources/Icons/General_Icons/icon_transaction.svg'))
#         self.institutions_screen.nav_buttonHistoryRecords.setIcon(QIcon('Resources/Icons/General_Icons/icon_historyrecord_closed.svg'))
#
#         self.institutions_screen.nav_buttonAdminPanel.setIcon(QIcon('Resources/Icons/General_Icons/icon_adminoverview_off.svg'))
#         self.institutions_screen.nav_buttonActivityLogs.setIcon(QIcon('Resources/Icons/General_Icons/icon_activitylogs_off.svg'))
#         self.institutions_screen.nav_isLocked.setIcon(QIcon('Resources/Icons/General_Icons/icon_isLocked.svg'))
#
#         self.institutions_screen.inst_ButtonCategory_Business.setIcon(QIcon('Resources/Images/General_Images/img_category_business.png'))
#         self.institutions_screen.inst_ButtonCategory_Infrastructure.setIcon(QIcon('Resources/Images/General_Images/img_category_infrastructure.png'))
#
#         # SUBPAGES : NAVIGATIONAL BUTTONS --> GOTO
#         self.institutions_screen.inst_ButtonCategory_Business.clicked.connect(self.goto_business_panel)
#         self.institutions_screen.inst_ButtonCategory_Infrastructure.clicked.connect(self.goto_infrastructure_panel)
#
#         # NAVIGATIONAL BUTTONS --> GOTO
#         self.institutions_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard_panel)
#         self.institutions_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
#         self.institutions_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics_panel)
#         # self.institutions_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions_panel)
#         self.institutions_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions_panel)
#         self.institutions_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_panel)
#         self.institutions_screen.logout_buttonLogout.clicked.connect(self.logout)
#
#     # GOTO NAVIGATIONS ================================
#     def goto_dashboard_panel(self):
#         """Return to dashboard screen"""
#         print("-- Navigating to Dashboard")
#         self.stack.setCurrentIndex(0)
#         self.setWindowTitle("MaPro: Dashboard")
#
#     def goto_citizen_panel(self):
#         """Handle navigation to Citizen Panel screen."""
#         print("-- Navigating to Citizen Panel")
#         if not hasattr(self, 'citizen_panel'):
#             from Controllers.Categories.citizen_func import citizen_func
#             self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.citizen_panel.citizen_panel_screen)
#
#         self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
#         self.setWindowTitle("MaPro: Citizen Panel")
#
#     def goto_statistics_panel(self):
#         """Handle navigation to Statistics Panel screen."""
#         print("-- Navigating to Statistics")
#         if not hasattr(self, 'statistics_panel'):
#             from Controllers.Categories.statistics_func import statistics_func
#             self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.statistics_panel.statistics_screen)
#
#         self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
#         self.setWindowTitle("MaPro: Statistics")
#
#     # def goto_institutions_panel(self):
#     #     """Handle navigation to Institutions Panel screen."""
#     #     print("-- Navigating to Institutions")
#     #     if not hasattr(self, 'institutions'):
#     #         from Controllers.Categories.institution_func import institutions_func
#     #         self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
#     #         self.stack.addWidget(self.institutions_panel.institutions_screen)
#     #
#     #     self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
#     #     self.setWindowTitle("MaPro: Institutions")
#
#     def goto_transactions_panel(self):
#         """Handle navigation to Transactions Panel screen."""
#         print("-- Navigating to Transactions")
#         if not hasattr(self, 'transactions'):
#             from Controllers.Categories.transaction_func import transaction_func
#             self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.transactions_panel.transactions_screen)
#
#         self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
#         self.setWindowTitle("MaPro: Transactions")
#
#     def goto_history_panel(self):
#         """Handle navigation to History Records Panel screen."""
#         print("-- Navigating to History Records")
#         if not hasattr(self, 'history'):
#             from Controllers.Categories.history_func import history_func
#             self.history_panel = history_func(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.history_panel.history_screen)
#
#         self.stack.setCurrentWidget(self.history_panel.history_screen)
#         self.setWindowTitle("MaPro: History Records")
#
#     # SUB PAGES : GOTO =============
#     def goto_business_panel(self):
#         """Handle navigation to Business Panel screen."""
#         print("-- Navigating to Business Panel")
#         if not hasattr(self, 'business'):
#             from Controllers.Categories.Business.business_func import business_func
#             self.business_panel = business_func(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.business_panel.inst_business_screen)
#
#         self.stack.setCurrentWidget(self.business_panel.inst_business_screen)
#         self.setWindowTitle("MaPro: Business")
#
#     def goto_infrastructure_panel(self):
#         """Handle navigation to Infrastructure Panel screen."""
#         print("-- Navigating to Infrastructure Panel")
#         if not hasattr(self, 'infrastructure'):
#             from Controllers.Categories.Infrastructure.infrastructure_func import infrastructure_func
#             self.infra_panel = infrastructure_func(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.infra_panel.inst_infrastructure_screen)
#
#         self.stack.setCurrentWidget(self.infra_panel.inst_infrastructure_screen)
#         self.setWindowTitle("MaPro: Infrastructure")
#
#     def logout(self):
#         confirmation = QMessageBox.question(
#             self,
#             "Confirm Logout",
#             "Are you sure you want to logout?",
#             QMessageBox.Yes | QMessageBox.No,
#         )
#         if confirmation == QMessageBox.Yes:
#             QApplication.closeAllWindows()
#
#             self.login_window.show()
#             self.login_window.clear_fields()
#
#
