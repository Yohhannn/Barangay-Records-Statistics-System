from PySide6.QtCore import QDate, QDateTime, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView

from Controllers.BaseFileController import BaseFileController
from Models.Statistics.HouseholdModel import HouseholdModel


class HouseholdController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/household.ui")
        self.model = HouseholdModel()

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

    #Populate the population per sitio table
    def populate_household_statistics(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_household_stat_per_sitio(from_date, to_date)

            if not result or not result['data']:
                self.view.household_tablePopulationPerStreet.setRowCount(0)
                return

            self._populate_table(
                self.view.household_tablePopulationPerStreet,
                result['columns'],
                result['data']
            )

        except Exception as e:
            self.show_error_message(
                "Household Data Error",
                "Could not load household statistics."
            )
            print(f"Error loading household data: {e}")

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

    def populate_highest_lowest_total_household(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_highest_lowest_total_households(from_date, to_date)

            if not result or not result['data'] or all(row[1] == 0 for row in result['data']):
                self.view.sitio_highest_total.setText("No Data")
                self.view.value_highest_total_household.setText("0")
                self.view.sitio_lowest_total.setText("No Data")
                self.view.total_ave_household_size.setText("0")
                return

            highest = result['data'][0]
            lowest = result['data'][1]

            # Extracting data
            highest_name, highest_count = highest
            lowest_name, lowest_count = lowest

            # Displaying data
            self.view.sitio_highest_total.setText(highest_name)
            self.view.value_highest_total_household.setText(str(highest_count))
            self.view.sitio_lowest_total.setText(lowest_name)
            self.view.total_ave_household_size.setText(str(lowest_count))

        except Exception as e:
            print(f"[ERROR] Failed to display highest/lowest sitio data: {e}")
            self.show_error_message(
                "Household Data Error",
                "Could not load highest and lowest sitio household population statistics."
            )
            self.view.sitio_highest_total.setText("0")
            self.view.value_highest_total_household.setText("0")
            self.view.sitio_lowest_total.setText("0")
            self.view.total_ave_household_size.setText("0")

    def populate_water_source(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_household_water_source(from_date, to_date)
            if not result:
                self.view.total_lvl1.setText("0")
                self.view.total_lvl2.setText("0")
                self.view.total_lvl3.setText("0")
                self.view.total_others.setText("0")
                return

            water_source_mapping = {
                'Level 1 - Point Source': self.view.total_lvl1,
                'Level 2 - Communal Faucet': self.view.total_lvl2,
                'Level 3 - Individual Connection': self.view.total_lvl3,
                'Others':self.view.total_others
            }

            for source, count in result:
                if source in water_source_mapping:
                    water_source_mapping[source].setText(f"{count:,}")

        except Exception as e:
            print(f"[ERROR] Failed to load water source: {e}")
            self.show_error_message(
                "Household Data Error",
                "Could not load water source statistics."
            )

    def populate_household_ownership(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_household_ownership_status(from_date, to_date)

            if not result:
                self.view.total_owned.setText("0")
                self.view.total_rented.setText("0")
                self.view.total_leased.setText("0")
                self.view.total_informal_settlers.setText("0")
                return

            ownership_status_mapping = {
                'Owned': self.view.total_owned,
                'Rented': self.view.total_rented,
                'Leased': self.view.total_leased,
                'Informal Settler': self.view.total_informal_settlers
            }

            for status, count in result:
                if status in ownership_status_mapping:
                    ownership_status_mapping[status].setText(f"{count:,}")

        except Exception as e:
            print(f"[ERROR] Failed to load household ownership: {e}")
            self.show_error_message(
                "Household Data Error",
                "Could not load household ownership statistics."
            )

    def refresh_statistics(self):
        try:
            self.populate_household_statistics()
            self.populate_highest_lowest_total_household()
            self.populate_water_source()
            self.populate_household_ownership()

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
