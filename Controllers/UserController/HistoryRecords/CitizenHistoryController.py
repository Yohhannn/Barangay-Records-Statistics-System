from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem

from Controllers.BaseFileController import BaseFileController
from Models.HistoryModel import HistoryModel
from Utils.util_popup import load_popup
from Views.HistoryRecords.CitizenHistoryView import CitizenHistoryView
from database import Database


class CitizenHistoryController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role


        self.stack = stack
        self.model = HistoryModel()
        self.view = CitizenHistoryView(self)


        self.hist_citizen_history_screen = self.load_ui("Resources/UIs/MainPages/HistoryRecordPages/citizen_history.ui")
        self.view.setup_citizen_history_ui(self.hist_citizen_history_screen)
        # self.view.setup_history_ui(self.hist_citizen_history_screen)
        self.center_on_screen()
        self.load_citizen_history_data()

        self.popup = None

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name


    def show_citizen_history_initialize(self):
        pass

    def load_citizen_history_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
                SELECT 
                    H.CIHI_ID,
                    C.CTZ_FIRST_NAME,
                    C.CTZ_LAST_NAME,
                    H.CIHI_DESCRIPTION,
                    TO_CHAR(H.CIHI_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_RECORDED,
                    C.CTZ_ID,
                    TO_CHAR(H.CIHI_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(H.CIHI_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED,
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
                FROM CITIZEN_HISTORY H
                JOIN CITIZEN C ON H.CTZ_ID = C.CTZ_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON H.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON H.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE H.CIHI_IS_DELETED = FALSE
                ORDER BY H.CIHI_DATE_ENCODED DESC
                LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.history_rows = rows

            table = self.hist_citizen_history_screen.histrec_tableView_List_RecordCitizenHistory
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["History ID", "Citizen Name", "History Type", "Date Recorded"])

            table.setColumnWidth(0, 100)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 250)
            table.setColumnWidth(3, 200)

            for row_idx, row in enumerate(rows):
                full_name = f"{row[1]} {row[2]}"
                for col_idx, value in enumerate([row[0], full_name, row[3], row[4]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.hist_citizen_history_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def search_citizen_history_data(self):
        search_term = self.hist_citizen_history_screen.histrec_HistoryID_fieldSearch.text().strip()


        if not search_term:
            self.load_citizen_history_data()
            return

        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            query = """
                SELECT 
                    H.CIHI_ID,
                    C.CTZ_FIRST_NAME,
                    C.CTZ_LAST_NAME,
                    H.CIHI_DESCRIPTION,
                    TO_CHAR(H.CIHI_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_RECORDED,
                    C.CTZ_ID,
                    TO_CHAR(H.CIHI_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(H.CIHI_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED,
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
                FROM CITIZEN_HISTORY H
                JOIN CITIZEN C ON H.CTZ_ID = C.CTZ_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON H.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON H.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE H.CIHI_IS_DELETED = FALSE AND CAST(H.CIHI_ID AS TEXT) ILIKE %s OR
                      C.CTZ_FIRST_NAME ILIKE %s OR
                      C.CTZ_LAST_NAME ILIKE %s OR
                      H.CIHI_DESCRIPTION ILIKE %s
                ORDER BY H.CIHI_DATE_ENCODED DESC
                LIMIT 50;
            """
            search_param = f"%{search_term}%"
            cursor.execute(query, (search_param, search_param, search_param, search_param))
            rows = cursor.fetchall()
            self._populate_citizen_history_table(rows)

        except Exception as e:
            QMessageBox.critical(self.hist_citizen_history_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def _populate_citizen_history_table(self, rows):
        table = self.hist_citizen_history_screen.histrec_tableView_List_RecordCitizenHistory
        table.setRowCount(len(rows))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["History ID", "Citizen Name", "History Type", "Date Recorded"])

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 250)
        table.setColumnWidth(3, 200)

        self.history_rows = rows  # Store for use in display panel

        for row_idx, row in enumerate(rows):
            full_name = f"{row[1]} {row[2]}"
            table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))  # History ID
            table.setItem(row_idx, 1, QTableWidgetItem(full_name))  # Citizen Name
            table.setItem(row_idx, 2, QTableWidgetItem(row[3]))  # History Type
            table.setItem(row_idx, 3, QTableWidgetItem(row[4] or "N/A"))  # Date Recorded

    def handle_row_click_citizen_history(self, row, column):
        table = self.hist_citizen_history_screen.histrec_tableView_List_RecordCitizenHistory
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()

        for record in self.history_rows:
            if str(record[0]) == selected_id:
                self.hist_citizen_history_screen.histrec_displayHistoryID.setText(str(record[0]))
                self.hist_citizen_history_screen.histrec_displayCitizenID.setText(str(record[5]))
                self.hist_citizen_history_screen.histrec_displayCitizenHistFirstName.setText(record[1])
                self.hist_citizen_history_screen.histrec_displayCitizenHistLastName.setText(record[2])
                self.hist_citizen_history_screen.histrec_displayHistoryType.setText(record[3])
                self.hist_citizen_history_screen.histrec_displayHistoryDescription.setText(record[3])
                self.hist_citizen_history_screen.display_DateEncoded.setText(record[6])
                self.hist_citizen_history_screen.display_DateUpdated.setText(record[7])
                self.hist_citizen_history_screen.display_EncodedBy.setText(record[8])
                self.hist_citizen_history_screen.display_UpdatedBy.setText(record[9])
                break

    # FORM DATA HERE [CITIZEN HISTORY] -------------------------------------------------------------------------------
    def get_form_data(self):
        return {
            'citizen_search': self.popup.record_citizenIDANDsearch.text().strip(),
            'hist_type': self.popup.record_comboBox_citizenhistory_type.currentText().strip(),
            'description': self.popup.record_citizenhistory_description.toPlainText().strip()
        }

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)