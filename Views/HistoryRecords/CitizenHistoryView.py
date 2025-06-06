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
        self.popup = load_popup("Resources/UIs/PopUp/Screen_HistoryRecords/record_citizen_history.ui")
        self.popup.setWindowTitle("Mapro: Record New Citizen History")
        self.popup.setFixedSize(self.popup.size())

        self.popup.record_buttonConfirmCitizenHistory_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.record_buttonConfirmCitizenHistory_SaveForm.clicked.connect(self.validate_citizen_hist_fields)
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.exec_()

    def validate_citizen_hist_fields(self):
        errors = []

        # Validate Citizen ID
        if not self.popup.record_citizenIDANDsearch.text().strip():
            errors.append("Info citizen ID is required")
            self.popup.record_citizenIDANDsearch.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_citizenIDANDsearch.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Citizen History Type
        if self.popup.record_comboBox_citizenhistory_type.currentIndex() == -1:
            errors.append("Medical history type is required")
            self.popup.record_comboBox_citizenhistory_type.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_comboBox_citizenhistory_type.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Validate Citizen Record Description
        if not self.popup.record_citizenhistory_description.toPlainText().strip():
            errors.append("Medical description is required")
            self.popup.record_citizenhistory_description.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.popup.record_citizenhistory_description.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if errors:
            QMessageBox.warning(
                self.popup,
                "Incomplete Form",
                "Please complete all required fields:\n\n• " + "\n• ".join(errors)
            )
        else:
            self.confirm_and_save()

    def confirm_and_save(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Record",
            "Are you sure you want to record this citizen history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print("-- Form Submitted")
            QMessageBox.information(self.popup, "Success", "Citizen History successfully recorded!")
            self.popup.close()
            self.controller.load_citizen_history_data()




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
