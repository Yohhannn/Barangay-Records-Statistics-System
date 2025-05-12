from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QPushButton

from Controllers.BaseFileController import BaseFileController
from Models.HistoryModel import HistoryModel
from Utils.util_popup import load_popup
from Views.HistoryRecords.CitizenHistoryView import CitizenHistoryView


class CitizenHistoryController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)


        self.stack = stack
        self.model = HistoryModel()
        self.view = CitizenHistoryView(self)


        self.hist_citizen_history_screen = self.load_ui("Resources/UIs/MainPages/HistoryRecordPages/citizen_history.ui")
        self.view.setup_citizen_history_ui(self.hist_citizen_history_screen)
        # self.view.setup_history_ui(self.hist_citizen_history_screen)
        self.center_on_screen()

        self.popup = None

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name


    def show_citizen_history_initialize(self):
        pass




    def goto_history_panel(self):
        """Handle navigation to History Records Panel screen."""
        print("-- Navigating to History Records")
        if not hasattr(self, 'history'):
            from Controllers.UserController.HistoryRecordsController import HistoryRecordsController
            self.history_panel = HistoryRecordsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.history_panel.history_screen)

        self.stack.setCurrentWidget(self.history_panel.history_screen)