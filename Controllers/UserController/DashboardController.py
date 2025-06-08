from PySide6.QtWidgets import QPushButton, QMessageBox, QApplication, QTableWidgetItem, QFrame, QLineEdit, QLabel
from PySide6.QtGui import QPixmap, QIcon, Qt
from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup
from Views.DashboardView import DashboardView
from database import Database
from passlib.hash import bcrypt


class DashboardController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role=None):
        super().__init__(login_window, emp_first_name, sys_user_id)

        self.user_role = user_role
        self.view = DashboardView(self)
        self.sys_user_id = sys_user_id


        self.dashboard_screen = self.load_ui("Resources/UIs/MainPages/dashboard.ui")
        self.stack.addWidget(self.dashboard_screen)
        self.view.setup_dashboard_ui(self.dashboard_screen)
        self.load_recent_citizens_data()
        self.load_account_info()
        self.load_account_info_dashboard()
        self.update_registered_citizens_count()

        admin_buttons = [
            self.dashboard_screen.findChild(QPushButton, "nav_buttonAdminPanel"),
            self.dashboard_screen.findChild(QPushButton, "nav_buttonActivityLogs"),
        ]
        admin_frame = self.dashboard_screen.findChild(QFrame, "baseNavFramesub2")  

        if self.user_role in ['Admin', 'Super Admin']:
            print("Should show admin buttons")
            for btn in admin_buttons:
                if btn:
                    btn.setVisible(True)
                    btn.setEnabled(True)
            if admin_frame:
                admin_frame.setVisible(True)
        else:
            print("Should hide admin buttons")
            for btn in admin_buttons:
                if btn:
                    btn.setVisible(False)
                    btn.setEnabled(False)
            if admin_frame:
                admin_frame.setVisible(False)

    def update_registered_citizens_count(self):
        """Fetches and updates the total number of registered citizens (non-deleted)."""
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor

            # SQL query to count active (non-deleted) citizens
            cursor.execute("""
                SELECT COUNT(*) FROM CITIZEN WHERE CTZ_IS_DELETED = FALSE;
            """)
            result = cursor.fetchone()

            if result:
                total_citizens = result[0]
                label = self.dashboard_screen.findChild(QLabel, "label_TotalNumberRegisteredCitizen")
                if label:
                    label.setText('[ ' + str(total_citizens) + ' ]')
                else:
                    print("Label 'label_TotalNumberRegisteredCitizen' not found!")
            else:
                print("No data returned from database.")
        except Exception as e:
            QMessageBox.critical(self.dashboard_screen, "Database Error", f"Failed to load citizen count: {str(e)}")
        finally:
            if connection:
                connection.close()

    def load_account_info(self):
        """Fetches and stores current user's system account information."""
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
                SELECT 
                    SYS_USER_ID,
                    SYS_FNAME,
                    SYS_MNAME,
                    SYS_LNAME,
                    SYS_ROLE
                FROM SYSTEM_ACCOUNT
                WHERE SYS_USER_ID = %s AND SYS_IS_ACTIVE = TRUE;
            """, (self.sys_user_id,))
            result = cursor.fetchone()

            if result:
                sys_user_id, fname, mname, lname, role = result
                self.account_data = {
                    "id": sys_user_id,
                    "fname": fname,
                    "mname": mname,
                    "lname": lname,
                    "role": role.title() if role else "N/A"
                }
            else:
                self.account_data = {
                    "id": "N/A",
                    "fname": "N/A",
                    "mname": "",
                    "lname": "N/A",
                    "role": "N/A"
                }
        except Exception as e:
            print(f"Error fetching account info: {e}")
            self.account_data = {
                "id": "Error",
                "fname": "Error",
                "mname": "",
                "lname": "Error",
                "role": "Error"
            }
        finally:
            if connection:
                connection.close()
    def load_account_info_dashboard(self):
        """Fetches and displays the current user's system account information."""
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor

            # Query the SYSTEM_ACCOUNT table for the current user
            cursor.execute("""
                SELECT
                    SYS_USER_ID,
                    SYS_FNAME,
                    SYS_MNAME,
                    SYS_LNAME,
                    SYS_ROLE
                FROM SYSTEM_ACCOUNT
                WHERE SYS_USER_ID = %s AND SYS_IS_ACTIVE = TRUE;
            """, (self.sys_user_id,))

            result = cursor.fetchone()

            if result:
                sys_user_id, fname, mname, lname, role = result

                # Format full name: First Name M.I. Last Name
                middle_initial = f"{mname[0]}." if mname and mname.strip() else ""
                full_name = f"{fname} {middle_initial} {lname}".strip()

                # Find labels by object names
                id_label = self.dashboard_screen.findChild(QLabel, "data_empIDAccInfo")
                name_label = self.dashboard_screen.findChild(QLabel, "data_empNameAccInfo")
                role_label = self.dashboard_screen.findChild(QLabel, "data_empAccessRole")

                # Update labels if found
                if id_label:
                    id_label.setText(str(sys_user_id))
                else:
                    print("Label 'data_empIDAccInfo' not found!")

                if name_label:
                    name_label.setText(full_name)
                else:
                    print("Label 'data_empNameAccInfo' not found!")

                if role_label:
                    role_label.setText(str(role).title())
                else:
                    print("Label 'data_empAccessRole' not found!")
            else:
                print("No active account found for the current user.")
        except Exception as e:
            QMessageBox.critical(self.dashboard_screen, "Database Error", f"Failed to load account info: {str(e)}")
        finally:
            if connection:
                connection.close()

    # def load_account_info(self):
    #     """Fetches and displays the current user's system account information."""
    #     connection = None
    #     try:
    #         connection = Database()
    #         cursor = connection.cursor
    #
    #         # Query the SYSTEM_ACCOUNT table for the current user
    #         cursor.execute("""
    #             SELECT
    #                 SYS_USER_ID,
    #                 SYS_FNAME,
    #                 SYS_MNAME,
    #                 SYS_LNAME,
    #                 SYS_ROLE
    #             FROM SYSTEM_ACCOUNT
    #             WHERE SYS_USER_ID = %s AND SYS_IS_ACTIVE = TRUE;
    #         """, (self.sys_user_id,))
    #
    #         result = cursor.fetchone()
    #
    #         if result:
    #             sys_user_id, fname, mname, lname, role = result
    #             full_name = f"{fname} {mname or ''} {lname}".strip()
    #
    #             # Find labels by object names
    #             id_label = self.dashboard_screen.findChild(QLabel, "data_empIDAccInfo")
    #             name_label = self.dashboard_screen.findChild(QLabel, "data_empNameAccInfo")
    #             role_label = self.dashboard_screen.findChild(QLabel, "data_empAccessRole")
    #
    #             # Update labels if found
    #             if id_label:
    #                 id_label.setText(str(sys_user_id))
    #             else:
    #                 print("Label 'data_empIDAccInfo' not found!")
    #
    #             if name_label:
    #                 name_label.setText(full_name)
    #             else:
    #                 print("Label 'data_empNameAccInfo' not found!")
    #
    #             if role_label:
    #                 role_label.setText(str(role).title())
    #             else:
    #                 print("Label 'data_empAccessRole' not found!")
    #         else:
    #             print("No active account found for the current user.")
    #     except Exception as e:
    #         QMessageBox.critical(self.dashboard_screen, "Database Error", f"Failed to load account info: {str(e)}")
    #     finally:
    #         if connection:
    #             connection.close()



    # def show_barangayinfo_initialize(self):
    #     print("-- Navigating to Dashboard > Barangay Info")
    #     try:
    #         popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/barangayinfo.ui", self)
    #         # if popup is None:
    #         #     raise Exception("Failed to load barangayinfo popup UI")
    #
    #         popup.setWindowTitle("Barangay Information")
    #         popup.brgyinfo_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))
    #         popup.setWindowModality(Qt.ApplicationModal)
    #         # popup.setWindowTitle(f"{APP_NAME}{self.controller.app_version}")
    #         popup.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
    #         popup.setFixedSize(popup.size())
    #         popup.show()
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to show barangay info: {str(e)}")
    #         print(f"Error showing barangay info popup: {e}")

    def show(self):
        """Override show to ensure proper centering"""
        super().show()
        self.center_on_screen()
    
    # def is_admin(self):
    #     return self.user_role in ['Admin', 'Super Admin']


    def goto_admin_panel(self):
        print("-- Navigating to Admin Panel")
        self.load_account_info()
        self.load_recent_citizens_data()
        if not hasattr(self, 'admin_panel'):
            from Controllers.AdminController.AdminPanelController import AdminPanelController
            self.admin_panel = AdminPanelController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.admin_panel.admin_panel_screen)
        self.stack.setCurrentWidget(self.admin_panel.admin_panel_screen)

    def goto_activity_logs(self):
        print("-- Navigating to Activity Logs")
        self.load_account_info()
        self.load_recent_citizens_data()
        if not hasattr(self, 'activity_logs'):
            from Controllers.AdminController.ActivityLogsController import ActivityLogsController
            self.activity_logs = ActivityLogsController(
                self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack
            )
            self.stack.addWidget(self.activity_logs.activity_logs_screen)
        self.stack.setCurrentWidget(self.activity_logs.activity_logs_screen)


    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        self.load_account_info()
        self.load_recent_citizens_data()
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        self.load_account_info()
        self.load_recent_citizens_data()
        if not hasattr(self, 'statistics_panel'):
            from Controllers.UserController.StatisticsController import StatisticsController
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)



    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        self.load_account_info()
        self.load_recent_citizens_data()
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        self.load_account_info()
        self.load_recent_citizens_data()
        if not hasattr(self, 'transactions_panel'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        self.load_account_info()
        self.load_recent_citizens_data()
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)

    def logout(self):
        self.load_account_info()
        self.load_recent_citizens_data()
        confirmation = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            QApplication.closeAllWindows()
            self.login_window.show()
            self.login_window.clear_fields()

    def load_recent_citizens_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor

            # SQL Query to fetch recently added citizens with middle name
            cursor.execute("""
                SELECT 
                    C.CTZ_ID, -- 0
                    C.HH_ID, -- 2
                    C.CTZ_LAST_NAME, -- 1
                    C.CTZ_FIRST_NAME, -- 3
                    C.CTZ_MIDDLE_NAME, -- 4
                    FLOOR(EXTRACT(YEAR FROM AGE(CURRENT_DATE, C.CTZ_DATE_OF_BIRTH))) AS CTZ_AGE, -- 5
                    C.CTZ_SEX, -- 6
                    S.SITIO_NAME, -- 7
                    TO_CHAR(C.CTZ_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED_FORMATTED -- 8
                FROM CITIZEN C
                JOIN SITIO S ON C.SITIO_ID = S.SITIO_ID
                WHERE C.CTZ_IS_DELETED = FALSE AND C.CTZ_IS_ALIVE = TRUE
                ORDER BY C.CTZ_DATE_ENCODED ASC
                LIMIT 10;
            """)
            rows = cursor.fetchall()
            self.citizen_rows = rows  # Optional: store data if needed later

            # Configure the dashboard table
            table = self.dashboard_screen.table_recentlyAddedCitizensDashboard
            table.setRowCount(len(rows))
            table.setColumnCount(9)  # Increased to 9 columns for Middle Name
            table.setHorizontalHeaderLabels([
                "Citizen ID", "Household ID", "Family Name", "First Name",
                "Middle Name", "Age", "Sex", "Sitio", "Date Encoded"
            ])

            # Set column widths (adjust as needed)
            table.setColumnWidth(0, 80)  # CTZ ID
            table.setColumnWidth(1, 150)  # Family Name
            table.setColumnWidth(2, 120)  # Household ID
            table.setColumnWidth(3, 150)  # First Name
            table.setColumnWidth(4, 150)  # Middle Name
            table.setColumnWidth(5, 60)  # Age
            table.setColumnWidth(6, 60)  # Sex
            table.setColumnWidth(7, 150)  # Sitio
            table.setColumnWidth(8, 200)  # Date Encoded

            # Populate the table with data
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

            # Optional: Enable sorting or other features
            table.sortByColumn(8, Qt.DescendingOrder)  # Sort by Date Encoded (descending)
            table.setSortingEnabled(True)

        except Exception as e:
            QMessageBox.critical(self.dashboard_screen, "Database Error", str(e))
        finally:
            if connection:
                connection

    def show_barangayinfo_popup(self):
        print("-- Navigating to Dashboard > Barangay Info")
        self.load_account_info()
        self.load_recent_citizens_data()
        popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/barangayinfo.ui", self)
        popup.setWindowTitle("Barangay Information")
        popup.brgyinfo_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))
        popup.setWindowModality(Qt.ApplicationModal)
        popup.setFixedSize(popup.size())
        popup.show()

    def show_aboutsoftware_popup(self):
        print("-- Navigating to Dashboard > About Software")
        self.load_account_info()
        self.load_recent_citizens_data()
        popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/aboutsoftware.ui", self)
        popup.setWindowTitle("About the Software")
        popup.aboutsoftwareinfo_imageRavenLabs.setPixmap(QPixmap("Resources/Icons/AppIcons/icon_ravenlabs.png"))
        popup.aboutsoftwareinfo_imageCTULOGO.setPixmap(QPixmap("Resources/Images/General_Images/img_ctulogo.png"))
        popup.aboutsoftwareinfo_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/img_mainappicon.png"))
        popup.setWindowModality(Qt.ApplicationModal)
        popup.setFixedSize(popup.size())
        popup.show()

    def show_account_popup(self):
        print("-- Navigating to Dashboard > Your Account")
        popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/youraccount.ui", self)
        popup.setWindowTitle("Your Account")
        popup.setWindowModality(Qt.ApplicationModal)
        popup.setFixedSize(popup.size())
        popup.employeeaccount_buttonChangePIN.setIcon(QIcon('Resources/Icons/FuncIcons/icon_changepin2.svg'))

        self.load_account_info()
        self.load_recent_citizens_data()
        # Labels inside the popup
        sys_id_label = popup.findChild(QLabel, "sysacc_displaySysID")
        fname_label = popup.findChild(QLabel, "employeeacc_displayfname")
        mname_label = popup.findChild(QLabel, "employeeacc_displaymname")
        lname_label = popup.findChild(QLabel, "employeeacc_displaylname")
        role_label = popup.findChild(QLabel, "displayemployeeacc_perm")

        # Set label texts using stored account data
        if hasattr(self, 'account_data'):
            if sys_id_label:
                sys_id_label.setText(str(self.account_data["id"]))
            if fname_label:
                fname_label.setText(self.account_data["fname"])
            if mname_label:
                mname_label.setText(self.account_data["mname"] or "")
            if lname_label:
                lname_label.setText(self.account_data["lname"])
            if role_label:
                role_label.setText(self.account_data["role"])
        else:
            # Fallback if no data is available
            for label in [sys_id_label, fname_label, mname_label, lname_label, role_label]:
                if label:
                    label.setText("N/A")

        # Connect buttons
        admin_override_button = popup.findChild(QPushButton, "employeeaccount_buttonAdminOverride")
        if admin_override_button:
            admin_override_button.clicked.connect(lambda: self.show_admin_override_popup(popup))

        change_pin_button = popup.findChild(QPushButton, "employeeaccount_buttonChangePIN")
        if change_pin_button:
            change_pin_button.clicked.connect(lambda: self.show_change_pin_popup(popup))

        popup.show()

    # def show_admin_override_popup(self, first_popup):
    #     print("-- Navigating to Dashboard > Your Account > Admin Override")
    #     first_popup.close()
    #     admin_popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/adminoverride.ui", self)
    #     admin_popup.setWindowTitle("Admin Override")
    #     admin_popup.setWindowModality(Qt.ApplicationModal)
    #     admin_popup.setFixedSize(admin_popup.size())
    #
    #     admin_popup.btn_return_to_youraccount.setIcon(QIcon('Resources/Icons/General_Icons/icon_return_light.svg'))
    #     admin_popup.adminoverride_buttonOverrideAsAdmin.setIcon(QIcon('Resources/Icons/FuncIcons/icon_override.svg'))
    #
    #     return_button = admin_popup.findChild(QPushButton, "btn_return_to_youraccount")
    #     if return_button:
    #         print("-- Found 'Return to Your Account' button")
    #         return_button.clicked.connect(lambda: self.return_to_account_popup(admin_popup))
    #     else:
    #         print("-- Error: 'Return to Your Account' button not found!")
    #
    #     admin_popup.show()

    def show_change_pin_popup(self, first_popup):
        print("-- Navigating to Dashboard > Your Account > Change Pin")
        first_popup.close()
        changepin_popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/changepin.ui", self)
        changepin_popup.setWindowTitle("Change PIN")
        changepin_popup.setWindowModality(Qt.ApplicationModal)
        changepin_popup.setFixedSize(changepin_popup.size())

        changepin_popup.btn_return_to_youraccount.setIcon(QIcon('Resources/Icons/General_Icons/icon_return_light.svg'))
        changepin_popup.acc_buttonConfirmChangePIN_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        # Set up password fields
        current_pin_field = changepin_popup.findChild(QLineEdit, "change_CurrentPIN")
        new_pin_field = changepin_popup.findChild(QLineEdit, "change_NewPIN")
        confirm_pin_field = changepin_popup.findChild(QLineEdit, "change_ConfirmPIN")

        if current_pin_field and new_pin_field and confirm_pin_field:
            # Make them password fields
            current_pin_field.setEchoMode(QLineEdit.Password)
            new_pin_field.setEchoMode(QLineEdit.Password)
            confirm_pin_field.setEchoMode(QLineEdit.Password)

        save_btn = changepin_popup.findChild(QPushButton, "acc_buttonConfirmChangePIN_SaveForm")
        if save_btn and current_pin_field and new_pin_field and confirm_pin_field:
            def confirm_and_save():
                # Retrieve input values
                current_pin = current_pin_field.text().strip()
                new_pin = new_pin_field.text().strip()
                confirm_pin = confirm_pin_field.text().strip()

                # Validate fields
                if not current_pin or not new_pin or not confirm_pin:
                    QMessageBox.warning(changepin_popup, "Validation Error", "All PIN fields must be filled.")
                    for field in [current_pin_field, new_pin_field, confirm_pin_field]:
                        field.setStyleSheet("border: 1px solid red;")
                    return

                if new_pin != confirm_pin:
                    QMessageBox.warning(changepin_popup, "Validation Error", "New PIN and Confirm PIN do not match.")
                    new_pin_field.setStyleSheet("border: 1px solid red;")
                    confirm_pin_field.setStyleSheet("border: 1px solid red;")
                    return

                # Reset borders
                for field in [current_pin_field, new_pin_field, confirm_pin_field]:
                    field.setStyleSheet("border: 1px solid gray;")

                try:
                    connection = Database()
                    cursor = connection.cursor

                    # Fetch current user's hashed PIN from DB
                    cursor.execute("""
                        SELECT SYS_PASSWORD FROM SYSTEM_ACCOUNT 
                        WHERE SYS_USER_ID = %s AND SYS_IS_ACTIVE = TRUE;
                    """, (self.sys_user_id,))
                    result = cursor.fetchone()

                    if not result:
                        QMessageBox.critical(changepin_popup, "Error", "User not found in the system.")
                        return

                    stored_hash = result[0]

                    # Verify current PIN
                    if not bcrypt.verify(current_pin, stored_hash):
                        QMessageBox.warning(changepin_popup, "Incorrect PIN",
                                            "The current PIN you entered is incorrect.")
                        current_pin_field.setStyleSheet("border: 1px solid red;")
                        return

                    # Prevent new PIN == old PIN
                    if bcrypt.verify(new_pin, stored_hash):
                        QMessageBox.warning(changepin_popup, "Invalid Input",
                                            "New PIN cannot be the same as the current PIN.")
                        new_pin_field.setStyleSheet("border: 1px solid red;")
                        confirm_pin_field.setStyleSheet("border: 1px solid red;")
                        return

                    # All checks passed — update the PIN
                    reply = QMessageBox.question(
                        changepin_popup,
                        "Confirm PIN Change",
                        "Are you sure you want to change your PIN?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No
                    )

                    if reply == QMessageBox.Yes:
                        # Hash the new PIN using bcrypt
                        new_hashed_pin = bcrypt.hash(new_pin)

                        # Update in database
                        cursor.execute("""
                            UPDATE SYSTEM_ACCOUNT SET SYS_PASSWORD = %s
                            WHERE SYS_USER_ID = %s;
                        """, (new_hashed_pin, self.sys_user_id))
                        connection.conn.commit()

                        QMessageBox.information(changepin_popup, "Success", "PIN successfully changed!")
                        changepin_popup.close()
                        QApplication.closeAllWindows()
                        self.login_window.show()
                        self.login_window.clear_fields()

                except Exception as e:
                    QMessageBox.critical(changepin_popup, "Database Error", f"Failed to update PIN: {str(e)}")
                finally:
                    if connection:
                        connection.close()

            save_btn.clicked.connect(confirm_and_save)

        return_button = changepin_popup.findChild(QPushButton, "btn_return_to_youraccount")
        if return_button:
            print("-- Found 'Return to Your Account' button")
            return_button.clicked.connect(lambda: self.return_to_account_popup(changepin_popup))
        else:
            print("-- Error: 'Return to Your Account' button not found!")

        changepin_popup.show()

    def return_to_account_popup(self, current_popup):
        print("-- Returning to Dashboard > Your Account")
        current_popup.close()
        self.show_account_popup()