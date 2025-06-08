from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon
from Utils.util_popup import load_popup

class ManageAccountsView:
    def __init__(self, controller):
        self.controller = controller
        self.manage_accounts_screen = None
    
    def setup_manage_accounts_ui(self, ui_screen):
        self.manage_accounts_screen = ui_screen
        self._setup_navigation_assets()
        self._connect_buttons()

    def show_register_account_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminPanel/register_account.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New System User")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.validate_fields)
        self._init_dropdowns()
        self.popup.show()
        return self.popup

    def get_form_data(self):
        return {
            'first_name': self.popup.RegAcc_input_fname.text().strip(),
            'last_name': self.popup.RegAcc_input_lname.text().strip(),
            'middle_name': self.popup.RegAcc_input_mname.text().strip(),
            'user_password': self.popup.RegAcc_input_PIN.text().strip(),
            'confirm_password': self.popup.RegAcc_confirm_PIN.text().strip(),
            'role': self.popup.RegAcc_select_role.currentText().strip()
        }

    def show_success_message(self):
        QMessageBox.information(self.popup, "Success", "System user successfully registered!")

    def show_error_dialog(self, error):
        QMessageBox.critical(self.popup, "Error", f"Failed to register System User.\n\n{error}")

    def confirm_registration(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Registration",
            "Are you sure you want to register this System User?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def _setup_navigation_assets(self):
        self.manage_accounts_screen.btn_returnToAdminPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))

    def _connect_buttons(self):
        self.manage_accounts_screen.btn_returnToAdminPanelPage.clicked.connect(self.controller.goto_admin_panel)
        self.manage_accounts_screen.admn_button_RegAcc.clicked.connect(
            lambda: self.show_register_account_popup(self.manage_accounts_screen)
    )
        
    def _init_dropdowns(self):
        self.popup.RegAcc_select_role.clear()
        self.popup.RegAcc_select_role.addItems(["Staff", "Admin"])