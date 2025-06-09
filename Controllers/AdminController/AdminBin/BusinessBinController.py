from Controllers.BaseFileController import BaseFileController
from PySide6.QtGui import QIcon, Qt, QPixmap
from PySide6.QtWidgets import (QMessageBox, QPushButton, QLabel, QFileDialog,
                               QButtonGroup, QRadioButton, QTableWidgetItem)
from Utils.util_popup import load_popup
from database import Database


class BusinessBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_business_id = None
        self.user_role = user_role

        self.stack = stack
        self.inst_businessbin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/BinBusiness/bin_business.ui")
        self.setup_business_ui()
        self.center_on_screen()
        self.load_business_data()

    def perform_business_search(self):
        search_text = self.inst_businessbin_screen.inst_BusinessName_fieldSearch.text().strip()

        if not search_text:
            # If empty, reload all businesses
            self.load_business_data()
            return

        query = """
            SELECT 
                BI.BS_ID,
                BI.BS_NAME,
                BI.BS_FNAME || ' ' || BI.BS_LNAME AS BUSINESS_OWNER,
                TO_CHAR(BI.BS_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_REGISTERED,
                BT.BST_TYPE_NAME,
                S.SITIO_NAME
            FROM BUSINESS_INFO BI
            JOIN BUSINESS_TYPE BT ON BI.BST_ID = BT.BST_ID
            JOIN SITIO S ON BI.SITIO_ID = S.SITIO_ID
            WHERE BI.BS_IS_DELETED = TRUE
              AND (
                  CAST(BI.BS_ID AS TEXT) ILIKE %s OR
                  BI.BS_NAME ILIKE %s OR
                  (BI.BS_FNAME || ' ' || BI.BS_LNAME) ILIKE %s
              )
            ORDER BY BI.BS_ID ASC
            LIMIT 50;
        """

        try:
            db = Database()
            cursor = db.get_cursor()
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()

            table = self.inst_businessbin_screen.inst_tableView_List_RegBusiness
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Business Name", "Owner", "Date Registered"])
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 200)
            table.setColumnWidth(3, 200)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[3]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.inst_businessbin_screen, "Database Error", str(e))
        finally:
            if db:
                db.close()

    def setup_business_ui(self):
        """Setup the Business Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Business")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set images and icons
        self.inst_businessbin_screen.btn_returnToTrashBinPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.inst_businessbin_screen.inst_BusinessName_buttonSearch.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.inst_businessbin_screen.inst_business_button_recover.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))

        # Connect signals
        self.inst_businessbin_screen.inst_tableView_List_RegBusiness.cellClicked.connect(self.handle_row_click_business)
        self.inst_businessbin_screen.inst_BusinessName_buttonSearch.clicked.connect(self.perform_business_search)
        self.inst_businessbin_screen.btn_returnToTrashBinPage.clicked.connect(self.goto_trashbin)
        self.inst_businessbin_screen.inst_business_button_recover.clicked.connect(
            self.restore_selected_business)  # <-- CONNECTED HERE


    def load_business_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute(""" 
                SELECT 
                    BI.BS_ID,
                    BI.BS_NAME,
                    BI.BS_FNAME || ' ' || BI.BS_LNAME AS BUSINESS_OWNER,
                    TO_CHAR(BI.BS_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS BS_DATE_ENCODED,
                    BT.BST_TYPE_NAME,
                    BI.BS_STATUS,
                    BI.BS_ADDRESS,
                    BI.BS_IS_DTI,
                    S.SITIO_NAME,
                    BI.BS_DESCRIPTION,
                    CASE 
                        WHEN SA.SYS_FNAME IS NULL THEN 'System'
                        ELSE CONCAT(
                            SA.SYS_FNAME, ' ', 
                            CASE WHEN SA.SYS_MNAME IS NOT NULL AND SA.SYS_MNAME != '' 
                                 THEN LEFT(SA.SYS_MNAME, 1) || '. ' 
                                 ELSE '' 
                            END,
                            SA.SYS_LNAME
                        )
                    END AS ENCODED_BY,
                    TO_CHAR(BI.BS_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED_FORMATTED,
                    TO_CHAR(BI.BS_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS LAST_UPDATED,
                    BI.ENCODED_BY_SYS_ID,
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' ||
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                             SUA.SYS_LNAME
                    END AS LAST_UPDATED_BY_NAME
                FROM BUSINESS_INFO BI
                JOIN BUSINESS_TYPE BT ON BI.BST_ID = BT.BST_ID
                JOIN SITIO S ON BI.SITIO_ID = S.SITIO_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON BI.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON BI.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE BI.BS_IS_DELETED = TRUE
                ORDER BY BI.BS_DATE_ENCODED DESC
                LIMIT 50
           """)
            rows = cursor.fetchall()
            self.rows = rows
            # Set the row and column count for the QTableWidget
            table = self.inst_businessbin_screen.inst_tableView_List_RegBusiness
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Business Name", "Owner", "Date Registered"])
            # Set column widths
            table.setColumnWidth(0, 50)  # ID
            table.setColumnWidth(1, 150)  # Business Name
            table.setColumnWidth(2, 150)  # Owner
            table.setColumnWidth(3, 200)  # Date Registered (wider for formatted date)
            # Populate the QTableWidget with data
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[3]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self.inst_businessbin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def handle_row_click_business(self, row, column):
        table = self.inst_businessbin_screen.inst_tableView_List_RegBusiness
        selected_item = table.item(row, 0)
        if not selected_item:
            return
        selected_id = selected_item.text()
        for record in self.rows:
            if str(record[0]) == selected_id:
                self.inst_businessbin_screen.inst_displayBusinessID.setText(str(record[0]))
                # Store selected business ID
                self.selected_business_id = selected_id
                self.inst_businessbin_screen.inst_displayBusinessName.setText(record[1])
                self.inst_businessbin_screen.inst_displayBusinessOwnerName.setText(record[2])  # BS_FNAME + BS_LNAME
                self.inst_businessbin_screen.inst_display_DateEncoded.setText(str(record[3]))
                self.inst_businessbin_screen.inst_displayBusinessType.setText(record[4])
                self.inst_businessbin_screen.inst_displayBusinessStatus.setText(record[5])
                self.inst_businessbin_screen.inst_displayBusinessAddress.setText(record[6])
                self.inst_businessbin_screen.inst_displayBusinessAddress_Sitio.setText(record[8])
                self.inst_businessbin_screen.inst_BusinessDescription.setText(record[9])
                # Display encoded by and last updated information
                self.inst_businessbin_screen.inst_display_EncodedBy.setText(record[10])  # ENCODED_BY
                self.inst_businessbin_screen.inst_display_DateUpdated.setText(
                    record[12] if record[12] else record[11])  # LAST_UPDATED or DATE_ENCODED_FORMATTED
                self.inst_businessbin_screen.display_UpdatedBy.setText(record[14])
                break

    def restore_selected_business(self):
        if not self.selected_business_id:
            QMessageBox.warning(self.inst_businessbin_screen, "No Selection", "Please select a business to restore.")
            return

        confirm = QMessageBox.question(
            self.inst_businessbin_screen,
            "Confirm Restore",
            f"Are you sure you want to restore business with ID: {self.selected_business_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            connection = None
            try:
                connection = Database()
                cursor = connection.cursor
                # Update BS_IS_DELETED to FALSE
                cursor.execute("""
                    UPDATE BUSINESS_INFO
                    SET BS_IS_DELETED = FALSE
                    WHERE BS_ID = %s
                """, (self.selected_business_id,))
                connection.commit()

                QMessageBox.information(self.inst_businessbin_screen, "Success", "Business restored successfully.")

                # Reload the business data to reflect changes
                self.load_business_data()
                self.clear_display_fields()  # Optional: clear or reset display fields

            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self.inst_businessbin_screen, "Database Error", str(e))
            finally:
                if connection:
                    connection.close()

    def clear_display_fields(self):
        screen = self.inst_businessbin_screen
        display_widgets = [
            screen.inst_displayBusinessID,
            screen.inst_displayBusinessName,
            screen.inst_displayBusinessOwnerName,
            screen.inst_displayBusinessType,
            screen.inst_displayBusinessStatus,
            screen.inst_displayBusinessAddress,
            screen.inst_displayBusinessAddress_Sitio,
            screen.inst_BusinessDescription,
            screen.inst_display_EncodedBy,
            screen.inst_display_DateUpdated,
            screen.display_UpdatedBy,
            screen.inst_display_DateEncoded,
        ]
        for widget in display_widgets:
            if isinstance(widget, QLabel):
                widget.setText("None")


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