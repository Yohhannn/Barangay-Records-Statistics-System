from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton

from Controllers.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class medical_history_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.hist_medical_history_screen = self.load_ui("Views/MainPages/HistoryRecordPages/medical_history.ui")
        self.setup_medical_history_ui()
        self.center_on_screen()

    def setup_medical_history_ui(self):
        """Setup the Medical History Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_medical_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Resources/FuncIcons/img_return.png'))
        self.hist_medical_history_screen.histrecMedHistoryID_buttonSearch.setIcon(QIcon('Resources/FuncIcons/icon_search_w.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_record.setIcon(QIcon('Resources/FuncIcons/icon_add.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_update.setIcon(QIcon('Resources/FuncIcons/icon_edit.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_remove.setIcon(QIcon('Resources/FuncIcons/icon_del.svg'))
        self.hist_medical_history_screen.medicalhistoryList_buttonFilter.setIcon(QIcon('Resources/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_medical_history_screen.histrec_medicalhistory_button_record.clicked.connect(self.show_medical_history_popup)

        # Return Button
        self.hist_medical_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)

    def show_medical_history_popup(self):
        print("-- Record Medical History Popup")
        popup = load_popup("Views/PopUp/Screen_HistoryRecords/record_medical_history.ui", self)
        popup.setWindowTitle("Mapro: Record New Medical History")
        popup.setFixedSize(popup.size())

        popup.record_buttonConfirmMedicalHistory_SaveForm.setIcon(QIcon('Resources/FuncIcons/icon_confirm.svg'))

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "record_buttonConfirmMedicalHistory_SaveForm")
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
                    QMessageBox.information(popup, "Success", "Medical History Successfully Recorded!")
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