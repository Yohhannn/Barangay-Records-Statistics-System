from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox

from Controllers.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class groups_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.stat_groups_screen = self.load_ui("Views/MainPages/StatisticPages/groups.ui")
        self.setup_groups_ui()
        self.center_on_screen()

    def setup_groups_ui(self):
        """Setup the Groups Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Groups")
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.stat_groups_screen.btn_returnToStatisticsPage.setIcon(QIcon('Resources/FuncIcons/img_return.png'))

        # Return Button
        self.stat_groups_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics_panel)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.MainController.Statistics.statistics_func import statistics_func
            self.statistics_panel = statistics_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")