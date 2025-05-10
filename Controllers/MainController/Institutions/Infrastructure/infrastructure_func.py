from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QButtonGroup, QRadioButton

from Controllers.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class infrastructure_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.inst_infrastructure_screen = self.load_ui("Views/MainPages/InstitutionPages/infrastructure.ui")
        self.setup_infrastructure_ui()
        self.center_on_screen()

    def setup_infrastructure_ui(self):
        """Setup the Infrastructure Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Infrastructure")
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.setIcon(QIcon('Resources/FuncIcons/img_return.png'))
        self.inst_infrastructure_screen.inst_InfraName_buttonSearch.setIcon(QIcon('Resources/FuncIcons/icon_search_w.svg'))
        self.inst_infrastructure_screen.inst_infra_button_register.setIcon(QIcon('Resources/FuncIcons/icon_add.svg'))
        self.inst_infrastructure_screen.inst_infra_button_update.setIcon(QIcon('Resources/FuncIcons/icon_edit.svg'))
        self.inst_infrastructure_screen.inst_infra_button_remove.setIcon(QIcon('Resources/FuncIcons/icon_del.svg'))
        self.inst_infrastructure_screen.InfrastructureList_buttonFilter.setIcon(QIcon('Resources/FuncIcons/icon_filter.svg'))

        # Return Button
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.clicked.connect(self.goto_institutions_panel)

     # REGISTER BUTTON
        self.inst_infrastructure_screen.inst_infra_button_register.clicked.connect(self.show_register_isfrastructure_popup)

    def show_register_isfrastructure_popup(self):
        print("-- Register Infrastructure Popup")
        popup = load_popup("Views/PopUp/Screen_Institutions/register_infrastructure.ui", self)
        popup.setWindowTitle("Mapro: Register New Infrastructure")
        popup.setFixedSize(popup.size())

        popup.register_buttonConfirmInfra_SaveForm.setIcon(QIcon('Resources/FuncIcons/icon_confirm.svg'))

        def setup_radio_button_groups_infrastructure():
            # Is Private or Public?
            radio_PP = QButtonGroup(popup)
            PP_Private = popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Private")
            PP_Public = popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Public")
            if PP_Private and PP_Public:
                radio_PP.addButton(PP_Private)
                radio_PP.addButton(PP_Public)

        setup_radio_button_groups_infrastructure()

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "register_buttonConfirmInfra_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Registration",
                    "Are you sure you want to register this infrastructure?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "infrastructure Successfully Registered!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Controllers.MainController.Institutions.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")