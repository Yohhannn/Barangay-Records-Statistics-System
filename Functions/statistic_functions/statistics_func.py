import cv2
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QLabel, QButtonGroup, QRadioButton
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class statistics_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.statistics_screen = self.load_ui("UI/MainPages/statistics.ui")
        self.setup_ui()
        self.center_on_screen()

    def setup_ui(self):
        """Setup the statistics UI layout."""
        self.setFixedSize(1350, 850)  # Set size for statistics screen
        self.setWindowTitle("MaPro: Statistics")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))


        self.statistics_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        self.statistics_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
        self.statistics_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
        self.statistics_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
        self.statistics_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
        self.statistics_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
        self.statistics_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

        self.statistics_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
        self.statistics_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
        self.statistics_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
        # self.citizen_panel_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
        self.statistics_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
        # self.statistics_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        # # self.statistics_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics) # UNNECESSARY
        # self.statistics_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
        # self.statistics_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
        # self.statistics_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

            # Set Images for the Statistics Categories
        self.statistics_screen.statistics_ButtonDemographic.setIcon(QIcon('Assets/Images/img_demographic.png'))
        self.statistics_screen.statistics_ButtonGeographic.setIcon(QIcon('Assets/Images/img_geographic.png'))
        self.statistics_screen.statistics_ButtonHousehold.setIcon(QIcon('Assets/Images/img_household.png'))
        self.statistics_screen.statistics_ButtonSocioEconomic.setIcon(QIcon('Assets/Images/img_socioeconomic.png'))
        self.statistics_screen.statistics_ButtonVoters.setIcon(QIcon('Assets/Images/img_voters.png'))
        self.statistics_screen.statistics_ButtonHealth.setIcon(QIcon('Assets/Images/img_health.png'))
        self.statistics_screen.statistics_ButtonJobs.setIcon(QIcon('Assets/Images/img_jobs.png'))
        self.statistics_screen.statistics_ButtonGroups.setIcon(QIcon('Assets/Images/img_groups.png'))

        # self.statistics_screen.statistics_ButtonDemographic.clicked.connect(self.goto_demographics)
        # self.statistics_screen.statistics_ButtonGeographic.clicked.connect(self.goto_geographics)
        # self.statistics_screen.statistics_ButtonHousehold.clicked.connect(self.goto_household)
        # self.statistics_screen.statistics_ButtonSocioEconomic.clicked.connect(self.goto_socioeco)
        # self.statistics_screen.statistics_ButtonVoters.clicked.connect(self.goto_voters)
        # self.statistics_screen.statistics_ButtonHealth.clicked.connect(self.goto_health)
        # self.statistics_screen.statistics_ButtonJobs.clicked.connect(self.goto_jobs)
        # self.statistics_screen.statistics_ButtonGroups.clicked.connect(self.goto_groups)

            # Connect logout button
        # self.statistics_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)


    def goto_dashboard(self):
        """Return to dashboard screen"""
        self.stack.setCurrentIndex(0)
        self.setWindowTitle("MaPro: Dashboard")

