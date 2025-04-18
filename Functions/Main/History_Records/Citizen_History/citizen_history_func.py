from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class citizen_history_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.hist_citizen_history_screen = self.load_ui("UI/MainPages/HistoryRecordPages/citizen_history.ui")
        self.setup_citizen_history_ui()
        self.center_on_screen()

    def setup_citizen_history_ui(self):
        """Setup the Citizen History UI layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_citizen_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))
        self.hist_citizen_history_screen.histrec_HistoryID_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_record.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_update.setIcon(QIcon('Assets/FuncIcons/icon_edit.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_remove.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))
        self.hist_citizen_history_screen.citizenhistoryList_buttonFilter.setIcon(QIcon('Assets/FuncIcons/icon_filter.svg'))

        # # REGISTER BUTTON
        # self.hist_citizen_history_screen.trans_Transact_button_create.clicked.connect(self.show_citizen_history_popup)

        # Return Button
        self.hist_citizen_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)

    # def show_citizen_history_popup(self):
    #     print("-- Create Citizen History Popup")
    #     popup = load_popup("UI/PopUp/Screen_Transactions/create_transaction.ui", self)
    #     popup.setWindowTitle("Mapro: Create New Transaction")
    #
    #     popup.register_buttonConfirmTransaction_SaveForm.setIcon(QIcon('Assets/FuncIcons/icon_confirm.svg'))
    #
    #     # Save final form with confirmation
    #     save_btn = popup.findChild(QPushButton, "register_buttonConfirmTransaction_SaveForm")
    #     if save_btn:
    #         def confirm_and_save():
    #             reply = QMessageBox.question(
    #                 popup,
    #                 "Confirm Creation",
    #                 "Are you sure you want to create this transaction?",
    #                 QMessageBox.Yes | QMessageBox.No,
    #                 QMessageBox.No
    #             )
    #
    #             if reply == QMessageBox.Yes:
    #                 print("-- Form Submitted")
    #                 QMessageBox.information(popup, "Success", "Transaction successfully registered!")
    #                 popup.close()
    #
    #         save_btn.clicked.connect(confirm_and_save)
    #
    #     popup.setWindowModality(Qt.ApplicationModal)
    #     popup.show()


    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Functions.Main.History_Records.history_func import history_func
            self.history_panel = history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)