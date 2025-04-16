import cv2
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QLabel, QButtonGroup, QRadioButton
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class institutions_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.institutions_screen = self.load_ui("UI/MainPages/institutions.ui")
        self.setup_ui()
        self.center_on_screen()

    def setup_ui(self):
        """Setup the institutions UI layout."""
        self.setFixedSize(1350, 850)  # Set size for business screen
        self.setWindowTitle("MaPro: Institutions")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        # Set images and icons for the navbar
        self.institutions_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        self.institutions_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
        self.institutions_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
        self.institutions_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
        self.institutions_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
        self.institutions_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
        self.institutions_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

        self.institutions_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
        self.institutions_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
        self.institutions_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

        self.institutions_screen.inst_ButtonCategory_Business.setIcon(QIcon('Assets/Images/img_category_business.png'))
        self.institutions_screen.inst_ButtonCategory_Infrastructure.setIcon(
            QIcon('Assets/Images/img_category_infrastructure.png'))

        # Connect navbar buttons
        self.institutions_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
        # self.institutions_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
        # self.institutions_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
        # # self.institutions.screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
        # self.institutions_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
        # self.institutions_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

        # self.institutions_screen.inst_ButtonCategory_Business.clicked.connect()
        # self.institutions_screen.inst_ButtonCategory_Infrastructure.clicked.connect()

        # Connect logout button
        # self.institutions_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)
    def goto_dashboard(self):
        """Return to dashboard screen"""
        self.stack.setCurrentIndex(0)
        self.setWindowTitle("MaPro: Dashboard")
