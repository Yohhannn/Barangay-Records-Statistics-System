from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPixmap, QIcon


class AdminActivityLogsView:
    def __init__(self, controller):
        self.controller = controller
        self.activity_logs_screen = None
        self.app_name = "MaPro"
        self.app_version = "5.1.10 - Alpha"

    def setup_activity_logs_ui(self, ui_screen):
        self.activity_logs_screen = ui_screen
        # self._setup_date()
        # self._setup_time()
        self._setup_window_properties()
        self._setup_navigation_assets()
        self._connect_buttons()

    def _setup_window_properties(self):
        self.activity_logs_screen.setFixedSize(1350, 850)
        self.controller.setFixedSize(1350, 850)
        self.controller.setWindowTitle(f"{self.app_name} {self.app_version}")
        self.controller.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # def _setup_time(self):
    #     self.timer = QTimer(self.activity_logs_screen)
    #     self._setup_date()
    #     self.timer.timeout.connect(self._setup_date)
    #     self.timer.start(1000)

    # def _setup_date(self):
    #     current_datetime = QDateTime.currentDateTime()
    #     formatted_date = current_datetime.toString("MMMM d, yyyy")
    #     day_of_week = current_datetime.toString("dddd")
    #     self.activity_logs_screen.label_dateDashboard.setText(f"{formatted_date} - {day_of_week}")
    #     formatted_time = current_datetime.toString("h:mm:ss AP")
    #     self.activity_logs_screen.label_timeDashboard.setText(formatted_time)

    def _setup_navigation_assets(self):
        nav_icons = {
            'nav_imageLogo': "Resources/Images/General_Images/logo_brgyClear.png",
            'nav_buttonDashboard': 'Resources/Icons/General_Icons/icon_dashboard.svg',
            'nav_buttonCitizenPanel': 'Resources/Icons/General_Icons/icon_citizenpanel.svg',
            'nav_buttonStatistics': 'Resources/Icons/General_Icons/icon_statistics.svg',
            'nav_buttonInstitutions': 'Resources/Icons/General_Icons/icon_institutions.svg',
            'nav_buttonTransactions': 'Resources/Icons/General_Icons/icon_transaction.svg',
            'nav_buttonHistoryRecords': 'Resources/Icons/General_Icons/icon_historyrecord_closed.svg',
            'nav_buttonAdminPanel': 'Resources/Icons/General_Icons/icon_adminoverview_off.svg',
            'nav_buttonActivityLogs': 'Resources/Icons/General_Icons/icon_activitylogs_off.svg'
        }

        for widget_name, icon_path in nav_icons.items():
            widget = getattr(self.activity_logs_screen, widget_name, None)
            if widget:
                if 'image' in widget_name:
                    widget.setPixmap(QPixmap(icon_path))
                else:
                    widget.setIcon(QIcon(icon_path))

    def _connect_buttons(self):

        # Navigation buttons
        self.activity_logs_screen.nav_buttonAdminPanel.clicked.connect(self.controller.goto_admin_panel)
        self.activity_logs_screen.nav_buttonDashboard.clicked.connect(self.controller.goto_dashboard_panel)
        self.activity_logs_screen.nav_buttonCitizenPanel.clicked.connect(self.controller.goto_citizen_panel)
        self.activity_logs_screen.nav_buttonStatistics.clicked.connect(self.controller.goto_statistics_panel)
        self.activity_logs_screen.nav_buttonInstitutions.clicked.connect(self.controller.goto_institutions_panel)
        self.activity_logs_screen.nav_buttonTransactions.clicked.connect(self.controller.goto_transactions_panel)
        self.activity_logs_screen.nav_buttonHistoryRecords.clicked.connect(self.controller.goto_history_panel)
        self.activity_logs_screen.logout_buttonLogout.clicked.connect(self.controller.logout)