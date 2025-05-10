from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton

from Controllers.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class settlement_history_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.hist_settlement_history_screen = self.load_ui("Views/MainPages/HistoryRecordPages/settlement_history.ui")
        self.setup_settlement_history_ui()
        self.center_on_screen()

    def setup_settlement_history_ui(self):
        """Setup the Settlement History Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_settlement_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Resources/FuncIcons/img_return.png'))
        self.hist_settlement_history_screen.histrec_SettlementID_buttonSearch.setIcon(QIcon('Resources/FuncIcons/icon_search_w.svg'))
        self.hist_settlement_history_screen.histrec_settlementhistory_button_record.setIcon(QIcon('Resources/FuncIcons/icon_add.svg'))
        self.hist_settlement_history_screen.histrec_settlementhistory_button_update.setIcon(QIcon('Resources/FuncIcons/icon_edit.svg'))
        self.hist_settlement_history_screen.histrec_settlementhistory_button_remove.setIcon(QIcon('Resources/FuncIcons/icon_del.svg'))
        self.hist_settlement_history_screen.settlementhistoryList_buttonFilter.setIcon(QIcon('Resources/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_settlement_history_screen.histrec_settlementhistory_button_record.clicked.connect(self.show_settlement_history_popup)

        # Return Button
        self.hist_settlement_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)


    def show_settlement_history_popup(self):
        print("-- Record Settlement History Popup")
        popup = load_popup("Views/PopUp/Screen_HistoryRecords/record_settlement_history.ui", self)
        popup.setWindowTitle("Mapro: Record New Settlement History")
        popup.setFixedSize(popup.size())

        popup.record_buttonConfirmSettlementHistory_SaveForm.setIcon(QIcon('Resources/FuncIcons/icon_confirm.svg'))

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "record_buttonConfirmSettlementHistory_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Creation",
                    "Are you sure you want to record this?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "Settlement History Successfully Recorded!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()


    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.MainController.History_Records.history_func import history_func
            self.history_panel = history_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)