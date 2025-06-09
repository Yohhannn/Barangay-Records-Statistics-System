from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QButtonGroup, QRadioButton, QTableWidgetItem
from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class InfrastructureController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_infra_id = None
        self.user_role = user_role
        self.selected_id = None
        self.stack = stack
        self.inst_infrastructure_screen = self.load_ui("Resources/UIs/MainPages/InstitutionPages/infrastructure.ui")
        self.setup_infrastructure_ui()
        self.center_on_screen()
        self.load_data_infrastructure()
        self.inst_infrastructure_screen.inst_tableView_List_RegInfra.cellClicked.connect(self.handle_row_click_infrastructure)
        self.inst_infrastructure_screen.inst_infra_button_remove.clicked.connect(self.handle_remove_infrastructure)
        self.inst_infrastructure_screen.inst_infra_button_update.clicked.connect(self.show_update_infrastructure_popup)


    def setup_infrastructure_ui(self):
        """Setup the Infrastructure Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Infrastructure")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
        # Set images and icons
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.setIcon(
            QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.inst_infrastructure_screen.inst_InfraName_buttonSearch.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.inst_infrastructure_screen.inst_infra_button_register.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.inst_infrastructure_screen.inst_infra_button_update.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.inst_infrastructure_screen.inst_infra_button_remove.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_del.svg'))

        # Return Button
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.clicked.connect(self.goto_institutions_panel)
        # REGISTER BUTTON
        self.inst_infrastructure_screen.inst_infra_button_register.clicked.connect(self.show_register_infrastructure_popup)
        self.inst_infrastructure_screen.inst_InfraName_buttonSearch.clicked.connect(self.perform_infrastructure_search)

    def show_update_infrastructure_popup(self):
        if not getattr(self, 'selected_infra_id', None):
            QMessageBox.warning(self.inst_infrastructure_screen, "No Selection",
                                "Please select an infrastructure to update.")
            return

        print("-- Update Infrastructure Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Institutions/Update/edit_register_infrastructure.ui", self)
        self.popup.setWindowTitle("Mapro: Update Infrastructure")
        self.popup.setFixedSize(self.popup.size())

        # Load related lists
        self.load_sitio_list()
        self.load_infra_type_list()

        # Set icon
        self.popup.register_buttonConfirmInfra_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        # Connect signals
        self.popup.register_buttonConfirmInfra_SaveForm.clicked.connect(self.validate_and_update_infrastructure)

        # Setup radio buttons
        self.setup_radio_button_groups_infrastructure()

        # Populate current infrastructure data
        self.populate_infrastructure_data_for_edit()

        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

    def populate_infrastructure_data_for_edit(self):
        infra_id = self.selected_infra_id
        try:
            db = Database()
            cursor = db.get_cursor()

            query = """
                SELECT 
                    INF.INF_NAME,
                    INF.INF_ACCESS_TYPE,
                    INF.INF_DESCRIPTION,
                    INF.INF_ADDRESS_DESCRIPTION,
                    COALESCE(IO.INFO_FNAME, '') AS OWNER_FNAME,
                    COALESCE(IO.INFO_LNAME, '') AS OWNER_LNAME,
                    IT.INFT_TYPE_NAME,
                    S.SITIO_NAME
                FROM INFRASTRUCTURE INF
                LEFT JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
                LEFT JOIN INFRASTRUCTURE_TYPE IT ON INF.INFT_ID = IT.INFT_ID
                LEFT JOIN SITIO S ON INF.SITIO_ID = S.SITIO_ID
                WHERE INF.INF_ID = %s AND INF.INF_IS_DELETED = FALSE;
            """
            cursor.execute(query, (infra_id,))
            result = cursor.fetchone()

            if not result:
                raise Exception(f"No infrastructure found with ID {infra_id}")

            (
                name, access_type, description, address,
                owner_fname, owner_lname, infra_type_name, sitio_name
            ) = result

            # Fill text fields
            self.popup.register_InfraName.setText(name)
            self.popup.register_InfraAddress.setText(address)
            self.popup.register_InfraDesc.setPlainText(description)
            self.popup.register_InfraOwnerFirstName.setText(owner_fname)
            self.popup.register_InfraOwnerLastName.setText(owner_lname)

            # Set combo boxes
            self.popup.register_comboBox_InfraType.setCurrentText(infra_type_name)
            self.popup.register_comboBox_InfraAddress_Sitio.setCurrentText(sitio_name)

            # Set radio buttons
            access_group = self.popup.findChild(QButtonGroup, "radio_PP")
            public_btn = self.popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Public")
            private_btn = self.popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Private")

            if access_type == "Public":
                public_btn.setChecked(True)
            elif access_type == "Private":
                private_btn.setChecked(True)

        except Exception as e:
            QMessageBox.critical(self.popup, "Error", f"Failed to load infrastructure data: {str(e)}")
        finally:
            db.close()

    def validate_and_update_infrastructure(self):
        errors = []

        if not self.popup.register_InfraName.text().strip():
            errors.append("Infrastructure name is required")
            self.popup.register_InfraName.setStyleSheet("border: 1px solid red;")
        else:
            self.popup.register_InfraName.setStyleSheet("border: 1px solid gray;")

        if not self.popup.register_InfraAddress.text().strip():
            errors.append("Infrastructure address is required")
            self.popup.register_InfraAddress.setStyleSheet("border: 1px solid red;")
        else:
            self.popup.register_InfraAddress.setStyleSheet("border: 1px solid gray;")

        if self.popup.register_comboBox_InfraType.currentIndex() == -1:
            errors.append("Infrastructure type is required")
            self.popup.register_comboBox_InfraType.setStyleSheet("border: 1px solid red;")
        else:
            self.popup.register_comboBox_InfraType.setStyleSheet("border: 1px solid gray;")

        if self.popup.register_comboBox_InfraAddress_Sitio.currentIndex() == -1:
            errors.append("Infrastructure sitio is required")
            self.popup.register_comboBox_InfraAddress_Sitio.setStyleSheet("border: 1px solid red;")
        else:
            self.popup.register_comboBox_InfraAddress_Sitio.setStyleSheet("border: 1px solid gray;")

        access_group = self.popup.findChild(QButtonGroup, "radio_PP")
        selected_button = access_group.checkedButton()
        if not selected_button:
            errors.append("Public or Private is required")
            self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: red")
            self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: red")
        else:
            self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: black")
            self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: black")

        if selected_button and selected_button.text() == "Private":
            if not self.popup.register_InfraOwnerFirstName.text().strip():
                errors.append("First name is required for private infrastructure")
                self.popup.register_InfraOwnerFirstName.setStyleSheet("border: 1px solid red;")
            else:
                self.popup.register_InfraOwnerFirstName.setStyleSheet("border: 1px solid gray;")

            if not self.popup.register_InfraOwnerLastName.text().strip():
                errors.append("Last name is required for private infrastructure")
                self.popup.register_InfraOwnerLastName.setStyleSheet("border: 1px solid red;")
            else:
                self.popup.register_InfraOwnerLastName.setStyleSheet("border: 1px solid gray;")

        if errors:
            QMessageBox.warning(
                self.popup,
                "Incomplete Form",
                "Please complete all required fields:\n• " + "\n• ".join(errors)
            )
            return
        else:
            self.confirm_and_update_infrastructure()

    def confirm_and_update_infrastructure(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Update",
            "Are you sure you want to update this infrastructure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        infra_id = self.selected_infra_id
        try:
            db = Database()
            cursor = db.get_cursor()

            infra_name = self.popup.register_InfraName.text().strip()
            infra_address = self.popup.register_InfraAddress.text().strip()
            infra_description = self.popup.register_InfraDesc.toPlainText().strip()
            owner_fname = self.popup.register_InfraOwnerFirstName.text().strip()
            owner_lname = self.popup.register_InfraOwnerLastName.text().strip()
            access_type = "Public" if self.popup.findChild(QRadioButton,
                                                           "register_radioButton_labelInfraPP_Public").isChecked() else "Private"

            # Fetch Sitio and Infra Type IDs
            sitio_name = self.popup.register_comboBox_InfraAddress_Sitio.currentText()
            cursor.execute("SELECT sitio_id FROM sitio WHERE sitio_name = %s", (sitio_name,))
            sitio_id = cursor.fetchone()[0]

            infra_type_name = self.popup.register_comboBox_InfraType.currentText()
            cursor.execute("SELECT inft_id FROM infrastructure_type WHERE inft_type_name = %s", (infra_type_name,))
            inft_id = cursor.fetchone()[0]

            # Handle Owner Info
            owner_id = None
            if access_type == "Private":
                if not owner_fname or not owner_lname:
                    raise Exception("First name and Last name are required for private owners.")

                # Check if owner exists or insert new
                cursor.execute("""
                    SELECT info_id FROM infrastructure_owner 
                    WHERE info_fname = %s AND info_lname = %s
                """, (owner_fname, owner_lname))
                result = cursor.fetchone()
                if result:
                    owner_id = result[0]
                else:
                    cursor.execute("""
                        INSERT INTO infrastructure_owner (INFO_FNAME, INFO_LNAME)
                        VALUES (%s, %s) RETURNING INFO_ID;
                    """, (owner_fname, owner_lname))
                    owner_id = cursor.fetchone()[0]

            # Update Query
            update_query = """
                UPDATE infrastructure SET
                    INF_NAME = %s,
                    INF_ACCESS_TYPE = %s,
                    INF_DESCRIPTION = %s,
                    INF_ADDRESS_DESCRIPTION = %s,
                    INFT_ID = %s,
                    INFO_ID = %s,
                    SITIO_ID = %s,
                    LAST_UPDATED_BY_SYS_ID = %s,
                    INF_LAST_UPDATED = NOW()
                WHERE INF_ID = %s;
            """
            cursor.execute(update_query, (
                infra_name, access_type, infra_description,
                infra_address, inft_id, owner_id, sitio_id,
                self.sys_user_id, infra_id
            ))
            db.conn.commit()

            QMessageBox.information(self.popup, "Success", "Infrastructure successfully updated!")
            self.popup.close()
            self.load_data_infrastructure()

        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self.popup, "Database Error", str(e))
        finally:
            db.close()


    def handle_remove_infrastructure(self):
        if not getattr(self, 'selected_infra_id', None):
            QMessageBox.warning(
                self.inst_infrastructure_screen,
                "No Selection",
                "Please select an infrastructure to remove."
            )
            return

        infra_id = self.selected_infra_id

        confirm = QMessageBox.question(
            self.inst_infrastructure_screen,
            "Confirm Deletion",
            f"Are you sure you want to delete infrastructure with ID {infra_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            db = Database()
            cursor = db.get_cursor()

            # Soft-delete the infrastructure
            cursor.execute("""
                UPDATE infrastructure
                SET INF_IS_DELETED = TRUE
                WHERE INF_ID = %s;
            """, (infra_id,))

            db.conn.commit()
            QMessageBox.information(
                self.inst_infrastructure_screen,
                "Success",
                f"Infrastructure {infra_id} has been deleted."
            )
            self.load_data_infrastructure()  # Refresh table

            if hasattr(self, 'selected_infra_id'):
                delattr(self, 'selected_infra_id')

        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(
                self.inst_infrastructure_screen,
                "Database Error",
                f"Failed to delete infrastructure: {str(e)}"
            )
        finally:
            db.close()

    def perform_infrastructure_search(self):
        search_text = self.inst_infrastructure_screen.inst_InfraName_fieldSearch.text().strip()
        if not search_text:
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
                LEFT JOIN SYSTEM_ACCOUNT SA ON INF.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON INF.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE INF.INF_IS_DELETED = FALSE
                ORDER BY COALESCE(INF.INF_LAST_UPDATED, INF.INF_DATE_ENCODED) DESC
                LIMIT 50
            """)
            rows = cursor.fetchall()
            self.rows = rows
            table = self.inst_infrastructure_screen.inst_tableView_List_RegInfra
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Name", "Owner", "Date Registered"])
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 150)
            table.setColumnWidth(3, 100)
            for row_idx, row_data in enumerate(rows):
                display_columns = [
                    row_data[0],  # INF_ID
                    row_data[1],  # INF_NAME
                    row_data[4],  # INFRASTRUCTURE_OWNER
                    row_data[3]   # INF_DATE_ENCODED
                ]
                for col_idx, value in enumerate(display_columns):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load infrastructure data: {str(e)}")
        finally:
            if connection:
                connection.close()

    def handle_row_click_infrastructure(self, row):
        self.selected_id = self.inst_infrastructure_screen.inst_tableView_List_RegInfra.item(row, 0).text()
        self.selected_infra_id = self.selected_id
        for record in self.rows:
            if str(record[0]) == self.selected_id:
                self.inst_infrastructure_screen.inst_displayInfraID.setText(str(record[0]))
                self.inst_infrastructure_screen.inst_displayInfraName.setText(record[1])
                self.inst_infrastructure_screen.inst_displayInfraOwnerName.setText(record[4])
                self.inst_infrastructure_screen.inst_displayInfraType.setText(record[5])
                self.inst_infrastructure_screen.inst_displayInfraAddress.setText(record[6])
                self.inst_infrastructure_screen.inst_displayInfraSitio.setText(record[7])
                self.inst_infrastructure_screen.inst_displayInfraPP.setText(record[2])
                self.inst_infrastructure_screen.inst_InfraDescription.setText(record[8])
                self.inst_infrastructure_screen.inst_display_EncodedBy.setText(record[9])
                self.inst_infrastructure_screen.inst_display_DateEncoded.setText(record[10])
                self.inst_infrastructure_screen.inst_display_UpdatedBy.setText(record[13])
                self.inst_infrastructure_screen.inst_display_DateUpdated.setText(
                    record[11] if record[11] else "Not updated")

    def show_register_infrastructure_popup(self):
        print("-- Register Infrastructure Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Institutions/register_infrastructure.ui", self)
        self.popup.setWindowTitle("Mapro: Register New Infrastructure")
        self.popup.setFixedSize(self.popup.size())
        self.load_sitio_list()
        self.load_infra_type_list()
        self.setup_radio_button_groups_infrastructure()
        self.popup.register_buttonConfirmInfra_SaveForm.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmInfra_SaveForm.clicked.connect(self.validate_infra_fields)
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

    def load_sitio_list(self):
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT sitio_id, sitio_name FROM sitio ORDER BY sitio_name ASC;")
            results = cursor.fetchall()
            combo = self.popup.register_comboBox_InfraAddress_Sitio
            combo.clear()
            for sitio_id, sitio_name in results:
                combo.addItem(sitio_name, sitio_id)
        except Exception as e:
            print(f"Failed to load sitios: {e}")
        finally:
            db.close()

    def load_infra_type_list(self):
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT inft_id, inft_type_name FROM infrastructure_type ORDER BY inft_type_name ASC;")
            results = cursor.fetchall()
            combo = self.popup.register_comboBox_InfraType
            combo.clear()
            for inft_id, inft_type_name in results:
                combo.addItem(inft_type_name, inft_id)
        except Exception as e:
            print(f"Failed to load infrastructure types: {e}")
        finally:
            db.close()

    def setup_radio_button_groups_infrastructure(self):
        radio_PP = QButtonGroup(self.popup)
        radio_PP.setObjectName("radio_PP")
        public_btn = self.popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Public")
        private_btn = self.popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Private")
        if public_btn and private_btn:
            radio_PP.addButton(public_btn)

            radio_PP.addButton(private_btn)
            # private_btn.setChecked(True)  # Default

    def validate_infra_fields(self):
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

        # Validate Public or Private
        access_group = self.popup.findChild(QButtonGroup, "radio_PP")
        selected_button = access_group.checkedButton()
        if not selected_button:
            errors.append("Public or Private is required")
            self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: red")
            self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: red")
        else:
            self.popup.register_radioButton_labelInfraPP_Private.setStyleSheet("color: black")
            self.popup.register_radioButton_labelInfraPP_Public.setStyleSheet("color: black")

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
                "Please complete all required fields:\n• " + "\n• ".join(errors)
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

        if reply != QMessageBox.Yes:
            return

        db = None
        connection = None
        try:
            db = Database()
            connection = db.conn
            cursor = connection.cursor()

            # --- Validate SITIO ---
            sitio_name = self.popup.register_comboBox_InfraAddress_Sitio.currentText().strip()
            cursor.execute("SELECT sitio_id FROM sitio WHERE sitio_name = %s", (sitio_name,))
            sitio_result = cursor.fetchone()
            if not sitio_result:
                raise Exception(f"Sitio '{sitio_name}' not found in database.")
            sitio_id = sitio_result[0]

            # --- Validate INFRASTRUCTURE TYPE ---
            infra_type_name = self.popup.register_comboBox_InfraType.currentText().strip()
            cursor.execute("SELECT inft_id FROM infrastructure_type WHERE inft_type_name = %s", (infra_type_name,))
            infra_type_result = cursor.fetchone()
            if not infra_type_result:
                raise Exception(f"Infrastructure type '{infra_type_name}' not found in database.")
            infra_type_id = infra_type_result[0]

            # --- Handle Public or Private access type ---
            access_group = self.popup.findChild(QButtonGroup, "radio_PP")
            selected_button = access_group.checkedButton()
            if not selected_button:
                raise Exception("Please select whether the infrastructure is Public or Private.")
            access_type = 'Public' if selected_button.text() == 'Public' else 'Private'

            # --- Get Owner Info (if private) ---
            owner_id = None
            if access_type == 'Private':
                owner_fname = self.popup.register_InfraOwnerFirstName.text().strip()
                owner_lname = self.popup.register_InfraOwnerLastName.text().strip()
                owner_mname = "None" or None

                if not owner_fname or not owner_lname:
                    raise Exception("First name and Last name are required for private infrastructure owners.")

                cursor.execute("""
                    INSERT INTO infrastructure_owner (INFO_FNAME, INFO_LNAME, INFO_MNAME)
                    VALUES (%s, %s, %s)
                    RETURNING INFO_ID;
                """, (owner_fname, owner_lname, owner_mname))

                owner_id = cursor.fetchone()[0]

            # --- Get form fields ---
            infra_name = self.popup.register_InfraName.text().strip()
            infra_address = self.popup.register_InfraAddress.text().strip()
            infra_description = self.popup.register_InfraDesc.toPlainText().strip()

            insert_query = """
            INSERT INTO infrastructure (
                INF_NAME, 
                INF_ACCESS_TYPE, 
                INF_DESCRIPTION, 
                INF_ADDRESS_DESCRIPTION, 
                INF_DATE_ENCODED, 
                INF_LAST_UPDATED, 
                INF_IS_DELETED, 
                INF_IS_PENDING_DELETE, 
                INF_DELETE_REQ_REASON, 
                INFT_ID, 
                INFO_ID, 
                SITIO_ID, 
                ENCODED_BY_SYS_ID, 
                LAST_UPDATED_BY_SYS_ID
            ) VALUES (
                %(name)s,
                %(access_type)s,
                %(description)s,
                %(address)s,
                NOW(),
                NOW(),
                FALSE,
                FALSE,
                NULL,
                %(inft_id)s,
                %(info_id)s,
                %(sitio_id)s,
                %(encoded_by)s,
                %(last_updated_by)s
            ) RETURNING INF_ID;
            """

            encoded_by = self.sys_user_id
            last_updated_by = self.sys_user_id

            cursor.execute(insert_query, {
                'name': infra_name,
                'access_type': access_type,
                'description': infra_description,
                'address': infra_address,
                'inft_id': infra_type_id,
                'info_id': owner_id,
                'sitio_id': sitio_id,
                'encoded_by': encoded_by,
                'last_updated_by': last_updated_by
            })

            new_inf_id = cursor.fetchone()[0]
            connection.commit()

            QMessageBox.information(self.popup, "Success", f"Infrastructure successfully registered! ID: {new_inf_id}")
            self.popup.close()
            self.load_data_infrastructure()

        except Exception as e:
            if connection:
                connection.rollback()
            QMessageBox.critical(self.popup, "Database Error", str(e))
        finally:
            if db:
                db.close()

    def goto_institutions_panel(self):
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                             self.user_role, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)
        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")