from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon

from Utils.util_popup import load_popup

class AdminControlsView:
    def __init__(self, controller):
        self.controller = controller
        self.admin_controls_screen = None
    
    def setup_admin_controls_ui(self, ui_screen):
        self.admin_controls_screen = ui_screen
        self._setup_navigation_assets()
        self._connect_buttons()

    def show_register_sitio_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/addsitio.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New Sitio")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.validate_fields)

        self.popup.show()
        return self.popup



    def get_form_data(self):
        return {
            'sitio_name': self.popup.AdmnCon_Input_Sitio.text().strip(),
        }

    def show_success_message(self):
        QMessageBox.information(self.popup, "Success", "System user successfully registered!")

    def show_error_dialog(self, error):
        QMessageBox.critical(self.popup, "Error", f"Failed to register System User.\n\n{error}")

    def confirm_registration(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Registration",
            "Are you sure you want to register this Sitio?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def _setup_navigation_assets(self):
            self.admin_controls_screen.btn_returnToAdminPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))

    def _connect_buttons(self):
            self.admin_controls_screen.btn_returnToAdminPanelPage.clicked.connect(self.controller.goto_admin_panel)
            self.admin_controls_screen.admn_button_RegAcc.clicked.connect(
                lambda: self.show_register_sitio_popup(self.admin_controls_screen)
        )
        



