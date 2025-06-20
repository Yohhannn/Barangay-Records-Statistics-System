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

        # if not form_data['house_number']:
        #     errors.append("House Number is required")
        if not form_data['sitio_id']:
            errors.append("Sitio is required")
            self.view.popup.register_household_comboBox_Sitio.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.view.popup.register_household_comboBox_Sitio.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        if not form_data['ownership_status']:
            errors.append("Ownership is required")
            self.view.popup.register_household_comboBox_OwnershipStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.view.popup.register_household_comboBox_OwnershipStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        if not form_data['home_address']:
            errors.append("Home Address is required")
            self.view.popup.register_household_homeAddress.setStyleSheet(
                        "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                    )
        else:
            self.view.popup.register_household_homeAddress.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        # if not form_data['interviewer_name']:
        #     errors.append("Interviewer Name is required")
        # if not form_data['reviewer_name']:
        #     errors.append("Reviewer Name is required")
        if not form_data['water_id']:
            errors.append("Water source is required")
            self.view.popup.register_household_comboBox_WaterSource.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.view.popup.register_household_comboBox_WaterSource.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        if not form_data['toilet_id']:
            errors.append("Toilet type is required")
            self.view.popup.register_household_comboBox_ToiletType.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.view.popup.register_household_comboBox_ToiletType.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        if errors:
            self.view.show_error_message(errors)
            # self.view.highlight_missing_fields(errors)
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
                    END AS LAST_UPDATED_BY_NAME, -- 13
                    COUNT(C.CTZ_ID) AS TOTAL_MEMBERS -- Total members from CITIZEN
                FROM HOUSEHOLD_INFO HH
                JOIN SITIO S ON HH.SITIO_ID = S.SITIO_ID
                LEFT JOIN TOILET_TYPE T ON HH.TOILET_ID = T.toil_id
                LEFT JOIN WATER_SOURCE W ON HH.WATER_ID = W.WATER_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON HH.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON HH.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                LEFT JOIN CITIZEN C ON HH.HH_ID = C.HH_ID AND C.CTZ_IS_DELETED = FALSE AND C.CTZ_IS_ALIVE = TRUE
                WHERE HH.HH_IS_DELETED = FALSE
                GROUP BY
                    HH.HH_ID,
                    HH.HH_HOUSE_NUMBER,
                    S.SITIO_NAME,
                    HH.HH_OWNERSHIP_STATUS,
                    HH.HH_HOME_GOOGLE_LINK,
                    T.TOIL_TYPE_NAME,
                    W.WATER_SOURCE_NAME,
                    HH.HH_INTERVIEWER_NAME,
                    HH.HH_DATE_VISIT,
                    HH.HH_DATE_ENCODED,
                    SA.SYS_FNAME,
                    SA.SYS_MNAME,
                    SA.SYS_LNAME,
                    HH.HH_REVIEWER_NAME,
                    SUA.SYS_FNAME,
                    SUA.SYS_MNAME,
                    SUA.SYS_LNAME,
                    HH.HH_LAST_UPDATED
                ORDER BY HH.HH_ID DESC
                LIMIT 20;
            """)
            rows = cursor.fetchall()
            self.household_rows = rows

            table = self.cp_household_screen.inst_tableView_List_RegHousehold
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Total Members", "Sitio", "Date Encoded"])

            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 200)
            table.setColumnWidth(3, 200)

            for row_idx, row_data in enumerate(rows):
                # col 1 now shows total members instead of household number
                for col_idx, value in enumerate([row_data[0], row_data[14], row_data[2], row_data[9]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.cp_household_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def display_family_members(self, hh_id):
        """
        Fetches and displays family members of the selected household,
        including their relationship names from the RELATIONSHIP_TYPE table.
        """
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor

            query = """
                SELECT 
                    C.CTZ_FIRST_NAME,
                    C.CTZ_LAST_NAME,
                    R.RTH_RELATIONSHIP_NAME
                FROM CITIZEN C
                JOIN RELATIONSHIP_TYPE R ON C.RTH_ID = R.RTH_ID
                WHERE C.HH_ID = %s AND C.CTZ_IS_DELETED = FALSE;
            """
            cursor.execute(query, (hh_id,))
            rows = cursor.fetchall()

            table = self.cp_household_screen.cp_tableView_List_DisplayFamilyMembers
            table.setRowCount(len(rows))
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["First Name", "Last Name", "Relationship"])
            table.setColumnWidth(0, 150)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 200)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
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
                self.cp_household_screen.cp_displayOwnershipStatus.setText(record[3] or "None")  # Ownership Status
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
                    label.setText("None")
                    label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
                self.cp_household_screen.cp_DisplayToiletType.setText(record[5] or "None")  # Toilet Type
                self.cp_household_screen.cp_displayWaterSource.setText(record[6] or "None")  # Water Source
                self.cp_household_screen.cp_displayInterviewedBy.setText(record[7] or "None")  # Interviewer
                self.cp_household_screen.cp_displayDateofVisit.setText(
                    record[8].strftime('%B %d, %Y') if record[8] else "None"
                )  # Date of Visit
                self.cp_household_screen.display_DateEncoded.setText(record[9] or "None")  # Date Encoded
                self.cp_household_screen.display_EncodedBy.setText(record[10] or "System")  # Encoded By
                self.cp_household_screen.display_DateUpdated.setText(record[11] or "None")  # Last Updated
                self.cp_household_screen.cp_displayReviewedBy.setText(record[12] or "None")
                self.cp_household_screen.display_UpdatedBy.setText(record[13] or "None")
                self.display_family_members(int(selected_id))
                # self.cp_household_screen.display_UpdatedBy.setText(record[12] or "System")  # Updated By

                break

    def save_household_data(self, form_data):
        sys_user_id = self.sys_user_id
        if not self.view.confirm_registration():
            return

        form_data['home_image_path'] = self.model.image_path

        if self.model.save_household_data(form_data, sys_user_id):
            self.view.show_success_message()
            self.view.popup.close()
            self.load_household_data()
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