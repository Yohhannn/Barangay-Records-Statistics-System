from PySide6.QtCore import QDate, QDateTime, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox

from Controllers.BaseFileController import BaseFileController
from Models.Statistics.DemographicModel import DemographicModel


class DemographicsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/demographic.ui")
        self.model = DemographicModel()

        # Initialize UI and data
        self.setup_view()
        self.setup_connections()
        self.refresh_statistics()
        self._setup_date()
        self._setup_time()

    def setup_view(self):
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Demographics")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set icons
        icons = {
            'btn_returnToStatisticsPage': 'Resources/Icons/FuncIcons/img_return.png',
            'icon_male': 'Resources/Icons/Icons/General_Icons/icon_male.png',
            'icon_female': 'Resources/Icons/Icons/General_Icons/icon_female.png'
        }
        for widget, path in icons.items():
            getattr(self.view, widget).setIcon(QIcon(path))

        # Initialize date filters
        today = QDate.currentDate()
        one_year_ago = today.addYears(-1)

        self.view.filter_date_min.setDate(one_year_ago)
        self.view.filter_date_max.setDate(today)
        self.view.filter_date_min.setMaximumDate(today)
        self.view.filter_date_max.setMaximumDate(today)
        self.view.filter_date_min.setDisplayFormat("yyyy-MM-dd")
        self.view.filter_date_max.setDisplayFormat("yyyy-MM-dd")

    def setup_connections(self):
        self.view.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics_panel)
        self.view.filter_stat_date_button.clicked.connect(self.refresh_statistics)

    def show_error_message(self, title, message):
        QMessageBox.critical(
            self,
            title,
            message,
            QMessageBox.Ok
        )

    def refresh_statistics(self):
        try:
            self.populate_population_overview()
            self.populate_age_group()
            self.populate_voter_statistics()
            self.populate_socio_economic_distribution()
            self.populate_civil_status_distribution()
            self.populate_religion_distribution()
        except Exception as e:
            self.show_error_message(
                "Data Loading Error",
                "Failed to refresh statistics. Please try again later."
            )
            print(f"Error refreshing statistics: {e}")

    #Get and validate the selected date range
    def get_date_range(self):
        from_date = self.view.filter_date_min.date().toPython()
        to_date = self.view.filter_date_max.date().toPython()

        # Validate date range
        if from_date > to_date:
            from_date, to_date = to_date, from_date
            self.view.filter_date_min.setDate(to_date)
            self.view.filter_date_max.setDate(from_date)

        return from_date, to_date

    #Update population overview statistics
    def populate_population_overview(self):
        from_date, to_date = self.get_date_range()
        try:
            male, female, ip_count, deceased = self.model.get_population_counts(from_date, to_date)

            self.view.demo_TotalMale.setText(f"{male:,}")
            self.view.demo_TotalFemale.setText(f"{female:,}")
            self.view.demo_TotalPopulation.setText(f"{male + female:,}")
            self.view.total_indppl.setText(f"{ip_count:,}")
            self.view.total_deceased.setText(f"{deceased:,}")
        except Exception as e:
            self.reset_population_overview()
            self.show_error_message(
                "Population Data Error",
                "Could not load population statistics. Showing default values."
            )
            print(f"Error loading population data: {e}")

    #Reset population overview to default/empty values
    def reset_population_overview(self):
        self.view.demo_TotalMale.setText("0")
        self.view.demo_TotalFemale.setText("0")
        self.view.demo_TotalPopulation.setText("0")
        self.view.total_indppl.setText("0")
        self.view.total_deceased.setText("0")

    #Update age group statistics
    def populate_age_group(self):
        from_date, to_date = self.get_date_range()
        try:
            age_counts = self.model.get_age_group_counts(from_date, to_date)
            if len(age_counts) != 6:
                raise ValueError("Unexpected number of age groups returned")

            labels = [
                self.view.demo_TotalChild,
                self.view.demo_TotalMinors,
                self.view.demo_TotalYoungAdults,
                self.view.demo_TotalAdults,
                self.view.demo_TotalMiddleAges,
                self.view.demo_TotalSeniors
            ]

            for label, count in zip(labels, age_counts):
                label.setText(f"{count:,}")
        except Exception as e:
            self.reset_age_groups()
            self.show_error_message(
                "Age Group Data Error",
                "Could not load age group statistics. Showing default values."
            )
            print(f"Error loading age group data: {e}")

    def reset_age_groups(self):
        age_labels = [
            self.view.demo_TotalChild,
            self.view.demo_TotalMinors,
            self.view.demo_TotalYoungAdults,
            self.view.demo_TotalAdults,
            self.view.demo_TotalMiddleAges,
            self.view.demo_TotalSeniors
        ]
        for label in age_labels:
            label.setText("0")

    #Update civil status distribution statistics
    def populate_civil_status_distribution(self):
        from_date, to_date = self.get_date_range()

        # Reset all values first
        self.reset_civil_status_distribution()

        try:
            civil_status_data = self.model.get_civil_status_distribution(from_date, to_date)
            if not civil_status_data:
                return

            status_mapping = {
                "Single": {
                    'male': self.view.demo_TotalSingle_male,
                    'female': self.view.demo_TotalSingle_female,
                    'total': self.view.demo_TotalSingle
                },
                "Married": {
                    'male': self.view.demo_TotalMarried_male,
                    'female': self.view.demo_TotalMarried_female,
                    'total': self.view.demo_TotalMarried
                },
                "Widowed": {
                    'male': self.view.demo_TotalWidowed_male,
                    'female': self.view.demo_TotalWidowed_female,
                    'total': self.view.demo_TotalWidowed
                },
                "Divorced": {
                    'male': self.view.demo_TotalDivorced_male,
                    'female': self.view.demo_TotalDivorced_female,
                    'total': self.view.demo_TotalDivorced
                }
            }

            for status, male, female, total in civil_status_data:
                if status in status_mapping:
                    status_mapping[status]['male'].setText(f"{male:,}")
                    status_mapping[status]['female'].setText(f"{female:,}")
                    status_mapping[status]['total'].setText(f"{total:,}")
        except Exception as e:
            self.show_error_message(
                "Civil Status Error",
                "Could not load civil status distribution data."
            )
            print(f"Error loading civil status data: {e}")

    def reset_civil_status_distribution(self):
        status_widgets = [
            ('Single', self.view.demo_TotalSingle_male, self.view.demo_TotalSingle_female, self.view.demo_TotalSingle),
            ('Married', self.view.demo_TotalMarried_male, self.view.demo_TotalMarried_female,
             self.view.demo_TotalMarried),
            ('Widowed', self.view.demo_TotalWidowed_male, self.view.demo_TotalWidowed_female,
             self.view.demo_TotalWidowed),
            ('Divorced', self.view.demo_TotalDivorced_male, self.view.demo_TotalDivorced_female,
             self.view.demo_TotalDivorced)
        ]

        for status, male_widget, female_widget, total_widget in status_widgets:
            male_widget.setText("0")
            female_widget.setText("0")
            total_widget.setText("0")

    #Update voter statistics
    def populate_voter_statistics(self):
        from_date, to_date = self.get_date_range()
        try:
            stats = self.model.get_voter_statistics(from_date, to_date)
            if len(stats) != 9:  # Verify we got all expected values
                raise ValueError("Unexpected number of voter statistics returned")

            (
                age_15_17, age_18_25, age_26_35,
                age_36_59, age_60_above,
                total_registered, total_unregistered,
                male_voters, female_voters
            ) = stats

            self.view.voter_15_17.setText(f"{age_15_17:,}")
            self.view.voter_18_25.setText(f"{age_18_25:,}")
            self.view.voter_26_35.setText(f"{age_26_35:,}")
            self.view.voter_36_59.setText(f"{age_36_59:,}")
            self.view.voter_60P.setText(f"{age_60_above:,}")

            self.view.voter_registered.setText(f"{total_registered:,}")
            self.view.voter_unregistered.setText(f"{total_unregistered:,}")

            self.view.voter_totalmale.setText(f"{male_voters:,}")
            self.view.voter_totalfemale.setText(f"{female_voters:,}")
        except Exception as e:
            self.reset_voter_statistics()
            self.show_error_message(
                "Voter Data Error",
                "Could not load voter statistics. Showing default values."
            )
            print(f"Error loading voter statistics: {e}")

    def reset_voter_statistics(self):
        voter_widgets = [
            self.view.voter_15_17,
            self.view.voter_18_25,
            self.view.voter_26_35,
            self.view.voter_36_59,
            self.view.voter_60P,
            self.view.voter_registered,
            self.view.voter_unregistered,
            self.view.voter_totalmale,
            self.view.voter_totalfemale
        ]

        for widget in voter_widgets:
            widget.setText("0")

    #Update socio-economic distribution statistics
    def populate_socio_economic_distribution(self):
        from_date, to_date = self.get_date_range()

        self.reset_socio_economic_distribution()

        try:
            data = self.model.get_socio_economic_distribution(from_date, to_date)
            if not data:
                return

            status_mapping = {
                'NHTS 4Ps': self.view.display_NHTS4Ps,
                'NHTS Non-4Ps': self.view.display_NHTSNon4Ps,
                'Non-NHTS': self.view.display_NonNHTS
            }

            for status, count in data:
                if status in status_mapping:
                    status_mapping[status].setText(f"{count:,}")
        except Exception as e:
            self.show_error_message(
                "Socio-Economic Error",
                "Could not load socio-economic distribution data."
            )
            print(f"Error loading socio-economic data: {e}")

    def reset_socio_economic_distribution(self):
        self.view.display_NHTS4Ps.setText("0")
        self.view.display_NHTSNon4Ps.setText("0")
        self.view.display_NonNHTS.setText("0")

    #Update religion distribution statistics
    def populate_religion_distribution(self):
        from_date, to_date = self.get_date_range()

        self.reset_religion_distribution()

        try:
            data = self.model.get_religion_distribution(from_date, to_date)
            if not data:
                return

            religion_mapping = {
                'Roman Catholic': self.view.total_eth_rc,
                'Christian': self.view.total_eth_ch,
                'Iglesia ni Cristo': self.view.total_eth_inc,
                'Born Again Christian': self.view.total_eth_ba,
                'Hinduism': self.view.total_eth_hd,
                'Church of God': self.view.total_eth_cog,
                "Jehovah's Witness": self.view.total_eth_jw,
                'Mormon': self.view.total_eth_mm,
                'Islam': self.view.total_eth_is,
                'Others': self.view.total_eth_others,
                'None': self.view.total_eth_none
            }

            for religion, count in data:
                if religion in religion_mapping:
                    religion_mapping[religion].setText(f"{count:,}")
        except Exception as e:
            self.show_error_message(
                "Religion Data Error",
                "Could not load religion distribution data."
            )
            print(f"Error loading religion data: {e}")


    def reset_religion_distribution(self):
        religion_widgets = [
            self.view.total_eth_rc,
            self.view.total_eth_ch,
            self.view.total_eth_inc,
            self.view.total_eth_ba,
            self.view.total_eth_hd,
            self.view.total_eth_cog,
            self.view.total_eth_jw,
            self.view.total_eth_mm,
            self.view.total_eth_is,
            self.view.total_eth_others,
            self.view.total_eth_none
        ]

        for widget in religion_widgets:
            widget.setText("0")

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
        """Navigate back to the statistics panel"""
        from Controllers.UserController.StatisticsController import StatisticsController
        self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.stack)
        self.stack.addWidget(self.statistics_panel.statistics_screen)
        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
