# from PySide6.QtGui import QIcon
#
# from Controllers.UserController.Statistics.Demographics.DemographicsController import DemographicsController
# from Controllers.BaseFileController import BaseFileController
#
# class DemographicsView(BaseFileController):
#     def __init__(self, login_window, emp_first_name, stack):
#         super().__init__(login_window, emp_first_name)
#         self.stack = stack
#         self.stat_demo_screen = self.load_ui("Resources/UIs/MainPages/StatisticPages/demographic.ui")
#         self.controller = DemographicsController(self)
#         self.setup_demo_ui()
#         self.center_on_screen()
#
#         # Call controller to load stats
#         self.controller.load_age_group_statistics()
#
#     def setup_demo_ui(self):
#         self.setFixedSize(1350, 850)
#         self.setWindowTitle("MaPro: Demographics")
#         self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
#
#         # Set images and icons
#         self.stat_demo_screen.btn_returnToStatisticsPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
#         self.stat_demo_screen.icon_male.setIcon(QIcon('Resources/Icons/Icons/General_Icons/icon_male.png'))
#         self.stat_demo_screen.icon_female.setIcon(QIcon('Resources/Icons/Icons/General_Icons/icon_female.png'))
#
#         # Return Button
#         self.stat_demo_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics_panel)
#         pass
#
#     def set_age_group_labels(self, data):
#         """Update labels for age groups from DB results."""
#         (child, minor, young_adult, adult, middle_aged, senior) = data
#         self.stat_demo_screen.lbl_child.setText(str(child))
#         self.stat_demo_screen.lbl_minor.setText(str(minor))
#         self.stat_demo_screen.lbl_young_adult.setText(str(young_adult))
#         self.stat_demo_screen.lbl_adult.setText(str(adult))
#         self.stat_demo_screen.lbl_middle_aged.setText(str(middle_aged))
#         self.stat_demo_screen.lbl_senior.setText(str(senior))
#
#     def set_civil_status_labels(self, data):
#         """Update civil status distribution labels."""
#         for status, male, female, total in data:
#             # Update labels dynamically for each status
#             pass
