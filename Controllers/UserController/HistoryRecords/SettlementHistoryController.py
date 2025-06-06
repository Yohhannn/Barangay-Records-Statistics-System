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
        self.hist_settlement_history_screen.settlementhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_settlement_history_screen.histrec_settlementhistory_button_record.clicked.connect(self.show_settlement_history_popup)
        self.hist_settlement_history_screen.histrec_tableView_List_RecordSettlementHistory.cellClicked.connect(self.handle_row_click_settlement_history)

        # Return Button
        self.hist_settlement_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)


    def show_settlement_history_popup(self):
        print("-- Record Settlement History Popup")
        popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_settlement_history.ui", self)
        popup.setWindowTitle("Mapro: Record New Settlement History")
        popup.setFixedSize(popup.size())

        popup.record_buttonConfirmSettlementHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "record_buttonConfirmSettlementHistory_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Creation",
                    "Are you sure you want to record this?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "Settlement History Successfully Recorded!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    def load_settlement_history_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
                SELECT 
                    SL.SETT_ID,
                    C1.CTZ_ID AS COMPLAINEE_ID,
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
                ORDER BY SL.SETT_DATE_ENCODED DESC
                LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.settlement_history_rows = rows

            table = self.hist_settlement_history_screen.histrec_tableView_List_RecordSettlementHistory
            table.setRowCount(len(rows))
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Settlement ID", "Complainee Name", "Date Recorded"])

            table.setColumnWidth(0, 100)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 200)

            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate([row[0], row[2], row[7]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.hist_settlement_history_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_settlement_history(self, row, column):
        table = self.hist_settlement_history_screen.histrec_tableView_List_RecordSettlementHistory
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()

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

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)