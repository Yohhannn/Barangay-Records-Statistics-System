from Controllers.BaseFileController import BaseFileController
from PySide6.QtGui import QIcon, Qt, QPixmap
from PySide6.QtWidgets import (QMessageBox, QPushButton, QLabel, QFileDialog,
                               QButtonGroup, QRadioButton, QTableWidgetItem)
from Utils.util_popup import load_popup
from database import Database


class BusinessController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.inst_business_screen = self.load_ui("Resources/UIs/MainPages/InstitutionPages/business.ui")
        self.setup_business_ui()
        self.center_on_screen()
        self.load_business_data()

    def setup_business_ui(self):
        """Setup the Business Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Business")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set images and icons
        self.inst_business_screen.btn_returnToInstitutionPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.inst_business_screen.inst_BusinessName_buttonSearch.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.inst_business_screen.inst_business_button_register.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.inst_business_screen.inst_business_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.inst_business_screen.inst_business_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        self.inst_business_screen.businessList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # Connect signals
        self.inst_business_screen.btn_returnToInstitutionPage.clicked.connect(self.goto_institutions_panel)
        self.inst_business_screen.inst_business_button_register.clicked.connect(self.show_register_business_popup)
        self.inst_business_screen.inst_tableView_List_RegBusiness.cellClicked.connect(self.handle_row_click_business)

    def load_business_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute(""" 
                SELECT 
                    BI.BS_ID,
                    BI.BS_NAME,
                    CONCAT(BO.BSO_FNAME, ' ', BO.BSO_LNAME) AS BUSINESS_OWNER,
                    TO_CHAR(BI.BS_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS BS_DATE_ENCODED,
                    BT.BST_TYPE_NAME,
                    BI.BS_STATUS,
                    BI.BS_ADDRESS,
                    BI.BS_IS_DTI,
                    S.SITIO_NAME,
                    BI.BS_DESCRIPTION,
                    CASE 
                        WHEN SA.SYS_FNAME IS NULL THEN 'System'
                        ELSE CONCAT(
                            SA.SYS_FNAME, ' ', 
                            CASE WHEN SA.SYS_MNAME IS NOT NULL AND SA.SYS_MNAME != '' 
                                 THEN LEFT(SA.SYS_MNAME, 1) || '. ' 
                                 ELSE '' 
                            END,
                            SA.SYS_LNAME
                        )
                    END AS ENCODED_BY,
                    TO_CHAR(BI.BS_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED_FORMATTED,
                    TO_CHAR(BI.BS_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS LAST_UPDATED,
                    BI.ENCODED_BY_SYS_ID,
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' ||
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                             SUA.SYS_LNAME
                    END AS LAST_UPDATED_BY_NAME --13
                FROM BUSINESS_INFO BI
                JOIN BUSINESS_OWNER BO ON BI.BSO_ID = BO.BSO_ID
                JOIN BUSINESS_TYPE BT ON BI.BST_ID = BT.BST_ID
                JOIN SITIO S ON BI.SITIO_ID = S.SITIO_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON BI.ENCODED_BY_SYS_ID = SA.SYS_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON BI.LAST_UPDATED_BY_SYS_ID = SUA.SYS_ID
                ORDER BY COALESCE(BI.BS_LAST_UPDATED, BI.BS_DATE_ENCODED) DESC
                LIMIT 20
           """)
            rows = cursor.fetchall()
            self.rows = rows

            # Set the row and column count for the QTableWidget
            table = self.inst_business_screen.inst_tableView_List_RegBusiness
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Business Name", "Owner", "Date Registered"])

            # Set column widths
            table.setColumnWidth(0, 50)  # ID
            table.setColumnWidth(1, 150)  # Business Name
            table.setColumnWidth(2, 150)  # Owner
            table.setColumnWidth(3, 200)  # Date Registered (wider for formatted date)

            # Populate the QTableWidget with data
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[3]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.inst_business_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_business(self, row, column):
        table = self.inst_business_screen.inst_tableView_List_RegBusiness
        selected_item = table.item(row, 0)

        if not selected_item:
            return

        selected_id = selected_item.text()

        for record in self.rows:
            if str(record[0]) == selected_id:
                self.inst_business_screen.inst_displayBusinessID.setText(str(record[0]))
                self.inst_business_screen.inst_displayBusinessName.setText(record[1])
                self.inst_business_screen.inst_displayBusinessOwnerName.setText(record[2])
                self.inst_business_screen.inst_display_DateEncoded.setText(str(record[3]))
                self.inst_business_screen.inst_displayBusinessType.setText(record[4])
                self.inst_business_screen.inst_displayBusinessStatus.setText(record[5])
                self.inst_business_screen.inst_displayBusinessAddress.setText(record[6])
                # self.inst_business_screen.inst_displayBusinessDTIRegistered.setText("Yes" if record[7] else "No")
                self.inst_business_screen.inst_displayBusinessAddress_Sitio.setText(record[8])
                self.inst_business_screen.inst_BusinessDescription.setText(record[9])

                # Display encoded by and last updated information
                self.inst_business_screen.inst_display_EncodedBy.setText(record[10])  # ENCODED_BY
                self.inst_business_screen.inst_display_DateUpdated.setText(
                    record[12] if record[12] else record[11])  # LAST_UPDATED or DATE_ENCODED_FORMATTED
                self.inst_business_screen.display_UpdatedBy.setText(record[14])

                break


    def show_register_business_popup(self):
        print("-- Register Business Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Institutions/register_business.ui", self)
        self.popup.setWindowTitle("Mapro: Register New Business")
        self.popup.setFixedSize(self.popup.size())

        self.popup.register_buttonConfirmBusiness_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        # self.popup.inst_DTIuploadButton.setIcon(QIcon('Resources/Icons/General_Icons/icon_upload_image.png'))

        # Connect signals
        self.popup.register_buttonConfirmBusiness_SaveForm.clicked.connect(self.validate_business_fields)
        # self.popup.inst_DTIuploadButton.clicked.connect(self.upload_business_image)

        # Setup radio button groups
        self.setup_radio_button_groups_business()

        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

    def upload_business_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.popup,
            "Select Business Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                image_label = self.popup.findChild(QLabel, "imageLabel")
                if image_label:
                    image_label.setPixmap(pixmap.scaled(
                        image_label.width(),
                        image_label.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    ))

    def setup_radio_button_groups_business(self):
        # Is DTI Registered?
        radio_DTI = QButtonGroup(self.popup)
        DTI_yes = self.popup.findChild(QRadioButton, "radioButton_DTI_Yes")
        DTI_no = self.popup.findChild(QRadioButton, "radioButton_DTI_No")

        if DTI_yes and DTI_no:
            radio_DTI.addButton(DTI_yes)
            radio_DTI.addButton(DTI_no)
            DTI_no.setChecked(True)  # Default selection

    def validate_business_fields(self):
        errors = []

        # Validate business name
        if not self.popup.register_BusinessName.text().strip():
            errors.append("Business name is required")
            self.popup.register_BusinessName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_BusinessName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate business status
        if self.popup.register_comboBox_BusinessStatus.currentIndex() == -1:
            errors.append("Business status is required")
            self.popup.register_comboBox_BusinessStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.popup.register_comboBox_BusinessStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # Validate address
        if not self.popup.register_BusinessAddress.text().strip():
            errors.append("Business address is required")
            self.popup.register_BusinessAddress.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_BusinessAddress.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate sitio
        if self.popup.register_comboBox_BusinessAddress_Sitio.currentIndex() == -1:
            errors.append("Business sitio is required")
            self.popup.register_comboBox_BusinessAddress_Sitio.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.popup.register_comboBox_BusinessAddress_Sitio.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # Validate owner first name
        if not self.popup.register_BusinessOwnerFirstName.text().strip():
            errors.append("Business owner firstname is required")
            self.popup.register_BusinessOwnerFirstName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_BusinessOwnerFirstName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate owner last name
        if not self.popup.register_BusinessOwnerLastName.text().strip():
            errors.append("Business owner lastname is required")
            self.popup.register_BusinessOwnerLastName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_BusinessOwnerLastName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if errors:
            QMessageBox.warning(
                self.popup,
                "Incomplete Form",
                "Please complete all required fields:\n\n• " + "\n• ".join(errors)
            )
        else:
            self.confirm_and_save()

    def confirm_and_save(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Registration",
            "Are you sure you want to register this business?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print("-- Form Submitted")
            QMessageBox.information(self.popup, "Success", "Business successfully registered!")
            self.popup.close()
            self.load_business_data()  # Refresh the business list

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")