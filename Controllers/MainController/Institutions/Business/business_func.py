from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton
from django.core.validators import validate_email

from Controllers.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class business_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.inst_business_screen = self.load_ui("Views/MainPages/InstitutionPages/business.ui")
        self.setup_business_ui()
        self.center_on_screen()

    def setup_business_ui(self):
        """Setup the Business Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Business")
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.inst_business_screen.btn_returnToInstitutionPage.setIcon(QIcon('Resources/FuncIcons/img_return.png'))
        self.inst_business_screen.inst_BusinessName_buttonSearch.setIcon(QIcon('Resources/FuncIcons/icon_search_w.svg'))
        self.inst_business_screen.inst_business_button_register.setIcon(QIcon('Resources/FuncIcons/icon_add.svg'))
        self.inst_business_screen.inst_business_button_update.setIcon(QIcon('Resources/FuncIcons/icon_edit.svg'))
        self.inst_business_screen.inst_business_button_remove.setIcon(QIcon('Resources/FuncIcons/icon_del.svg'))
        self.inst_business_screen.businessList_buttonFilter.setIcon(QIcon('Resources/FuncIcons/icon_filter.svg'))

        # Return Button
        self.inst_business_screen.btn_returnToInstitutionPage.clicked.connect(self.goto_institutions_panel)

        # REGISTER BUTTON
        self.inst_business_screen.inst_business_button_register.clicked.connect(self.show_register_business_popup)

    def show_register_business_popup(self):
        print("-- Register Business Popup")
        self.popup = load_popup("Views/PopUp/Screen_Institutions/register_business.ui", self)
        self.popup.setWindowTitle("Mapro: Register New Business")
        self.popup.setFixedSize(self.popup.size())

        self.popup.register_buttonConfirmBusiness_SaveForm.setIcon(QIcon('Resources/FuncIcons/icon_confirm.svg'))
        self.popup.inst_DTIuploadButton.setIcon(QIcon('Resources/Icons/icon_upload_image.png'))
        self.popup.register_buttonConfirmBusiness_SaveForm.clicked.connect(self.validate_business_fields)

        self.popup.setWindowModality(Qt.ApplicationModal)

        self.popup.exec_()


    def validate_business_fields(self):
        errors = []
        print("test")
        if not self.popup.register_BusinessName.text().strip():
            errors.append("Business name is required")
            self.popup.register_BusinessName.setStyleSheet("border: 1px solid red")
        elif self.popup.register_BusinessName.text().strip():
            self.popup.register_BusinessName.setStyleSheet("border: 1px solid gray")
        print("remove border")
        if self.popup.register_comboBox_BusinessStatus.currentIndex() == -1:
            errors.append("Business status is required")
        if not self.popup.register_BusinessAddress.text().strip():
            errors.append("Business address is required")
        if self.popup.register_comboBox_BusinessAddress_Sitio.currentIndex() == -1:
            errors.append("Business sitio is required")
        if not self.popup.register_BusinessOwnerFirstName.text().strip():
            errors.append("Business owner firstname is required")
        if not self.popup.register_BusinessOwnerLastName.text().strip():
            errors.append("Business owner lastname is required")
        if errors:
            QMessageBox.warning(self.popup, "Incomplete Form", "Please complete all required fields:\n\n• " + "\n• ".join(errors))
            # self.highlight_missing_fields(errors)
        else:
            pass


    # def highlight_missing_fields(self, errors):
    #     if "Business name is required" in errors:
    #         self.popup.register_BusinessName.setStyleSheet("border: 1px solid red")
    #     if "Business status is required" in errors:
    #         self.popup.register_comboBox_BusinessStatus.setStyleSheet("border: 1px solid red")
    #     # if



        # upload_button = self.popup.findChild(QPushButton, "inst_DTIuploadButton")
        # image_label = self.popup.findChild(QLabel, "imageLabel")



        # def setup_radio_button_groups_business():
        #     # Is DTI Registered?
        #     radio_DTI = QButtonGroup(self.popup)
        #     DTI_yes = self.popup.findChild(QRadioButton, "radioButton_DTI_Yes")
        #     DTI_no = self.popup.findChild(QRadioButton, "radioButton_DTI_No")
        #     if DTI_yes and DTI_no:
        #         radio_DTI.addButton(DTI_yes)
        #         radio_DTI.addButton(DTI_no)

        # setup_radio_button_groups_business()
        #
        # if image_label:
        #     image_label.setAlignment(Qt.AlignCenter)  # Center the image inside the label
        #
        # if upload_button:
        #     upload_button.setIcon(QIcon("Resources/Icons/icon_upload_image.svg"))
        #
        #     def upload_image():
        #         file_path, _ = QFileDialog.getOpenFileName(self.popup, "Select an Image", "",
        #                                                    "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        #         if file_path:
        #             pixmap = QPixmap(file_path)
        #             image_label.setPixmap(
        #                 pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio,
        #                               Qt.SmoothTransformation)
        #             )
        #
        #     upload_button.clicked.connect(upload_image)
        #
        # # Save final form with confirmation
        # save_btn = self.popup.findChild(QPushButton, "register_buttonConfirmBusiness_SaveForm")
        # if save_btn:
        #     def confirm_and_save():
        #         reply = QMessageBox.question(
        #             self.popup,
        #             "Confirm Registration",
        #             "Are you sure you want to register this business?",
        #             QMessageBox.Yes | QMessageBox.No,
        #             QMessageBox.No
        #         )
        #
        #         if reply == QMessageBox.Yes:
        #             print("-- Form Submitted")
        #             QMessageBox.information(self.popup, "Success", "Citizen successfully registered!")
        #             self.popup.close()
        #
        #     save_btn.clicked.connect(confirm_and_save)

        # self.popup.show()


    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Controllers.MainController.Institutions.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")