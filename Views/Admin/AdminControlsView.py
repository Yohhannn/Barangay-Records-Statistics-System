from PySide6.QtCore import QDateTime, QTimer
from PySide6.QtWidgets import QPushButton, QMessageBox, QApplication
from PySide6.QtGui import QPixmap, QIcon, Qt

from Utils.util_popup import load_popup

class AdminControlsView:
    def __init__(self, controller):
        self.controller = controller

        self.manage_accounts_screen = None
        self.app_name = "MaPro"
        self.app_version = "5.1.10 - Alpha"
    
    def setup_manage_accounts_ui(self, ui_screen):
        self.manage_accounts_screen = ui_screen
        # self._setup_window_properties()
        self._setup_navigation_assets()
        self._connect_buttons()
    
    # def _setup_window_properties(self):
    #     self.admin_panel_screen.setFixedSize(1350, 850)
    #     self.controller.setFixedSize(1350, 850)
    #     self.controller.setWindowTitle(f"{self.app_name} {self.app_version}")

    def _setup_navigation_assets(self):
        self.manage_accounts_screen.btn_returnToAdminPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))

    def _connect_buttons(self):
        self.manage_accounts_screen.btn_returnToAdminPanelPage.clicked.connect(self.controller.goto_admin_panel)
