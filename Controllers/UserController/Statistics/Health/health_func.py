from PySide6.QtGui import QIcon

from Controllers.BaseFileController import BaseFileController
class health_func(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.stat_health_screen = self.load_ui("Resources/UIs/MainPages/StatisticPages/health.ui")
        self.setup_health_ui()
        self.center_on_screen()

    def setup_health_ui(self):
        """Setup the Health Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Health")
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.stat_health_screen.btn_returnToStatisticsPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))

        # Return Button
        self.stat_health_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics_panel)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.UserController.StatisticsController import StatisticsController
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")