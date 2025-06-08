from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class SettlementHistoryController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role

        self.stack = stack
        self.hist_settlement_history_screen = self.load_ui("Resources/UIs/MainPages/HistoryRecordPages/settlement_history.ui")
        self.setup_settlement_history_ui()
        self.center_on_screen()
        self.load_settlement_history_data()

    def setup_settlement_history_ui(self):
        """Setup the Settlement History Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_settlement_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.hist_settlement_history_screen.histrec_SettlementID_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.hist_settlement_history_screen.histrec_settlementhistory_button_record.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.hist_settlement_history_screen.histrec_settlementhistory_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.hist_settlement_history_screen.histrec_settlementhistory_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        # self.hist_settlement_history_screen.settlementhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_settlement_history_screen.histrec_settlementhistory_button_record.clicked.connect(self.show_settlement_history_popup)
        self.hist_settlement_history_screen.histrec_tableView_List_RecordSettlementHistory.cellClicked.connect(self.handle_row_click_settlement_history)
        self.hist_settlement_history_screen.histrec_settlementhistory_button_remove.clicked.connect(
            self.handle_remove_settlement)
        # Return Button
        self.hist_settlement_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)
        self.hist_settlement_history_screen.histrec_SettlementID_buttonSearch.clicked.connect(
            self.search_settlement_history_data)

    def search_settlement_history_data(self):
        search_term = self.hist_settlement_history_screen.histrec_SettlementID_fieldSearch.text().strip()

        if not search_term:
            self.load_settlement_history_data()
            return

        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            query = """
                SELECT 
                    SL.SETT_ID,
                    C1.CTZ_ID AS COMPLAINEE_CITIZEN_ID,
                    C1.CTZ_FIRST_NAME || ' ' || C1.CTZ_LAST_NAME AS COMPLAINEE_NAME,
                    C2.COMP_FNAME || ' ' || C2.COMP_LNAME AS COMPLAINANT_NAME,
                    SL.SETT_COMPLAINT_DESCRIPTION,
                    SL.SETT_SETTLEMENT_DESCRIPTION,
                    TO_CHAR(SL.SETT_DATE_OF_SETTLEMENT, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_OF_SETTLEMENT,
                    TO_CHAR(SL.SETT_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(SL.SETT_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED,
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
                FROM SETTLEMENT_LOG SL
                JOIN COMPLAINANT C2 ON SL.COMP_ID = C2.COMP_ID
                JOIN CITIZEN_HISTORY CH ON SL.CIHI_ID = CH.CIHI_ID
                JOIN CITIZEN C1 ON CH.CTZ_ID = C1.CTZ_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON SL.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON SL.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE SL.SETT_IS_DELETED = FALSE AND CAST(SL.SETT_ID AS TEXT) ILIKE %s OR
                      C1.CTZ_FIRST_NAME ILIKE %s OR
                      C1.CTZ_LAST_NAME ILIKE %s OR
                      C2.COMP_FNAME ILIKE %s OR
                      C2.COMP_LNAME ILIKE %s OR
                      C1.CTZ_ID::TEXT ILIKE %s
                ORDER BY SL.SETT_DATE_ENCODED DESC
                LIMIT 50;
            """
            search_param = f"%{search_term}%"
            cursor.execute(query, (search_param, search_param, search_param, search_param, search_param, search_param))
            rows = cursor.fetchall()
            self._populate_settlement_history_table(rows)

        except Exception as e:
            QMessageBox.critical(self.hist_settlement_history_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def show_settlement_history_popup(self):
        print("-- Record Settlement History Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_settlement_history.ui", self)
        self.popup.setWindowTitle("Mapro: Record New Settlement History")
        self.popup.setFixedSize(self.popup.size())

        self.popup.record_buttonConfirmSettlementHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.record_buttonConfirmSettlementHistory_SaveForm.clicked.connect(self.validate_settlement_hist_fields)
        self.popup.record_citizenIDANDsearch.textChanged.connect(self.handle_citizen_id_search)

        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

    def handle_citizen_id_search(self):
        citizen_search = self.popup.record_citizenIDANDsearch.text().strip()
        if not citizen_search:
            self.popup.display_citizenFullName.setText("None")
            return

        connection = None
        try:
            connection = Database()
            cursor = connection.cursor

            # Try match by ID first
            query = """
                    SELECT CTZ_FIRST_NAME, CTZ_LAST_NAME
                    FROM CITIZEN
                    WHERE CTZ_ID = %s \
                      AND CTZ_IS_DELETED = FALSE; \
                    """
            cursor.execute(query, (citizen_search,))
            result = cursor.fetchone()

            # If no match, try by name
            if not result:
                query = """
                        SELECT CTZ_FIRST_NAME, CTZ_LAST_NAME
                        FROM CITIZEN
                        WHERE CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s \
                          AND CTZ_IS_DELETED = FALSE; \
                        """
                cursor.execute(query, (f"%{citizen_search}%",))
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


    def load_settlement_history_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
                SELECT 
                    SL.SETT_ID,
                    C1.CTZ_ID AS COMPLAINEE_CITIZEN_ID,
                    C1.CTZ_FIRST_NAME || ' ' || C1.CTZ_LAST_NAME AS COMPLAINEE_NAME,
                    C2.COMP_FNAME || ' ' || C2.COMP_LNAME AS COMPLAINANT_NAME,
                    SL.SETT_COMPLAINT_DESCRIPTION,
                    SL.SETT_SETTLEMENT_DESCRIPTION,
                    TO_CHAR(SL.SETT_DATE_OF_SETTLEMENT, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_OF_SETTLEMENT,
                    TO_CHAR(SL.SETT_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(SL.SETT_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED,
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
                FROM SETTLEMENT_LOG SL
                JOIN COMPLAINANT C2 ON SL.COMP_ID = C2.COMP_ID
                JOIN CITIZEN_HISTORY CH ON SL.CIHI_ID = CH.CIHI_ID
                JOIN CITIZEN C1 ON CH.CTZ_ID = C1.CTZ_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON SL.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON SL.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE SL.SETT_IS_DELETED = FALSE
                ORDER BY SL.SETT_DATE_ENCODED DESC
                LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.settlement_history_rows = rows

            table = self.hist_settlement_history_screen.histrec_tableView_List_RecordSettlementHistory
            table.setRowCount(len(rows))
            table.setColumnCount(5)  # Updated from 3 to 5
            table.setHorizontalHeaderLabels(
                ["Settlement ID", "Complainee Name", "Complainant Name", "Complainee CID", "Date Recorded"])

            # Set column widths
            table.setColumnWidth(0, 100)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 200)
            table.setColumnWidth(3, 150)
            table.setColumnWidth(4, 200)

            for row_idx, row in enumerate(rows):
                table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))  # Settlement ID
                table.setItem(row_idx, 1, QTableWidgetItem(row[2]))  # Complainee Name
                table.setItem(row_idx, 2, QTableWidgetItem(row[3]))  # Complainant Name
                table.setItem(row_idx, 3, QTableWidgetItem(str(row[1])))  # Complainee Citizen ID
                table.setItem(row_idx, 4, QTableWidgetItem(row[7] or "N/A"))  # Date Recorded

        except Exception as e:
            QMessageBox.critical(self.hist_settlement_history_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def _populate_settlement_history_table(self, rows):
        table = self.hist_settlement_history_screen.histrec_tableView_List_RecordSettlementHistory
        table.setRowCount(len(rows))
        table.setColumnCount(5)  # Updated from 3 to 5
        table.setHorizontalHeaderLabels(
            ["Settlement ID", "Complainee Name", "Complainant Name", "Complainee CID", "Date Recorded"])

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 200)
        table.setColumnWidth(3, 150)
        table.setColumnWidth(4, 200)

        self.settlement_history_rows = rows  # Store for use in display panel

        for row_idx, row in enumerate(rows):
            table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))  # Settlement ID
            table.setItem(row_idx, 1, QTableWidgetItem(row[2]))  # Complainee Name
            table.setItem(row_idx, 2, QTableWidgetItem(row[3]))  # Complainant Name
            table.setItem(row_idx, 3, QTableWidgetItem(str(row[1])))  # Complainee Citizen ID
            table.setItem(row_idx, 4, QTableWidgetItem(row[7] or "N/A"))  # Date Recorded


    def handle_row_click_settlement_history(self, row, column):
        table = self.hist_settlement_history_screen.histrec_tableView_List_RecordSettlementHistory
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()
        # Store selected settlement ID
        self.selected_settlement_id = selected_id

        for record in self.settlement_history_rows:
            if str(record[0]) == selected_id:
                self.hist_settlement_history_screen.histrec_displaySettID.setText(str(record[0]))
                self.hist_settlement_history_screen.histrec_displayComCtzID.setText(str(record[1]))
                self.hist_settlement_history_screen.histrec_displayComplainantName.setText(record[3])
                self.hist_settlement_history_screen.histrec_displayComplaineeName.setText(record[2])
                self.hist_settlement_history_screen.histrec_displayHistoryComplaintDescription.setText(record[4])
                self.hist_settlement_history_screen.histrec_displayHistorySettlementDescription.setText(record[5])
                self.hist_settlement_history_screen.histrec_displayDateSettlement.setText(record[6])
                self.hist_settlement_history_screen.display_DateEncoded.setText(record[7])
                self.hist_settlement_history_screen.display_DateUpdated.setText(record[8])
                self.hist_settlement_history_screen.display_EncodedBy.setText(record[9])
                self.hist_settlement_history_screen.display_UpdatedBy.setText(record[10])
                break

    # FORM DATA HERE [SETTLEMENT HISTORY] -------------------------------------------------------------------------------
    def get_form_data(self):
        return {
            'comp_fname': self.popup.record_ComplainantFirstName.text().strip(),
            'comp_mname': self.popup.record_ComplainantMiddleInitial.text().strip() or None,
            'comp_lname': self.popup.record_ComplainantLastName.text().strip(),
            'ctz_search': self.popup.record_citizenIDANDsearch.text().strip(),
            'complaint_desc': self.popup.record_ComplaintDesc.toPlainText().strip(),
            'settlement_desc': self.popup.record_SettlementDesc.toPlainText().strip(),
            'date_settled': self.popup.record_DateOfSettlement.date().toString("yyyy-MM-dd"),
        }
    def validate_settlement_hist_fields(self):
        errors = []

        # Validate Settlement Record Complainant First Name
        if not self.popup.record_ComplainantFirstName.text().strip():
            errors.append("Complainant First Name is required")
            self.popup.record_ComplainantFirstName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_ComplainantFirstName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Settlement Record Complainant Middle Initial
        if not self.popup.record_ComplainantMiddleInitial.text().strip():
            errors.append("Complainant Middle Initial is required")
            self.popup.record_ComplainantMiddleInitial.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_ComplainantMiddleInitial.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Settlement Record Complainant Last Name
        if not self.popup.record_ComplainantLastName.text().strip():
            errors.append("Complainant Last Name is required")
            self.popup.record_ComplainantLastName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_ComplainantLastName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Settlement Record Complainee ID
        ctz_search = self.popup.record_citizenIDANDsearch.text().strip()
        if not ctz_search:
            errors.append("Complainee citizen ID or name is required")
            self.popup.record_citizenIDANDsearch.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:

            self.popup.record_citizenIDANDsearch.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

            try:
                db = Database()
                cursor = db.cursor
                cursor.execute("""
                               SELECT CTZ_ID, CTZ_IS_DELETED
                               FROM CITIZEN
                               WHERE CTZ_IS_DELETED = FALSE
                                 AND (CTZ_ID::TEXT = %s OR CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s)
                               """, (ctz_search, f"%{ctz_search}%"))

                ctz_result = cursor.fetchone()
                if not ctz_result:
                    errors.append(f"No citizen found with ID '{ctz_search}'")

                    self.popup.record_citizenIDANDsearch.setStyleSheet(
                        "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                    )
                    ctz_id = ctz_result[0]
            except Exception as e:
                print(str(e))

        # Validate Settlement Record Complaint Desc
        if not self.popup.record_ComplaintDesc.toPlainText().strip():
            errors.append("Complaint Description is required")
            self.popup.record_ComplaintDesc.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_ComplaintDesc.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Settlement Record Settlement Desc
        if not self.popup.record_SettlementDesc.toPlainText().strip():
            errors.append("Settlement Description is required")
            self.popup.record_SettlementDesc.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_SettlementDesc.setStyleSheet(
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

    def handle_remove_settlement(self):
        if not getattr(self, 'selected_settlement_id', None):
            QMessageBox.warning(
                self.hist_settlement_history_screen,
                "No Selection",
                "Please select a settlement record to remove."
            )
            return

        sett_id = self.selected_settlement_id

        confirm = QMessageBox.question(
            self.hist_settlement_history_screen,
            "Confirm Deletion",
            f"Are you sure you want to delete settlement record with ID {sett_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            db = Database()
            cursor = db.get_cursor()

            # Soft-delete the settlement record
            cursor.execute("""
                UPDATE SETTLEMENT_LOG
                SET SETT_IS_DELETED = TRUE
                WHERE SETT_ID = %s;
            """, (sett_id,))

            db.conn.commit()
            QMessageBox.information(
                self.hist_settlement_history_screen,
                "Success",
                f"Settlement record {sett_id} has been deleted."
            )
            self.load_settlement_history_data()  # Refresh table

            if hasattr(self, 'selected_settlement_id'):
                delattr(self, 'selected_settlement_id')

        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(
                self.hist_settlement_history_screen,
                "Database Error",
                f"Failed to delete settlement record: {str(e)}"
            )
        finally:
            db.close()

    def confirm_and_save(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Settlement",
            "Are you sure you want to record this settlement?",
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
            db.set_user_id(self.sys_user_id)  # user ID for auditing
            connection = db.conn
            cursor = connection.cursor()

            # Get form data
            comp_fname = self.popup.record_ComplainantFirstName.text().strip()
            comp_mname = self.popup.record_ComplainantMiddleInitial.text().strip() or None
            comp_lname = self.popup.record_ComplainantLastName.text().strip()
            ctz_search = self.popup.record_citizenIDANDsearch.text().strip()
            complaint_desc = self.popup.record_ComplaintDesc.toPlainText().strip()
            settlement_desc = self.popup.record_SettlementDesc.toPlainText().strip()
            date_settled = self.popup.record_DateOfSettlement.date().toString("yyyy-MM-dd")

            # Validate required fields
            if not comp_fname:
                raise Exception("Complainant First Name is required")
            if not comp_lname:
                raise Exception("Complainant Last Name is required")
            if not ctz_search:
                raise Exception("Citizen ID or Name is required")
            if not complaint_desc:
                raise Exception("Complaint Description is required")
            if not settlement_desc:
                raise Exception("Settlement Description is required")

            # Step 1: Insert into COMPLAINANT
            cursor.execute("""
                INSERT INTO COMPLAINANT (COMP_FNAME, COMP_MNAME, COMP_LNAME)
                VALUES (%s, %s, %s)
                RETURNING COMP_ID;
            """, (comp_fname, comp_mname, comp_lname))

            comp_id = cursor.fetchone()[0]

            # Step 2: Find CITIZEN by ID or name
            cursor.execute("""
                SELECT CTZ_ID, CTZ_IS_DELETED FROM CITIZEN 
                WHERE CTZ_IS_DELETED = FALSE AND CTZ_ID::TEXT = %s OR CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s
            """, (ctz_search, f"%{ctz_search}%"))

            ctz_result = cursor.fetchone()
            if not ctz_result:
                raise Exception(f"No citizen found with ID or name containing '{ctz_search}'")
            ctz_id = ctz_result[0]

            # Step 3: Insert into CITIZEN_HISTORY (needed before settlement)
            db.cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
            cursor.execute("""
                INSERT INTO CITIZEN_HISTORY (CIHI_DESCRIPTION, HIST_ID, CTZ_ID, ENCODED_BY_SYS_ID, LAST_UPDATED_BY_SYS_ID)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING CIHI_ID;
            """, (
                complaint_desc,  # As part of citizen history
                1,  # Assuming default HIST_ID for complaint
                ctz_id,
                self.sys_user_id,
                self.sys_user_id
            ))

            cihi_id = cursor.fetchone()[0]

            # Step 4: Insert into SETTLEMENT_LOG
            insert_query = """
            INSERT INTO SETTLEMENT_LOG (
                SETT_COMPLAINT_DESCRIPTION,
                SETT_SETTLEMENT_DESCRIPTION,
                SETT_DATE_OF_SETTLEMENT,
                SETT_DATE_ENCODED,
                SETT_LAST_UPDATED,
                SETT_IS_DELETED,
                SETT_IS_PENDING_DELETE,
                COMP_ID,
                CIHI_ID,
                ENCODED_BY_SYS_ID,
                LAST_UPDATED_BY_SYS_ID
            ) VALUES (
                %(complaint_desc)s,
                %(settlement_desc)s,
                %(date_settled)s,
                NOW(),
                NOW(),
                FALSE,
                FALSE,
                %(comp_id)s,
                %(cihi_id)s,
                %(encoded_by)s,
                %(last_updated_by)s
            ) RETURNING SETT_ID;
            """

            encoded_by = self.sys_user_id
            last_updated_by = self.sys_user_id

            db.cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
            cursor.execute(insert_query, {
                'complaint_desc': complaint_desc,
                'settlement_desc': settlement_desc,
                'date_settled': date_settled,
                'comp_id': comp_id,
                'cihi_id': cihi_id,
                'encoded_by': encoded_by,
                'last_updated_by': last_updated_by
            })

            new_sett_id = cursor.fetchone()[0]
            connection.commit()

            QMessageBox.information(self.popup, "Success", f"Settlement successfully recorded! ID: {new_sett_id}")
            self.popup.close()
            self.load_settlement_history_data()  # Refresh the list

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