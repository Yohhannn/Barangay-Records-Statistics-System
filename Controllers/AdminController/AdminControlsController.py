from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox, QTableView
from PySide6.QtCore import Qt, QModelIndex
from Controllers.BaseFileController import BaseFileController
from Models.AdminModels.AdminControlsModel import AdminControlsModel
from Views.Admin.AdminControlsView import AdminControlsView
from database import Database
import bcrypt

class AdminControlsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role
        self.stack = stack
        self.sys_user_id = sys_user_id

        self.selected_sitio_id = None
        self.selected_sitio_name = ""

        self.selected_infra_id = None
        self.selected_infra_name = ""

        self.selected_transaction_id = None
        self.selected_transaction_name = ""

        self.selected_history_id = None
        self.selected_history_name = ""

        self.selected_med_history_id = None
        self.selected_med_history_name = ""


        self.view = AdminControlsView(self)
        self.model = AdminControlsModel(self.sys_user_id)
        self.admin_controls_screen = self.load_ui("Resources/UIs/AdminPages/AdminPanel/AdminControls/admincontrols.ui")

        self.view.setup_admin_controls_ui(self.admin_controls_screen)
        self.admin_controls_screen.setWindowTitle("Admin Panel - MaPro")

        self._refresh()
        # self.admin_controls_screen.adminpanel_tableView_List_Sitio.clicked.connect(self.handle_row_click_account)


    def show_popup(self):
        self.view.show_register_sitio_popup(self.view.admin_controls_screen)
        self.view.show_edit_sitio_popup(self.view.admin_controls_screen)
        self.view.show_register_infra_type_popup(self.view.admin_controls_screen)
        self.view.show_edit_infra_type_popup(self.view.admin_controls_screen)
        self.view.show_register_history_type_popup(self.view.admin_controls_screen)
        self.view.show_edit_history_type_popup(self.view.admin_controls_screen)
        self.view.show_edit_transaction_type_popup(self.view.admin_controls_screen)
        self.view.show_register_transaction_type_popup(self.view.admin_controls_screen)
        self.view.show_edit_medical_type_popup(self.view.admin_controls_screen)
        self.view.show_register_medical_type_popup(self.view.admin_controls_screen)


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
            self.model.sitio_rows = result['data']
            self._populate_table(
                self.view.admin_controls_screen.adminpanel_tableView_List_Sitio,
                result['columns'],
                result['data']
            )
        except Exception as e:
            QMessageBox.critical(self,"Sitio Data Error", "Could not load system Sitio Data.")
            print(f"Error loading Sitio Data: {e}")

    def populate_infrastructure_table(self):
        try:
            result = self.model.get_infrastructure_types()
            if not result or not result['data']:
                return
            self.model.infra_rows = result['data']
            self._populate_table(
                self.view.admin_controls_screen.adminpanel_tableView_List_InfraType,
                result['columns'],
                result['data']
            )
        except Exception as e:
            QMessageBox.critical(self,"Infrastructure Type Error", "Could not load infrastructure types.")
            print(f"Error loading infrastructure types: {e}")

    def populate_transaction_table(self):
        try:
            result = self.model.get_transaction_types()
            if not result or not result['data']:
                return
            self.model.transact_rows = result['data']
            self._populate_table(
                self.view.admin_controls_screen.adminpanel_tableView_List_TransType,
                result['columns'],
                result['data']
            )
        except Exception as e:
            QMessageBox.critical(self,"Transaction Type Error", "Could not load Transaction types.")
            print(f"Error loading Transaction types: {e}")

    def populate_history_table(self):
        try:
            result = self.model.get_history_types()
            if not result or not result['data']:
                return
            self.model.transact_rows = result['data']
            self._populate_table(
                self.view.admin_controls_screen.adminpanel_tableView_List_HistType,
                result['columns'],
                result['data']
            )
        except Exception as e:
            QMessageBox.critical(self,"History Type Error", "Could not load History types.")
            print(f"Error loading History types: {e}")


    def populate_medical_table(self):
        try:
            result = self.model.get_medical_types()
            if not result or not result['data']:
                return
            self.model.transact_rows = result['data']
            self._populate_table(
                self.view.admin_controls_screen.adminpanel_tableView_List_MedType,
                result['columns'],
                result['data']
            )
        except Exception as e:
            QMessageBox.critical(self,"Medical History Type Error", "Could not load Medical History types.")
            print(f"Error loading Medical History types: {e}")

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

    def handle_row_click_sitio(self, index: QModelIndex = None):
        table = self.admin_controls_screen.adminpanel_tableView_List_Sitio

        if table.model().rowCount() == 0:
            return

        if index is None or not index.isValid():
            index = table.model().index(0, 0)

        row = index.row()
        selected_index = table.model().index(row, 0)
        selected_id = selected_index.data()
        selected_name = table.model().index(row, 1).data()

        if not selected_id:
            return

        self.selected_sitio_id = str(selected_id)
        self.selected_sitio_name = str(selected_name)
        print(f"[DEBUG] Clicked Sitio ID: {self.selected_sitio_id}")
        print(f"[DEBUG] Clicked Sitio Name: {self.selected_sitio_name}")




    def handle_row_click_infrastructure(self):
        table = self.admin_controls_screen.adminpanel_tableView_List_InfraType
        if table.model().rowCount() == 0:
            return

        index = table.currentIndex()
        if not index.isValid():
            index = table.model().index(0, 0)

        row = index.row()
        selected_id = table.model().index(row, 0).data()
        selected_name = table.model().index(row, 1).data()

        if selected_id:
            self.selected_infra_id = str(selected_id)
            self.selected_infra_name = str(selected_name)
            print(f"[DEBUG] Infra ID: {self.selected_infra_id}")
            print(f"[DEBUG] Infra Type: {self.selected_infra_name}")

    def handle_row_click_transaction(self):
        table = self.admin_controls_screen.adminpanel_tableView_List_TransType
        if table.model().rowCount() == 0:
            return

        index = table.currentIndex()
        if not index.isValid():
            index = table.model().index(0, 0)

        row = index.row()
        selected_id = table.model().index(row, 0).data()
        selected_name = table.model().index(row, 1).data()

        if selected_id:
            self.selected_transaction_id = str(selected_id)
            self.selected_transaction_name = str(selected_name)
            print(f"[DEBUG] Transaction ID: {self.selected_transaction_id}")
            print(f"[DEBUG] Transaction Type: {self.selected_transaction_name}")


    def handle_row_click_history(self):
        table = self.admin_controls_screen.adminpanel_tableView_List_HistType
        if table.model().rowCount() == 0:
            return

        index = table.currentIndex()
        if not index.isValid():
            index = table.model().index(0, 0)

        row = index.row()
        selected_id = table.model().index(row, 0).data()
        selected_name = table.model().index(row, 1).data()

        if selected_id:
            self.selected_history_id = str(selected_id)
            self.selected_history_name = str(selected_name)
            print(f"[DEBUG] History Type ID: {self.selected_history_id}")
            print(f"[DEBUG] History Type: {self.selected_history_name}")

    def handle_row_click_medical_type(self):
        table = self.admin_controls_screen.adminpanel_tableView_List_MedType
        if table.model().rowCount() == 0:
            return

        index = table.currentIndex()
        if not index.isValid():
            index = table.model().index(0, 0)

        row = index.row()
        selected_id = table.model().index(row, 0).data()
        selected_name = table.model().index(row, 1).data()

        if selected_id:
            self.selected_med_history_id = str(selected_id)
            self.selected_med_history_name = str(selected_name)
            print(f"[DEBUG] Medical Type ID: {self.selected_med_history_id}")
            print(f"[DEBUG] Medical Type: {self.selected_med_history_name}")


    def handle_remove_sitio(self):
        if not hasattr(self, 'selected_sitio_id') or not self.selected_sitio_id:
            QMessageBox.warning(
                self.admin_controls_screen,
                "No Sitio Selected",
                "Please select a sitio first."
            )
            return

        sitio_name = getattr(self, 'selected_sitio_name', "Unknown Sitio")

        clarification = QMessageBox.question(
            self.admin_controls_screen,
            "Soft Delete Note",
            f"Make sure that no citizen is using Sitio: {sitio_name} as reference.\n"
            "Do you wish to continue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if clarification != QMessageBox.Yes:
            return  # User cancelled

        confirm = QMessageBox.question(
            self.admin_controls_screen,
            "Confirm Delete",
            f"Are you sure you want to delete Sitio: {sitio_name}?\n"
            "This action is permanent.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return  # User cancelled

        sitio_deleted = self.model.soft_delete_sitio_data(self.selected_sitio_id)
        if sitio_deleted:
            QMessageBox.information(
                self.admin_controls_screen,
                "Deleted",
                f"Sitio '{sitio_name}' deleted successfully."
            )


            self._refresh()
        else:
            QMessageBox.critical(
                self.admin_controls_screen,
                "Deletion Failed",
                "An error occurred while deleting the Sitio."
            )

    def handle_remove_infrastructure_type(self):
        if not hasattr(self, 'selected_infra_id') or not self.selected_infra_id:
            QMessageBox.warning(
                self.admin_controls_screen,
                "No Infrastructure Selected",
                "Please select an infrastructure record first."
            )
            return

        infra_name = getattr(self, 'selected_infra_name', "Unknown Infrastructure")

        confirm = QMessageBox.question(
            self.admin_controls_screen,
            "Confirm Delete",
            f"Are you sure you want to delete Infrastructure: {infra_name}?\n"
            "This action is permanent.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        infra_deleted = self.model.soft_delete_infrastructure_data(self.selected_infra_id)
        if infra_deleted:
            QMessageBox.information(
                self.admin_controls_screen,
                "Deleted",
                f"Infrastructure '{infra_name}' deleted successfully."
            )
            self._refresh()
        else:
            QMessageBox.critical(
                self.admin_controls_screen,
                "Deletion Failed",
                "An error occurred while deleting the Infrastructure."
            )

    def handle_remove_transaction_type(self):
        if not hasattr(self, 'selected_transaction_id') or not self.selected_transaction_id:
            QMessageBox.warning(
                self.admin_controls_screen,
                "No Transaction Type Selected",
                "Please select a transaction type first."
            )
            return

        transaction_name = getattr(self, 'selected_transaction_name', "Unknown Transaction Type")

        confirm = QMessageBox.question(
            self.admin_controls_screen,
            "Confirm Delete",
            f"Are you sure you want to delete Transaction Type: {transaction_name}?\n"
            "This action is permanent.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        transaction_type_deleted = self.model.soft_delete_transaction_type(self.selected_transaction_id)
        if transaction_type_deleted:
            QMessageBox.information(
                self.admin_controls_screen,
                "Deleted",
                f"Transaction Type '{transaction_name}' deleted successfully."
            )
            self._refresh()
        else:
            QMessageBox.critical(
                self.admin_controls_screen,
                "Deletion Failed",
                "An error occurred while deleting the Transaction Type."
            )

    def handle_remove_history_type(self):
        if not hasattr(self, 'selected_history_id') or not self.selected_history_id:
            QMessageBox.warning(
                self.admin_controls_screen,
                "No History Type Selected",
                "Please select a history type first."
            )
            return

        history_name = getattr(self, 'selected_history_name', "Unknown History Type")

        confirm = QMessageBox.question(
            self.admin_controls_screen,
            "Confirm Delete",
            f"Are you sure you want to delete History Type: {history_name}?\n"
            "This action is permanent.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        history_type_deleted = self.model.soft_delete_history_type(self.selected_history_id)
        if history_type_deleted:
            QMessageBox.information(
                self.admin_controls_screen,
                "Deleted",
                f"History Type '{history_name}' deleted successfully."
            )
            self._refresh()
        else:
            QMessageBox.critical(
                self.admin_controls_screen,
                "Deletion Failed",
                "An error occurred while deleting the History Type."
            )

    def handle_remove_med_history_type(self):
        if not hasattr(self, 'selected_med_history_id') or not self.selected_med_history_id:
            QMessageBox.warning(
                self.admin_controls_screen,
                "No Medical History Type Selected",
                "Please select a medical history type first."
            )
            return

        med_hist_name = getattr(self, 'selected_med_history_name', "Unknown Medical History Type")

        confirm = QMessageBox.question(
            self.admin_controls_screen,
            "Confirm Delete",
            f"Are you sure you want to delete Medical History Type: {med_hist_name}?\n"
            "This action is permanent.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        med_type_deleted = self.model.soft_delete_medical_hist_type(self.selected_med_history_id)
        if med_type_deleted:
            QMessageBox.information(
                self.admin_controls_screen,
                "Deleted",
                f"Medical History Type '{med_hist_name}' deleted successfully."
            )
            self._refresh()
        else:
            QMessageBox.critical(
                self.admin_controls_screen,
                "Deletion Failed",
                "An error occurred while deleting the Medical History Type."
            )

    def _refresh(self):
        try:
            self.populate_sitio_table()
            self.populate_history_table()
            self.populate_medical_table()
            self.populate_transaction_table()
            self.populate_infrastructure_table()

            self.selected_sitio_id = None
            self.selected_infra_id = None
            self.selected_transaction_id = None
            self.selected_history_id = None

            self.admin_controls_screen.adminpanel_tableView_List_Sitio.clicked.connect(
                self.handle_row_click_sitio
            )
            self.admin_controls_screen.adminpanel_tableView_List_InfraType.clicked.connect(
                self.handle_row_click_infrastructure
            )
            self.admin_controls_screen.adminpanel_tableView_List_TransType.clicked.connect(
                self.handle_row_click_transaction
            )
            self.admin_controls_screen.adminpanel_tableView_List_HistType.clicked.connect(
                self.handle_row_click_history
            )
            self.admin_controls_screen.adminpanel_tableView_List_MedType.clicked.connect(
                self.handle_row_click_medical_type
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Manage Accounts Error",
                "Error refreshing Admin Controls.",
                QMessageBox.Ok
            )
            print(f"Error refreshing Admin Controls: {e}")




    def save_sitio_data(self, form_data):
        if not self.view.confirm_registration(
                "Confirm Registration",
                "Are you sure you want to register this Sitio?"):
            return

        success = self.model.save_new_sitio_data(form_data)
        if success:
            self.view.show_success_message("Success", "System user successfully registered!")
            self.view.popup.close()
            self.populate_sitio_table()
        else:
            self.view.show_error_dialog("Error",f"Failed to register System User.Database error occurred")

    def rename_sitio(self, sitio_id, new_name):
        old_name = self.model.get_sitio_name_by_id(sitio_id)  # returns string directly
        if old_name is None:
            QMessageBox.warning(None, "Warning", "Sitio not found.")
            return

        print(f"Old Sitio Name: {old_name}")

        if old_name == new_name:
            QMessageBox.information(None, "Info", "The name is already the same.")
            return

        success = self.model.update_sitio_name(sitio_id, new_name)
        self._refresh()
        if success:
            QMessageBox.information(None, "Success", f"Sitio renamed from '{old_name}' to '{new_name}'")
            self.view.popup.close()
        else:
            QMessageBox.critical(None, "Error", "Failed to update Sitio name.")

    def handle_sitio_search(self):
        sitio_id = self.view.popup.input_id_search.text().strip()
        if not sitio_id.isdigit():
            self.view.popup.display_searched.setText("Invalid ID")
            return

        sitio_name = self.model.get_sitio_name_by_id(int(sitio_id))
        if sitio_name:
            self.view.popup.display_searched.setText(sitio_name)
        else:
            self.view.popup.display_searched.setText("Not found")

    def save_infrastructure_type(self):
        infra_data = self.view.get_infra_data()

        if not infra_data['infra_name']:
            self.view.show_error_dialog("Please fill out the following required fields:\n- Infrastructure Type Name")
            return

        if not self.view.confirm_registration(
                "Confirm Registration",
                "Are you sure you want to register this Infrastructure type?"):
            return

        success = self.model.save_new_infrastructure_type(infra_data)
        if success:
            self.view.show_success_message("Success", "Infrastructure type successfully registered!")
            self.view.popup.close()
            self.populate_infrastructure_table()
        else:
            self.view.show_error_dialog("Database error occurred",f"Failed to register History type")

    def rename_infra_type(self, infra_id, new_name):
        old_name = self.model.get_infrastructure_type_by_id(infra_id)  # returns string directly
        if old_name is None:
            QMessageBox.warning(None, "Warning", "Sitio not found.")
            return

        print(f"Old Infrastructure Name: {old_name}")

        if old_name == new_name:
            QMessageBox.information(None, "Info", "The name is already the same.")
            return

        success = self.model.update_infrastructure_type(infra_id, new_name)
        self._refresh()
        if success:
            self.view.show_success_message("Success", f"Infrastructure type renamed from '{old_name}' to '{new_name}'")
            self.view.popup.close()
        else:
            self.view.show_error_dialog("Error", "Failed to update Infrastructure Type name.")

    def handle_infra_search(self):
        infra_id = self.view.popup.input_id_search.text().strip()
        if not infra_id.isdigit():
            self.view.popup.display_searched.setText("Invalid ID")
            return

        infra_name = self.model.get_infrastructure_type_by_id(int(infra_id))
        if infra_name:
            self.view.popup.display_searched.setText(infra_name)
        else:
            self.view.popup.display_searched.setText("Not found")

    def save_history_type(self):
        history_data = self.view.get_history_data()

        if not history_data['history_name']:
            self.view.show_error_dialog("Please fill out the following required fields:\n- History Type Name")
            return

        if not self.view.confirm_registration(
                "Confirm Registration",
                "Are you sure you want to register this History type?"):
            return

        success = self.model.save_new_history_type(history_data)
        if success:
            self.view.show_success_message("Success", "History type successfully registered!")
            self.view.popup.close()
            self.populate_history_table()
        else:
            self.view.show_error_dialog("Database error occurred",f"Failed to register History type")

    def rename_history_type(self, history_id, new_name):
        old_name = self.model.get_history_type_by_id(history_id)  # returns string directly
        if old_name is None:
            QMessageBox.warning(None, "Warning", "History type not found.")
            return

        print(f"Old History type Name: {old_name}")

        if old_name == new_name:
            QMessageBox.information(None, "Info", "The name is already the same.")
            return

        success = self.model.update_history_type(history_id, new_name)
        self._refresh()
        if success:
            self.view.show_success_message("Success", f"History type renamed from '{old_name}' to '{new_name}'")
            self.view.popup.close()
        else:
            self.view.show_error_dialog("Database error occurred", "Failed to update History type name.")

    def handle_history_search(self):
        history_id = self.view.popup.input_id_search.text().strip()
        if not history_id.isdigit():
            self.view.popup.display_searched.setText("Invalid ID")
            return

        type_name = self.model.get_history_type_by_id(int(history_id))
        if type_name:
            self.view.popup.display_searched.setText(type_name)
        else:
            self.view.popup.display_searched.setText("Not found")


    def save_transaction_type(self):
        transaction_data = self.view.get_transaction_data()

        if not transaction_data['transaction_name']:
            self.view.show_error_dialog("Please fill out the following required fields:\n- transaction Type Name")
            return

        if not self.view.confirm_registration(
                "Confirm Registration",
                "Are you sure you want to register this transaction type?"):
            return

        success = self.model.save_new_transaction_type(transaction_data)
        if success:
            self.view.show_success_message("Success", "transaction type successfully registered!")
            self.view.popup.close()
            self.populate_transaction_table()
        else:
            self.view.show_error_dialog("Database error occurred",f"Failed to register transaction type")

    def rename_transaction_type(self, transaction_id, new_name):
        old_name = self.model.get_transaction_type_by_id(transaction_id)  # returns string directly
        if old_name is None:
            QMessageBox.warning(None, "Warning", "transaction type not found.")
            return

        print(f"Old transaction type Name: {old_name}")

        if old_name == new_name:
            QMessageBox.information(None, "Info", "The name is already the same.")
            return

        success = self.model.update_transaction_type(transaction_id, new_name)
        self._refresh()
        if success:
            self.view.show_success_message("Success", f"transaction type renamed from '{old_name}' to '{new_name}'")
            self.view.popup.close()
        else:
            self.view.show_error_dialog("Database error occurred", "Failed to update transaction type name.")

    def handle_transaction_search(self):
        transaction_id = self.view.popup.input_id_search.text().strip()
        if not transaction_id.isdigit():
            self.view.popup.display_searched.setText("Invalid ID")
            return

        type_name = self.model.get_transaction_type_by_id(int(transaction_id))
        if type_name:
            self.view.popup.display_searched.setText(type_name)
        else:
            self.view.popup.display_searched.setText("Not found")

    def save_medical_type(self):
        medical_data = self.view.get_medical_data()

        if not medical_data['medical_name']:
            self.view.show_error_dialog("Please fill out the following required fields:\n- medical Type Name")
            return

        if not self.view.confirm_registration(
                "Confirm Registration",
                "Are you sure you want to register this Medical type?"):
            return

        success = self.model.save_new_medical_type(medical_data)
        if success:
            self.view.show_success_message("Success", "Medical History type successfully registered!")
            self.view.popup.close()
            self.populate_medical_table()
        else:
            self.view.show_error_dialog("Database error occurred",f"Failed to register Medical History type")

    def rename_medical_type(self, medical_id, new_name):
        old_name = self.model.get_medical_type_by_id(medical_id)  # returns string directly
        if old_name is None:
            QMessageBox.warning(None, "Warning", "Medical history type not found.")
            return

        print(f"Old medical type Name: {old_name}")

        if old_name == new_name:
            QMessageBox.information(None, "Info", "The name is already the same.")
            return

        success = self.model.update_medical_type(medical_id, new_name)
        self._refresh()
        if success:
            self.view.show_success_message("Success", f"Medical History type renamed from '{old_name}' to '{new_name}'")
            self.view.popup.close()
        else:
            self.view.show_error_dialog("Database error occurred", "Failed to update Medical History type name.")

    def handle_medical_search(self):
        medical_id = self.view.popup.input_id_search.text().strip()
        if not medical_id.isdigit():
            self.view.popup.display_searched.setText("Invalid ID")
            return

        type_name = self.model.get_medical_type_by_id(int(medical_id))
        if type_name:
            self.view.popup.display_searched.setText(type_name)
        else:
            self.view.popup.display_searched.setText("Not found")



    def goto_admin_panel(self):
        if not hasattr(self, 'admin_panel'):
            from Controllers.AdminController.AdminPanelController import AdminPanelController
            self.admin_panel = AdminPanelController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_panel.admin_panel_screen)
        self.stack.setCurrentWidget(self.admin_panel.admin_panel_screen)

    def goto_trashbin_panel(self):
        print("-- Navigating to AdmiTrashhbin Panel")

        if not hasattr(self, 'trashbin_panel'):
            from Controllers.AdminController.AdminBinController import AdminBinController
            self.trashbin_panel = AdminBinController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.trashbin_panel.trashbin_screen)
        self.stack.setCurrentWidget(self.trashbin_panel.trashbin_screen)