# import cv2
# from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
# from PySide6.QtCore import QTimer
# from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton
#
# from Controllers.base_file_func import base_file_func
# from Utils.utils_datetime import update_date_label
# from Utils.util_popup import load_popup
#
# class household_func(base_file_func):
#     def __init__(self, login_window, emp_first_name, stack):
#         super().__init__(login_window, emp_first_name)
#         self.stack = stack
#         self.cp_household_screen = self.load_ui("Views/MainPages/CitizenPanelPages/cp_household.ui")
#         self.setup_household_ui()
#         self.center_on_screen()
#         self.popup = None
#
#     def setup_household_ui(self):
#         self.setFixedSize(1350, 850)
#         self.setWindowTitle("MaPro: Household")
#         self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
#
#     # Set images and icons
#         self.cp_household_screen.btn_returnToCitizenPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
#         self.cp_household_screen.cp_HouseholdName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
#         self.cp_household_screen.cp_household_button_register.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
#         self.cp_household_screen.cp_household_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
#         self.cp_household_screen.cp_household_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
#         self.cp_household_screen.householdList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))
#
#         # BUTTONS REGISTRATIOPN
#         self.cp_household_screen.btn_returnToCitizenPanelPage.clicked.connect(self.goto_citizen_panel)
#         self.cp_household_screen.cp_household_button_register.clicked.connect(self.show_register_household_popup)
#
#
#
#     def show_register_household_popup(self):
#         print("-- Register New Household Popup")
#         self.popup = load_popup("Views/PopUp/Screen_CitizenPanel/ScreenHousehold/register_household.ui", self)
#         self.popup.setWindowTitle("Mapro: Register New Household")
#         self.popup.setWindowModality(Qt.ApplicationModal)
#         self.popup.setFixedSize(self.popup.size())
#
#         self.popup.register_buttonConfirmHousehold_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
#
#
#         # BUTTON REGISTRATION
#         self.popup.register_buttonConfirmHousehold_SaveForm.clicked.connect(self.validate_part_fields)
#         self.popup.cp_HomeImageuploadButton.clicked.connect(self.upload_function)
#
#         # ICON LOAD
#
#         self.popup.cp_HomeImageuploadButton.setIcon(QIcon("Resources/Icons/General_Icons/icon_upload_image.svg"))
#         self.popup.imageLabel.setAlignment(Qt.AlignCenter)
#
#
#         self.popup.exec_()
#
#
#         # DO NOT REMOVE FOR FUTURE FIX
#         #
#         # upload_button = self.popup.findChild(QPushButton, "cp_HomeImageuploadButton")
#         # image_label = self.popup.findChild(QLabel, "imageLabel")
#         #
#         # if image_label:
#         #     image_label.setAlignment(Qt.AlignCenter)  # Center the image inside the label
#         #
#         # if upload_button:
#         #     upload_button.setIcon(QIcon("Resources/Icons/General_Icons/icon_upload_image.svg"))
#         #
#         #     def upload_image():
#         #         file_path, _ = QFileDialog.getOpenFileName(self.popup, "Select an Image", "",
#         #                                                    "General_Images (*.png *.jpg *.jpeg *.bmp *.gif)")
#         #         if file_path:
#         #             pixmap = QPixmap(file_path)
#         #             image_label.setPixmap(
#         #                 pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio,
#         #                               Qt.SmoothTransformation)
#         #             )
#         #
#         #     upload_button.clicked.connect(upload_image)
#
#
#
#     def validate_part_fields(self):
#         errors_household = []
#         if not self.popup.register_household_homeAddress.text().strip():
#             errors_household.append("Home address is required")
#             self.popup.register_household_homeAddress.setStyleSheet("border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
#         else:
#             self.popup.register_household_homeAddress.setStyleSheet("border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")
#
#
#         if self.popup.register_household_comboBox_Sitio.currentIndex() == -1:
#             errors_household.append("Sitio is required")
#             self.popup.register_household_comboBox_Sitio.setStyleSheet("border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)")
#         else:
#             self.popup.register_household_comboBox_Sitio.setStyleSheet(
#                 "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
#             )
#
#         if self.popup.register_household_comboBox_OwnershipStatus.currentIndex() == -1:
#             errors_household.append("Ownership Status is required")
#             self.popup.register_household_comboBox_OwnershipStatus.setStyleSheet("border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)")
#         else:
#             self.popup.register_household_comboBox_OwnershipStatus.setStyleSheet(
#                 "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
#             )
#
#         if errors_household:
#             QMessageBox.warning(self.popup, "Incomplete Form", "Please complete all required fields:\n\n• " + "\n• ".join(errors_household))
#         else:
#             self.confirm_and_save()
#
#
#
#     def upload_function(self):
#
#         file_path, _ = QFileDialog.getOpenFileName(self.popup, "Select an Image", "","General_Images (*.png *.jpg *.jpeg *.bmp *.gif)")
#         if file_path:
#             pixmap = QPixmap(file_path)
#             self.popup.imageLabel.setPixmap(pixmap.scaled(self.popup.imageLabel.width(),
#             self.popup.imageLabel.height(),
#             Qt.KeepAspectRatio, Qt.SmoothTransformation)
#             )
#
#
#
#     def confirm_and_save(self):
#         reply = QMessageBox.question(self.popup, "Confirm Registration", "Are you sure you want to register this household?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#         if reply == QMessageBox.Yes:
#             print("-- Form Submitted")
#             QMessageBox.information(self.popup, "Success", "Household successfully registered!")
#             # self.citizen_data = {}
#             self.popup.close()
#
#
#
#     def goto_citizen_panel(self):
#         """Handle navigation to Citizen Panel screen."""
#         print("-- Navigating to Citizen Panel")
#         if not hasattr(self, 'citizen_panel'):
#             from Controllers.Categories.citizen_func import citizen_func
#             self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
#             self.stack.addWidget(self.citizen_panel.citizen_panel_screen)
#
#         self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
#         self.setWindowTitle("MaPro: Citizen Panel")