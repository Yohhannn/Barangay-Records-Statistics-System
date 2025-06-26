from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem, QLabel

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class MedicalHistoryBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_medical_history_id = None
        self.user_role = user_role

        self.stack = stack
        self.hist_medical_history_bin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/BinHistory/bin_medical_history.ui")
        self.setup_medical_history_ui()
        self.center_on_screen()
        self.load_medical_history_data()

    def setup_medical_history_ui(self):
        """Setup the Medical History Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_medical_history_bin_screen.btn_returnToTrashBinPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.hist_medical_history_bin_screen.histrecMedHistoryID_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.hist_medical_history_bin_screen.histrec_medicalhistory_button_restore.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        # self.hist_medical_history_bin_screen.medicalhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_medical_history_bin_screen.histrec_tableView_List_RecordMedicalHistory.cellClicked.connect(self.handle_row_click_medical_history)
        # Return Button

        self.hist_medical_history_bin_screen.btn_returnToTrashBinPage.clicked.connect(self.goto_trashbin)
        self.hist_medical_history_bin_screen.histrecMedHistoryID_buttonSearch.clicked.connect(

            self.search_medical_history_data)
        self.hist_medical_history_bin_screen.histrec_medicalhistory_button_restore.clicked.connect(
            self.restore_selected_medical_history)


    def restore_selected_medical_history(self):
        if not self.selected_medical_history_id:
            QMessageBox.warning(self.hist_medical_history_bin_screen, "No Selection",
                                "Please select a medical history record to restore.")
            return

        confirm = QMessageBox.question(
            self.hist_medical_history_bin_screen,
            "Confirm Restore",
            f"Are you sure you want to restore medical history record with ID: {self.selected_medical_history_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            connection = None
            try:
                connection = Database()
                cursor = connection.cursor

                # Update MH_IS_DELETED to FALSE
                cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
                cursor.execute("""
                    UPDATE MEDICAL_HISTORY
                    SET MH_IS_DELETED = FALSE
                    WHERE MH_ID = %s
                """, (self.selected_medical_history_id,))

                connection.commit()

                QMessageBox.information(self.hist_medical_history_bin_screen, "Success",
                                        "Medical history record restored successfully.")

                # Reload data and clear display
                self.load_medical_history_data()
                self.clear_display_fields()

            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self.hist_medical_history_bin_screen, "Database Error", str(e))
            finally:
                if connection:
                    connection.close()

    def clear_display_fields(self):
        screen = self.hist_medical_history_bin_screen
        display_widgets = [
            screen.histrec_displayHistoryID,
            screen.histrec_displayCitizenID,
            screen.histrec_displayCitizenHistFirstName,
            screen.histrec_displayCitizenHistLastName,
            screen.histrec_displayMedicalHistoryType,
            screen.histrec_displayHistoryDescription,
            screen.display_DateEncoded,
            screen.display_DateUpdated,
            screen.display_EncodedBy,
            screen.display_UpdatedBy,
        ]
        for widget in display_widgets:
            if isinstance(widget, QLabel):
                widget.setText("N/A")

    def search_medical_history_data(self):
        search_term = self.hist_medical_history_bin_screen.histrec_HistoryID_fieldSearch.text().strip()

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
                WHERE MH.MH_IS_DELETED = TRUE AND CAST(MH.MH_ID AS TEXT) ILIKE %s OR
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
            QMessageBox.critical(self.hist_medical_history_bin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()
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
                WHERE MH.MH_IS_DELETED = TRUE
                ORDER BY MH.MH_DATE_ENCODED DESC
                LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.medical_history_rows = rows

            table = self.hist_medical_history_bin_screen.histrec_tableView_List_RecordMedicalHistory
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
            QMessageBox.critical(self.hist_medical_history_bin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_medical_history(self, row, column):
        table = self.hist_medical_history_bin_screen.histrec_tableView_List_RecordMedicalHistory
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()

        # Store selected medical history ID
        self.selected_medical_history_id = selected_id

        for record in self.medical_history_rows:
            if str(record[0]) == selected_id:
                self.hist_medical_history_bin_screen.histrec_displayHistoryID.setText(str(record[0]))
                self.hist_medical_history_bin_screen.histrec_displayCitizenID.setText(str(record[6]))
                self.hist_medical_history_bin_screen.histrec_displayCitizenHistFirstName.setText(record[1])
                self.hist_medical_history_bin_screen.histrec_displayCitizenHistLastName.setText(record[2])
                self.hist_medical_history_bin_screen.histrec_displayMedicalHistoryType.setText(record[3])
                self.hist_medical_history_bin_screen.histrec_displayHistoryDescription.setText(record[4])
                self.hist_medical_history_bin_screen.display_DateEncoded.setText(record[7])
                self.hist_medical_history_bin_screen.display_DateUpdated.setText(record[8])
                self.hist_medical_history_bin_screen.display_EncodedBy.setText(record[9])
                self.hist_medical_history_bin_screen.display_UpdatedBy.setText(record[10])
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