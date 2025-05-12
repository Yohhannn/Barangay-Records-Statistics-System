from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton

from Controllers.BaseFileController import BaseFileController
from Utils.util_popup import load_popup

class MedicalHistoryController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.hist_medical_history_screen = self.load_ui("Resources/UIs/MainPages/HistoryRecordPages/medical_history.ui")
        self.setup_medical_history_ui()
        self.center_on_screen()

    def setup_medical_history_ui(self):
        """Setup the Medical History Views layout."""
        self.setFixedSize(1350, 850)
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_medical_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.hist_medical_history_screen.histrecMedHistoryID_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_record.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.hist_medical_history_screen.histrec_medicalhistory_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        self.hist_medical_history_screen.medicalhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_medical_history_screen.histrec_medicalhistory_button_record.clicked.connect(self.show_medical_history_popup)

        # Return Button
        self.hist_medical_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.goto_history_panel)

    def show_medical_history_popup(self):
        print("-- Record Medical History Popup")
        popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_medical_history.ui", self)
        popup.setWindowTitle("Mapro: Record New Medical History")
        popup.setFixedSize(popup.size())

        popup.record_buttonConfirmMedicalHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

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
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)