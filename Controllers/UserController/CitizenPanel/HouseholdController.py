from PySide6.QtCore import QDate

from Controllers.BaseFileController import BaseFileController
from Models.HouseholdModel import HouseholdModel
from Views.CitizenPanel.HouseholdView import HouseholdView


class HouseholdController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.model = HouseholdModel()
        self.view = HouseholdView(self)

        # Load UI
        self.cp_household_screen = self.load_ui("Resources/Uis/MainPages/CitizenPanelPages/cp_household.ui")
        self.view.setup_household_ui(self.cp_household_screen)
        self.center_on_screen()

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name

    def show_register_household_popup(self):
        print("-- Register New Household Popup")
        popup = self.view.show_register_household_popup(self)
        popup.exec_()

    def get_current_date(self):
        """Returns today's date as QDate"""
        return QDate.currentDate()

    def validate_date(self, date_string):
        """Validate that the date is not in the future"""
        selected_date = QDate.fromString(date_string, "yyyy-MM-dd")
        if selected_date > QDate.currentDate():
            return False
        return True

    def validate_fields(self):
        form_data = self.view.get_form_data()
        errors = []

        if not form_data['house_number']:
            errors.append("House Number is required")
        if not form_data['sitio_id']:
            errors.append("Sitio is required")
        if not form_data['interviewer_name']:
            errors.append("Interviewer Name is required")
        if not form_data['reviewer_name']:
            errors.append("Reviewer Name is required")
        if not form_data['water_id']:
            errors.append("Water source is required")
        if not form_data['toilet_id']:
            errors.append("Toilet type is required")
        if not form_data['date_of_visit']:
            errors.append("Date of visit cannot be in the future")

        if errors:
            self.view.show_error_message(errors)
            self.view.highlight_missing_fields(errors)
        else:
            self.save_household_data(form_data)

    def save_household_data(self, form_data):
        if not self.view.confirm_registration():
            return

        form_data['home_image_path'] = self.model.image_path

        if self.model.save_household_data(form_data):
            self.view.show_success_message()
            self.view.popup.close()
        else:
            self.view.show_error_dialog("Database error occurred")

    def upload_image(self):
        file_path = self.view.get_file_path()
        if file_path:
            saved_path = self.model.save_image(file_path)
            self.view.show_image_preview(file_path)

    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

        # self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")