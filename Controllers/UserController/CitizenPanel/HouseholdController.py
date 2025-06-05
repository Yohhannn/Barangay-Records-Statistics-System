from PySide6.QtCore import QDate
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox

from Controllers.BaseFileController import BaseFileController
from Models.HouseholdModel import HouseholdModel
from Views.CitizenPanel.HouseholdView import HouseholdView
from database import Database

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class HouseholdController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.stack = stack
        self.model = HouseholdModel()
        self.view = HouseholdView(self)

        # Load UI
        self.cp_household_screen = self.load_ui("Resources/Uis/MainPages/CitizenPanelPages/cp_household.ui")
        self.view.setup_household_ui(self.cp_household_screen)
        self.center_on_screen()
        self.load_household_data()

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name

    def show_register_household_popup(self):
        print("-- Register New Household Popup")
        popup = self.view.show_register_household_popup(self)
        popup.exec_()

    def get_current_date(self):
        """Returns today's date as QDate"""
        return QDate.currentDate()

    def validate_date(self, date_string):
        """Validate that the date is not in the future"""
        selected_date = QDate.fromString(date_string, "yyyy-MM-dd")
        if selected_date > QDate.currentDate():
            return False
        return True

    def validate_fields(self):
        form_data = self.view.get_form_data()
        errors = []

        if not form_data['house_number']:
            errors.append("House Number is required")
        if not form_data['sitio_id']:
            errors.append("Sitio is required")
        if not form_data['interviewer_name']:
            errors.append("Interviewer Name is required")
        if not form_data['reviewer_name']:
            errors.append("Reviewer Name is required")
        if not form_data['water_id']:
            errors.append("Water source is required")
        if not form_data['toilet_id']:
            errors.append("Toilet type is required")
        if not form_data['date_of_visit']:
            errors.append("Date of visit cannot be in the future")

        if errors:
            self.view.show_error_message(errors)
            self.view.highlight_missing_fields(errors)
        else:
            self.save_household_data(form_data)

    def load_household_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
                SELECT 
                    HH.HH_ID, -- 0
                    HH.HH_HOUSE_NUMBER, -- 1
                    S.SITIO_NAME, -- 2
                    HH.HH_OWNERSHIP_STATUS, -- 3
                    HH.HH_HOME_GOOGLE_LINK, -- 4
                    T.TOIL_TYPE_NAME, -- 5
                    W.WATER_SOURCE_NAME, -- 6
                    HH.HH_INTERVIEWER_NAME, -- 7
                    HH.HH_DATE_VISIT, -- 8
                    TO_CHAR(HH.HH_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED_FORMATTED, -- 9
                    SA.SYS_FNAME || ' ' || COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') || SA.SYS_LNAME AS ENCODED_BY, -- 10
                    TO_CHAR(HH.HH_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED_FORMATTED, -- 11
                    HH.HH_REVIEWER_NAME, -- 12
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' ||
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                             SUA.SYS_LNAME
                    END AS LAST_UPDATED_BY_NAME --13
                 ---   SU.SYS_FNAME || ' ' || COALESCE(LEFT(SU.SYS_MNAME, 1) || '. ', '') || SU.SYS_LNAME AS UPDATED_BY -- 12
                FROM HOUSEHOLD_INFO HH
                JOIN SITIO S ON HH.SITIO_ID = S.SITIO_ID
                LEFT JOIN TOILET_TYPE T ON HH.TOILET_ID = T.toil_id  -- ⬅️ Fixed here
                LEFT JOIN WATER_SOURCE W ON HH.WATER_ID = W.WATER_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON HH.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                -- Join for LAST_UPDATED_BY
                LEFT JOIN SYSTEM_ACCOUNT SUA ON HH.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
            ---    LEFT JOIN SYSTEM_ACCOUNT SU ON HH.SYS_ID_UPDATED = SU.SYS_ID
                WHERE HH.HH_IS_DELETED = FALSE
                ORDER BY HH.HH_ID DESC
                LIMIT 20;
            """)
            rows = cursor.fetchall()
            self.household_rows = rows

            table = self.cp_household_screen.inst_tableView_List_RegHousehold
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Household No.", "Sitio", "Date Encoded"])

            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 200)
            table.setColumnWidth(3, 200)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[9]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.cp_household_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_household(self, row, column):
        table = self.cp_household_screen.inst_tableView_List_RegHousehold
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()

        for record in self.household_rows:
            if str(record[0]) == selected_id:
                self.cp_household_screen.cp_displayHouseholdNum.setText(str(record[1]))  # HH Number
                self.cp_household_screen.cp_displayHouseholdID.setText(str(record[0]))  # HH ID
                self.cp_household_screen.cp_displaySitio.setText(record[2])  # Sitio Name
                self.cp_household_screen.cp_displayOwnershipStatus.setText(record[3] or "N/A")  # Ownership Status
                from PySide6.QtCore import Qt
                from PySide6.QtWidgets import QLabel


                link = record[4]
                label: QLabel = self.cp_household_screen.cp_displayHomeLink

                if link:
                    label.setText(f'<a href="{link}">Google Link</a>')

                    # Combine flags properly
                    interaction_flags = Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.LinksAccessibleByMouse
                    label.setTextInteractionFlags(Qt.TextInteractionFlag(interaction_flags))

                    label.setOpenExternalLinks(True)
                    label.setStyleSheet("QLabel { color: blue; text-decoration: underline; }")
                else:
                    label.setText("N/A")
                    label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
                self.cp_household_screen.cp_DisplayToiletType.setText(record[5] or "N/A")  # Toilet Type
                self.cp_household_screen.cp_displayWaterSource.setText(record[6] or "N/A")  # Water Source
                self.cp_household_screen.cp_displayInterviewedBy.setText(record[7] or "N/A")  # Interviewer
                self.cp_household_screen.cp_displayDateofVisit.setText(
                    record[8].strftime('%B %d, %Y') if record[8] else "N/A"
                )  # Date of Visit
                self.cp_household_screen.display_DateEncoded.setText(record[9] or "N/A")  # Date Encoded
                self.cp_household_screen.display_EncodedBy.setText(record[10] or "System")  # Encoded By
                self.cp_household_screen.display_DateUpdated.setText(record[11] or "N/A")  # Last Updated
                self.cp_household_screen.cp_displayReviewedBy.setText(record[12] or "N/A")
                self.cp_household_screen.display_UpdatedBy.setText(record[13] or "N/A")
                # self.cp_household_screen.display_UpdatedBy.setText(record[12] or "System")  # Updated By

                break

    def save_household_data(self, form_data):
        if not self.view.confirm_registration():
            return

        form_data['home_image_path'] = self.model.image_path

        if self.model.save_household_data(form_data):
            self.view.show_success_message()
            self.view.popup.close()
        else:
            self.view.show_error_dialog("Database error occurred")

    def upload_image(self):
        file_path = self.view.get_file_path()
        if file_path:
            saved_path = self.model.save_image(file_path)
            self.view.show_image_preview(file_path)

    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

        # self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")