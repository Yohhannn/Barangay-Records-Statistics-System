from PySide6.QtGui import QIcon, Qt
from database import Database

from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem, QLabel

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup


class ServicesBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_transaction_id = None
        self.user_role = user_role

        self.stack = stack
        self.trans_servicesbin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/BinServices/bin_services.ui")
        self.setup_services_ui()
        self.center_on_screen()
        self.load_transaction_data()

    def setup_services_ui(self):
        """Setup the Services Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Services")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set images and icons
        self.trans_servicesbin_screen.btn_returnToTrashBinPage.setIcon(
            QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.trans_servicesbin_screen.inst_Transaction_buttonSearch.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.trans_servicesbin_screen.trans_Transact_button_restore.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))

        self.trans_servicesbin_screen.inst_tableView_List_RegBusiness.cellClicked.connect(
            self.handle_row_click_transaction)


        # Return Button
        self.trans_servicesbin_screen.inst_Transaction_buttonSearch.clicked.connect(self.search_transaction_data)
        self.trans_servicesbin_screen.btn_returnToTrashBinPage.clicked.connect(self.goto_trashbin)
        self.trans_servicesbin_screen.trans_Transact_button_restore.clicked.connect(
            self.restore_selected_transaction)  # <-- CONNECTED HERE

    def restore_selected_transaction(self):
        if not self.selected_transaction_id:
            QMessageBox.warning(self.trans_servicesbin_screen, "No Selection",
                                "Please select a transaction to restore.")
            return

        confirm = QMessageBox.question(
            self.trans_servicesbin_screen,
            "Confirm Restore",
            f"Are you sure you want to restore transaction with ID: {self.selected_transaction_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            connection = None
            try:
                connection = Database()
                cursor = connection.cursor
                cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
                # Update TL_IS_DELETED to FALSE
                cursor.execute("""
                    UPDATE TRANSACTION_LOG
                    SET tl_is_deleted = FALSE
                    WHERE tl_id = %s
                """, (self.selected_transaction_id,))
                connection.commit()

                QMessageBox.information(self.trans_servicesbin_screen, "Success", "Transaction restored successfully.")

                # Reload the transaction data to reflect changes
                self.load_transaction_data()
                self.clear_display_fields()  # Optional: clear or reset display fields

            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self.trans_servicesbin_screen, "Database Error", str(e))
            finally:
                if connection:
                    connection.close()

    def clear_display_fields(self):
        screen = self.trans_servicesbin_screen
        display_widgets = [
            screen.trans_displayFirstName,
            screen.trans_displayLastName,
            screen.trans_displayDateRequested,
            screen.trans_displayStatus,
            screen.trans_displayTransactionType,
            screen.trans_displayPurpose,
            screen.display_DateEncoded,
            screen.display_EncodedBy,
            screen.display_DateUpdated,
            screen.display_UpdatedBy,
        ]
        for widget in display_widgets:
            if isinstance(widget, QLabel):
                widget.setText("N/A")


    def search_transaction_data(self):
        """Filter transaction data based on ID or Name."""
        search_term = self.trans_servicesbin_screen.trans_TransactionID_fieldSearch.text().strip()
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
                WHERE TL.tl_is_deleted = TRUE
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
            QMessageBox.critical(self.trans_servicesbin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()






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

                WHERE TL.tl_is_deleted = TRUE
                ORDER BY TL.tl_id DESC
                LIMIT 50;
            """)

            rows = cursor.fetchall()
            self.transaction_rows = rows

            table = self.trans_servicesbin_screen.inst_tableView_List_RegBusiness
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
            QMessageBox.critical(self.trans_servicesbin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_transaction(self, row, column):

        table = self.trans_servicesbin_screen.inst_tableView_List_RegBusiness
        selected_item = table.item(row, 0)
        if not selected_item:
            return
        selected_id = selected_item.text()
        # Store selected transaction ID
        self.selected_transaction_id = selected_id

        for record in self.transaction_rows:
            if str(record[0]) == selected_id:
                self.trans_servicesbin_screen.trans_displayFirstName.setText(record[1] or "N/A")
                self.trans_servicesbin_screen.trans_displayLastName.setText(record[2] or "N/A")
                self.trans_servicesbin_screen.trans_displayDateRequested.setText(record[3] or "N/A")
                self.trans_servicesbin_screen.trans_displayStatus.setText(record[4] or "N/A")
                self.trans_servicesbin_screen.trans_displayTransactionType.setText(record[5] or "N/A")
                self.trans_servicesbin_screen.trans_displayPurpose.setText(record[6] or "N/A")
                self.trans_servicesbin_screen.display_DateEncoded.setText(record[7] or "N/A")
                self.trans_servicesbin_screen.display_EncodedBy.setText(record[8] or "System")
                self.trans_servicesbin_screen.display_DateUpdated.setText(record[9] or "N/A")
                self.trans_servicesbin_screen.display_UpdatedBy.setText(record[10] or "N/A")

                break


    def goto_trashbin(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.AdminController.AdminBinController import AdminBinController
            self.adminbin_panel = AdminBinController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                     self.user_role, self.stack)
            self.stack.addWidget(self.adminbin_panel.trashbin_screen)

        self.stack.setCurrentWidget(self.adminbin_panel.trashbin_screen)

        # self.stack.setCurrentWidget(self.adminbin_panel.adminbin_panel_screen)
        self.setWindowTitle("MaPro: Admin Bin Panel")