from PySide6.QtCore import QDate, QDateTime, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView

from Controllers.BaseFileController import BaseFileController
from Models.Statistics.BusinessModel import BusinessModel


class BusinessController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.user_role = user_role
        
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/business.ui")
        self.model = BusinessModel()

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
        self.setWindowTitle("MaPro: Business")
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
    def populate_business_statistics(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_business_stat_per_sitio(from_date, to_date)

            if not result or not result['data']:
                self.view.business_table_stat_per_street.setRowCount(0)
                return

            self._populate_table(
                self.view.business_table_stat_per_street,
                result['columns'],
                result['data']
            )

        except Exception as e:
            self.show_error_message(
                "Household Data Error",
                "Could not load business statistics."
            )
            print(f"Error loading business data: {e}")

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



    def populate_active_business_type_stat(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_active_business_type(from_date, to_date)
            if not result:
                self.view.total_Sole.setText("No data")
                self.view.total_Partnership.setText("No data")
                self.view.total_Corp.setText("No data")
                self.view.total_Coop.setText("No data")
                self.view.total_Franchise.setText("No data")
                self.view.total_Others.setText("No data")
                return

            bst_mapping = {
                'Sole Proprietorship': self.view.total_Sole,
                'Partnership': self.view.total_Partnership,
                'Corporation': self.view.total_Corp,
                'Cooperative': self.view.total_Coop,
                'Franchise': self.view.total_Franchise,
                'Others': self.view.total_Others
            }

            for type, count in result:
                if type in bst_mapping:
                    bst_mapping[type].setText(f"{count:,}")

        except Exception as e:
            print(f"[ERROR] Failed to load active business type data: {e}")
            self.show_error_message(
                "Business Data Error",
                "Could not load active business type statistics."
            )



    def refresh_statistics(self):
        try:
            self.populate_business_statistics()
            self.populate_active_business_type_stat()

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
            self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.sys_user_id, self.user_role, self.stack)
            self.stack.addWidget(self.statistics_panel.statistics_screen)

        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
        self.setWindowTitle("MaPro: Statistics")
