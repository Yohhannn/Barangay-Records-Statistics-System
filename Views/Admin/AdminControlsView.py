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
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/Sitio/addsitio.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New Sitio")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.validate_fields)

        self.popup.show()
        return self.popup

    def show_edit_sitio_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/Sitio/editsitio.ui", parent)
        self.popup.setWindowTitle("Mapro: Edit Sitio")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.edit_sitio_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.input_id_search.setText(self.controller.selected_sitio_id)
        self.popup.display_searched.setText(self.controller.selected_sitio_name)


        self.popup.edit_sitio_buttonConfirmAccount_SaveForm.clicked.connect(self.on_save_sitio_name)
        self.popup.input_id_search.textChanged.connect(self.controller.handle_sitio_search)


        self.popup.show()
        return self.popup

    def on_save_sitio_name(self):
        sitio_id = self.popup.input_id_search.text().strip()
        new_name = self.popup.AdmnCon_Input_Sitio.text().strip()

        if not sitio_id or not new_name:
            QMessageBox.warning(self.popup, "Input Error", "ID and new name must be provided.")
            return

        self.controller.rename_sitio(sitio_id, new_name)

    def get_form_data(self):
        return {
            'sitio_name': self.popup.AdmnCon_Input_Sitio.text().strip(),
        }

    def show_register_infra_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/InfraType/addinfra.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New Infrastructure Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.save_infrastructure_type)

        self.popup.show()
        return self.popup

    def show_edit_infra_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/InfraType/editinfra.ui", parent)
        self.popup.setWindowTitle("Mapro: Edit Infrastructure Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.edit_sitio_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.input_id_search.setText(self.controller.selected_infra_id)
        self.popup.display_searched.setText(self.controller.selected_infra_name)


        self.popup.edit_sitio_buttonConfirmAccount_SaveForm.clicked.connect(self.on_save_infra_type)
        self.popup.input_id_search.textChanged.connect(self.controller.handle_infra_search)


        self.popup.show()
        return self.popup

    def on_save_infra_type(self):
        infra_id = self.popup.input_id_search.text().strip()
        new_name = self.popup.update_InfraType.text().strip()

        if not infra_id or not new_name:
            QMessageBox.warning(self.popup, "Input Error", "ID and new name must be provided.")
            return

        self.controller.rename_infra_type(infra_id, new_name)

    def get_infra_data(self):
        return {
            'infra_name': self.popup.AdmnCon_Input_infra.text().strip(),
        }

    def show_register_history_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/HistType/addhist.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New History Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.save_history_type)

        self.popup.show()
        return self.popup

    def show_edit_history_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/HistType/edithist.ui", parent)
        self.popup.setWindowTitle("Mapro: Edit History Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.edit_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.input_id_search.setText(self.controller.selected_history_id)
        self.popup.display_searched.setText(self.controller.selected_history_name)


        self.popup.edit_buttonConfirmAccount_SaveForm.clicked.connect(self.on_save_history_type)
        self.popup.input_id_search.textChanged.connect(self.controller.handle_history_search)


        self.popup.show()
        return self.popup

    def on_save_history_type(self):
        history_id = self.popup.input_id_search.text().strip()
        new_name = self.popup.update_HistoryType.text().strip()

        if not history_id or not new_name:
            QMessageBox.warning(self.popup, "Input Error", "ID and new name must be provided.")
            return

        self.controller.rename_history_type(history_id, new_name)

    def get_history_data(self):
        return {
            'history_name': self.popup.AdmnCon_Input_hist.text().strip(),
        }

    def show_register_transaction_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/TransType/addtrans.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New Transaction Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.save_transaction_type)

        self.popup.show()
        return self.popup

    def show_edit_transaction_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/TransType/edittrans.ui", parent)
        self.popup.setWindowTitle("Mapro: Edit Transaction Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.edit_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.input_id_search.setText(self.controller.selected_transaction_id)
        self.popup.display_searched.setText(self.controller.selected_transaction_name)


        self.popup.edit_buttonConfirmAccount_SaveForm.clicked.connect(self.on_save_transaction_type)
        self.popup.input_id_search.textChanged.connect(self.controller.handle_transaction_search)


        self.popup.show()
        return self.popup

    def on_save_transaction_type(self):
        transaction_id = self.popup.input_id_search.text().strip()
        new_name = self.popup.update_TransType.text().strip()

        if not transaction_id or not new_name:
            QMessageBox.warning(self.popup, "Input Error", "ID and new name must be provided.")
            return

        self.controller.rename_transaction_type(transaction_id, new_name)

    def get_transaction_data(self):
        return {
            'transaction_name': self.popup.AdmnCon_Input_trans.text().strip(),
        }

    def show_register_medical_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/MedType/addmed.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New Medical History Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.save_medical_type)

        self.popup.show()
        return self.popup

    def show_edit_medical_type_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminControls/MedType/editmed.ui", parent)
        self.popup.setWindowTitle("Mapro: Edit Medical History Type")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.edit_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.input_id_search.setText(self.controller.selected_med_history_id)
        self.popup.display_searched.setText(self.controller.selected_med_history_name)


        self.popup.edit_buttonConfirmAccount_SaveForm.clicked.connect(self.on_save_medical_type)
        self.popup.input_id_search.textChanged.connect(self.controller.handle_medical_search)


        self.popup.show()
        return self.popup

    def on_save_medical_type(self):
        medical_id = self.popup.input_id_search.text().strip()
        new_name = self.popup.update_MedHistType.text().strip()

        if not medical_id or not new_name:
            QMessageBox.warning(self.popup, "Input Error", "ID and new name must be provided.")
            return

        self.controller.rename_medical_type(medical_id, new_name)

    def get_medical_data(self):
        return {
            'medical_name': self.popup.AdmnCon_Input_MedType.text().strip(),
        }

    def show_success_message(self, title, message):
        QMessageBox.information(self.popup, title, message)

    def show_error_dialog(self, title,message):
        QMessageBox.critical(self.popup, title, message)

    def confirm_registration(self, title, text):
        reply = QMessageBox.question(
            self.popup,
            title,
            text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def _setup_navigation_assets(self):
            self.admin_controls_screen.btn_returnToAdminPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
            self.admin_controls_screen.admn_button_RegSitio.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
            self.admin_controls_screen.admn_button_UpdSitio.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
            self.admin_controls_screen.admn_button_RemSitio.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))

            self.admin_controls_screen.admn_button_AddInfra.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
            self.admin_controls_screen.admn_button_UpdInfra.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
            self.admin_controls_screen.admn_button_RemInfra.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))

    def _connect_buttons(self):


        self.admin_controls_screen.btn_returnToAdminPanelPage.clicked.connect(self.controller.goto_admin_panel)
        self.admin_controls_screen.admn_button_RegSitio.clicked.connect(
            lambda: self.show_register_sitio_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_UpdSitio.clicked.connect(
            lambda: self.show_edit_sitio_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_AddInfra.clicked.connect(
            lambda: self.show_register_infra_type_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_UpdInfra.clicked.connect(
            lambda: self.show_edit_infra_type_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_AddHist.clicked.connect(
            lambda: self.show_register_history_type_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_UpdHist.clicked.connect(
            lambda: self.show_edit_history_type_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_AddTrans.clicked.connect(
            lambda: self.show_register_transaction_type_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_UpdTrans.clicked.connect(
            lambda: self.show_edit_transaction_type_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_AddMed.clicked.connect(
            lambda: self.show_register_medical_type_popup(self.admin_controls_screen))
        self.admin_controls_screen.admn_button_UpdMed.clicked.connect(
            lambda: self.show_edit_medical_type_popup(self.admin_controls_screen))
        # self.admin_controls_screen.nav_buttonTrashBin.clicked.connect(self.controller.goto)




        self.admin_controls_screen.admn_button_RemSitio.clicked.connect(self.controller.handle_remove_sitio)
        self.admin_controls_screen.admn_button_RemInfra.clicked.connect(self.controller.handle_remove_infrastructure_type)
        self.admin_controls_screen.admn_button_RemTrans.clicked.connect(
            self.controller.handle_remove_transaction_type)
        self.admin_controls_screen.admn_button_RemHist.clicked.connect(
            self.controller.handle_remove_history_type)
        self.admin_controls_screen.admn_button_RemMed.clicked.connect(
            self.controller.handle_remove_med_history_type)










