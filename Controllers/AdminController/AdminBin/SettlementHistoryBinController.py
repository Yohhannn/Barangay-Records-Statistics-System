from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem, QLabel

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class SettlementHistoryBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role

        self.stack = stack
        self.hist_settlement_history_bin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/BinHistory/bin_settlement_history.ui")
        self.setup_settlement_history_ui()
        self.center_on_screen()
        self.load_settlement_history_data()

    def setup_settlement_history_ui(self):
        """Setup the Settlement History Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_settlement_history_bin_screen.btn_returnToTrashBinPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.hist_settlement_history_bin_screen.histrec_SettlementID_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.hist_settlement_history_bin_screen.histrec_settlementhistory_button_restore.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        # self.hist_settlement_history_bin_screen.settlementhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_settlement_history_bin_screen.histrec_tableView_List_RecordSettlementHistory.cellClicked.connect(self.handle_row_click_settlement_history)
        self.hist_settlement_history_bin_screen.btn_returnToTrashBinPage.clicked.connect(self.goto_trashbin)

        # Return Button
        self.hist_settlement_history_bin_screen.histrec_SettlementID_buttonSearch.clicked.connect(self.search_settlement_history_data)
        self.hist_settlement_history_bin_screen.histrec_settlementhistory_button_restore.clicked.connect(
            self.restore_selected_settlement)

    def restore_selected_settlement(self):
        if not getattr(self, "selected_settlement_id", None):
            QMessageBox.warning(self.hist_settlement_history_bin_screen, "No Selection",
                                "Please select a settlement record to restore.")
            return

        confirm = QMessageBox.question(
            self.hist_settlement_history_bin_screen,
            "Confirm Restore",
            f"Are you sure you want to restore settlement with ID: {self.selected_settlement_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            connection = None
            try:
                connection = Database()
                cursor = connection.cursor

                # Update SETT_IS_DELETED to FALSE
                cursor.execute("""
                    UPDATE SETTLEMENT_LOG
                    SET SETT_IS_DELETED = FALSE
                    WHERE SETT_ID = %s
                """, (self.selected_settlement_id,))

                connection.commit()

                QMessageBox.information(self.hist_settlement_history_bin_screen, "Success",
                                        "Settlement record restored successfully.")

                # Reload data and clear display
                self.load_settlement_history_data()
                self.clear_display_fields()

            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self.hist_settlement_history_bin_screen, "Database Error", str(e))
            finally:
                if connection:
                    connection.close()

    def clear_display_fields(self):
        screen = self.hist_settlement_history_bin_screen
        display_widgets = [
            screen.histrec_displaySettID,
            screen.histrec_displayComCtzID,
            screen.histrec_displayComplainantName,
            screen.histrec_displayComplaineeName,
            screen.histrec_displayHistoryComplaintDescription,
            screen.histrec_displayHistorySettlementDescription,
            screen.histrec_displayDateSettlement,
            screen.display_DateEncoded,
            screen.display_DateUpdated,
            screen.display_EncodedBy,
            screen.display_UpdatedBy,
        ]
        for widget in display_widgets:
            if isinstance(widget, QLabel):
                widget.setText("N/A")


    def search_settlement_history_data(self):
        search_term = self.hist_settlement_history_bin_screen.histrec_SettlementID_fieldSearch.text().strip()

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
                WHERE SL.SETT_IS_DELETED = TRUE AND CAST(SL.SETT_ID AS TEXT) ILIKE %s OR
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
            QMessageBox.critical(self.hist_settlement_history_bin_screen, "Database Error", str(e))
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
                WHERE SL.SETT_IS_DELETED = TRUE
                ORDER BY SL.SETT_DATE_ENCODED DESC
                LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.settlement_history_rows = rows

            table = self.hist_settlement_history_bin_screen.histrec_tableView_List_RecordSettlementHistory
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
            QMessageBox.critical(self.hist_settlement_history_bin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()



    def handle_row_click_settlement_history(self, row, column):
        table = self.hist_settlement_history_bin_screen.histrec_tableView_List_RecordSettlementHistory
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()
        # Store selected settlement ID
        self.selected_settlement_id = selected_id

        for record in self.settlement_history_rows:
            if str(record[0]) == selected_id:
                self.hist_settlement_history_bin_screen.histrec_displaySettID.setText(str(record[0]))
                self.hist_settlement_history_bin_screen.histrec_displayComCtzID.setText(str(record[1]))
                self.hist_settlement_history_bin_screen.histrec_displayComplainantName.setText(record[3])
                self.hist_settlement_history_bin_screen.histrec_displayComplaineeName.setText(record[2])
                self.hist_settlement_history_bin_screen.histrec_displayHistoryComplaintDescription.setText(record[4])
                self.hist_settlement_history_bin_screen.histrec_displayHistorySettlementDescription.setText(record[5])
                self.hist_settlement_history_bin_screen.histrec_displayDateSettlement.setText(record[6])
                self.hist_settlement_history_bin_screen.display_DateEncoded.setText(record[7])
                self.hist_settlement_history_bin_screen.display_DateUpdated.setText(record[8])
                self.hist_settlement_history_bin_screen.display_EncodedBy.setText(record[9])
                self.hist_settlement_history_bin_screen.display_UpdatedBy.setText(record[10])
                break

    # FORM DATA HERE [SETTLEMENT HISTORY] -------------------------------------------------------------------------------



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