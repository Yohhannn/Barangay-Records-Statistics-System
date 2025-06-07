from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QButtonGroup, QRadioButton, QTableWidgetItem
from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class InfrastructureController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role

        self.selected_id = None
        self.stack = stack
        self.inst_infrastructure_screen = self.load_ui("Resources/UIs/MainPages/InstitutionPages/infrastructure.ui")
        self.setup_infrastructure_ui()
        self.center_on_screen()
        self.load_data_infrastructure()
        self.inst_infrastructure_screen.inst_tableView_List_RegInfra.cellClicked.connect(self.handle_row_click_infrastructure)

    def setup_infrastructure_ui(self):
        """Setup the Infrastructure Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Infrastructure")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set images and icons
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.inst_infrastructure_screen.inst_InfraName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.inst_infrastructure_screen.inst_infra_button_register.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.inst_infrastructure_screen.inst_infra_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.inst_infrastructure_screen.inst_infra_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        # self.inst_infrastructure_screen.InfrastructureList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # Return Button
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.clicked.connect(self.goto_institutions_panel)

        # REGISTER BUTTON
        self.inst_infrastructure_screen.inst_infra_button_register.clicked.connect(self.show_register_infrastructure_popup)
        self.inst_infrastructure_screen.inst_InfraName_buttonSearch.clicked.connect(self.perform_infrastructure_search)

    def perform_infrastructure_search(self):
        search_text = self.inst_infrastructure_screen.inst_InfraName_fieldSearch.text().strip()

        if not search_text:
            # If empty, reload all infrastructure records
            self.load_data_infrastructure()
            return

        query = """
            SELECT 
                INF.INF_ID,
                INF.INF_NAME,
                IO.INFO_FNAME || ' ' || IO.INFO_LNAME AS INFRASTRUCTURE_OWNER,
                TO_CHAR(INF.INF_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_REGISTERED
            FROM INFRASTRUCTURE INF
            LEFT JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
            WHERE INF.INF_IS_DELETED = FALSE
              AND (
                  CAST(INF.INF_ID AS TEXT) ILIKE %s OR
                  INF.INF_NAME ILIKE %s OR
                  (IO.INFO_FNAME || ' ' || IO.INFO_LNAME) ILIKE %s
              )
            ORDER BY INF.INF_DATE_ENCODED DESC
            LIMIT 50;
        """

        try:
            connection = Database()
            cursor = connection.cursor
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()

            table = self.inst_infrastructure_screen.inst_tableView_List_RegInfra
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Name", "Owner", "Date Registered"])
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 200)
            table.setColumnWidth(3, 200)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.inst_infrastructure_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def load_data_infrastructure(self):
        try:
            connection = Database()
            cursor = connection.cursor

            # Keep the original query to fetch all data (needed for row click handling)
            cursor.execute(""" 
                SELECT 
                    INF.INF_ID,
                    INF.INF_NAME,
                    INF.INF_ACCESS_TYPE,
                    TO_CHAR(INF.INF_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS INF_DATE_ENCODED,
                    CASE 
                        WHEN IO.INFO_FNAME IS NULL THEN 'No Owner'
                        ELSE CONCAT(
                            IO.INFO_FNAME, ' ', 
                            CASE WHEN IO.INFO_MNAME IS NOT NULL AND IO.INFO_MNAME != '' 
                                 THEN LEFT(IO.INFO_MNAME, 1) || '. ' 
                                 ELSE '' 
                            END,
                            IO.INFO_LNAME
                        )
                    END AS INFRASTRUCTURE_OWNER,
                    COALESCE(IT.INFT_TYPE_NAME, 'No Type') AS INFT_TYPE_NAME,
                    INF.INF_ADDRESS_DESCRIPTION,
                    COALESCE(S.SITIO_NAME, 'No Sitio') AS SITIO_NAME,
                    INF.INF_DESCRIPTION,
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
                    TO_CHAR(INF.INF_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(INF.INF_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS LAST_UPDATED,
                    INF.ENCODED_BY_SYS_ID,
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' ||
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                             SUA.SYS_LNAME
                    END AS LAST_UPDATED_BY_NAME 
                FROM INFRASTRUCTURE INF
                LEFT JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
                LEFT JOIN INFRASTRUCTURE_TYPE IT ON INF.INFT_ID = IT.INFT_ID
                LEFT JOIN SITIO S ON INF.SITIO_ID = S.SITIO_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON INF.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID

                LEFT JOIN SYSTEM_ACCOUNT SA ON INF.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                ORDER BY COALESCE(INF.INF_LAST_UPDATED, INF.INF_DATE_ENCODED) DESC
                LIMIT 20
            """)

            rows = cursor.fetchall()
            print(f"Number of rows fetched: {len(rows)}")  # Debug

            self.rows = rows

            # Update table view with only the 4 specified columns (now showing Owner instead of Access)
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setRowCount(len(rows))
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnCount(4)
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setHorizontalHeaderLabels(
                ["ID", "Name", "Owner", "Date Registered"]
            )

            # Set column widths
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(0, 50)  # ID
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(1, 150)  # Name
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(2,
                                                                                        150)  # Owner (wider for names)
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(3, 100)  # Date

            for row_idx, row_data in enumerate(rows):
                # Display columns in this order: ID, Name, Owner, Date Registered
                display_columns = [
                    row_data[0],  # INF_ID
                    row_data[1],  # INF_NAME
                    row_data[4],  # INFRASTRUCTURE_OWNER (was previously Access Type)
                    row_data[3]  # INF_DATE_ENCODED
                ]

                for col_idx, value in enumerate(display_columns):
                    item = QTableWidgetItem(str(value))
                    self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load infrastructure data: {str(e)}")
        finally:
            if 'connection' in locals():
                connection.close()


    def handle_row_click_infrastructure(self, row):
        self.selected_id = self.inst_infrastructure_screen.inst_tableView_List_RegInfra.item(row, 0).text()

        for record in self.rows:
            if str(record[0]) == self.selected_id:
                # Set basic information
                self.inst_infrastructure_screen.inst_displayInfraID.setText(str(record[0]))
                self.inst_infrastructure_screen.inst_displayInfraName.setText(record[1])
                self.inst_infrastructure_screen.inst_displayInfraOwnerName.setText(record[4])
                self.inst_infrastructure_screen.inst_displayInfraType.setText(record[5])
                self.inst_infrastructure_screen.inst_displayInfraAddress.setText(record[6])
                self.inst_infrastructure_screen.inst_displayInfraSitio.setText(record[7])
                self.inst_infrastructure_screen.inst_displayInfraPP.setText(record[2])
                self.inst_infrastructure_screen.inst_InfraDescription.setText(record[8])

                # Set encoded by information
                self.inst_infrastructure_screen.inst_display_EncodedBy.setText(record[9])
                self.inst_infrastructure_screen.inst_display_DateEncoded.setText(record[10])
                self.inst_infrastructure_screen.inst_display_UpdatedBy.setText(record[13])

                # Set last updated information
                self.inst_infrastructure_screen.inst_display_DateUpdated.setText(
                    record[11] if record[11] else "Not updated")

                # # Get and display who updated the record
                # updated_by_name = self.get_updater_name(record[12])
                # self.inst_infrastructure_screen.inst_display_UpdatedBy.setText(updated_by_name)

        print(self.selected_id)

    def show_register_infrastructure_popup(self):
        print("-- Register Infrastructure Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Institutions/register_infrastructure.ui", self)
        self.popup.setWindowTitle("Mapro: Register New Infrastructure")
        self.popup.setFixedSize(self.popup.size())

        # Connect signals
        self.popup.register_buttonConfirmInfra_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmInfra_SaveForm.clicked.connect(self.validate_infra_fields)

        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

    # def setup_radio_button_groups_infrastructure(self):
    #     # Is Private or Public?
    #     radio_PP = QButtonGroup(self.popup)
    #     PP_Private = self.popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Private")
    #     PP_Public = self.popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Public")
    #
    #     if PP_Private and PP_Public:
    #         radio_PP.addButton(PP_Private)
    #         radio_PP.addButton(PP_Public)
    #         # DTI_no.setChecked(True)  # Default selection

    # FORM DATA HERE [INFRASTRUCTURE] -------------------------------------------------------------------------------
    def get_form_data(self):
        return {
            'infra_name': self.popup.register_InfraName.text().strip(),  # REQUIRED
            'infra_address': self.popup.register_InfraAddress.text().strip(),  # REQUIRED
            'infra_sitio': self.popup.register_comboBox_InfraAddress_Sitio.text().strip(),  # REQUIRED
            'infra_type': self.popup.register_comboBox_InfraType.text().strip(),  # REQUIRED
            'infra_pp': self.popup.radio_button_pp_infrastructure(),  # Public or Private
            'infra_desc': self.popup.register_InfraDesc.text().strip() or None,
            'infra_ownerfname': self.popup.register_InfraOwnerFirstName.text().strip(),  # REQUIRED
            'infra_ownerlname': self.popup.register_InfraOwnerLastName.text().strip(),  # REQUIRED
        }

    # THIS SHI HERE RADIO
    # def radio_button_pp_infrastructure(self):
    #     if self.popup.register_radioButton_labelInfraPP_Private.isChecked():
    #         pp_value = 'Private'
    #     elif self.popup.register_radioButton_labelInfraPP_Public.isChecked():
    #         pp_value = 'Public'
    #     else:
    #         pp_value = ''
    #     return pp_value

    def validate_infra_fields(self):
        # form_data = self.get_form_data()
        # print(form_data)
        errors = []


        # Validate Infra name
        if not self.popup.register_InfraName.text().strip():
            errors.append("Infrastructure name is required")
            self.popup.register_InfraName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_InfraName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Infra address
        if not self.popup.register_InfraAddress.text().strip():
            errors.append("Infrastructure address is required")
            self.popup.register_InfraAddress.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_InfraAddress.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Infra Type
        if self.popup.register_comboBox_InfraType.currentIndex() == -1:
            errors.append("Infrastructure type is required")
            self.popup.register_comboBox_InfraType.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.popup.register_comboBox_InfraType.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # Validate Private or Public
        if not (self.popup.register_radioButton_labelInfraPP_Private.isChecked() or
                self.popup.register_radioButton_labelInfraPP_Public.isChecked()):
            errors.append("Public or Private is required")
            self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: red")
            self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: red")
        else:
            self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: rgb(18, 18, 18)")
            self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: rgb(18, 18, 18)")

        # if not form_data['infra_pp']:
        #     errors.append("Private or Public is required.")
        #     self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: red")
        #     self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: red")
        # else:
        #     self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: rgb(18, 18, 18)")

        # Validate Infra Sitio
        if self.popup.register_comboBox_InfraAddress_Sitio.currentIndex() == -1:
            errors.append("Infrastructure sitio is required")
            self.popup.register_comboBox_InfraAddress_Sitio.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.popup.register_comboBox_InfraAddress_Sitio.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # Validate First name
        if not self.popup.register_InfraOwnerFirstName.text().strip():
            errors.append("Infrastructure owner firstname is required")
            self.popup.register_InfraOwnerFirstName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_InfraOwnerFirstName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Last name
        if not self.popup.register_InfraOwnerLastName.text().strip():
            errors.append("Infrastructure owner lastname is required")
            self.popup.register_InfraOwnerLastName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_InfraOwnerLastName.setStyleSheet(
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
            "Are you sure you want to register this infrastructure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print("-- Form Submitted")
            QMessageBox.information(self.popup, "Success", "Infrastructure successfully registered!")
            self.popup.close()
            self.load_data_infrastructure()

        # # Save final form with confirmation
        # save_btn = self.popup.findChild(QPushButton, "register_buttonConfirmInfra_SaveForm")
        # if save_btn:
        #     def confirm_and_save():
        #         reply = QMessageBox.question(
        #             self.popup,
        #             "Confirm Registration",
        #             "Are you sure you want to register this infrastructure?",
        #             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        #             QMessageBox.StandardButton.No
        #         )
        #
        #         if reply == QMessageBox.StandardButton.Yes:
        #             print("-- Form Submitted")
        #             QMessageBox.information(self.popup, "Success", "Infrastructure Successfully Registered!")
        #             self.popup.close()
        #             self.load_data_infrastructure()  # Refresh the data
        #
        #     save_btn.clicked.connect(confirm_and_save)
        #
        # self.popup.setWindowModality(Qt.WindowModality.ApplicationModal)
        # self.popup.show()

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")