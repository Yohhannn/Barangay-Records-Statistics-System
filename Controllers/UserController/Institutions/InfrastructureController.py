from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton, QButtonGroup, QRadioButton, QTableWidgetItem
from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from database import Database


class InfrastructureController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.selected_id = None
        self.stack = stack
        self.inst_infrastructure_screen = self.load_ui("Resources/UIs/MainPages/InstitutionPages/infrastructure.ui")
        self.setup_infrastructure_ui()
        self.center_on_screen()
        self.load_data_infrastructure()
        self.inst_infrastructure_screen.inst_tableView_List_RegInfra.cellClicked.connect(self.handle_row_click_infrastructure)

    def setup_infrastructure_ui(self):
        """Setup the Infrastructure Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Infrastructure")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set images and icons
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.inst_infrastructure_screen.inst_InfraName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.inst_infrastructure_screen.inst_infra_button_register.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.inst_infrastructure_screen.inst_infra_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.inst_infrastructure_screen.inst_infra_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        self.inst_infrastructure_screen.InfrastructureList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # Return Button
        self.inst_infrastructure_screen.btn_returnToInstitutionPage.clicked.connect(self.goto_institutions_panel)

        # REGISTER BUTTON
        self.inst_infrastructure_screen.inst_infra_button_register.clicked.connect(self.show_register_infrastructure_popup)

    def load_data_infrastructure(self):
        try:
            connection = Database()
            cursor = connection.cursor

            # Keep the original query to fetch all data (needed for row click handling)
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
                    INF.SYS_ID  
                FROM INFRASTRUCTURE INF
                LEFT JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
                LEFT JOIN INFRASTRUCTURE_TYPE IT ON INF.INFT_ID = IT.INFT_ID
                LEFT JOIN SITIO S ON INF.SITIO_ID = S.SITIO_ID
                LEFT JOIN SYSTEM_ACCOUNT SA ON INF.SYS_ID = SA.SYS_ID
                ORDER BY COALESCE(INF.INF_LAST_UPDATED, INF.INF_DATE_ENCODED) DESC
                LIMIT 20
            """)

            rows = cursor.fetchall()
            print(f"Number of rows fetched: {len(rows)}")  # Debug

            self.rows = rows

            # Update table view with only the 4 specified columns (now showing Owner instead of Access)
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setRowCount(len(rows))
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnCount(4)
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setHorizontalHeaderLabels(
                ["ID", "Name", "Owner", "Date Registered"]
            )

            # Set column widths
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(0, 50)  # ID
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(1, 150)  # Name
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(2,
                                                                                        150)  # Owner (wider for names)
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnWidth(3, 100)  # Date

            for row_idx, row_data in enumerate(rows):
                # Display columns in this order: ID, Name, Owner, Date Registered
                display_columns = [
                    row_data[0],  # INF_ID
                    row_data[1],  # INF_NAME
                    row_data[4],  # INFRASTRUCTURE_OWNER (was previously Access Type)
                    row_data[3]  # INF_DATE_ENCODED
                ]

                for col_idx, value in enumerate(display_columns):
                    item = QTableWidgetItem(str(value))
                    self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load infrastructure data: {str(e)}")
        finally:
            if 'connection' in locals():
                connection.close()


    def handle_row_click_infrastructure(self, row):
        self.selected_id = self.inst_infrastructure_screen.inst_tableView_List_RegInfra.item(row, 0).text()

        for record in self.rows:
            if str(record[0]) == self.selected_id:
                # Set basic information
                self.inst_infrastructure_screen.inst_displayInfraID.setText(str(record[0]))
                self.inst_infrastructure_screen.inst_displayInfraName.setText(record[1])
                self.inst_infrastructure_screen.inst_displayInfraOwnerName.setText(record[4])
                self.inst_infrastructure_screen.inst_displayInfraType.setText(record[5])
                self.inst_infrastructure_screen.inst_displayInfraAddress.setText(record[6])
                self.inst_infrastructure_screen.inst_displayInfraSitio.setText(record[7])
                self.inst_infrastructure_screen.inst_displayInfraPP.setText(record[2])
                self.inst_infrastructure_screen.inst_InfraDescription.setText(record[8])

                # Set encoded by information
                self.inst_infrastructure_screen.inst_display_EncodedBy.setText(record[9])
                self.inst_infrastructure_screen.inst_display_DateEncoded.setText(record[10])

                # Set last updated information
                self.inst_infrastructure_screen.inst_display_DateUpdated.setText(
                    record[11] if record[11] else "Not updated")

                # # Get and display who updated the record
                # updated_by_name = self.get_updater_name(record[12])
                # self.inst_infrastructure_screen.inst_display_UpdatedBy.setText(updated_by_name)

        print(self.selected_id)

    def show_register_infrastructure_popup(self):
        print("-- Register Infrastructure Popup")
        popup = load_popup("Resources/UIs/PopUp/Screen_Institutions/register_infrastructure.ui", self)
        popup.setWindowTitle("Mapro: Register New Infrastructure")
        popup.setFixedSize(popup.size())

        popup.register_buttonConfirmInfra_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        def setup_radio_button_groups_infrastructure():
            # Is Private or Public?
            radio_PP = QButtonGroup(popup)
            PP_Private = popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Private")
            PP_Public = popup.findChild(QRadioButton, "register_radioButton_labelInfraPP_Public")
            if PP_Private and PP_Public:
                radio_PP.addButton(PP_Private)
                radio_PP.addButton(PP_Public)

        setup_radio_button_groups_infrastructure()

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "register_buttonConfirmInfra_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Registration",
                    "Are you sure you want to register this infrastructure?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "Infrastructure Successfully Registered!")
                    popup.close()
                    self.load_data_infrastructure()  # Refresh the data

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.WindowModality.ApplicationModal)
        popup.show()

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")