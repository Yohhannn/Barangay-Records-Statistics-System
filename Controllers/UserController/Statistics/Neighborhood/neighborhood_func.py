# from PySide6.QtGui import QIcon
# from PySide6.QtCore import QTimer
# from PySide6.QtCore import QDateTime
#
# from Controllers.BaseFileController import BaseFileController
#
# class neighborhood_func(BaseFileController):
#     def __init__(self, login_window, emp_first_name, stack):
#         super().__init__(login_window, emp_first_name)
#         self.stack = stack
#         self.stat_neighborhood_screen = self.load_ui("Resources/UIs/MainPages/StatisticPages/neighborhood.ui")
#         self._setup_date()
#         self._setup_time()
#         self.setup_neighborhood_ui()
#         self.center_on_screen()
#
#     def setup_neighborhood_ui(self):
#         """Setup the Neighborhood Views layout."""
#         self.setFixedSize(1350, 850)
#         self.setWindowTitle("MaPro: Neighborhood")
#         self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))
#
#     # Set images and icons
#         self.stat_neighborhood_screen.btn_returnToStatisticsPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
#
#         # Return Button
#         self.stat_neighborhood_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics_panel)
#
#     def _setup_time(self):
#         self.timer = QTimer(self.stat_neighborhood_screen)
#
#         # Initialize with current date/time
#         self._setup_date()
#
#         # Connect timer to update function
#         self.timer.timeout.connect(self._setup_date)
#         self.timer.start(1000)  # Update every second
#
#     def _setup_date(self):
#         """Update both date and time labels"""
#         current_datetime = QDateTime.currentDateTime()
#
#         # Update date label
#         formatted_date = current_datetime.toString("MMMM d, yyyy")
#         day_of_week = current_datetime.toString("dddd")
#         self.stat_neighborhood_screen.text_date.setText(f"{formatted_date} - {day_of_week}")
#
#         # Update time label
#         formatted_time = current_datetime.toString("h:mm:ss AP")
#         self.stat_neighborhood_screen.text_time.setText(formatted_time)
#
#     def goto_statistics_panel(self):
#         """Handle navigation to Statistics Panel screen."""
#         print("-- Navigating to Statistics")
#         if not hasattr(self, 'statistics_panel'):
#             from Controllers.UserController.StatisticsController import StatisticsController
#             self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.statistics_panel.statistics_screen)
#
#         self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
#         self.setWindowTitle("MaPro: Statistics")