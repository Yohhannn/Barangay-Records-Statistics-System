from PySide6.QtGui import QPixmap, QIcon, Qt, QImage, QBrush
from PySide6.QtCore import QTimer
from PySide6.QtSql import QSqlTableModel, QSqlQueryModel
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton, \
    QTableWidgetItem

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup
from database import Database


class business_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.inst_business_screen = self.load_ui("UI/MainPages/InstitutionPages/business.ui")
        self.setup_business_ui()
        self.center_on_screen()
        self.load_business_data()

        # Add to stack and show it
        self.stack.addWidget(self.inst_business_screen)
        self.stack.setCurrentWidget(self.inst_business_screen)

        # Connect signal
        self.inst_business_screen.inst_tableView_List_RegBusiness.cellClicked.connect(self.handle_row_click_business)


    def load_business_data(self):
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute(""" 
                SELECT 
                    BI.BS_ID,
                    BI.BS_NAME,
                    CONCAT(BO.BSO_FIRSTNAME, ' ', BO.BSO_LASTNAME) AS BUSINESS_OWNER,
                    BI.BS_DATE_REGISTERED,
                    BT.BST_TYPE_NAME,
                    BI.BS_STATUS,
                    BI.BS_ADDRESS,
                    BI.BS_IS_DTI,
                    S.SITIO_NAME,
                    BI.BS_DESCRIPTION
                FROM BUSINESS_INFO BI
                JOIN BUSINESS_OWNER BO ON BI.BSO_ID = BO.BSO_ID
                JOIN BUSINESS_TYPE BT ON BI.BST_ID = BT.BST_ID
                JOIN SITIO S ON BI.SITIO_ID = S.SITIO_ID; 
           """)
            rows = cursor.fetchall()
            self.rows = rows

            # Set the row and column count for the QTableWidget
            self.inst_business_screen.inst_tableView_List_RegBusiness.setRowCount(len(rows))
            self.inst_business_screen.inst_tableView_List_RegBusiness.setColumnCount(4)
            self.inst_business_screen.inst_tableView_List_RegBusiness.setHorizontalHeaderLabels(
                ["ID", "Business Name", "Owner", "Date Registered"])

            # Populate the QTableWidget with data
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[3]]):
                    item = QTableWidgetItem(str(value))
                    self.inst_business_screen.inst_tableView_List_RegBusiness.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.inst_business_screen, "Database Error", str(e))


    def handle_row_click_business(self, row, column):
        selected_id = self.inst_business_screen.inst_tableView_List_RegBusiness.item(row, 0).text()

        for record in self.rows:
            if str(record[0]) == selected_id:
                # Set full data to QLabel widgets
                self.inst_business_screen.inst_displayBusinessID.setText(str(record[0]))
                self.inst_business_screen.inst_displayBusinessName.setText(record[1])
                self.inst_business_screen.inst_displayBusinessOwnerName.setText(record[2])
                self.inst_business_screen.inst_displayBusinessDateRegistered.setText(str(record[3]))
                self.inst_business_screen.inst_displayBusinessType.setText(record[4])
                self.inst_business_screen.inst_displayBusinessStatus.setText(record[5])
                self.inst_business_screen.inst_displayBusinessAddress.setText(record[6])
                self.inst_business_screen.inst_displayBusinessDTIRegistered.setText("Yes" if record[7] else "No")
                self.inst_business_screen.inst_displayBusinessAddress_Sitio.setText(record[8])
                self.inst_business_screen.inst_BusinessDescription.setText(record[9])
                break

    def setup_business_ui(self):
        """Setup the Business UI layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Business")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.inst_business_screen.btn_returnToInstitutionPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))
        self.inst_business_screen.inst_BusinessName_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
        self.inst_business_screen.inst_business_button_register.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
        self.inst_business_screen.inst_business_button_update.setIcon(QIcon('Assets/FuncIcons/icon_edit.svg'))
        self.inst_business_screen.inst_business_button_remove.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))

        # Return Button
        self.inst_business_screen.btn_returnToInstitutionPage.clicked.connect(self.goto_institutions_panel)

        # REGISTER BUTTON
        self.inst_business_screen.inst_business_button_register.clicked.connect(self.show_register_business_popup)

    def show_register_business_popup(self):
        print("-- Register Business Popup")
        popup = load_popup("UI/PopUp/Screen_Institutions/register_business.ui", self)
        popup.setWindowTitle("Mapro: Register New Business")

        popup.register_buttonConfirmBusiness_SaveForm.setIcon(QIcon('Assets/FuncIcons/icon_confirm.svg'))
        popup.inst_DTIuploadButton.setIcon(QIcon('Assets/Icons/icon_upload_image.png'))

        upload_button = popup.findChild(QPushButton, "inst_DTIuploadButton")
        image_label = popup.findChild(QLabel, "imageLabel")

        def setup_radio_button_groups_business():
            # Is DTI Registered?
            radio_DTI = QButtonGroup(popup)
            DTI_yes = popup.findChild(QRadioButton, "radioButton_DTI_Yes")
            DTI_no = popup.findChild(QRadioButton, "radioButton_DTI_No")
            if DTI_yes and DTI_no:
                radio_DTI.addButton(DTI_yes)
                radio_DTI.addButton(DTI_no)

        setup_radio_button_groups_business()

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
        save_btn = popup.findChild(QPushButton, "register_buttonConfirmBusiness_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Registration",
                    "Are you sure you want to register this business?",
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


    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Functions.Main.Institutions.institution_func import institutions_func
            self.institutions_panel = institutions_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")

