from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QButtonGroup, QRadioButton, QTableWidgetItem, QLabel
from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class InfrastructureBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_infra_id = None
        self.user_role = user_role
        self.selected_id = None
        self.stack = stack
        self.inst_infrastructurebin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/BinInfrastructure/bin_infrastructure.ui")
        self.setup_infrastructure_ui()
        self.center_on_screen()
        self.load_data_infrastructure()
        self.inst_infrastructurebin_screen.inst_tableView_List_RegInfra.cellClicked.connect(self.handle_row_click_infrastructure)


    def setup_infrastructure_ui(self):
        """Setup the Infrastructure Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Infrastructure")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
        # Set images and icons
        self.inst_infrastructurebin_screen.btn_returnToTrashBinPage.setIcon(
            QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.inst_infrastructurebin_screen.inst_infra_button_restore.setIcon(
            QIcon('Resources/Icons/FuncIcons/icon_add.svg'))

        # Return Button
        # REGISTER BUTTON
        self.inst_infrastructurebin_screen.inst_InfraName_buttonSearch.clicked.connect(self.perform_infrastructure_search)
        self.inst_infrastructurebin_screen.btn_returnToTrashBinPage.clicked.connect(self.goto_trashbin)
        self.inst_infrastructurebin_screen.inst_infra_button_restore.clicked.connect(
            self.restore_selected_infrastructure)  








    def perform_infrastructure_search(self):
        search_text = self.inst_infrastructurebin_screen.inst_InfraName_fieldSearch.text().strip()
        if not search_text:
            self.load_data_infrastructure()
            return
        query = """
            SELECT 
                INF.INF_ID,
                INF.INF_NAME,
                IO.INFO_FNAME || ' ' || IO.INFO_LNAME AS INFRASTRUCTURE_OWNER,
                TO_CHAR(INF.INF_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_REGISTERED
            FROM INFRASTRUCTURE INF
            LEFT JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
            WHERE INF.INF_IS_DELETED = TRUE
              AND (
                  CAST(INF.INF_ID AS TEXT) ILIKE %s OR
                  INF.INF_NAME ILIKE %s OR
                  (IO.INFO_FNAME || ' ' || IO.INFO_LNAME) ILIKE %s
              )
            ORDER BY INF.INF_DATE_ENCODED DESC
            LIMIT 50;
        """
        try:
            connection = Database()
            cursor = connection.cursor
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()
            table = self.inst_infrastructurebin_screen.inst_tableView_List_RegInfra
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Name", "Owner", "Date Registered"])
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 200)
            table.setColumnWidth(2, 200)
            table.setColumnWidth(3, 200)
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self.inst_infrastructurebin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    def load_data_infrastructure(self):
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
                SELECT 
                    INF.INF_ID,
                    INF.INF_NAME,
                    INF.INF_ACCESS_TYPE,
                    TO_CHAR(INF.INF_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS INF_DATE_ENCODED,
                    CASE 
                        WHEN IO.INFO_FNAME IS NULL THEN 'No Owner'
                        ELSE CONCAT(
                            IO.INFO_FNAME, ' ', 
                            CASE WHEN IO.INFO_MNAME IS NOT NULL AND IO.INFO_MNAME != '' 
                                 THEN LEFT(IO.INFO_MNAME, 1) || '. ' 
                                 ELSE '' 
                            END,
                            IO.INFO_LNAME
                        )
                    END AS INFRASTRUCTURE_OWNER,
                    COALESCE(IT.INFT_TYPE_NAME, 'No Type') AS INFT_TYPE_NAME,
                    INF.INF_ADDRESS_DESCRIPTION,
                    COALESCE(S.SITIO_NAME, 'No Sitio') AS SITIO_NAME,
                    INF.INF_DESCRIPTION,
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
                    TO_CHAR(INF.INF_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED,
                    TO_CHAR(INF.INF_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS LAST_UPDATED,
                    INF.ENCODED_BY_SYS_ID,
                    CASE 
                        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
                        ELSE SUA.SYS_FNAME || ' ' ||
                             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
                             SUA.SYS_LNAME
                    END AS LAST_UPDATED_BY_NAME 
                FROM INFRASTRUCTURE INF
                LEFT JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
                LEFT JOIN INFRASTRUCTURE_TYPE IT ON INF.INFT_ID = IT.INFT_ID
                LEFT JOIN SITIO S ON INF.SITIO_ID = S.SITIO_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON INF.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
                LEFT JOIN SYSTEM_ACCOUNT SUA ON INF.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
                WHERE INF.INF_IS_DELETED = TRUE
                ORDER BY COALESCE(INF.INF_LAST_UPDATED, INF.INF_DATE_ENCODED) DESC
                LIMIT 50
            """)
            rows = cursor.fetchall()
            self.rows = rows
            table = self.inst_infrastructurebin_screen.inst_tableView_List_RegInfra
            table.setRowCount(len(rows))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["ID", "Name", "Owner", "Date Registered"])
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 150)
            table.setColumnWidth(3, 100)
            for row_idx, row_data in enumerate(rows):
                display_columns = [
                    row_data[0],  # INF_ID
                    row_data[1],  # INF_NAME
                    row_data[4],  # INFRASTRUCTURE_OWNER
                    row_data[3]   # INF_DATE_ENCODED
                ]
                for col_idx, value in enumerate(display_columns):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load infrastructure data: {str(e)}")
        finally:
            if connection:
                connection.close()

    def handle_row_click_infrastructure(self, row):
        self.selected_id = self.inst_infrastructurebin_screen.inst_tableView_List_RegInfra.item(row, 0).text()
        self.selected_infra_id = self.selected_id
        for record in self.rows:
            if str(record[0]) == self.selected_id:
                self.inst_infrastructurebin_screen.inst_displayInfraID.setText(str(record[0]))
                self.inst_infrastructurebin_screen.inst_displayInfraName.setText(record[1])
                self.inst_infrastructurebin_screen.inst_displayInfraOwnerName.setText(record[4])
                self.inst_infrastructurebin_screen.inst_displayInfraType.setText(record[5])
                self.inst_infrastructurebin_screen.inst_displayInfraAddress.setText(record[6])
                self.inst_infrastructurebin_screen.inst_displayInfraSitio.setText(record[7])
                self.inst_infrastructurebin_screen.inst_displayInfraPP.setText(record[2])
                self.inst_infrastructurebin_screen.inst_InfraDescription.setText(record[8])
                self.inst_infrastructurebin_screen.inst_display_EncodedBy.setText(record[9])
                self.inst_infrastructurebin_screen.inst_display_DateEncoded.setText(record[10])
                self.inst_infrastructurebin_screen.inst_display_UpdatedBy.setText(record[13])
                self.inst_infrastructurebin_screen.inst_display_DateUpdated.setText(
                    record[11] if record[11] else "Not updated")

    def restore_selected_infrastructure(self):
        if not self.selected_infra_id:
            QMessageBox.warning(self.inst_infrastructurebin_screen, "No Selection",
                                "Please select an infrastructure to restore.")
            return

        confirm = QMessageBox.question(
            self.inst_infrastructurebin_screen,
            "Confirm Restore",
            f"Are you sure you want to restore infrastructure with ID: {self.selected_infra_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            connection = None
            try:
                connection = Database()
                cursor = connection.cursor
                # Update INF_IS_DELETED to FALSE
                cursor.execute("""
                    UPDATE INFRASTRUCTURE
                    SET INF_IS_DELETED = FALSE
                    WHERE INF_ID = %s
                """, (self.selected_infra_id,))
                connection.commit()

                QMessageBox.information(self.inst_infrastructurebin_screen, "Success",
                                        "Infrastructure restored successfully.")

                # Reload the infrastructure data to reflect changes
                self.load_data_infrastructure()
                self.clear_display_fields()  # Optional: clear or reset display fields

            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self.inst_infrastructurebin_screen, "Database Error", str(e))
            finally:
                if connection:
                    connection.close()

    def clear_display_fields(self):
        screen = self.inst_infrastructurebin_screen
        display_widgets = [
            screen.inst_displayInfraID,
            screen.inst_displayInfraName,
            screen.inst_displayInfraOwnerName,
            screen.inst_displayInfraType,
            screen.inst_displayInfraAddress,
            screen.inst_displayInfraSitio,
            screen.inst_displayInfraPP,
            screen.inst_InfraDescription,
            screen.inst_display_EncodedBy,
            screen.inst_display_DateEncoded,
            screen.inst_display_UpdatedBy,
            screen.inst_display_DateUpdated,
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