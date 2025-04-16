import cv2
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class household_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.cp_household_screen = self.load_ui("UI/MainPages/CitizenPanelPages/cp_household.ui")
        self.setup_household_ui()
        self.center_on_screen()

    def setup_household_ui(self):
        """Setup the Household UI layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Household")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.cp_household_screen.btn_returnToCitizenPanelPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))
        self.cp_household_screen.cp_HouseholdName_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
        self.cp_household_screen.cp_household_button_register.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
        self.cp_household_screen.cp_household_button_update.setIcon(QIcon('Assets/FuncIcons/icon_edit.svg'))
        self.cp_household_screen.cp_household_button_remove.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))

        # Return Button
        self.cp_household_screen.btn_returnToCitizenPanelPage.clicked.connect(self.goto_citizen_panel)

        # REGISTER BUTTON
        self.cp_household_screen.cp_household_button_register.clicked.connect(self.show_register_household_popup)

    def show_register_household_popup(self):
        print("-- Register New Household Popup")
        popup = load_popup("UI/PopUp/Screen_CitizenPanel/ScreenHousehold/register_household.ui", self)
        popup.setWindowTitle("Mapro: Register New Household")
        popup.setWindowModality(Qt.ApplicationModal)

        popup.register_buttonConfirmHousehold_SaveForm.setIcon(QIcon('Assets/FuncIcons/icon_confirm.svg'))

        upload_button = popup.findChild(QPushButton, "cp_HomeImageuploadButton")
        image_label = popup.findChild(QLabel, "imageLabel")

        if image_label:
            image_label.setAlignment(Qt.AlignCenter)  # Center the image inside the label

        if upload_button:
            upload_button.setIcon(QIcon("Assets/Icons/icon_upload_image.svg"))

            def upload_image():
                file_path, _ = QFileDialog.getOpenFileName(popup, "Select an Image", "",
                                                           "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
                if file_path:
                    pixmap = QPixmap(file_path)
                    image_label.setPixmap(
                        pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio,
                                      Qt.SmoothTransformation)
                    )

            upload_button.clicked.connect(upload_image)

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "register_buttonConfirmHousehold_SaveForm")
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
                    QMessageBox.information(popup, "Success", "Citizen successfully registered!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Functions.Main.Citizen_Panel.citizen_func import citizen_func
            self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")