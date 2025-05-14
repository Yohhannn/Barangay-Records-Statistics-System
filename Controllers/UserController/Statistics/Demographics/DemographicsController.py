from PySide6.QtGui import QIcon
from Controllers.BaseFileController import BaseFileController
from Models.Statistics.DemographicModel import DemographicModel

class DemographicsController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.view = self.load_ui("Resources/UIs/MainPages/StatisticPages/demographic.ui")
        self.model = DemographicModel()

        self.setup_view()
        self.populate_sex_statistics()
        self.populate_age_group()
        self.populate_voter_statistics()
        self.populate_socio_economic_distribution()
        self.populate_civil_status_distribution()
        self.populate_religion_distribution()
        self.center_on_screen()

    def setup_view(self):
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Demographics")
        self.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        self.view.btn_returnToStatisticsPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.view.icon_male.setIcon(QIcon('Resources/Icons/Icons/General_Icons/icon_male.png'))
        self.view.icon_female.setIcon(QIcon('Resources/Icons/Icons/General_Icons/icon_female.png'))
        self.view.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics_panel)

    def populate_sex_statistics(self):
        male, female = self.model.get_sex_counts()
        self.view.demo_TotalMale.setText(f"{male:,}")
        self.view.demo_TotalFemale.setText(f"{female:,}")
        self.view.demo_TotalPopulation.setText(f"{male + female:,}")

    def populate_age_group(self):
        age_counts = self.model.get_age_group_counts()
        self.view.demo_TotalChild.setText(f"{age_counts[0]:,}")
        self.view.demo_TotalMinors.setText(f"{age_counts[1]:,}")
        self.view.demo_TotalYoungAdults.setText(f"{age_counts[2]:,}")
        self.view.demo_TotalAdults.setText(f"{age_counts[3]:,}")
        self.view.demo_TotalMiddleAges.setText(f"{age_counts[4]:,}")
        self.view.demo_TotalSeniors.setText(f"{age_counts[5]:,}")

    def populate_civil_status_distribution(self):
        civil_status_data = self.model.get_civil_status_distribution()
        for row in civil_status_data:
            status, male, female, total = row

            if status == "Single":
                self.view.demo_TotalSingle_male.setText(str(male))
                self.view.demo_TotalSingle_female.setText(str(female))
                self.view.demo_TotalSingle.setText(str(total))
            elif status == "Married":
                self.view.demo_TotalMarried_male.setText(str(male))
                self.view.demo_TotalMarried_female.setText(str(female))
                self.view.demo_TotalMarried.setText(str(total))
            elif status == "Widowed":
                self.view.demo_TotalWidowed_male.setText(str(male))
                self.view.demo_TotalWidowed_female.setText(str(female))
                self.view.demo_TotalWidowed.setText(str(total))
            elif status == "Divorced":
                self.view.demo_TotalDivorced_male.setText(str(male))
                self.view.demo_TotalDivorced_female.setText(str(female))
                self.view.demo_TotalDivorced.setText(str(total))

    def populate_voter_statistics(self):
        stats = self.model.get_voter_statistics()

        (
            age_15_17, age_18_25, age_26_35,
            age_36_59, age_60_above,
            total_registered, total_unregistered,
            male_voters, female_voters
        ) = stats

        # Assign to labels in the view
        self.view.voter_15_17.setText(str(age_15_17))
        self.view.voter_18_25.setText(str(age_18_25))
        self.view.voter_26_35.setText(str(age_26_35))
        self.view.voter_36_59.setText(str(age_36_59))
        self.view.voter_60P.setText(str(age_60_above))

        self.view.voter_registered.setText(str(total_registered))
        self.view.voter_unregistered.setText(str(total_unregistered))

        self.view.voter_totalmale.setText(str(male_voters))
        self.view.voter_totalfemale.setText(str(female_voters))



    def populate_socio_economic_distribution(self):
        data = self.model.get_socio_economic_distribution()

        self.view.label_nhts_4ps.setText("0")
        self.view.label_nhts_non_4ps.setText("0")
        self.view.label_non_nhts.setText("0")
        self.view.label_unspecified.setText("0")

        for status, count in data:
            if status == 'NHTS 4Ps':
                self.view.label_nhts_4ps.setText(str(count))
            elif status == 'NHTS Non-4Ps':
                self.view.label_nhts_non_4ps.setText(str(count))
            elif status == 'Non-NHTS':
                self.view.label_non_nhts.setText(str(count))
            elif status == 'Unspecified':
                self.view.label_unspecified.setText(str(count))

    def populate_religion_distribution(self):
        data = self.model.get_religion_distribution()

        self.view.total_eth_rc.setText("0")
        self.view.total_eth_ch.setText("0")
        self.view.total_eth_inc.setText("0")
        self.view.total_eth_ba.setText("0")
        self.view.total_eth_hd.setText("0")
        self.view.total_eth_cog.setText("0")
        self.view.total_eth_jw.setText("0")
        self.view.total_eth_mm.setText("0")
        self.view.total_eth_is.setText("0")
        self.view.total_eth_others.setText("0")
        self.view.total_eth_none.setText("0")

        for religion, count in data:
            if religion == 'Roman Catholic':
                self.view.total_eth_rc.setText(str(count))
            elif religion == 'Christian':
                self.view.total_eth_ch.setText(str(count))
            elif religion == 'Iglesia ni Cristo':
                self.view.total_eth_inc.setText(str(count))
            elif religion == 'Born Again Christian':
                self.view.total_eth_ba.setText(str(count))
            elif religion == 'Hinduism':
                self.view.total_eth_hd.setText(str(count))
            elif religion == 'Church of God':
                self.view.total_eth_cog.setText(str(count))
            elif religion == "Jehovah's Witness":
                self.view.total_eth_jw.setText(str(count))
            elif religion == 'Mormon':
                self.view.total_eth_cog.setText(str(count))
            elif religion == 'Islam':
                self.view.total_eth_cog.setText(str(count))
            elif religion == 'Others':
                self.view.total_eth_cog.setText(str(count))
            elif religion == 'None':
                self.view.total_eth_cog.setText(str(count))

    def goto_statistics_panel(self):
        from Controllers.UserController.StatisticsController import StatisticsController
        self.statistics_panel = StatisticsController(self.login_window, self.emp_first_name, self.stack)
        self.stack.addWidget(self.statistics_panel.statistics_screen)
        self.stack.setCurrentWidget(self.statistics_panel.statistics_screen)
