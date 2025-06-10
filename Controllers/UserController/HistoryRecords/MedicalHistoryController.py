from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class MedicalHistoryController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_medical_history_id = None
        self.user_role = user_role

        self.stack = stack
        self.hist_medical_history_screen = self.load_ui("Resources/UIs/MainPages/HistoryRecordPages/medical_history.ui")
        self.setup_medical_history_ui()
        self.center_on_screen()
        self.load_medical_history_data()

    def setup_medical_history_ui(self):
        """Setup the Medical History Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_medical_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.hist_medical_history_screen.histrecMedHistoryID_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_record.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        # self.hist_medical_history_screen.medicalhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_medical_history_screen.histrec_medicalhistory_button_record.clicked.connect(self.show_medical_history_popup)
        self.hist_medical_history_screen.histrec_tableView_List_RecordMedicalHistory.cellClicked.connect(self.handle_row_click_medical_history)
        self.hist_medical_history_screen.histrec_medicalhistory_button_update.clicked.connect(
            self.show_update_medical_history_popup
        )
        self.hist_medical_history_screen.histrec_medicalhistory_button_remove.clicked.connect(
            self.handle_remove_medical_history)
        # Return Button

        self.hist_medical_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)
        self.hist_medical_history_screen.histrecMedHistoryID_buttonSearch.clicked.connect(
            self.search_medical_history_data)

    def show_update_medical_history_popup(self):

        if not getattr(self, 'selected_medical_history_id', None):
            QMessageBox.warning(
                self.hist_medical_history_screen,
                "No Selection",
                "Please select a medical history record to update."
            )
            return


        mh_id = self.selected_medical_history_id

        try:
            db = Database()
            cursor = db.get_cursor()

            # Fetch full medical history record
            cursor.execute("""
                SELECT 
                    MH.MH_ID,
                    C.CTZ_ID,
                    C.CTZ_FIRST_NAME || ' ' || C.CTZ_LAST_NAME AS CTZ_FULLNAME,
                    MH.MH_DESCRIPTION,
                    MHT.MHT_TYPE_NAME,
                    MH.MH_DATE_DIAGNOSED
                FROM MEDICAL_HISTORY MH
                JOIN CITIZEN C ON MH.CTZ_ID = C.CTZ_ID
                JOIN MEDICAL_HISTORY_TYPE MHT ON MH.MHT_ID = MHT.MHT_ID
                WHERE MH.MH_ID = %s AND MH.MH_IS_DELETED = FALSE;
            """, (mh_id,))
            result = cursor.fetchone()

            if not result:
                QMessageBox.critical(
                    self.hist_medical_history_screen,
                    "Not Found",
                    f"No medical history found with ID {mh_id}"
                )
                return

            mh_id, ctz_id, fullname, description, mht_type_name, diagnosed_date = result

            # Load the popup UI

            self.popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/Update/edit_record_medical_history.ui")
            self.popup.setWindowTitle("Mapro: Edit Medical History")
            self.popup.setFixedSize(self.popup.size())
            self.popup.setWindowModality(Qt.ApplicationModal)

            self.load_medical_history_types()

            # Populate fields
            self.popup.record_citizenIDANDsearch.setText(str(ctz_id))
            self.popup.display_citizenFullName.setText(fullname)
            self.popup.record_medicalhistory_description.setPlainText(description)
            self.popup.register_citizen_comboBox_MedicalHistoryOption.setCurrentText(mht_type_name)

            # Connect Save button
            self.popup.record_buttonConfirmMedicalHistory_SaveForm.clicked.connect(
                lambda: self.save_updated_medical_history(mh_id)
            )


            self.popup.exec_()

        except Exception as e:
            QMessageBox.critical(self.hist_medical_history_screen, "Database Error", str(e))
        finally:
            db.close()

    def save_updated_medical_history(self, mh_id):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Update",
            "Are you sure you want to update this medical history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            db = Database()
            connection = db.conn
            cursor = connection.cursor()

            # Get form data
            ctz_search = self.popup.record_citizenIDANDsearch.text().strip()
            mht_type_name = self.popup.register_citizen_comboBox_MedicalHistoryOption.currentText().strip()
            description = self.popup.record_medicalhistory_description.toPlainText().strip()

            # Validate required fields
            if not ctz_search:
                raise Exception("Citizen ID or Name is required")
            if not mht_type_name:
                raise Exception("Medical history type is required")
            if not description:
                raise Exception("Description is required")

            # Get CTZ_ID
            cursor.execute("""
                SELECT CTZ_ID FROM CITIZEN 
                WHERE CTZ_IS_DELETED = FALSE AND (
                    CTZ_ID::TEXT = %s OR 
                    CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s
                )
            """, (ctz_search, f"%{ctz_search}%"))
            ctz_result = cursor.fetchone()
            if not ctz_result:
                raise Exception(f"No citizen found matching '{ctz_search}'")
            ctz_id = ctz_result[0]

            # Get MHT_ID
            cursor.execute("SELECT MHT_ID FROM MEDICAL_HISTORY_TYPE WHERE MHT_TYPE_NAME = %s", (mht_type_name,))
            mht_result = cursor.fetchone()
            if not mht_result:
                raise Exception(f"Medical history type '{mht_type_name}' not found.")
            mht_id = mht_result[0]

            # Update record
            cursor.execute("""
                UPDATE MEDICAL_HISTORY
                SET MH_DESCRIPTION = %s,
                    MHT_ID = %s,
                    CTZ_ID = %s,
                    LAST_UPDATED_BY_SYS_ID = %s,
                    MH_LAST_UPDATED = NOW()
                WHERE MH_ID = %s;
            """, (
                description,
                mht_id,
                ctz_id,
                self.sys_user_id,
                mh_id
            ))

            connection.commit()
            QMessageBox.information(self.popup, "Success", "Medical history updated successfully!")
            self.popup.close()
            self.load_medical_history_data()  # Refresh list

        except Exception as e:
            connection.rollback()
            QMessageBox.critical(self.popup, "Error", f"Failed to update medical history: {str(e)}")
        finally:
            db.close()




    def handle_remove_medical_history(self):
        if not getattr(self, 'selected_medical_history_id', None):
            QMessageBox.warning(
                self.hist_medical_history_screen,
                "No Selection",
                "Please select a medical history record to remove."
            )
            return

        mh_id = self.selected_medical_history_id

        confirm = QMessageBox.question(
            self.hist_medical_history_screen,
            "Confirm Deletion",
            f"Are you sure you want to delete medical history record with ID {mh_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            db = Database()
            cursor = db.get_cursor()

            # Soft-delete the medical history record
            cursor.execute("""
                UPDATE MEDICAL_HISTORY
                SET MH_IS_DELETED = TRUE
                WHERE MH_ID = %s;
            """, (mh_id,))

            db.conn.commit()
            QMessageBox.information(
                self.hist_medical_history_screen,
                "Success",
                f"Medical history record {mh_id} has been deleted."
            )
            self.load_medical_history_data()  # Refresh table

            if hasattr(self, 'selected_medical_history_id'):
                delattr(self, 'selected_medical_history_id')

        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(
                self.hist_medical_history_screen,
                "Database Error",
                f"Failed to delete medical history record: {str(e)}"
            )
        finally:
            db.close()

    def show_medical_history_popup(self):
        print("-- Record Medical History Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_medical_history.ui", self)
        self.popup.setWindowTitle("Mapro: Record New Medical History")
        self.popup.setFixedSize(self.popup.size())

        self.popup.record_buttonConfirmMedicalHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.record_buttonConfirmMedicalHistory_SaveForm.clicked.connect(self.validate_medical_hist_fields)
        self.popup.record_citizenIDANDsearch.textChanged.connect(self.handle_citizen_id_search)

        self.popup.setWindowModality(Qt.ApplicationModal)
        self.load_medical_history_types()
        self.popup.exec_()

    def handle_citizen_id_search(self):
        citizen_id = self.popup.record_citizenIDANDsearch.text().strip()
        if not citizen_id:
            self.popup.display_citizenFullName.setText("None")
            return

        connection = None
        try:
            connection = Database()
            cursor = connection.cursor

            # Query to fetch citizen by ID or name
            query = """
                    SELECT CTZ_FIRST_NAME, CTZ_LAST_NAME
                    FROM CITIZEN
                    WHERE CTZ_ID = %s \
                      AND CTZ_IS_DELETED = FALSE; \
                    """
            cursor.execute(query, (citizen_id,))
            result = cursor.fetchone()

            if result:
                full_name = f"{result[0]} {result[1]}"
                self.popup.display_citizenFullName.setText(full_name)
            else:
                self.popup.display_citizenFullName.setText("Not Found")

        except Exception as e:
            QMessageBox.critical(self.popup, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def load_medical_history_types(self):
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT MHT_ID, MHT_TYPE_NAME FROM MEDICAL_HISTORY_TYPE ORDER BY MHT_TYPE_NAME ASC;")
            results = cursor.fetchall()
            combo = self.popup.register_citizen_comboBox_MedicalHistoryOption
            combo.clear()
            for mht_id, mht_name in results:
                combo.addItem(mht_name, mht_id)
        except Exception as e:
            print(f"Failed to load medical history types: {e}")
        finally:
            db.close()
    def search_medical_history_data(self):
        search_term = self.hist_medical_history_screen.histrec_HistoryID_fieldSearch.text().strip()

        if not search_term:
            self.load_medical_history_data()
            return

        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            query = """
                SELECT 
                    MH.MH_ID,
                    C.CTZ_FIRST_NAME,
                    C.CTZ_LAST_NAME,
                    MHT.MHT_TYPE_NAME AS MEDICAL_TYPE,
                    MH.MH_DESCRIPTION,
                    TO_CHAR(MH.MH_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_RECORDED,
                    C.CTZ_ID,
                    TO_CHAR(MH.MH_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(MH.MH_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED,
                    CASE 
                        WHEN SA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SA.SYS_FNAME || ' ' || 
                             COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') || 
                             SA.SYS_LNAME
                    END AS ENCODED_BY,
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' || 
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') || 
                             SUA.SYS_LNAME
                    END AS UPDATED_BY
                FROM MEDICAL_HISTORY MH
                JOIN CITIZEN C ON MH.CTZ_ID = C.CTZ_ID
                JOIN MEDICAL_HISTORY_TYPE MHT ON MH.MHT_ID = MHT.MHT_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON MH.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON MH.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE MH.MH_IS_DELETED = FALSE AND CAST(MH.MH_ID AS TEXT) ILIKE %s OR
                      C.CTZ_FIRST_NAME ILIKE %s OR
                      C.CTZ_LAST_NAME ILIKE %s OR
                      MHT.MHT_TYPE_NAME ILIKE %s
                ORDER BY MH.MH_DATE_ENCODED DESC
                LIMIT 50;
            """
            search_param = f"%{search_term}%"
            cursor.execute(query, (search_param, search_param, search_param, search_param))
            rows = cursor.fetchall()
            self._populate_medical_history_table(rows)

        except Exception as e:
            QMessageBox.critical(self.hist_medical_history_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def _populate_medical_history_table(self, rows):
        table = self.hist_medical_history_screen.histrec_tableView_List_RecordMedicalHistory
        table.setRowCount(len(rows))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Medical ID", "Citizen Name", "Medical Type", "Date Recorded"])

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 250)
        table.setColumnWidth(3, 200)

        self.medical_history_rows = rows  # Store for use in display panel

        for row_idx, row in enumerate(rows):
            full_name = f"{row[1]} {row[2]}"
            table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))  # Medical ID
            table.setItem(row_idx, 1, QTableWidgetItem(full_name))  # Citizen Name
            table.setItem(row_idx, 2, QTableWidgetItem(row[3]))  # Medical Type
            table.setItem(row_idx, 3, QTableWidgetItem(row[5] or "N/A"))  # Date Recorded


    def load_medical_history_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
                SELECT 
                    MH.MH_ID,
                    C.CTZ_FIRST_NAME,
                    C.CTZ_LAST_NAME,
                    MHT.MHT_TYPE_NAME AS MEDICAL_TYPE,
                    MH.MH_DESCRIPTION,
                    TO_CHAR(MH.MH_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_RECORDED,
                    C.CTZ_ID,
                    TO_CHAR(MH.MH_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(MH.MH_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED,
                    CASE 
                        WHEN SA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SA.SYS_FNAME || ' ' || 
                             COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') || 
                             SA.SYS_LNAME
                    END AS ENCODED_BY,
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' || 
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') || 
                             SUA.SYS_LNAME
                    END AS UPDATED_BY
                FROM MEDICAL_HISTORY MH
                JOIN CITIZEN C ON MH.CTZ_ID = C.CTZ_ID
                JOIN MEDICAL_HISTORY_TYPE MHT ON MH.MHT_ID = MHT.MHT_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON MH.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON MH.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE MH.MH_IS_DELETED = FALSE
                ORDER BY MH.MH_DATE_ENCODED DESC
                LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.medical_history_rows = rows

            table = self.hist_medical_history_screen.histrec_tableView_List_RecordMedicalHistory
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Medical ID", "Citizen Name", "Medical Type", "Date Recorded"])

            table.setColumnWidth(0, 100)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 250)
            table.setColumnWidth(3, 200)

            for row_idx, row in enumerate(rows):
                full_name = f"{row[1]} {row[2]}"
                for col_idx, value in enumerate([row[0], full_name, row[3], row[5]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.hist_medical_history_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_medical_history(self, row, column):
        table = self.hist_medical_history_screen.histrec_tableView_List_RecordMedicalHistory
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()

        # Store selected medical history ID
        self.selected_medical_history_id = selected_id

        for record in self.medical_history_rows:
            if str(record[0]) == selected_id:
                self.hist_medical_history_screen.histrec_displayHistoryID.setText(str(record[0]))
                self.hist_medical_history_screen.histrec_displayCitizenID.setText(str(record[6]))
                self.hist_medical_history_screen.histrec_displayCitizenHistFirstName.setText(record[1])
                self.hist_medical_history_screen.histrec_displayCitizenHistLastName.setText(record[2])
                self.hist_medical_history_screen.histrec_displayMedicalHistoryType.setText(record[3])
                self.hist_medical_history_screen.histrec_displayHistoryDescription.setText(record[4])
                self.hist_medical_history_screen.display_DateEncoded.setText(record[7])
                self.hist_medical_history_screen.display_DateUpdated.setText(record[8])
                self.hist_medical_history_screen.display_EncodedBy.setText(record[9])
                self.hist_medical_history_screen.display_UpdatedBy.setText(record[10])
                break

    # FORM DATA HERE [MEDICAL HISTORY] -------------------------------------------------------------------------------
    def get_form_data(self):
        return {
            'ctz_id_search': self.popup.record_citizenIDANDsearch.text().strip(),  # REQUIRED
            'medical_hist_type': self.popup.register_citizen_comboBox_MedicalHistoryOption.text().strip(),  # REQUIRED
            'medical_hist_desc': self.popup.record_medicalhistory_description.text().strip() or None,
        }

    def validate_medical_hist_fields(self):
        errors = []

        # Validate Medical Record Citizen ID
        citizen_search = self.popup.record_citizenIDANDsearch.text().strip()
        if not citizen_search:
            errors.append("Citizen ID or Name is required")
            self.popup.record_citizenIDANDsearch.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            db = None
            try:
                db = Database()
                cursor = db.get_cursor()
                cursor.execute("""
                    SELECT CTZ_ID, CTZ_IS_DELETED FROM CITIZEN 
                    WHERE CTZ_IS_DELETED = FALSE AND CTZ_ID::TEXT = %s OR CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s
                """, (citizen_search, f"%{citizen_search}%"))

                result = cursor.fetchone()
                if not result:
                    errors.append("Citizen ID or Name does not exist")
                    self.popup.record_citizenIDANDsearch.setStyleSheet(
                        "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                    )
                else:
                    self.popup.record_citizenIDANDsearch.setStyleSheet(
                        "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                    )
            except Exception as e:
                errors.append("Error validating citizen info")
                self.popup.record_citizenIDANDsearch.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            finally:
                if db:
                    db.close()

        # Validate Medical History Type
        if self.popup.register_citizen_comboBox_MedicalHistoryOption.currentIndex() == -1:
            errors.append("Medical history type is required")
            self.popup.register_citizen_comboBox_MedicalHistoryOption.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_citizen_comboBox_MedicalHistoryOption.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Medical Record Description
        if not self.popup.record_medicalhistory_description.toPlainText().strip():
            errors.append("Medical description is required")
            self.popup.record_medicalhistory_description.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_medicalhistory_description.setStyleSheet(
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
            "Confirm Medical History",
            "Are you sure you want to record this medical history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        db = None
        connection = None
        try:
            # Initialize DB connection
            db = Database()
            connection = db.conn
            cursor = connection.cursor()

            # Get form data
            ctz_id_search = self.popup.record_citizenIDANDsearch.text().strip()
            mht_type_name = self.popup.register_citizen_comboBox_MedicalHistoryOption.currentText().strip()
            mh_description = self.popup.record_medicalhistory_description.toPlainText().strip()

            # Validate required fields
            if not ctz_id_search:
                raise Exception("Citizen ID or Name is required")
            if not mht_type_name:
                raise Exception("Medical History Type is required")
            if not mh_description:
                raise Exception("Medical Description is required")

            # Find CITIZEN by ID or name
            cursor.execute("""
                SELECT CTZ_ID, CTZ_IS_DELETED FROM CITIZEN 
                WHERE CTZ_IS_DELETED = FALSE AND CTZ_ID= %s OR CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s
            """, (ctz_id_search, f"%{ctz_id_search}%"))

            ctz_result = cursor.fetchone()
            if not ctz_result:
                raise Exception(f"No citizen found with ID or name containing '{ctz_id_search}'")
            ctz_id = ctz_result[0]

            # Get MEDICAL_HISTORY_TYPE ID
            cursor.execute("SELECT MHT_ID FROM MEDICAL_HISTORY_TYPE WHERE MHT_TYPE_NAME = %s", (mht_type_name,))
            mht_result = cursor.fetchone()
            if not mht_result:
                raise Exception(f"Medical history type '{mht_type_name}' not found.")
            mht_id = mht_result[0]

            # Insert into MEDICAL_HISTORY
            insert_query = """
            INSERT INTO MEDICAL_HISTORY (
                MH_DESCRIPTION,
                MH_DATE_DIAGNOSED,
                MHT_ID,
                CTZ_ID,
                ENCODED_BY_SYS_ID,
                LAST_UPDATED_BY_SYS_ID
            ) VALUES (
                %(description)s,
                NOW(),
                %(mht_id)s,
                %(ctz_id)s,
                %(encoded_by)s,
                %(last_updated_by)s
            ) RETURNING MH_ID;
            """

            encoded_by = self.sys_user_id
            last_updated_by = self.sys_user_id

            cursor.execute(insert_query, {
                'description': mh_description,
                'mht_id': mht_id,
                'ctz_id': ctz_id,
                'encoded_by': encoded_by,
                'last_updated_by': last_updated_by
            })

            new_mh_id = cursor.fetchone()[0]
            connection.commit()

            QMessageBox.information(self.popup, "Success", f"Medical History successfully recorded! ID: {new_mh_id}")
            self.popup.close()
            self.load_medical_history_data()  # Refresh the history list

        except Exception as e:
            if connection:
                connection.rollback()
            QMessageBox.critical(self.popup, "Database Error", str(e))
        finally:
            if db:
                db.close()


    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)