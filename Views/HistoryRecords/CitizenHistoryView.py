from PySide6.QtGui import QPixmap, QIcon, Qt
import cv2
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QButtonGroup, QRadioButton, QStackedWidget
from Controllers.BaseFileController import BaseFileController
from Models.CitizenModel import CitizenModel
from Views.CitizenPanel.CitizenView import CitizenView
from Utils.util_popup import load_popup


class CitizenHistoryView:
    def __init__(self, controller):
        self.controller = controller

        self.popup = None

        self.hist_citizen_history_screen = None

    def show_citizen_history_popup(self):
        print("-- Record Citizen History Popup")
        popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_citizen_history.ui")
        popup.setWindowTitle("Mapro: Record New Citizen History")
        popup.setFixedSize(popup.size())

        popup.record_buttonConfirmCitizenHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "record_buttonConfirmCitizenHistory_SaveForm")
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
                    QMessageBox.information(popup, "Success", "Citizen History Successfully Recorded!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()




    def setup_citizen_history_ui(self, ui_screen):
        self.hist_citizen_history_screen = ui_screen

        """Setup the Citizen History Views layout."""
        ui_screen.setFixedSize(1350, 850)
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

    # Set images and icons
        self.hist_citizen_history_screen.btn_returnToHistoryRecordPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.hist_citizen_history_screen.histrec_HistoryID_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_record.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.hist_citizen_history_screen.histrec_citizenhistory_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        self.hist_citizen_history_screen.citizenhistoryList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # RECORD BUTTON
        self.hist_citizen_history_screen.histrec_citizenhistory_button_record.clicked.connect(self.show_citizen_history_popup)

        # Return Button
        self.hist_citizen_history_screen.btn_returnToHistoryRecordPage.clicked.connect(self.controller.goto_history_panel)
        self.hist_citizen_history_screen.histrec_tableView_List_RecordCitizenHistory.cellClicked.connect(self.controller.handle_row_click_citizen_history)
