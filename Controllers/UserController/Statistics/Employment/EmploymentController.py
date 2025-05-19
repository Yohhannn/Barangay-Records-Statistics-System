from PySide6.QtCore import QDate, QDateTime, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView

from Controllers.BaseFileController import BaseFileController
from Models.Statistics.EmploymentModel import EmploymentModel


class EmploymentController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/employment.ui")
        self.model = EmploymentModel()

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
        self.setWindowTitle("MaPro: Neighborhood")
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

    def populate_employment_stat(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_employment_data_per_sitio(from_date, to_date)

            if not result or not result['data']:
                return

            self._populate_table(
                self.view.employment_tablePerStreet,
                result['columns'],
                result['data']
            )

        except Exception as e:
            self.show_error_message(
                "Employment Data Error",
                "Could not load employment status per sitio statistics."
            )
            print(f"Error loading employment status data: {e}")

    #Populate the population per sitio table
    def populate_gov_nongov_overview(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_total_gov_nongov_worker(from_date, to_date)

            if not result:
                self.view.total_gov_worker.setText("No Data")
                self.view.total_nongov_worker.setText("No Data")
                return

            total_gov_workers, total_non_gov_workers = result

            self.view.total_gov_worker.setText(str(total_gov_workers))
            self.view.total_nongov_worker.setText(str(total_non_gov_workers))

        except Exception as e:
            print(f"[ERROR] Failed to display total government and non government workers data: {e}")
            self.show_error_message(
                "Employment Data Error",
                "Could not load total government and non government workers statistics."
            )

    def populate_overall_employment_distribution(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_overall_employment_stats(from_date, to_date)

            if result:
                employed, unemployed, self_employed, not_in_labor_force = result

                self.view.demo_Employed.setText(str(employed))
                self.view.demo_Unemployed.setText(str(unemployed))
                self.view.demo_SelfEmployed.setText(str(self_employed))
                self.view.demo_nilf.setText(str(not_in_labor_force))

        except Exception as e:
            print(f"[ERROR] Failed to display overall employment stats: {e}")
            self.show_error_message(
                "Employment Stats Error",
                "Could not load overall employment statistics."
            )

    def _populate_table(self, table, headers, data):
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setForeground(Qt.black)

                if col_idx > 0:
                    item.setTextAlignment(Qt.AlignCenter)

                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()

        header = table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def refresh_statistics(self):
        try:
            self.populate_employment_stat()
            self.populate_overall_employment_distribution()
            self.populate_gov_nongov_overview()

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
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")
