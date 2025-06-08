from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt, QModelIndex
from Controllers.BaseFileController import BaseFileController
from Models.AdminModels.AccountControlsModel import AdminControlsModel
from Views.Admin.AdminControlsView import AdminControlsView
from database import Database
import bcrypt

class AdminControlsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role
        self.stack = stack

        self.view = AdminControlsView(self)
        self.model = AdminControlsModel(sys_user_id=self.sys_user_id)
        self.admin_controls_screen = self.load_ui("Resources/UIs/AdminPages/AdminPanel/AdminControls/admincontrols.ui")

        self.view.setup_admin_controls_ui(self.admin_controls_screen)
        self.admin_controls_screen.setWindowTitle("Admin Panel - MaPro")

        self._refresh()
        # self.admin_controls_screen.adminpanel_tableView_List_Sitio.clicked.connect(self.handle_row_click_account)


    def _populate_table(self, table, headers, data):
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setForeground(Qt.black)
                if col_idx > 0:
                    item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def validate_fields(self):
        form_data = self.view.get_form_data()

        if not form_data['sitio_name']:
            self.view.show_error_dialog("Please fill out the following required fields:\n- Sitio Name")
            return

        # Continue saving
        self.save_sitio_data(form_data)


    def populate_sitio_table(self):
        try:
            result = self.model.get_sitio_names()
            if not result or not result['data']:
                return
            self.model.account_rows = result['data']
            self._populate_table(
                self.view.admin_controls_screen.adminpanel_tableView_List_Sitio,
                result['columns'],
                result['data']
            )
        except Exception as e:
            self.show_error_message("System Account Data Error", "Could not load system user accounts.")
            print(f"Error loading system user accounts: {e}")
    
    # def handle_row_click_account(self, index: QModelIndex = None):
    #     table = self.admin_controls_screen.adminpanel_tableView_List_StaffAccounts

    #     if index is None:
    #         if table.rowCount() == 0:
    #             return  
    #         index = table.model().index(0, 0)

    #     row = index.row()
    #     selected_index = table.model().index(row, 0) 
    #     selected_id = selected_index.data()

    #     if not selected_id:
    #         return

    #     selected_id = str(selected_id)
    #     print(f"[DEBUG] Clicked ID: {selected_id}")

    #     for record in self.model.account_rows:
    #         if str(record[0]) == selected_id:
    #             self.admin_controls_screen.ap_display_user_id.setText(str(record[0]))

    #             full_name_parts = record[1].replace(",", "").split()

    #             self.admin_controls_screen.ap_display_user_lname.setText(full_name_parts[0] if len(full_name_parts) > 0 else "")
    #             self.admin_controls_screen.ap_display_user_fname.setText(full_name_parts[1] if len(full_name_parts) > 1 else "")
    #             self.admin_controls_screen.ap_display_user_mname.setText(full_name_parts[2] if len(full_name_parts) > 2 else "")

    #             self.admin_controls_screen.ap_display_user_role.setText(record[2])  # SYS_ROLE
    #             self.admin_controls_screen.ap_display_user_status.setText("Active" if record[3] else "Inactive")  # SYS_IS_ACTIVE
    #             break


    def _refresh(self):
        try:
            self.populate_sitio_table()
            # self.handle_row_click_account()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Manage Accounts Error",
                "Error refreshing Admin Controls.",
                QMessageBox.Ok
            )
            print(f"Error refreshing Adimn Controls: {e}")


    def save_sitio_data(self, form_data):
        if not self.view.confirm_registration():
            return

        success = self.model.save_new_sitio_data(form_data)
        if success:
            self.view.show_success_message()
            self.view.popup.close()
            self.populate_sitio_table()
        else:
            self.view.show_error_dialog("Database error occurred")

    def show_register_account_popup(self):
        self.view.show_register_sitio_popup(self.view.admin_controls_screen)
    
    def goto_admin_panel(self):
        if not hasattr(self, 'admin_panel'):
            from Controllers.AdminController.AdminPanelController import AdminPanelController
            self.admin_panel = AdminPanelController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_panel.admin_panel_screen)
        self.stack.setCurrentWidget(self.admin_panel.admin_panel_screen)