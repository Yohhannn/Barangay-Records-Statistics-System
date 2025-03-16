
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QPushButton
from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtCore import QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from Utils.utils_datetime import update_date_label
from Utils.utils_realtime import update_time_label
from Utils.util_popup import load_popup

class MainWindow(QMainWindow):
    def __init__(self, login_window, emp_first_name):
        super().__init__()
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.loader = QUiLoader()

        #------------------------------------------------------------------------------#
        # MAIN PAGES SET UI
        self.dashboard_screen = self.load_ui("UI/MainPages/dashboard.ui")
        self.citizen_profile_screen = self.load_ui("UI/MainPages/citizenprofile.ui")
        self.statistics_screen = self.load_ui("UI/MainPages/statistics.ui")
        self.business_screen = self.load_ui("UI/MainPages/business.ui")
        self.schedules_screen = self.load_ui("UI/MainPages/schedule.ui")
        # ------------------------------------------------#
        # SUB PAGES SET UI
        self.statistics_demo_screen = self.load_ui("UI/MainPages/StatisticPages/demographic.ui")
        self.statistics_geo_screen = self.load_ui("UI/MainPages/StatisticPages/geographic.ui")
        self.statistics_household_screen = self.load_ui("UI/MainPages/StatisticPages/household.ui")
        self.statistics_socio_screen = self.load_ui("UI/MainPages/StatisticPages/socioeconomic.ui")
        self.statistics_voters_screen = self.load_ui("UI/MainPages/StatisticPages/voters.ui")
        self.statistics_health_screen = self.load_ui("UI/MainPages/StatisticPages/health.ui")
        #------------------------------------------------------------------------------#
        # SUB PAGES ADD ON STACK
        self.stack.addWidget(self.dashboard_screen)
        self.stack.addWidget(self.citizen_profile_screen)
        self.stack.addWidget(self.statistics_screen)
        self.stack.addWidget(self.business_screen)
        self.stack.addWidget(self.schedules_screen)
        # ------------------------------------------------#
        # SUB PAGES ADD ON STACK
        self.stack.addWidget(self.statistics_demo_screen)
        self.stack.addWidget(self.statistics_geo_screen)
        self.stack.addWidget(self.statistics_household_screen)
        self.stack.addWidget(self.statistics_socio_screen)
        self.stack.addWidget(self.statistics_voters_screen)
        self.stack.addWidget(self.statistics_health_screen)
        # ------------------------------------------------#
        # MAIN PAGES INITIALIZATION
        self.dashboard_initialized = False
        self.citizen_profile_initialized = False
        self.statistics_initialized = False
        self.business_initialized = False
        self.schedules_initialized = False
        # ------------------------------------------------#
        # SUB PAGES INITIALIZATION
        self.statistics_demo_initialized = False
        self.statistics_geo_initialized = False
        self.statistics_household_initialized = False
        self.statistics_socio_initialized = False
        self.statistics_voters_initialized = False
        self.statistics_health_initialized = False
        # ------------------------------------------------------------------------------#

        self.setup_dashboard_ui()
        self.stack.setCurrentIndex(0)

    def load_ui(self, ui_path):
        file = QFile(ui_path)
        if not file.exists():
            print(f"Error: UI file not found: {ui_path}")
            return None
        file.open(QFile.ReadOnly)
        ui = self.loader.load(file, None)
        file.close()
        return ui
    # ===============================================================================================
    def setup_dashboard_ui(self):
        """Setup the dashboard UI layout and connect buttons."""
        self.setFixedSize(1350, 850)  # Set size for dashboard screen
        self.setWindowTitle("MRSS: Dashboard")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.dashboard_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.dashboard_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.dashboard_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.dashboard_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.dashboard_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.dashboard_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.dashboard_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.dashboard_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.dashboard_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            self.dashboard_screen.dashboard_buttonAboutSoftware.setIcon(QIcon('Assets/Icons/icon_aboutsoftware.svg'))
            self.dashboard_screen.dashboard_buttonBarangayInfo.setIcon(QIcon('Assets/Icons/icon_brgyinfo.svg'))
            self.dashboard_screen.dashboard_buttonViewEmployees.setIcon(QIcon('Assets/Icons/icon_viewemplist.svg'))

            # Set the rest of the icons to the page.
            self.dashboard_screen.acc_buttonYourAccount.setIcon(QIcon('Assets/Icons/icon_myprofile.svg'))

            # Update date label
            update_date_label(self.dashboard_screen.label_dateDashboard)

            # Welcome Message Display Name
            self.dashboard_screen.title_employeeFirstNameDashboard.setText(self.emp_first_name)

            # Set up and start the timer for real-time time updates
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: update_time_label(self.dashboard_screen.label_timeDashboard))
            self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

            # Connect navbar buttons
            # self.dashboard_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard) # UNNECESSARY
            self.dashboard_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.dashboard_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.dashboard_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.dashboard_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.dashboard_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.dashboard_initialized = True

            # Connect the button to the popup method
            self.dashboard_screen.acc_buttonYourAccount.clicked.connect(self.show_account_popup)
            self.dashboard_screen.dashboard_buttonViewEmployees.clicked.connect(self.show_employee_popup)
            self.dashboard_screen.dashboard_buttonBarangayInfo.clicked.connect(self.show_barangayinfo_popup)
            self.dashboard_screen.dashboard_buttonAboutSoftware.clicked.connect(self.show_aboutsoftware_popup)

    def show_employee_popup(self):
        print("-- Navigating to Dashboard > List of Employees")
        popup = load_popup("UI/PopUp/Screen_Dashboard/listofemployees.ui", self)
        popup.setWindowTitle("List of Employees")  # Set a title for the popup
        popup.setWindowModality(Qt.ApplicationModal)  # Make the popup modal
        popup.show()

    def show_barangayinfo_popup(self):
        print("-- Navigating to Dashboard > Barangay Info")
        popup = load_popup("UI/PopUp/Screen_Dashboard/barangayinfo.ui", self)
        popup.setWindowTitle("Barangay Information")  # Set a title for the popup
        popup.brgyinfo_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        popup.setWindowModality(Qt.ApplicationModal)  # Make the popup modal
        popup.show()

    def show_aboutsoftware_popup(self):
        print("-- Navigating to Dashboard > About Software")
        popup = load_popup("UI/PopUp/Screen_Dashboard/aboutsoftware.ui", self)
        popup.setWindowTitle("About the Software")  # Set a title for the popup
        popup.aboutsoftwareinfo_imageRavenLabs.setPixmap(QPixmap("Assets/AppIcons/icon_ravenlabs.png"))
        popup.aboutsoftwareinfo_imageCTULOGO.setPixmap(QPixmap("Assets/Images/img_ctulogo.png"))
        popup.aboutsoftwareinfo_imageLogo.setPixmap(QPixmap("Assets/Images/img_mainappicon.png"))
        popup.setWindowModality(Qt.ApplicationModal)  # Make the popup modal
        popup.show()

    def show_account_popup(self):
        print("-- Navigating to Dashboard > Your Account")
        popup = load_popup("UI/PopUp/Screen_Dashboard/youraccount.ui", self)
        popup.setWindowTitle("Your Account")  # Optional title
        popup.setWindowModality(Qt.ApplicationModal)  # Make it modal

        # Find the "Admin Override" button inside the popup UI
        admin_override_button = popup.findChild(QPushButton, "employeeaccount_buttonAdminOverride")

        if admin_override_button:
            admin_override_button.clicked.connect(lambda: self.show_admin_override_popup(popup))

        popup.show()

    def show_admin_override_popup(self, first_popup):
        print("-- Navigating to Dashboard > Your Account > Admin Override")
        first_popup.close()  # Close the first popup
        admin_popup = load_popup("UI/PopUp/Screen_Dashboard/adminoverride.ui", self)
        admin_popup.setWindowTitle("Admin Override")
        admin_popup.setWindowModality(Qt.ApplicationModal)  # Modal type para dili ma click ang other window na nag open.

        admin_popup.btn_return_to_youraccount.setIcon(QIcon('Assets/Icons/icon_return_light.svg'))

        # Find the "Return to Your Account" button inside the Admin Override popup
        return_button = admin_popup.findChild(QPushButton, "btn_return_to_youraccount")

        if return_button:
            print("-- Found 'Return to Your Account' button")
            return_button.clicked.connect(lambda: self.return_to_account_popup(admin_popup))
        else:
            print("-- Error: 'Return to Your Account' button not found!")

        admin_popup.show()

    def return_to_account_popup(self, current_popup):
        print("-- Returning to Dashboard > Your Account")
        current_popup.close()  # Close the current popup
        self.show_account_popup()  # Reopen the 'Your Account' popup

    # ===============================================================================================

    def setup_citizen_profile_ui(self):
        """Setup the citizen profile UI layout."""
        self.setFixedSize(1350, 850)  # Set size for citizen profile screen
        self.setWindowTitle("MRSS: Citizen Profiles")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.citizen_profile_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.citizen_profile_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.citizen_profile_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.citizen_profile_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.citizen_profile_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.citizen_profile_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.citizen_profile_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.citizen_profile_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.citizen_profile_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Set Icons
            self.citizen_profile_screen.profileList_buttonCreate.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
            self.citizen_profile_screen.profileList_buttonDelete.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))
            self.citizen_profile_screen.profileList_buttonSelectAll.setIcon(QIcon('Assets/FuncIcons/icon_selectall.svg'))
            self.citizen_profile_screen.profileList_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
            self.citizen_profile_screen.profileList_buttonFilter.setIcon(QIcon('Assets/FuncIcons/icon_filter.svg'))

            # SINCE SEARCHING IS EITHER NAME OR ID, CHECK FIRST IF THE INPUT IS NUMERIC OR NOT IF NUMERIC SEARCH IT AS ID IF NOT SEARCH IT BY THE NAME.

            # Connect navbar buttons
            self.citizen_profile_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            # self.citizen_profile_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles) # UNNECESSARY
            self.citizen_profile_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.citizen_profile_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.citizen_profile_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Click to Popup Filter Options
            self.citizen_profile_screen.profileList_buttonFilter.clicked.connect(self.show_filter_popup)

            # Connect logout button
            self.citizen_profile_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.citizen_profile_initialized = True

    def show_filter_popup(self):
        print("-- Navigating to Profile List > Filter Options")
        popup = load_popup("UI/PopUp/Screen_CitizenProfiles/filteroptions.ui", self)
        popup.setWindowTitle("Filter Options")  # Set a title for the popup
        popup.setWindowModality(Qt.ApplicationModal)  # Make the popup modal

        save_button = popup.findChild(QPushButton, "filteroptions_buttonSave")
        if save_button:
            save_button.clicked.connect(lambda: self.save_filter_options(popup))

        popup.show()

    # PLEASE ADD FUNCTIONALITY ARI NA MO SAVE ANG CHANGES NYA BASTA
    def save_filter_options(self, popup):
        print("Filter options saved.")
        self.filter_options_changed = False  # Reset the change flag
        popup.close()


    # ===============================================================================================

    def setup_statistics_ui(self):
        """Setup the statistics UI layout."""
        self.setFixedSize(1350, 850)  # Set size for statistics screen
        self.setWindowTitle("MRSS: Statistics")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.statistics_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.statistics_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.statistics_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.statistics_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.statistics_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.statistics_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.statistics_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.statistics_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.statistics_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.statistics_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            # self.statistics_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics) # UNNECESSARY
            self.statistics_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            self.statistics_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Set Images for the Statistics Categories
            self.statistics_screen.statistics_ButtonDemographic.setIcon(QIcon('Assets/Images/img_demographic.png'))
            self.statistics_screen.statistics_ButtonGeographic.setIcon(QIcon('Assets/Images/img_geographic.png'))
            self.statistics_screen.statistics_ButtonHousehold.setIcon(QIcon('Assets/Images/img_household.png'))
            self.statistics_screen.statistics_ButtonSocioEconomic.setIcon(QIcon('Assets/Images/img_socioeconomic.png'))
            self.statistics_screen.statistics_ButtonVoters.setIcon(QIcon('Assets/Images/img_voters.png'))
            self.statistics_screen.statistics_ButtonHealth.setIcon(QIcon('Assets/Images/img_health.png'))
            self.statistics_screen.statistics_ButtonFFU.setIcon(QIcon('Assets/Images/img_FFU.png'))

            self.statistics_screen.statistics_ButtonDemographic.clicked.connect(self.goto_demographics)
            self.statistics_screen.statistics_ButtonGeographic.clicked.connect(self.goto_geographics)
            self.statistics_screen.statistics_ButtonHousehold.clicked.connect(self.goto_household)
            self.statistics_screen.statistics_ButtonSocioEconomic.clicked.connect(self.goto_socioeco)
            self.statistics_screen.statistics_ButtonVoters.clicked.connect(self.goto_voters)
            self.statistics_screen.statistics_ButtonHealth.clicked.connect(self.goto_health)

            # Connect logout button
            self.statistics_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.statistics_initialized = True

    # ===============================================================================================

    def setup_business_ui(self):
        """Setup the business UI layout."""
        self.setFixedSize(1350, 850)  # Set size for business screen
        self.setWindowTitle("MRSS: Business")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.business_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.business_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.business_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.business_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.business_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.business_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.business_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.business_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.business_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.business_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.business_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.business_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            # self.business_screen.nav_buttonBusiness.clicked.connect(self.goto_business) # UNNECESSARY
            self.business_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules)

            # Connect logout button
            self.business_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.business_initialized = True

    # ===============================================================================================

    def setup_schedules_ui(self):
        """Setup the schedules UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MRSS: Schedules")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.schedules_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.schedules_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.schedules_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.schedules_screen.nav_buttonCitizenProfiles.setIcon(QIcon('Assets/Icons/icon_citizenprofiles.svg'))
            self.schedules_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.schedules_screen.nav_buttonBusiness.setIcon(QIcon('Assets/Icons/icon_business.svg'))
            self.schedules_screen.nav_buttonSchedules.setIcon(QIcon('Assets/Icons/icon_schedule.svg'))
            self.schedules_screen.nav_buttonAdminOverview.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.schedules_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.schedules_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.schedules_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_profiles)
            self.schedules_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.schedules_screen.nav_buttonBusiness.clicked.connect(self.goto_business)
            # self.schedules_screen.nav_buttonSchedules.clicked.connect(self.goto_schedules) # UNNECESSARY

            # Connect logout button
            self.schedules_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.schedules_initialized = True

    # ===============================================================================================

    def setup_demographics_ui(self):
        """Setup the Demographics UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MRSS: Statistics > Demographics")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_demo_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_demo_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_demo_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_demo_initialized = True

    # ===============================================================================================

    def setup_geographic_ui(self):
        """Setup the Geographic UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MRSS: Statistics > Geographic")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_geo_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_geo_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_geo_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_geo_initialized = True

    # ===============================================================================================

    def setup_household_ui(self):
        """Setup the Household UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MRSS: Statistics > Household")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_household_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_household_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_household_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_household_initialized = True

    # ===============================================================================================

    def setup_socioeco_ui(self):
        """Setup the Socio-Economic UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MRSS: Statistics > Socio-Economic")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_socio_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_socio_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_socio_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_socio_initialized = True

    # ===============================================================================================

    def setup_voters_ui(self):
        """Setup the Voter UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MRSS: Statistics > Voters")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_voters_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_voters_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_voters_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_voters_initialized = True

    # ===============================================================================================

    def setup_health_ui(self):
        """Setup the Health UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MRSS: Statistics > Health")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_health_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_health_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_health_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_health_initialized = True

    # ===============================================================================================

    def logout_button_clicked(self):
        """Handle logout button click."""
        confirmation = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            print("-- Logout Confirmed")
            self.login_window.show()  # Show the login window again
            self.close()

    def goto_dashboard(self):
        """Handle navigation to dashboard screen."""
        print("-- Navigating to Dashboard")
        self.setup_dashboard_ui()  # Ensure dashboard is set up
        self.stack.setCurrentIndex(0)  # Switch to dashboard screen

    def goto_citizen_profiles(self):
        """Handle navigation to citizen profiles screen."""
        print("-- Navigating to Citizen Profiles")
        self.setup_citizen_profile_ui()  # Ensure citizen profile is set up
        self.stack.setCurrentIndex(1)  # Switch to citizen profile screen

    def goto_statistics(self):
        """Handle navigation to statistics screen."""
        print("-- Navigating to Statistics")
        self.setup_statistics_ui()  # Ensure statistics is set up
        self.stack.setCurrentIndex(2)  # Switch to statistics screen

    def goto_business(self):
        """Handle navigation to business screen."""
        print("-- Navigating to Business")
        self.setup_business_ui()  # Ensure business is set up
        self.stack.setCurrentIndex(3)  # Switch to business screen

    def goto_schedules(self):
        """Handle navigation to schedules screen."""
        print("-- Navigating to Schedules")
        self.setup_schedules_ui()  # Ensure schedules is set up
        self.stack.setCurrentIndex(4)  # Switch to schedules screen

    def goto_demographics(self):
        """Handle navigation to demographic screen."""
        print("-- Navigating to Statistics > Demographics")
        self.setup_demographics_ui()  # Ensure Demographics is set up
        self.stack.setCurrentIndex(5)  # Switch to Demographics screen

    def goto_geographics(self):
        """Handle navigation to geographic screen."""
        print("-- Navigating to Statistics > Geographics")
        self.setup_geographic_ui()  # Ensure Geographics is set up
        self.stack.setCurrentIndex(6)  # Switch to Geographics screen

    def goto_household(self):
        """Handle navigation to household screen."""
        print("-- Navigating to Statistics > Household")
        self.setup_household_ui()  # Ensure Household is set up
        self.stack.setCurrentIndex(7)  # Switch to Household screen

    def goto_socioeco(self):
        """Handle navigation to socio-economic screen."""
        print("-- Navigating to Statistics > Socio-Economic")
        self.setup_socioeco_ui()  # Ensure Socio-Economic is set up
        self.stack.setCurrentIndex(8)  # Switch to Socio-Economic screen

    def goto_voters(self):
        """Handle navigation to voters screen."""
        print("-- Navigating to Statistics > Voters")
        self.setup_voters_ui()  # Ensure Voters is set up
        self.stack.setCurrentIndex(9)  # Switch to Voters screen

    def goto_health(self):
        """Handle navigation to health screen."""
        print("-- Navigating to Statistics > Health")
        self.setup_health_ui()  # Ensure Health is set up
        self.stack.setCurrentIndex(10)  # Switch to Health screen

    def logout_button_clicked(self):
        confirmation = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            self.login_window.show()  # Show the login window again
            self.close()