from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class services_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.trans_services_screen = self.load_ui("UI/MainPages/TransactionPages/services.ui")
        self.setup_services_ui()
        self.center_on_screen()

    def setup_services_ui(self):
        """Setup the Services UI layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Services")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.trans_services_screen.btn_returnToTransactionPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))
        self.trans_services_screen.inst_BusinessName_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
        self.trans_services_screen.trans_Transact_button_create.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
        self.trans_services_screen.trans_Transact_button_update.setIcon(QIcon('Assets/FuncIcons/icon_edit.svg'))
        self.trans_services_screen.trans_Transact_button_remove.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))
        self.trans_services_screen.transactionList_buttonFilter.setIcon(QIcon('Assets/FuncIcons/icon_filter.svg'))

        # REGISTER BUTTON
        self.trans_services_screen.trans_Transact_button_create.clicked.connect(self.show_transaction_popup)

        # Return Button
        self.trans_services_screen.btn_returnToTransactionPage.clicked.connect(self.goto_transactions_panel)

    def show_transaction_popup(self):
        print("-- Create Transaction Popup")
        popup = load_popup("UI/PopUp/Screen_Transactions/create_transaction.ui", self)
        popup.setWindowTitle("Mapro: Create New Transaction")
        popup.setFixedSize(popup.size())

        popup.register_buttonConfirmTransaction_SaveForm.setIcon(QIcon('Assets/FuncIcons/icon_confirm.svg'))

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "register_buttonConfirmTransaction_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Creation",
                    "Are you sure you want to create this transaction?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "Transaction successfully registered!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()


    def goto_transactions_panel(self):
        """Handle navigation to Transactions Panel screen."""
        print("-- Navigating to Transactions")
        if not hasattr(self, 'transactions'):
            from Functions.Main.Transactions.transaction_func import transaction_func
            self.transactions_panel = transaction_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.transactions_panel.transactions_screen)

        self.stack.setCurrentWidget(self.transactions_panel.transactions_screen)
        self.setWindowTitle("MaPro: Transactions")