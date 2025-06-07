from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QTableWidgetItem

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class MedicalHistoryController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
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

        # Return Button
        self.hist_medical_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)

    def show_medical_history_popup(self):
        print("-- Record Medical History Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_medical_history.ui", self)
        self.popup.setWindowTitle("Mapro: Record New Medical History")
        self.popup.setFixedSize(self.popup.size())

        self.popup.record_buttonConfirmMedicalHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.record_buttonConfirmMedicalHistory_SaveForm.clicked.connect(self.validate_medical_hist_fields)
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

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
        if not self.popup.record_citizenIDANDsearch.text().strip():
            errors.append("Info citizen ID is required")
            self.popup.record_citizenIDANDsearch.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_citizenIDANDsearch.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

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
            "Confirm Record",
            "Are you sure you want to record this medical history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print("-- Form Submitted")
            QMessageBox.information(self.popup, "Success", "Medical History successfully recorded!")
            self.popup.close()
            self.load_medical_history_data()


    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)