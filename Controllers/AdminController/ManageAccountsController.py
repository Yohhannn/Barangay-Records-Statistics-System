from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt, QModelIndex
from Controllers.BaseFileController import BaseFileController
from Models.AdminModels.ManageAccountsModel import ManageAccountsModel
from Views.Admin.ManageAccountsView import ManageAccountsView

import bcrypt


class ManageAccountsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role
        self.stack = stack
        self.sys_user_id = sys_user_id
        self.selected_user_id = None

        self.view = ManageAccountsView(self)
        self.model = ManageAccountsModel(self.sys_user_id)
        self.admin_manage_accounts_screen = self.load_ui(
            "Resources/UIs/AdminPages/AdminPanel/ManageAccounts/manageaccounts.ui")

        self.view.setup_manage_accounts_ui(self.admin_manage_accounts_screen)
        self.admin_manage_accounts_screen.setWindowTitle("Admin Panel - MaPro")

        self._refresh()
        self.admin_manage_accounts_screen.adminpanel_tableView_List_StaffAccounts.clicked.connect(
            self.handle_row_click_account)

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

    def handle_remove_user(self):
        if not hasattr(self, 'selected_user_id') or not self.selected_user_id:
            QMessageBox.warning(
                self.admin_manage_accounts_screen,
                "No user selected",
                "Please select a user first."
            )
            return

        name = getattr(self, 'selected_user_name', "Unknown")
        role = getattr(self, 'selected_user_role', "Unknown")

        confirm = QMessageBox.question(
            self.admin_manage_accounts_screen,
            "Confirm Delete Account",
            f"Are you sure you want to delete {role} {name}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            success = self.model.soft_delete_account_data({'user_id': self.selected_user_id})

            if success:
                QMessageBox.information(
                    self.admin_manage_accounts_screen,
                    "User Removed",
                    f"System user {role} {name} has been successfully removed."
                )
                self._refresh()
            else:
                QMessageBox.critical(
                    self.admin_manage_accounts_screen,
                    "Error",
                    "Failed to remove the selected user."
                )

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
            self.view.show_error_dialog(
                "Please fill out the following required fields:\n- " + "\n- ".join(missing_fields))
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

    def validate_update_fields(self):
        form_data = self.view.get_update_form_data()
        system_user_id = self.view.popup.input_id_search.text().strip()

        if not system_user_id:
            self.view.show_error_dialog("Invalid System User ID. Please search and select a valid user.")
            return

        # Validate input fields
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
            missing_fields.append("Role")
        if form_data['status'] not in ['Active', 'Inactive']:
            missing_fields.append("Status")

        if missing_fields:
            self.view.show_error_dialog(
                "Please fill out the following required fields:\n- " + "\n- ".join(missing_fields))
            return

        if form_data['user_password'] != form_data['confirm_password']:
            self.view.show_error_dialog("Passwords do not match.")
            return

        # Convert 'Active'/'Inactive' to Boolean strings
        form_data['is_active'] = 'True' if form_data['status'] == 'Active' else 'False'

        # Hash password
        password_bytes = form_data['user_password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        form_data['user_password'] = hashed_password
        del form_data['confirm_password']

        self.save_updated_system_account_data(form_data, system_user_id)

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
            QMessageBox.critical(self,"System Account Data Error", "Could not load system user accounts.")
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

        self.selected_user_id = str(selected_id)
        print(f"[DEBUG] Clicked ID: {self.selected_user_id}")

        for record in self.model.account_rows:
            if str(record[0]) == selected_id:
                self.admin_manage_accounts_screen.ap_display_user_id.setText(str(record[0]))

                full_name_parts = record[1].replace(",", "").split()

                lname = full_name_parts[0] if len(full_name_parts) > 0 else ""
                fname = full_name_parts[1] if len(full_name_parts) > 1 else ""
                mname = full_name_parts[2] if len(full_name_parts) > 2 else ""

                self.admin_manage_accounts_screen.ap_display_user_lname.setText(lname)
                self.admin_manage_accounts_screen.ap_display_user_fname.setText(fname)
                self.admin_manage_accounts_screen.ap_display_user_mname.setText(mname)

                role = record[2]  # SYS_ROLE
                self.admin_manage_accounts_screen.ap_display_user_role.setText(role)

                status = "Active" if record[3] else "Inactive"
                self.admin_manage_accounts_screen.ap_display_user_status.setText(status)

                #  Store full name and role for confirmation dialogs
                self.selected_user_name = f"{fname} {mname} {lname}".strip()
                self.selected_user_role = role
                break

    def _refresh(self):
        try:
            self.populate_system_account_table()
            self.handle_row_click_account()
            self.selected_user_id = None

        except Exception as e:
            QMessageBox.critical(
                self,
                "Manage Accounts Error",
                "Error refreshing Manage Accounts",
                QMessageBox.Ok
            )
            print(f"Error refreshing Manage Accounts: {e}")

    def save_system_account_data(self, form_data):
        if not self.view.confirm_registration(
                "Confirm Registration",
                "Are you sure you want to register this System User?"):
            return

        success = self.model.save_new_account_data(form_data)
        if success:
            self.view.show_success_message("Success","System user successfully registered!" )
            self.view.popup.close()
            self.populate_system_account_table()
        else:
            self.view.show_error_dialog("Database error occurred")

    def save_updated_system_account_data(self, form_data, system_user_id):
        if not self.view.confirm_registration("Confirm Update", "Are you sure you want to update this System User?"):
            return

        success = self.model.save_updated_account_data(form_data, system_user_id)
        self._refresh()
        if success:
            self.view.show_success_message("Success", "System user successfully updated!")
            self.view.popup.close()
            self.populate_system_account_table()
        else:
            self.view.show_error_dialog("Database error occurred while updating.")

    # def update_system_user(self, system_user_id, new_name):
    #     old_name = self.model.get_system_user_by_id(system_user_id)  # returns string directly
    #     if old_name is None:
    #         QMessageBox.warning(None, "Warning", "system_user type not found.")
    #         return
    #
    #     print(f"Old system_user type Name: {old_name}")
    #
    #     if old_name == new_name:
    #         QMessageBox.information(None, "Info", "The name is already the same.")
    #         return
    #
    #     success = self.model.save_updated_account_data(system_user_id)
    #     self._refresh()
    #     if success:
    #         self.view.show_success_message("Success", f"System user updated Succefully!'")
    #         self.view.popup.close()
    #     else:
    #         QMessageBox.critical(self,"Database error occurred", "Failed to update System user.")

    def handle_system_user_search(self):
        system_user_id = self.view.popup.input_id_search.text().strip()
        if not system_user_id:
            self.view.popup.display_searched.setText("Invalid ID")
            return

        user_name = self.model.get_system_user_by_id(system_user_id)
        if user_name:
            self.view.popup.display_searched.setText(user_name)
        else:
            self.view.popup.display_searched.setText("Not found")

    def show_register_account_popup(self):
        self.view.show_register_account_popup(self.view.manage_accounts_screen)
        self.view.show_update_account_popup(self.view.manage_accounts_screen)

    def show_error_message(self, title, message):
        QMessageBox.critical(
            self,
            title,
            message,
            QMessageBox.Ok
        )

    def goto_admin_panel(self):
        if not hasattr(self, 'admin_panel'):
            from Controllers.AdminController.AdminPanelController import AdminPanelController
            self.admin_panel = AdminPanelController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_panel.admin_panel_screen)
        self.stack.setCurrentWidget(self.admin_panel.admin_panel_screen)