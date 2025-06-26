from PySide6.QtGui import QIcon, Qt
from database import Database

from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup


class ServiceController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_transaction_id = None
        self.user_role = user_role
        self.sys_user_id = sys_user_id
        
        self.stack = stack
        self.trans_services_screen = self.load_ui("Resources/UIs/MainPages/TransactionPages/services.ui")
        self.setup_services_ui()
        self.center_on_screen()
        self.load_transaction_data()

    def setup_services_ui(self):
        """Setup the Services Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Services")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.trans_services_screen.btn_returnToTransactionPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.trans_services_screen.inst_Transaction_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.trans_services_screen.trans_Transact_button_create.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.trans_services_screen.trans_Transact_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.trans_services_screen.trans_Transact_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        # self.trans_services_screen.transactionList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # REGISTER BUTTON
        self.trans_services_screen.trans_Transact_button_create.clicked.connect(self.show_transaction_popup)
        self.trans_services_screen.inst_tableView_List_RegBusiness.cellClicked.connect(self.handle_row_click_transaction)

        self.trans_services_screen.trans_Transact_button_remove.clicked.connect(self.handle_remove_transaction)

        # Return Button
        self.trans_services_screen.inst_Transaction_buttonSearch.clicked.connect(self.search_transaction_data)
        self.trans_services_screen.trans_Transact_button_update.clicked.connect(self.show_update_transaction_popup)
        self.trans_services_screen.btn_returnToTransactionPage.clicked.connect(self.goto_transactions_panel)



    def search_transaction_data(self):
        """Filter transaction data based on ID or Name."""
        search_term = self.trans_services_screen.trans_TransactionID_fieldSearch.text().strip()
        if not search_term:
            self.load_transaction_data()
            return

        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            query = """
                SELECT 
                    TL.tl_id,
                    TL.tl_fname,
                    TL.tl_lname,
                    TO_CHAR(TL.tl_date_requested, 'FMMonth FMDD, YYYY') AS tl_date_requested_formatted,
                    TL.tl_status,
                    TT.tt_type_name,
                    TL.tl_purpose,
                    TO_CHAR(TL.tl_date_encoded, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS tl_date_encoded_formatted,
                    SA.SYS_FNAME || ' ' || COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') || SA.SYS_LNAME AS ENCODED_BY,
                    TO_CHAR(TL.tl_last_updated, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS tl_last_updated_formatted,
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' ||
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                             SUA.SYS_LNAME
                    END AS LAST_UPDATED_BY_NAME
                FROM TRANSACTION_LOG TL
                LEFT JOIN TRANSACTION_TYPE TT ON TL.tt_id = TT.tt_id
                LEFT JOIN SYSTEM_ACCOUNT SA ON TL.ENCODED_BY_sys_id = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON TL.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE TL.tl_is_deleted = FALSE
                  AND (
                    CAST(TL.tl_id AS TEXT) ILIKE %s OR
                    TL.tl_fname ILIKE %s OR
                    TL.tl_lname ILIKE %s
                  )
                ORDER BY TL.tl_id ASC
                LIMIT 50;
            """
            search_param = f"%{search_term}%"
            cursor.execute(query, (search_param, search_param, search_param))
            rows = cursor.fetchall()
            self._populate_table(rows)

        except Exception as e:
            QMessageBox.critical(self.trans_services_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def show_update_transaction_popup(self):
        if not getattr(self, 'selected_transaction_id', None):
            QMessageBox.warning(
                self.trans_services_screen,
                "No Selection",
                "Please select a transaction to update."
            )
            return

        print("-- Update Transaction Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Transactions/Update/edit_create_transaction.ui", self)
        self.popup.setWindowTitle("Mapro: Update Transaction")
        self.popup.setFixedSize(self.popup.size())

        # Set icon
        self.popup.register_buttonConfirmTransaction_SaveForm.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        # Connect signals
        self.popup.register_buttonConfirmTransaction_SaveForm.clicked.connect(self.validate_and_update_transaction)

        # Load transaction types
        self.load_transaction_types()

        # Populate current transaction data
        self.populate_transaction_data_for_edit()

        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

    def populate_transaction_data_for_edit(self):
        tl_id = self.selected_transaction_id
        try:
            db = Database()
            cursor = db.get_cursor()

            query = """
                SELECT 
                    TL_FNAME, TL_LNAME, TL_STATUS, TL_PURPOSE, TT_TYPE_NAME
                FROM TRANSACTION_LOG TL
                LEFT JOIN TRANSACTION_TYPE TT ON TL.TT_ID = TT.TT_ID
                WHERE TL_ID = %s AND TL_IS_DELETED = FALSE;
            """
            cursor.execute(query, (tl_id,))
            result = cursor.fetchone()

            if not result:
                raise Exception(f"No transaction found with ID {tl_id}")

            fname, lname, status, purpose, tt_name = result

            # Fill text fields
            self.popup.register_ReqFirstName.setText(fname)
            self.popup.register_ReqLastName.setText(lname)
            self.popup.register_Purpose.setPlainText(purpose)

            # Set combo boxes
            index = self.popup.register_comboBox_TransactionType.findText(tt_name)
            if index >= 0:
                self.popup.register_comboBox_TransactionType.setCurrentIndex(index)

            index_status = self.popup.register_comboBox_TransactionStatus.findText(status)
            if index_status >= 0:
                self.popup.register_comboBox_TransactionStatus.setCurrentIndex(index_status)

        except Exception as e:
            QMessageBox.critical(self.popup, "Error", f"Failed to load transaction data: {str(e)}")
        finally:
            db.close()

    def validate_and_update_transaction(self):
        errors = []

        # Validate requestor first name
        if not self.popup.register_ReqFirstName.text().strip():
            errors.append("Requester firstname is required")
            self.popup.register_ReqFirstName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_ReqFirstName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate requestor last name
        if not self.popup.register_ReqLastName.text().strip():
            errors.append("Requester lastname is required")
            self.popup.register_ReqLastName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_ReqLastName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate request status
        if self.popup.register_comboBox_TransactionStatus.currentIndex() == -1:
            errors.append("Request Status is required")
            self.popup.register_comboBox_TransactionStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_comboBox_TransactionStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate transaction type
        if self.popup.register_comboBox_TransactionType.currentIndex() == -1:
            errors.append("Transaction type is required")
            self.popup.register_comboBox_TransactionType.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_comboBox_TransactionType.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate transaction purpose
        if not self.popup.register_Purpose.toPlainText().strip():
            errors.append("Request purpose is required")
            self.popup.register_Purpose.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_Purpose.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if errors:
            QMessageBox.warning(
                self.popup,
                "Incomplete Form",
                "Please complete all required fields:\n• " + "\n• ".join(errors)
            )
            return
        else:
            self.confirm_and_update_transaction()

    def confirm_and_update_transaction(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Update",
            "Are you sure you want to update this transaction?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        tl_id = self.selected_transaction_id
        try:
            db = Database()
            cursor = db.get_cursor()

            fname = self.popup.register_ReqFirstName.text().strip()
            lname = self.popup.register_ReqLastName.text().strip()
            status = self.popup.register_comboBox_TransactionStatus.currentText().strip()
            purpose = self.popup.register_Purpose.toPlainText().strip()
            tt_name = self.popup.register_comboBox_TransactionType.currentText().strip()

            # Get transaction type ID
            cursor.execute("SELECT TT_ID FROM TRANSACTION_TYPE WHERE TT_TYPE_NAME = %s", (tt_name,))
            tt_result = cursor.fetchone()
            if not tt_result:
                raise Exception(f"Transaction type '{tt_name}' not found.")
            tt_id = tt_result[0]

            # Perform update
            update_query = """
                UPDATE TRANSACTION_LOG SET
                    TL_FNAME = %s,
                    TL_LNAME = %s,
                    TL_STATUS = %s,
                    TL_PURPOSE = %s,
                    TT_ID = %s,
                    LAST_UPDATED_BY_SYS_ID = %s,
                    TL_LAST_UPDATED = NOW()
                WHERE TL_ID = %s;
            """
            cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
            cursor.execute(update_query, (
                fname, lname, status, purpose,
                tt_id, self.sys_user_id, tl_id
            ))
            db.conn.commit()

            QMessageBox.information(self.popup, "Success", "Transaction successfully updated!")
            self.popup.close()
            self.load_transaction_data()

        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self.popup, "Database Error", str(e))
        finally:
            db.close()


    def _populate_table(self, rows):
        table = self.trans_services_screen.inst_tableView_List_RegBusiness
        table.setRowCount(len(rows))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Name", "Date Requested", "Status"])
        # Set column widths
        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 150)

        self.transaction_rows = rows  # Store for later use in display panel

        for row_idx, row_data in enumerate(rows):
            full_name = f"{row_data[1]} {row_data[2]}"
            table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))  # ID
            table.setItem(row_idx, 1, QTableWidgetItem(full_name))  # Name
            table.setItem(row_idx, 2, QTableWidgetItem(row_data[3]))  # Date Requested
            table.setItem(row_idx, 3, QTableWidgetItem(row_data[4] or "N/A"))  # Status

    def load_transaction_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor

            cursor.execute("""
                SELECT 
                    TL.tl_id, -- 0
                    TL.tl_fname, -- 1
                    TL.tl_lname, -- 2
                    TO_CHAR(TL.tl_date_requested, 'FMMonth FMDD, YYYY') AS tl_date_requested_formatted, -- 3
                    TL.tl_status, -- 4 (no join needed)
                    TT.tt_type_name, -- 5
                    TL.tl_purpose, -- 6
                    TO_CHAR(TL.tl_date_encoded, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS tl_date_encoded_formatted, -- 7
                    SA.SYS_FNAME || ' ' || COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') || SA.SYS_LNAME AS ENCODED_BY, -- 8
                    TO_CHAR(TL.tl_last_updated, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS tl_last_updated_formatted, -- 9
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' ||
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                             SUA.SYS_LNAME
                    END AS LAST_UPDATED_BY_NAME --10
                FROM TRANSACTION_LOG TL
                LEFT JOIN TRANSACTION_TYPE TT ON TL.tt_id = TT.tt_id
                LEFT JOIN SYSTEM_ACCOUNT SA ON TL.ENCODED_BY_sys_id = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON TL.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID

                WHERE TL.tl_is_deleted = FALSE
                ORDER BY TL.tl_id DESC
                LIMIT 50;
            """)

            rows = cursor.fetchall()
            self.transaction_rows = rows

            table = self.trans_services_screen.inst_tableView_List_RegBusiness
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Name", "Date Requested", "Status"])

            # Set column widths
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 150)
            table.setColumnWidth(3, 150)

            # Populate table
            for row_idx, row_data in enumerate(rows):
                full_name = f"{row_data[1]} {row_data[2]}"
                table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))  # ID
                table.setItem(row_idx, 1, QTableWidgetItem(full_name))  # Name
                table.setItem(row_idx, 2, QTableWidgetItem(row_data[3]))  # Date Requested
                table.setItem(row_idx, 3, QTableWidgetItem(row_data[4] or "N/A"))  # Status

        except Exception as e:
            QMessageBox.critical(self.trans_services_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_transaction(self, row, column):

        table = self.trans_services_screen.inst_tableView_List_RegBusiness
        selected_item = table.item(row, 0)
        if not selected_item:
            return
        selected_id = selected_item.text()
        # Store selected transaction ID
        self.selected_transaction_id = selected_id


        for record in self.transaction_rows:
            if str(record[0]) == selected_id:
                self.trans_services_screen.trans_displayFirstName.setText(record[1] or "N/A")
                self.trans_services_screen.trans_displayLastName.setText(record[2] or "N/A")
                self.trans_services_screen.trans_displayDateRequested.setText(record[3] or "N/A")
                self.trans_services_screen.trans_displayStatus.setText(record[4] or "N/A")
                self.trans_services_screen.trans_displayTransactionType.setText(record[5] or "N/A")
                self.trans_services_screen.trans_displayPurpose.setText(record[6] or "N/A")
                self.trans_services_screen.display_DateEncoded.setText(record[7] or "N/A")
                self.trans_services_screen.display_EncodedBy.setText(record[8] or "System")
                self.trans_services_screen.display_DateUpdated.setText(record[9] or "N/A")
                self.trans_services_screen.display_UpdatedBy.setText(record[10] or "N/A")

                break

    def show_transaction_popup(self):
        print("-- Create Transaction Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Transactions/create_transaction.ui", self)
        self.popup.setWindowTitle("Mapro: Create New Transaction")
        self.popup.setFixedSize(self.popup.size())

        self.popup.register_buttonConfirmTransaction_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmTransaction_SaveForm.clicked.connect(self.validate_transaction_fields)

        self.popup.setWindowModality(Qt.ApplicationModal)
        self.load_transaction_types()
        self.popup.exec_()

    # FORM DATA HERE [SERVICES] -------------------------------------------------------------------------------
    def get_form_data(self):
        return {
            'fname': self.popup.register_ReqFirstName.text().strip(),
            'lname': self.popup.register_ReqLastName.text().strip(),
            'status': self.popup.register_comboBox_TransactionStatus.currentText().strip(),
            'purpose': self.popup.register_Purpose.toPlainText().strip(),
            'transaction_type': self.popup.register_comboBox_TransactionType.currentText().strip()
        }

    def confirm_and_save(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Transaction",
            "Are you sure you want to create this transaction?",
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
            req_fname = self.popup.register_ReqFirstName.text().strip()
            req_lname = self.popup.register_ReqLastName.text().strip()
            status = self.popup.register_comboBox_TransactionStatus.currentText().strip()
            purpose = self.popup.register_Purpose.toPlainText().strip()
            transaction_type = self.popup.register_comboBox_TransactionType.currentText().strip()

            # Validate required fields
            if not req_fname:
                raise Exception("Requester First Name is required")
            if not req_lname:
                raise Exception("Requester Last Name is required")
            if not transaction_type:
                raise Exception("Transaction Type is required")

            # Get transaction type ID
            cursor.execute("SELECT TT_ID FROM TRANSACTION_TYPE WHERE TT_TYPE_NAME = %s", (transaction_type,))
            tt_result = cursor.fetchone()
            if not tt_result:
                raise Exception(f"Transaction type '{transaction_type}' not found.")
            tt_id = tt_result[0]

            # Insert into TRANSACTION_LOG
            insert_query = """
            INSERT INTO TRANSACTION_LOG (
                TL_FNAME,
                TL_LNAME,
                TL_STATUS,
                TL_PURPOSE,
                TL_DATE_REQUESTED,
                TT_ID,
                ENCODED_BY_SYS_ID,
                LAST_UPDATED_BY_SYS_ID
            ) VALUES (
                %(fname)s,
                %(lname)s,
                %(status)s,
                %(purpose)s,
                NOW(),
                %(tt_id)s,
                %(encoded_by)s,
                %(last_updated_by)s
            ) RETURNING TL_ID;
            """

            encoded_by = self.sys_user_id
            last_updated_by = self.sys_user_id

            cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
            cursor.execute(insert_query, {
                'fname': req_fname,
                'lname': req_lname,
                'status': status,
                'purpose': purpose,
                'tt_id': tt_id,
                'encoded_by': encoded_by,
                'last_updated_by': last_updated_by
            })

            new_tl_id = cursor.fetchone()[0]
            connection.commit()

            QMessageBox.information(self.popup, "Success", f"Transaction successfully created! ID: {new_tl_id}")
            self.popup.close()
            self.load_transaction_data()  # Refresh the transaction list

        except Exception as e:
            if connection:
                connection.rollback()
            QMessageBox.critical(self.popup, "Database Error", str(e))
        finally:
            if db:
                db.close()


    def validate_transaction_fields(self):
        errors = []

        # Validate requestor first name
        if not self.popup.register_ReqFirstName.text().strip():
            errors.append("Requester firstname is required")
            self.popup.register_ReqFirstName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_ReqFirstName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate requestor last name
        if not self.popup.register_ReqLastName.text().strip():
            errors.append("Requester lastname is required")
            self.popup.register_ReqLastName.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_ReqLastName.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate request status
        if self.popup.register_comboBox_TransactionStatus.currentIndex() == -1:
            errors.append("Request Status is required")
            self.popup.register_comboBox_TransactionStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_comboBox_TransactionStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate transaction type
        if self.popup.register_comboBox_TransactionType.currentIndex() == -1:
            errors.append("transaction type is required")
            self.popup.register_comboBox_TransactionType.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_comboBox_TransactionType.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate transaction reason
        # if not self.popup.register_Reason.toPlainText().strip():
        #     errors.append("Request reason is required")
        #     self.popup.register_Reason.setStyleSheet(
        #         "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff;"
        #     )
        # else:
        #     self.popup.register_Reason.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff;"
        #     )

        # Validate transaction purpose
        if not self.popup.register_Purpose.toPlainText().strip():
            errors.append("Request purpose is required")
            self.popup.register_Purpose.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.register_Purpose.setStyleSheet(
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

    def reset_transaction_profile_display(self):
        # Transaction Info
        self.trans_services_screen.trans_displayFirstName.setText("N/A")
        self.trans_services_screen.trans_displayLastName.setText("N/A")
        self.trans_services_screen.trans_displayDateRequested.setText("N/A")
        self.trans_services_screen.trans_displayStatus.setText("N/A")
        self.trans_services_screen.trans_displayTransactionType.setText("N/A")
        self.trans_services_screen.trans_displayPurpose.setText("N/A")
        self.trans_services_screen.display_DateEncoded.setText("N/A")
        self.trans_services_screen.display_EncodedBy.setText("System")
        self.trans_services_screen.display_DateUpdated.setText("N/A")
        self.trans_services_screen.display_UpdatedBy.setText("N/A")

    def handle_remove_transaction(self):
        if not getattr(self, 'selected_transaction_id', None):
            QMessageBox.warning(self.trans_services_screen, "No Selection", "Please select a transaction to remove.")
            return

        trans_id = self.selected_transaction_id
        confirm = QMessageBox.question(
            self.trans_services_screen,
            "Confirm Deletion",
            f"Are you sure you want to delete transaction with ID {trans_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        try:
            db = Database()
            db.set_user_id(self.sys_user_id)  # Set user for auditing

            db.execute_with_user("""
                UPDATE transaction_log
                SET tl_is_deleted = TRUE
                WHERE tl_id = %s;
            """, (trans_id,))

            db.conn.commit()

            QMessageBox.information(self.trans_services_screen, "Success", f"Transaction {trans_id} has been deleted.")
            self.load_transaction_data()  # Refresh table
            self.reset_transaction_profile_display()  # Clear profile display

            if hasattr(self, 'selected_transaction_id'):
                delattr(self, 'selected_transaction_id')  # Clear selection

        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self.trans_services_screen, "Database Error",
                                 f"Failed to delete transaction: {str(e)}")
        finally:
            db.close()

    def load_transaction_types(self):
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT TT_ID, TT_TYPE_NAME FROM TRANSACTION_TYPE ORDER BY TT_TYPE_NAME ASC;")
            results = cursor.fetchall()
            combo = self.popup.register_comboBox_TransactionType
            combo.clear()
            for tt_id, tt_name in results:
                combo.addItem(tt_name, tt_id)
        except Exception as e:
            print(f"Failed to load transaction types: {e}")
        finally:
            db.close()



    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
        self.setWindowTitle("MaPro: Transactions")