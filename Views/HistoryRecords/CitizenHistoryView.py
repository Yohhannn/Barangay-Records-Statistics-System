from PySide6.QtGui import QPixmap, QIcon, Qt
import cv2
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QButtonGroup, QRadioButton, QStackedWidget
from Controllers.BaseFileController import BaseFileController
from Models.CitizenModel import CitizenModel
from Views.CitizenPanel.CitizenView import CitizenView
from Utils.util_popup import load_popup
from database import Database


class CitizenHistoryView:
    def __init__(self, controller):
        self.controller = controller

        self.popup = None

        self.hist_citizen_history_screen = None

    def show_citizen_history_popup(self):
        print("-- Record Citizen History Popup")
        self.popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_citizen_history.ui")
        self.popup.setWindowTitle("Mapro: Record New Citizen History")
        self.popup.setFixedSize(self.popup.size())

        self.popup.record_buttonConfirmCitizenHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.record_buttonConfirmCitizenHistory_SaveForm.clicked.connect(self.validate_citizen_hist_fields)
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.load_history_type()
        self.popup.exec_()


    def load_history_type(self):
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT hist_id, hist_type_name FROM HISTORY_TYPE ORDER BY hist_type_name ASC;")
            results = cursor.fetchall()
            combo = self.popup.record_comboBox_citizenhistory_type
            combo.clear()
            for hist_id, hist_type_name in results:
                combo.addItem(hist_type_name, hist_id)
        except Exception as e:
            print(f"Failed to load transaction types: {e}")
        finally:
            db.close()

    def validate_citizen_hist_fields(self):
        errors = []

        # Validate Citizen ID
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
                    SELECT CTZ_ID FROM CITIZEN 
                    WHERE CTZ_ID::TEXT = %s OR CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s
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

        # Validate Citizen History Type
        if self.popup.record_comboBox_citizenhistory_type.currentIndex() == -1:
            errors.append("Citizen history type is required")
            self.popup.record_comboBox_citizenhistory_type.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_comboBox_citizenhistory_type.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Citizen Record Description
        if not self.popup.record_citizenhistory_description.toPlainText().strip():
            errors.append("Citizen description is required")
            self.popup.record_citizenhistory_description.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_citizenhistory_description.setStyleSheet(
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
            "Are you sure you want to record this citizen history?",
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
            citizen_search = self.popup.record_citizenIDANDsearch.text().strip()
            hist_type_name = self.popup.record_comboBox_citizenhistory_type.currentText().strip()
            description = self.popup.record_citizenhistory_description.toPlainText().strip()

            # Validate required fields
            if not citizen_search:
                raise Exception("Citizen ID or Name is required")
            if not hist_type_name:
                raise Exception("History Type is required")
            if not description:
                raise Exception("Description is required")

            # Find CITIZEN by ID or name
            cursor.execute("""
                SELECT CTZ_ID FROM CITIZEN 
                WHERE CTZ_ID = %s OR CTZ_FIRST_NAME || ' ' || CTZ_LAST_NAME ILIKE %s
            """, (citizen_search, f"%{citizen_search}%"))

            ctz_result = cursor.fetchone()
            if not ctz_result:
                raise Exception(f"No citizen found with ID or name containing '{citizen_search}'")
            ctz_id = ctz_result[0]

            if not self.popup.record_citizenIDANDsearch.text().strip():
                errors.append("Info citizen ID is required")
                self.popup.record_citizenIDANDsearch.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            else:
                self.popup.record_citizenIDANDsearch.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )

            # Get HISTORY_TYPE ID
            cursor.execute("SELECT HIST_ID FROM HISTORY_TYPE WHERE HIST_TYPE_NAME = %s", (hist_type_name,))
            hist_result = cursor.fetchone()
            if not hist_result:
                raise Exception(f"History type '{hist_type_name}' not found.")
            hist_id = hist_result[0]

            # Insert into CITIZEN_HISTORY
            insert_query = """
            INSERT INTO CITIZEN_HISTORY (
                CIHI_DESCRIPTION,
                HIST_ID,
                CTZ_ID,
                ENCODED_BY_SYS_ID,
                LAST_UPDATED_BY_SYS_ID
            ) VALUES (
                %(description)s,
                %(hist_id)s,
                %(ctz_id)s,
                %(encoded_by)s,
                %(last_updated_by)s
            ) RETURNING CIHI_ID;
            """

            encoded_by = self.controller.sys_user_id
            last_updated_by = self.controller.sys_user_id

            cursor.execute(insert_query, {
                'description': description,
                'hist_id': hist_id,
                'ctz_id': ctz_id,
                'encoded_by': encoded_by,
                'last_updated_by': last_updated_by
            })

            new_cihi_id = cursor.fetchone()[0]
            connection.commit()

            QMessageBox.information(self.popup, "Success", f"Citizen History successfully recorded! ID: {new_cihi_id}")
            self.popup.close()
            self.controller.load_citizen_history_data()  # Refresh the list

        except Exception as e:
            if connection:
                connection.rollback()
            QMessageBox.critical(self.popup, "Database Error", str(e))
        finally:
            if db:
                db.close()



    def setup_citizen_history_ui(self, ui_screen):
        self.hist_citizen_history_screen = ui_screen

        """Setup the Citizen History Views layout."""
        ui_screen.setFixedSize(1350, 850)
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_citizen_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.hist_citizen_history_screen.histrec_HistoryID_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_record.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        # self.hist_citizen_history_screen.citizenhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_citizen_history_screen.histrec_citizenhistory_button_record.clicked.connect(self.show_citizen_history_popup)

        # Return Button
        self.hist_citizen_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.controller.goto_history_panel)
        self.hist_citizen_history_screen.histrec_HistoryID_buttonSearch.clicked.connect(
            self.controller.search_citizen_history_data)

        self.hist_citizen_history_screen.histrec_tableView_List_RecordCitizenHistory.cellClicked.connect(self.controller.handle_row_click_citizen_history)
