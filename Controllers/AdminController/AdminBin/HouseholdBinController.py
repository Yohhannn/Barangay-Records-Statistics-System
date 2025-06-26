from datetime import date

import cv2
from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QMessageBox, QPushButton, QLabel, QFileDialog,
                               QButtonGroup, QRadioButton, QTableWidgetItem)
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QButtonGroup, QRadioButton, QStackedWidget
from Controllers.BaseFileController import BaseFileController
from Models.CitizenModel import CitizenModel
from Views.CitizenPanel.CitizenView import CitizenView
from database import Database


class HouseholdBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_household_id = None
        self.stack = stack

        self.user_role = user_role

        # Load UI
        self.cp_householdbin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/BinHousehold/bin_cp_household.ui")
        self.setup_household_ui(self.cp_householdbin_screen)
        self.center_on_screen()
        self.load_household_data()

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name

    def setup_household_ui(self, ui_screen):
        self.cp_householdbin_screen = ui_screen
        ui_screen.cp_household_button_restore.clicked.connect(self.restore_selected_household)
        ui_screen.setWindowTitle("MaPro: Household")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set icons
        ui_screen.btn_returnToTrashBinPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        ui_screen.cp_HouseholdName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        ui_screen.cp_household_button_restore.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        # ui_screen.householdList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # Connect buttons
        ui_screen.btn_returnToTrashBinPage.clicked.connect(self.goto_trashbin)

        ui_screen.inst_tableView_List_RegHousehold.cellClicked.connect(self.handle_row_click_household)

        ui_screen.cp_HouseholdName_buttonSearch.clicked.connect(self.perform_household_search)

    def perform_household_search(self):
        search_text = self.cp_householdbin_screen.cp_HouseholdName_fieldSearch.text().strip()

        if not search_text:
            # If empty, reload all households
            self.load_household_data()
            return

        query = """
            SELECT 
                HH.HH_ID,
                HH.HH_HOUSE_NUMBER,
                S.SITIO_NAME,
                HH.HH_OWNERSHIP_STATUS,
                HH.HH_HOME_GOOGLE_LINK,
                T.TOIL_TYPE_NAME,
                W.WATER_SOURCE_NAME,
                HH.HH_INTERVIEWER_NAME,
                HH.HH_DATE_VISIT,
                TO_CHAR(HH.HH_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED_FORMATTED,
                SA.SYS_FNAME || ' ' || COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') || SA.SYS_LNAME AS ENCODED_BY,
                TO_CHAR(HH.HH_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED_FORMATTED,
                HH.HH_REVIEWER_NAME,
                CASE 
                    WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                    ELSE SUA.SYS_FNAME || ' ' ||
                         COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                         SUA.SYS_LNAME
                END AS LAST_UPDATED_BY_NAME,
                COUNT(C.CTZ_ID) AS TOTAL_MEMBERS
            FROM HOUSEHOLD_INFO HH
            JOIN SITIO S ON HH.SITIO_ID = S.SITIO_ID
            LEFT JOIN TOILET_TYPE T ON HH.TOILET_ID = T.toil_id
            LEFT JOIN WATER_SOURCE W ON HH.WATER_ID = W.WATER_ID
            LEFT JOIN SYSTEM_ACCOUNT SA ON HH.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
            LEFT JOIN SYSTEM_ACCOUNT SUA ON HH.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
            LEFT JOIN CITIZEN C ON HH.HH_ID = C.HH_ID AND C.CTZ_IS_DELETED = FALSE AND C.CTZ_IS_ALIVE = TRUE
            WHERE HH.HH_IS_DELETED = TRUE
              AND CAST(HH.HH_ID AS TEXT) ILIKE %s
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
            ORDER BY HH.HH_ID ASC
            LIMIT 50;
        """

        try:
            db = Database()
            cursor = db.get_cursor()
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern,))
            rows = cursor.fetchall()

            table = self.cp_householdbin_screen.inst_tableView_List_RegHousehold
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Total Members", "Sitio", "Date Encoded"])
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 200)
            table.setColumnWidth(3, 200)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[14], row_data[2], row_data[9]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.cp_householdbin_screen, "Database Error", str(e))
        finally:
            if db:
                db.close()

    def restore_selected_household(self):
        if not self.selected_household_id:
            QMessageBox.warning(self.cp_householdbin_screen, "No Selection", "Please select a household to restore.")
            return

        confirm = QMessageBox.question(
            self.cp_householdbin_screen,
            "Confirm Restore",
            f"Are you sure you want to restore household with ID: {self.selected_household_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            connection = None
            try:
                connection = Database()
                cursor = connection.cursor
                # Update HH_IS_DELETED to FALSE
                cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
                cursor.execute("""
                    UPDATE HOUSEHOLD_INFO
                    SET HH_IS_DELETED = FALSE
                    WHERE HH_ID = %s
                """, (self.selected_household_id,))
                connection.commit()

                QMessageBox.information(self.cp_householdbin_screen, "Success", "Household restored successfully.")

                # Reload the household data to reflect changes
                self.load_household_data()
                self.clear_display_fields()  # Optional: clear profile display after restore

            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self.cp_householdbin_screen, "Database Error", str(e))
            finally:
                if connection:
                    connection.close()

    def clear_display_fields(self):
        screen = self.cp_householdbin_screen
        display_widgets = [
            screen.cp_displayHouseholdID,
            screen.cp_displayHouseholdNum,
            screen.cp_displaySitio,
            screen.cp_displayOwnershipStatus,
            screen.cp_DisplayToiletType,
            screen.cp_displayWaterSource,
            screen.cp_displayInterviewedBy,
            screen.cp_displayDateofVisit,
            screen.display_DateEncoded,
            screen.display_EncodedBy,
            screen.display_DateUpdated,
            screen.display_UpdatedBy,
            screen.cp_displayReviewedBy,
            screen.cp_displayHomeLink,
        ]
        for widget in display_widgets:
            if isinstance(widget, QLabel):
                widget.setText("N/A")

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
                WHERE HH.HH_IS_DELETED = TRUE
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
                LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.household_rows = rows

            table = self.cp_householdbin_screen.inst_tableView_List_RegHousehold
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
            QMessageBox.critical(self.cp_householdbin_screen, "Database Error", str(e))
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

            table = self.cp_householdbin_screen.cp_tableView_List_DisplayFamilyMembers
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
            QMessageBox.critical(self.cp_householdbin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_household(self, row, column):
        table = self.cp_householdbin_screen.inst_tableView_List_RegHousehold
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()

        for record in self.household_rows:
            if str(record[0]) == selected_id:
                self.cp_householdbin_screen.cp_displayHouseholdNum.setText(str(record[1]))  # HH Number
                self.cp_householdbin_screen.cp_displayHouseholdID.setText(str(record[0]))  # HH ID
                self.cp_householdbin_screen.cp_displaySitio.setText(record[2])  # Sitio Name
                self.cp_householdbin_screen.cp_displayOwnershipStatus.setText(record[3] or "None")  # Ownership Status
                from PySide6.QtCore import Qt
                from PySide6.QtWidgets import QLabel

                link = record[4]
                label: QLabel = self.cp_householdbin_screen.cp_displayHomeLink

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
                self.cp_householdbin_screen.cp_DisplayToiletType.setText(record[5] or "None")  # Toilet Type
                self.cp_householdbin_screen.cp_displayWaterSource.setText(record[6] or "None")  # Water Source
                self.cp_householdbin_screen.cp_displayInterviewedBy.setText(record[7] or "None")  # Interviewer
                self.cp_householdbin_screen.cp_displayDateofVisit.setText(
                    record[8].strftime('%B %d, %Y') if record[8] else "None"
                )  # Date of Visit
                self.cp_householdbin_screen.display_DateEncoded.setText(record[9] or "None")  # Date Encoded
                self.cp_householdbin_screen.display_EncodedBy.setText(record[10] or "System")  # Encoded By
                self.cp_householdbin_screen.display_DateUpdated.setText(record[11] or "None")  # Last Updated
                self.cp_householdbin_screen.cp_displayReviewedBy.setText(record[12] or "None")
                self.cp_householdbin_screen.display_UpdatedBy.setText(record[13] or "None")
                # Store selected household ID
                self.selected_household_id = selected_id
                self.display_family_members(int(selected_id))
                # self.cp_householdbin_screen.display_UpdatedBy.setText(record[12] or "System")  # Updated By

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