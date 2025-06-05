from PySide6.QtCore import QDate, QDateTime, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView

from Controllers.BaseFileController import BaseFileController
from Models.Statistics.EducationModel import EducationModel


class EducationController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/education.ui")
        self.model = EducationModel()

        # Initialize UI and data
        self.setup_view()
        self.setup_connections()
        self.refresh_statistics()
        self._setup_date()
        self._setup_time()

    def setup_connections(self):
        self.view.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics_panel)
        self.view.filter_stat_date_button.clicked.connect(self.refresh_statistics)

    def setup_view(self):
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Education")
        self.setWindowIcon(QIcon("Resources/AppIcons/appicon_active_u.ico"))

        # Set images and icons
        self.view.btn_returnToStatisticsPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))

        # Initialize date filters
        today = QDate.currentDate()
        one_year_ago = today.addYears(-1)

        self.view.filter_date_min.setDate(one_year_ago)
        self.view.filter_date_max.setDate(today)
        self.view.filter_date_min.setMaximumDate(today)
        self.view.filter_date_max.setMaximumDate(today)
        self.view.filter_date_min.setDisplayFormat("yyyy-MM-dd")
        self.view.filter_date_max.setDisplayFormat("yyyy-MM-dd")

    #Populate the population per sitio table
    def populate_students_and_not_overview(self):
        from_date, to_date = self.get_date_range()
        self.view.total_students.setStyleSheet("color: black;")
        self.view.total_non_students.setStyleSheet("color: black;")

        try:
            result = self.model.get_total_students_and_not(from_date, to_date)

            if not result:
                self.view.total_students.setText("No Data")
                self.view.total_non_students.setText("No Data")
                return
            self.view.total_students.setStyleSheet("color: black;")  # or any visible color
            self.view.total_non_students.setStyleSheet("color: black;")

            total_currently_studying, total_not_currently_studying = result

            self.view.total_students.setText(
                f"{total_currently_studying:,}" if total_currently_studying is not None else "0")
            self.view.total_non_students.setText(
                f"{total_not_currently_studying:,}" if total_not_currently_studying is not None else "0")

        except Exception as e:
            print(f"[ERROR] Failed to display total students or not students data: {e}")
            self.show_error_message(
                "Education Data Error",
                "Could not load total students and not students statistics."
            )

    def populate_educational_attainment_stats(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_all_educational_attainment_stats(to_date)

            attainment_mapping = {
                'No Formal Education': self.view.educ_attainment_nfe,
                'Kindergarten': self.view.educ_attainment_kinder,
                'Elementary Undergraduate': self.view.educ_attainment_eu,
                'Elementary Graduate': self.view.educ_attainment_eg,
                'Junior High School Undergraduate': self.view.educ_attainment_jhsu,
                'Junior High School Graduate': self.view.educ_attainment_jhsg,
                'Senior High School Undergraduate': self.view.educ_attainment_shsu,
                'Senior High School Graduate': self.view.educ_attainment_shsg,
                'Vocational / Technical Graduate': self.view.educ_attainment_vocational,
                'College Undergraduate': self.view.educ_attainment_cu,
                'College Graduate': self.view.educ_attainment_cg,
                'Postgraduate': self.view.educ_attainment_postgraduate
            }

            # Set all labels to 0 first
            for label in attainment_mapping.values():
                label.setText("0")

            # Update labels with actual data
            for attainment, count in result:
                if attainment in attainment_mapping:
                    attainment_mapping[attainment].setText(str(count))

        except Exception as e:
            print(f"[ERROR] Failed to display educational attainment stats: {e}")
            self.show_error_message(
                "Education Stats Error",
                "Could not load educational attainment statistics."
            )

    def refresh_statistics(self):
        try:
            self.populate_students_and_not_overview()
            self.populate_educational_attainment_stats()

        except Exception as e:
            self.show_error_message(
                "Refresh Error",
                "Failed to refresh statistics data."
            )
            print(f"Error refreshing statistics: {e}")

    #Get and validate the selected date range
    def get_date_range(self):
        from_date = self.view.filter_date_min.date().toPython()
        to_date = self.view.filter_date_max.date().toPython()

        # Validate date range
        if from_date > to_date:
            self.show_error_message(
                "Invalid Date Range",
                "The 'From' date must be earlier than or equal to the 'To' date."
            )

        return from_date, to_date

    def show_error_message(self, title, message):
        QMessageBox.critical(
            self,
            title,
            message,
            QMessageBox.Ok
        )

    def _setup_time(self):
        self.timer = QTimer(self.view)

        # Initialize with current date/time
        self._setup_date()

        # Connect timer to update function
        self.timer.timeout.connect(self._setup_date)
        self.timer.start(1000)  # Update every second

    def _setup_date(self):
        """Update both date and time labels"""
        current_datetime = QDateTime.currentDateTime()

        # Update date label
        formatted_date = current_datetime.toString("MMMM d, yyyy")
        day_of_week = current_datetime.toString("dddd")
        self.view.text_date.setText(f"{formatted_date} - {day_of_week}")

        # Update time label
        formatted_time = current_datetime.toString("h:mm:ss AP")
        self.view.text_time.setText(formatted_time)

    def goto_statistics_panel(self):
        """Handle navigation to Statistics Panel screen."""
        print("-- Navigating to Statistics")
        if not hasattr(self, 'statistics_panel'):
            from Controllers.UserController.StatisticsController import StatisticsController
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.sys_user_id, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")
