from PyQt6.QtCore import QDateTime
from PySide6.QtWidgets import QPushButton, QMessageBox, QApplication
from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtCore import QTimer

from Utils.util_popup import load_popup
from Utils.utils_datetime import update_date_label
from Utils.utils_realtime import update_time_label


class DashboardView:
    def __init__(self, controller):
        self.controller = controller
        self.dashboard_screen = None

        self.app_name = "MaPro"
        self.app_version = "4.2.3 - Pre Alpha"

    def setup_dashboard_ui(self, ui_screen):
        self.dashboard_screen = ui_screen
        self._setup_date()
        self._setup_time()
        self._setup_window_properties()
        self._setup_navigation_assets()
        self._setup_dashboard_assets()



        self._connect_buttons()

    def _setup_window_properties(self):
        self.dashboard_screen.setFixedSize(1350, 850)
        self.controller.setFixedSize(1350, 850)  # <- Prevent resizing the actual window

        self.controller.setWindowTitle(f"{self.app_name} {self.app_version}")
        self.controller.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
        print("test")


    def _setup_time(self):
        self.timer = QTimer(self.dashboard_screen)

        # Initialize with current date/time
        self._setup_date()

        # Connect timer to update function
        self.timer.timeout.connect(self._setup_date)
        self.timer.start(1000)  # Update every second

    def _setup_date(self):
        """Update both date and time labels"""
        current_datetime = QDateTime.currentDateTime()

        # Update date label
        formatted_date = current_datetime.toString("MMMM d, yyyy")
        day_of_week = current_datetime.toString("dddd")
        self.dashboard_screen.label_dateDashboard.setText(f"{formatted_date} - {day_of_week}")

        # Update time label
        formatted_time = current_datetime.toString("h:mm:ss AP")
        self.dashboard_screen.label_timeDashboard.setText(formatted_time)
    #
    # def _setup_date_timers(self):
    #     self.timer = QTimer(self.dashboard_screen)
    #     self.timer.timeout.connect(lambda: update_time_label(self.dashboard_screen.label_timeDashboard))
    #     self.timer.start(1000)
    #     update_date_label(self.dashboard_screen.label_dateDashboard)


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
            'nav_buttonActivityLogs': 'Resources/Icons/General_Icons/icon_activitylogs_off.svg',
            'nav_isLocked': 'Resources/Icons/General_Icons/icon_isLocked.svg'
        }

        for widget_name, icon_path in nav_icons.items():
            widget = getattr(self.dashboard_screen, widget_name, None)
            if widget:
                if 'image' in widget_name:
                    widget.setPixmap(QPixmap(icon_path))
                else:
                    widget.setIcon(QIcon(icon_path))

    def _setup_dashboard_assets(self):

        content_icons = {
            'dashboard_buttonAboutSoftware': 'Resources/Icons/General_Icons/icon_aboutsoftware.svg',
            'dashboard_buttonBarangayInfo': 'Resources/Icons/General_Icons/icon_brgyinfo.svg',
            'acc_buttonYourAccount': 'Resources/Icons/General_Icons/icon_myprofile.svg'
        }

        for widget_name, icon_path in content_icons.items():
            widget = getattr(self.dashboard_screen, widget_name, None)
            if widget:
                widget.setIcon(QIcon(icon_path))

        # Display current date and employee name
        self.dashboard_screen.title_employeeFirstNameDashboard.setText(self.controller.emp_first_name)
        self.dashboard_screen.label_UpdateVersion.setText(" " + self.app_version)

    def _connect_buttons(self):

        self.dashboard_screen.acc_buttonYourAccount.clicked.connect(self.controller.show_account_popup)
        self.dashboard_screen.dashboard_buttonBarangayInfo.clicked.connect(self.controller.show_barangayinfo_popup)
        self.dashboard_screen.dashboard_buttonAboutSoftware.clicked.connect(self.controller.show_aboutsoftware_popup)

        # Navigation buttons
        self.dashboard_screen.nav_buttonCitizenPanel.clicked.connect(self.controller.goto_citizen_panel)
        self.dashboard_screen.nav_buttonStatistics.clicked.connect(self.controller.goto_statistics_panel)
        self.dashboard_screen.nav_buttonInstitutions.clicked.connect(self.controller.goto_institutions_panel)
        self.dashboard_screen.nav_buttonTransactions.clicked.connect(self.controller.goto_transactions_panel)
        self.dashboard_screen.nav_buttonHistoryRecords.clicked.connect(self.controller.goto_history_panel)
        self.dashboard_screen.logout_buttonLogout.clicked.connect(self.controller.logout)


    # def show_barangayinfo_popup(self):
    #     popup = self.dashboard_screen
    #     print("asdasdasd")
    #     # print("-- Navigating to Dashboard > Barangay Info")
    #     try:
    #         # popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/barangayinfo.ui", self)
    #         # if popup is None:
    #         #     raise Exception("Failed to load barangayinfo popup UI")
    #
    #         popup.setWindowTitle("Barangay Information")
    #         popup.brgyinfo_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))
    #         popup.setWindowModality(Qt.ApplicationModal)
    #         # popup.setWindowTitle(f"{APP_NAME}{self.controller.app_version}")
    #         popup.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
    #         popup.setFixedSize(popup.size())
    #         popup.show()
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to show barangay info: {str(e)}")
    #         print(f"Error showing barangay info popup: {e}")