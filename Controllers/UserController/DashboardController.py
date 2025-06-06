from PySide6.QtWidgets import QPushButton, QMessageBox, QApplication, QTableWidgetItem
from PySide6.QtGui import QPixmap, QIcon, Qt
from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup  # Make sure this import exists
from Views.DashboardView import DashboardView
from database import Database


class DashboardController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id):
        super().__init__(login_window, emp_first_name, sys_user_id)

        self.view = DashboardView(self)

        self.sys_user_id = sys_user_id

        print(self.sys_user_id)
        self.dashboard_screen = self.load_ui("Resources/UIs/MainPages/dashboard.ui")
        # self.setWindowTitle(f"{APP_NAME}{self.app_version}")
        # self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
        self.stack.addWidget(self.dashboard_screen)
        self.view.setup_dashboard_ui(self.dashboard_screen)
        self.load_recent_citizens_data()

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

    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.UserController.StatisticsController import StatisticsController
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)



    def goto_institutions_panel(self):
        """Handle navigation to Institutions Panel screen."""
        print("-- Navigating to Institutions")
        if not hasattr(self, 'institutions_panel'):
            from Controllers.UserController.InstitutionController import InstitutionsController
            self.institutions_panel = InstitutionsController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.institutions_panel.institutions_screen)

        self.stack.setCurrentWidget(self.institutions_panel.institutions_screen)

    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions_panel'):
            from Controllers.UserController.TransactionController import TransactionController
            self.transactions_panel = TransactionController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)

    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history_panel'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)

    def logout(self):
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
                ORDER BY C.CTZ_DATE_ENCODED DESC
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
        popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/barangayinfo.ui", self)
        popup.setWindowTitle("Barangay Information")
        popup.brgyinfo_imageLogo.setPixmap(QPixmap("Resources/Images/General_Images/logo_brgyClear.png"))
        popup.setWindowModality(Qt.ApplicationModal)
        popup.setFixedSize(popup.size())
        popup.show()

    def show_aboutsoftware_popup(self):
        print("-- Navigating to Dashboard > About Software")
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
        popup.employeeaccount_buttonAdminOverride.setIcon(QIcon('Resources/Icons/FuncIcons/icon_adminoverride.svg'))

        admin_override_button = popup.findChild(QPushButton, "employeeaccount_buttonAdminOverride")
        if admin_override_button:
            admin_override_button.clicked.connect(lambda: self.show_admin_override_popup(popup))

        change_pin_button = popup.findChild(QPushButton, "employeeaccount_buttonChangePIN")
        if change_pin_button:
            change_pin_button.clicked.connect(lambda: self.show_change_pin_popup(popup))

        popup.show()

    def show_admin_override_popup(self, first_popup):
        print("-- Navigating to Dashboard > Your Account > Admin Override")
        first_popup.close()
        admin_popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/adminoverride.ui", self)
        admin_popup.setWindowTitle("Admin Override")
        admin_popup.setWindowModality(Qt.ApplicationModal)
        admin_popup.setFixedSize(admin_popup.size())

        admin_popup.btn_return_to_youraccount.setIcon(QIcon('Resources/Icons/General_Icons/icon_return_light.svg'))
        admin_popup.adminoverride_buttonOverrideAsAdmin.setIcon(QIcon('Resources/Icons/FuncIcons/icon_override.svg'))

        return_button = admin_popup.findChild(QPushButton, "btn_return_to_youraccount")
        if return_button:
            print("-- Found 'Return to Your Account' button")
            return_button.clicked.connect(lambda: self.return_to_account_popup(admin_popup))
        else:
            print("-- Error: 'Return to Your Account' button not found!")

        admin_popup.show()

    def show_change_pin_popup(self, first_popup):
        print("-- Navigating to Dashboard > Your Account > Change Pin")
        first_popup.close()
        changepin_popup = load_popup("Resources/UIs/PopUp/Screen_Dashboard/changepin.ui", self)
        changepin_popup.setWindowTitle("Change PIN")
        changepin_popup.setWindowModality(Qt.ApplicationModal)
        changepin_popup.setFixedSize(changepin_popup.size())

        changepin_popup.btn_return_to_youraccount.setIcon(QIcon('Resources/Icons/General_Icons/icon_return_light.svg'))
        changepin_popup.acc_buttonConfirmChangePIN_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        # Save final form with confirmation
        save_btn = changepin_popup.findChild(QPushButton, "acc_buttonConfirmChangePIN_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    changepin_popup,
                    "Confirm Registration",
                    "Are you sure to Change your PIN?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(changepin_popup, "Success", "PIN Successfully Changed!")
                    changepin_popup.close()
                    QApplication.closeAllWindows()
                    self.login_window.show()
                    self.login_window.clear_fields()
                    
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