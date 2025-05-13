from PyQt6.QtWidgets import QTableWidgetItem
from Controllers.BaseFileController import BaseFileController
from PySide6.QtGui import QIcon, Qt, QImage, QBrush
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton, \
    QTableWidgetItem
from Utils.util_popup import load_popup

from database import Database




class InfastructureController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
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
        self.inst_infrastructure_screen.inst_infra_button_register.clicked.connect(self.show_register_isfrastructure_popup)

    def load_data_infrastructure(self):
        try:
            connection = Database()
            cursor = connection.cursor

            # Modified query with LEFT JOINs and COALESCE for NULL values
            cursor.execute(""" 
                SELECT 
                    INF.INF_ID,
                    INF.INF_NAME,
                    INF.INF_ACCESS_TYPE,
                    INF.INF_DATE_ENCODED,
                    COALESCE(
                        CONCAT(IO.INFO_FNAME, ' ', 
                        COALESCE(NULLIF(LEFT(IO.INFO_MNAME, 1), '') || '. ', ''), 
                        IO.INFO_LNAME
                    ), 'No Owner') AS INFRASTRUCTURE_OWNER,
                    COALESCE(IT.INFT_TYPE_NAME, 'No Type') AS INFT_TYPE_NAME,
                    INF.INF_ADDRESS_DESCRIPTION,
                    COALESCE(S.SITIO_NAME, 'No Sitio') AS SITIO_NAME,
                    INF.INF_DESCRIPTION
                FROM INFRASTRUCTURE INF
                LEFT JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
                LEFT JOIN INFRASTRUCTURE_TYPE IT ON INF.INFT_ID = IT.INFT_ID
                LEFT JOIN SITIO S ON INF.SITIO_ID = S.SITIO_ID
                ORDER BY INF.INF_ID
            """)

            rows = cursor.fetchall()
            print(f"Number of rows fetched: {len(rows)}")  # Debug

            self.rows = rows

            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setRowCount(len(rows))
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setColumnCount(4)
            self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setHorizontalHeaderLabels(
                ["ID", "Infrastructure Name", "Public/Private", "Date Registered"]
            )

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[3]]):
                    item = QTableWidgetItem(str(value))
                    self.inst_infrastructure_screen.inst_tableView_List_RegInfra.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load infrastructure data: {str(e)}")

    def handle_row_click_infrastructure(self, row):
        selected_id = self.inst_infrastructure_screen.inst_tableView_List_RegInfra.item(row, 0).text()

        for record in self.rows:
            if str(record[0]) == selected_id:
                self.inst_infrastructure_screen.inst_displayInfraID.setText(str(record[0]))
                self.inst_infrastructure_screen.inst_displayInfraName.setText(record[1])
                self.inst_infrastructure_screen.inst_displayInfraOwnerName.setText(record[4])
                self.inst_infrastructure_screen.inst_displayInfraType.setText(record[5])
                self.inst_infrastructure_screen.inst_displayInfraAddress.setText(record[6])
                self.inst_infrastructure_screen.inst_displayInfraSitio.setText(record[7])
                self.inst_infrastructure_screen.inst_displayInfraPP.setText(record[2])
                self.inst_infrastructure_screen.inst_InfraDescription.setText(record[8])
                self.inst_infrastructure_screen.inst_displayInfraDateRegistered.setText(str(record[3]))
                break

    def show_register_isfrastructure_popup(self):
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
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "infrastructure Successfully Registered!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)
        self.setWindowTitle("MaPro: Institutions")