from PySide6.QtCore import QDate, QDateTime, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView

from Controllers.BaseFileController import BaseFileController
from Models.Statistics.InfrastructureModel import InfrastructureModel


class InfrastructureController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/infrastructure.ui")
        self.model = InfrastructureModel()

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
        self.setWindowTitle("MaPro: Infrastructure")
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

    def populate_sitio_infrastructure_distribution(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_total_sitio_infrastructure(from_date, to_date)

            if not result or not result['data']:
                return

            self._populate_table(
                self.view.infra_table,
                result['columns'],
                result['data']
            )

        except Exception as e:
            self.show_error_message(
                "Infrastructure Data Error",
                "Could not load total Infrastructure date per sitio."
            )
            print(f"Error loading Infrastructure date per sitio: {e}")

    def populate_infrastructure_type_distribution(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_total_infrastructure_type(from_date, to_date)

            if not result or not result['data']:
                return

            self._populate_table(
                self.view.infra_table_2,
                result['columns'],
                result['data']
            )

        except Exception as e:
            self.show_error_message(
                "Infrastructure Data Error",
                "Could not load total Infrastructure types ."
            )
            print(f"Error loading Infrastructure types: {e}")

    #Populate the population per sitio table
    def populate_total_infrastructures(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_total_infrastructures(from_date, to_date)

            if not result:
                self.view.total_public_infra.setText("No Data")
                self.view.total_private_infra.setText("No Data")
                self.view.total_infrastructures.setText("No Data")
                return

            total_public, total_private, total_infra = result

            self.view.total_public_infra.setText(str(total_public))
            self.view.total_private_infra.setText(str(total_private))
            self.view.total_infrastructures.setText(str(total_infra))

        except Exception as e:
            print(f"[ERROR] Failed to display total infrastructures: {e}")
            self.show_error_message(
                "Infrastructure Data Error",
                "Could not load total infrastructures"
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
            self.populate_infrastructure_type_distribution()
            self.populate_sitio_infrastructure_distribution()
            self.populate_total_infrastructures()

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
