from PySide6.QtCore import QDate, QDateTime, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView

from Controllers.BaseFileController import BaseFileController
from Models.Statistics.HealthModel import HealthModel


class HealthController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/health.ui")
        self.model = HealthModel()

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
        self.setWindowTitle("MaPro: Health")
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

    def populate_health_risk_group_overview(self):
        from_date, to_date = self.get_date_range()

        try:
            result = self.model.get_health_risk_group_data(from_date, to_date)
            if not result:
                self.view.total_P.setText("No data")
                self.view.total_AP.setText("No data")
                self.view.total_PP.setText("No data")
                self.view.total_I.setText("No data")
                self.view.total_Under.setText("No data")
                self.view.total_PWD.setText("No data")
                return

            risk_group_mapping = {
                'Pregnant': self.view.total_P,
                'Adolescent Pregnant': self.view.total_AP,
                'Postpartum': self.view.total_PP,
                'Infant': self.view.total_I,
                'Under 5 Years Old': self.view.total_Under,
                'Person With Disability': self.view.total_PWD
            }

            for type, count in result:
                if type in risk_group_mapping:
                    risk_group_mapping[type].setText(f"{count:,}")

        except Exception as e:
            self.show_error_message(
                "Employment Data Error",
                "Could not load employment status per sitio statistics."
            )
            print(f"Error loading employment status data: {e}")


    def populate_blood_type_distribution(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_blood_type_distribution(from_date, to_date)

            if not result:
                self.view.total_blood_pos_a.setText("No Data")
                self.view.total_blood_pos_b.setText("No Data")
                self.view.total_blood_pos_o.setText("No Data")
                self.view.total_blood_pos_ab.setText("No Data")
                self.view.total_blood_neg_a.setText("No Data")
                self.view.total_blood_neg_b.setText("No Data")
                self.view.total_blood_neg_ab.setText("No Data")
                self.view.total_blood_unknown.setText("No Data")
                return

            blood_type_mapping = {
                'A+': self.view.total_blood_pos_a,
                'B+': self.view.total_blood_pos_b,
                'O+': self.view.total_blood_pos_o,
                'AB+': self.view.total_blood_pos_ab,
                'A-': self.view.total_blood_neg_a,
                'B-': self.view.total_blood_neg_b,
                'O-': self.view.total_blood_neg_o,
                'AB-': self.view.total_blood_neg_ab,
                'Unknown': self.view.total_blood_unknown
            }

            for type, count in result:
                if type in blood_type_mapping:
                    blood_type_mapping[type].setText(f"{count:,}")

        except Exception as e:
            print(f"[ERROR] Failed to display blood type data: {e}")
            self.show_error_message(
                "Health Stats Error",
                "Could not load total blood type statistics."
            )

    def populate_total_gender_with_med_record(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_total_gender_with_med_record(from_date, to_date)

            if not result:
                return

            male_total = 0
            female_total = 0
            for gender, total in result:
                if gender == 'M':
                    male_total = total
                elif gender == 'F':
                    female_total = total


            self.view.total_female_record.setText(str(female_total))
            self.view.total_male_record.setText(str(male_total))
            self.view.overall_total.setText(str(female_total + male_total))

        except Exception as e:
            print(f"[ERROR] Failed to display total gender with medical records: {e}")
            self.show_error_message(
                "Health Stats Error",
                "Could not load total gender with medical records."
            )

    def populate_philhealth_distribution(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_philhealth_categories(from_date, to_date)

            if not result:
                self.view.total_FEP.setText("No Data")
                self.view.total_FEG.setText("No Data")
                self.view.total_IE.setText("No Data")
                self.view.total_NHTS.setText("No Data")
                self.view.total_SC.setText("No Data")
                self.view.total_IP.setText("No Data")
                self.view.total_U.setText("No Data")
                return

            phil_category_mapping = {
                'Formal Economy Private': self.view.total_FEP,
                'Formal Economy Government': self.view.total_FEG,
                'Informal Economy': self.view.total_IE,
                'NHTS': self.view.total_NHTS,
                'Senior Citizen': self.view.total_SC,
                'Indigenous People': self.view.total_IP,
                'Unknown': self.view.total_U
            }

            for category, count in result:
                if category in phil_category_mapping:
                    phil_category_mapping[category].setText(f"{count:,}")

        except Exception as e:
            print(f"[ERROR] Failed to display blood type data: {e}")
            self.show_error_message(
                "Health Stats Error",
                "Could not load total blood type statistics."
            )
    
    def populate_top_5_medical_cases(self):
        from_date, to_date = self.get_date_range()
        try:
            result = self.model.get_top_5_medical_case(from_date, to_date)

            # if not result:
            #     raise ValueError('No Medical Cases found: ',  )

            label_list = [
                self.view.common_med_case_1st,
                self.view.common_med_case_2nd,
                self.view.common_med_case_3rd,
                self.view.common_med_case_4th,
                self.view.common_med_case_5th,
            ]


            for i in range(5):
                if i < len(result):
                    mht_type, total = result[i]
                    label_list[i].setText(f"{mht_type} ({total:,})")
                else:
                    label_list[i].setText("No Data (0)")

        except Exception as e:
            print(f"[ERROR] Failed to display top 5 ranking medical history cases: {e}")
            self.show_error_message(
                "Health Stats Error",
                "Could not load top 5 ranking medical history cases."
            )

    def refresh_statistics(self):
        try:
            self.populate_health_risk_group_overview()
            self.populate_blood_type_distribution()
            self.populate_total_gender_with_med_record()
            self.populate_philhealth_distribution()
            self.populate_top_5_medical_cases()
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
