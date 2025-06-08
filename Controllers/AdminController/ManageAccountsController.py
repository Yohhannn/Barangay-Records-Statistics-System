from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt, QModelIndex
from Controllers.BaseFileController import BaseFileController
from Models.AdminModels.ManageAccountsModel import ManageAccountsModel
from Views.Admin.ManageAccountsView import ManageAccountsView
from database import Database
import bcrypt

class ManageAccountsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role
        self.stack = stack

        self.view = ManageAccountsView(self)
        self.model = ManageAccountsModel(sys_user_id=self.sys_user_id)
        self.admin_manage_accounts_screen = self.load_ui("Resources/UIs/AdminPages/AdminPanel/ManageAccounts/manageaccounts.ui")

        self.view.setup_manage_accounts_ui(self.admin_manage_accounts_screen)
        self.admin_manage_accounts_screen.setWindowTitle("Admin Panel - MaPro")

        self._refresh()
        self.admin_manage_accounts_screen.adminpanel_tableView_List_StaffAccounts.clicked.connect(self.handle_row_click_account)
    
        # self.set_current_user_id()
    
    # def set_current_user_id(self):
    #     """Set the current user ID for the dashboard."""
    #     try:
    #         connection = Database()
    #         cursor = connection.cursor
    #         cursor.execute("Set app.current_user_id = %s", (str(self.sys_user_id),))
    #         connection.commit()
    #         print(f"Current user ID set to: {self.sys_user_id}")
    #     except Exception as e:
    #         print(f"Error setting current user ID: {e}")
    #         connection.close()

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

        missing_fields = []
        if not form_data['first_name']:
            missing_fields.append("First Name")
        if not form_data['last_name']:
            missing_fields.append("Last Name")
        if not form_data['user_password']:
            missing_fields.append("Password")
        if not form_data['confirm_password']:
            missing_fields.append("Confirm Password")
        if form_data['role'] not in ['Staff', 'Admin']:
            missing_fields.append("Role Selection")

        if missing_fields:
            self.view.show_error_dialog("Please fill out the following required fields:\n- " + "\n- ".join(missing_fields))
            return

        # Check if passwords match
        if form_data['user_password'] != form_data['confirm_password']:
            self.view.show_error_dialog("Passwords do not match.")
            return

        # Hash the password using bcrypt
        password_bytes = form_data['user_password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

 
        form_data['user_password'] = hashed_password
        del form_data['confirm_password']  # Remove confirm field from payload

        # Continue saving
        self.save_system_account_data(form_data)


    def populate_system_account_table(self):
        try:
            result = self.model.get_system_users()
            if not result or not result['data']:
                return
            self.model.account_rows = result['data']
            self._populate_table(
                self.view.manage_accounts_screen.adminpanel_tableView_List_StaffAccounts,
                result['columns'],
                result['data']
            )
        except Exception as e:
            self.show_error_message("System Account Data Error", "Could not load system user accounts.")
            print(f"Error loading system user accounts: {e}")
    
    def handle_row_click_account(self, index: QModelIndex = None):
        table = self.admin_manage_accounts_screen.adminpanel_tableView_List_StaffAccounts

        if index is None:
            if table.rowCount() == 0:
                return  
            index = table.model().index(0, 0)

        row = index.row()
        selected_index = table.model().index(row, 0) 
        selected_id = selected_index.data()

        if not selected_id:
            return

        selected_id = str(selected_id)
        print(f"[DEBUG] Clicked ID: {selected_id}")

        for record in self.model.account_rows:
            if str(record[0]) == selected_id:
                self.admin_manage_accounts_screen.ap_display_user_id.setText(str(record[0]))

                full_name_parts = record[1].replace(",", "").split()

                self.admin_manage_accounts_screen.ap_display_user_lname.setText(full_name_parts[0] if len(full_name_parts) > 0 else "")
                self.admin_manage_accounts_screen.ap_display_user_fname.setText(full_name_parts[1] if len(full_name_parts) > 1 else "")
                self.admin_manage_accounts_screen.ap_display_user_mname.setText(full_name_parts[2] if len(full_name_parts) > 2 else "")

                self.admin_manage_accounts_screen.ap_display_user_role.setText(record[2])  # SYS_ROLE
                self.admin_manage_accounts_screen.ap_display_user_status.setText("Active" if record[3] else "Inactive")  # SYS_IS_ACTIVE
                break


    def _refresh(self):
        try:
            self.populate_system_account_table()
            self.handle_row_click_account()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Manage Accounts Error",
                "Error refreshing Manage Accounts",
                QMessageBox.Ok
            )
            print(f"Error refreshing Manage Accounts: {e}")


    def save_system_account_data(self, form_data):
        if not self.view.confirm_registration():
            return

        success = self.model.save_new_account_data(form_data)
        if success:
            self.view.show_success_message()
            self.view.popup.close()
            self.populate_system_account_table()
        else:
            self.view.show_error_dialog("Database error occurred")

    def show_register_account_popup(self):
        self.view.show_register_account_popup(self.view.manage_accounts_screen)
    
    def goto_admin_panel(self):
        if not hasattr(self, 'admin_panel'):
            from Controllers.AdminController.AdminPanelController import AdminPanelController
            self.admin_panel = AdminPanelController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_panel.admin_panel_screen)
        self.stack.setCurrentWidget(self.admin_panel.admin_panel_screen)