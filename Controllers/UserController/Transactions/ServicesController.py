from PySide6.QtGui import QIcon, Qt
from database import Database

from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup


class ServiceController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role
        
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
        self.trans_services_screen.inst_BusinessName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.trans_services_screen.trans_Transact_button_create.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.trans_services_screen.trans_Transact_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.trans_services_screen.trans_Transact_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        self.trans_services_screen.transactionList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # REGISTER BUTTON
        self.trans_services_screen.trans_Transact_button_create.clicked.connect(self.show_transaction_popup)
        self.trans_services_screen.inst_tableView_List_RegBusiness.cellClicked.connect(self.handle_row_click_transaction)

        # Return Button
        self.trans_services_screen.btn_returnToTransactionPage.clicked.connect(self.goto_transactions_panel)

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
                LIMIT 20;
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
        popup = load_popup("Resources/UIs/PopUp/Screen_Transactions/create_transaction.ui", self)
        popup.setWindowTitle("Mapro: Create New Transaction")
        popup.setFixedSize(popup.size())

        popup.register_buttonConfirmTransaction_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "register_buttonConfirmTransaction_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Creation",
                    "Are you sure you want to create this transaction?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "Transaction successfully registered!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()


    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
        self.setWindowTitle("MaPro: Transactions")