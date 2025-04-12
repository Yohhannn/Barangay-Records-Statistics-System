import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QPushButton, QFileDialog, QLabel, \
    QButtonGroup, QRadioButton
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from Utils.utils_datetime import update_date_label
from Utils.utils_realtime import update_time_label
from Utils.util_popup import load_popup

class dashboard_func(QMainWindow):

    def __init__(self, login_window, emp_first_name):
        super().__init__()
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.loader = QUiLoader()

        # ------------------------------------------------------------------------------#
        # MAIN PAGES SET UI
        self.dashboard_screen = self.load_ui("UI/MainPages/dashboard.ui")
        self.citizen_panel_screen = self.load_ui("UI/MainPages/citizenpanel.ui")
        self.statistics_screen = self.load_ui("UI/MainPages/statistics.ui")
        self.institutions_screen = self.load_ui("UI/MainPages/institutions.ui")
        self.transactions_screen = self.load_ui("UI/MainPages/transactions.ui")
        self.history_records_screen = self.load_ui("UI/MainPages/historyrecords.ui")
        # ------------------------------------------------#
        # SUB PAGES SET UI
        self.statistics_demo_screen = self.load_ui("UI/MainPages/StatisticPages/demographic.ui")
        self.statistics_geo_screen = self.load_ui("UI/MainPages/StatisticPages/geographic.ui")
        self.statistics_household_screen = self.load_ui("UI/MainPages/StatisticPages/household.ui")
        self.statistics_socio_screen = self.load_ui("UI/MainPages/StatisticPages/socioeconomic.ui")
        self.statistics_voters_screen = self.load_ui("UI/MainPages/StatisticPages/voters.ui")
        self.statistics_health_screen = self.load_ui("UI/MainPages/StatisticPages/health.ui")
        self.statistics_jobs_screen = self.load_ui("UI/MainPages/StatisticPages/jobs.ui")
        self.statistics_groups_screen = self.load_ui("UI/MainPages/StatisticPages/groups.ui")
        # ------------------------------------------------------------------------------#
        # SUB PAGES ADD ON STACK
        self.stack.addWidget(self.dashboard_screen)
        self.stack.addWidget(self.citizen_panel_screen)
        self.stack.addWidget(self.statistics_screen)
        self.stack.addWidget(self.institutions_screen)
        self.stack.addWidget(self.transactions_screen)
        self.stack.addWidget(self.history_records_screen)
        # ------------------------------------------------#
        # SUB PAGES ADD ON STACK
        self.stack.addWidget(self.statistics_demo_screen)
        self.stack.addWidget(self.statistics_geo_screen)
        self.stack.addWidget(self.statistics_household_screen)
        self.stack.addWidget(self.statistics_socio_screen)
        self.stack.addWidget(self.statistics_voters_screen)
        self.stack.addWidget(self.statistics_health_screen)
        self.stack.addWidget(self.statistics_jobs_screen)
        self.stack.addWidget(self.statistics_groups_screen)
        # ------------------------------------------------#
        # MAIN PAGES INITIALIZATION
        self.dashboard_initialized = False
        self.citizen_panel_initialized = False
        self.statistics_initialized = False
        self.institutions_initialized = False
        self.transactions_initialized = False
        self.history_records_initialized = False
        # ------------------------------------------------#
        # SUB PAGES INITIALIZATION
        self.statistics_demo_initialized = False
        self.statistics_geo_initialized = False
        self.statistics_household_initialized = False
        self.statistics_socio_initialized = False
        self.statistics_voters_initialized = False
        self.statistics_health_initialized = False
        self.statistics_jobs_initialized = False
        self.statistics_groups_initialized = False
        # ------------------------------------------------------------------------------#

        self.setup_dashboard_ui()
        self.stack.setCurrentIndex(0)

        self.center_on_screen()

    def center_on_screen(self):
        center_point = QApplication.primaryScreen().availableGeometry().center()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

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
        self.setWindowTitle("MaPro: Dashboard")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.dashboard_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.dashboard_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.dashboard_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.dashboard_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
            self.dashboard_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.dashboard_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
            self.dashboard_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
            self.dashboard_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

            self.dashboard_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.dashboard_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
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
            self.dashboard_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
            self.dashboard_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.dashboard_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
            self.dashboard_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
            self.dashboard_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

            self.dashboard_screen.label_UpdateVersion.setText("V2.8.2 - Alpha")

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

    def setup_citizen_panel_ui(self):
        """Setup the citizen panel UI layout."""
        self.setFixedSize(1350, 850)  # Set size for citizen profile screen
        self.setWindowTitle("MaPro: Citizen Panel")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.citizen_panel_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            # ------ MAIN ------
            self.citizen_panel_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.citizen_panel_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.citizen_panel_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
            self.citizen_panel_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.citizen_panel_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
            self.citizen_panel_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
            self.citizen_panel_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))
            # ------ ADMIN ------
            self.citizen_panel_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.citizen_panel_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
            self.citizen_panel_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            #Set Icons
            self.citizen_panel_screen.profileList_buttonRegister.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
            self.citizen_panel_screen.profileList_buttonRegisterHousehold.setIcon(QIcon('Assets/FuncIcons/icon_household.svg'))
            self.citizen_panel_screen.profileList_buttonDelete.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))
            self.citizen_panel_screen.profileList_buttonUpdate.setIcon(QIcon('Assets/FuncIcons/icon_edit.svg'))
            self.citizen_panel_screen.profileList_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
            self.citizen_panel_screen.profileList_buttonFilter.setIcon(QIcon('Assets/FuncIcons/icon_filter.svg'))

            # SINCE SEARCHING IS EITHER NAME OR ID, CHECK FIRST IF THE INPUT IS NUMERIC OR NOT IF NUMERIC SEARCH IT AS ID IF NOT SEARCH IT BY THE NAME.

            # Connect navbar buttons
            self.citizen_panel_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            # self.citizen_profile_screen.nav_buttonCitizenProfiles.clicked.connect(self.goto_citizen_panel)
            self.citizen_panel_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.citizen_panel_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
            self.citizen_panel_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
            self.citizen_panel_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

            # Click to Popup Filter Options
            self.citizen_panel_screen.profileList_buttonFilter.clicked.connect(self.show_filter_popup)
            self.citizen_panel_screen.profileList_buttonRegister.clicked.connect(self.show_register_citizen_part_01_popup)
            #self.citizen_panel_screen.profileList_buttonRegister.clicked.connect(self.show_register_citizen_popup)

            # Connect logout button
            self.citizen_panel_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.citizen_panel_initialized = True

    def show_filter_popup(self):
        print("-- Navigating to Profile List > Filter Options")
        popup = load_popup("UI/PopUp/Screen_CitizenProfiles/filteroptions.ui", self)
        popup.setWindowTitle("Filter Options")
        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

    # ==================================

    def show_register_citizen_part_01_popup(self):
        print("-- Register New Citizen Profile")
        popup = load_popup("UI/PopUp/Screen_CitizenProfiles/register_citizen_part_01.ui", self)
        popup.setWindowTitle("Register New Citizen")
        popup.setWindowModality(Qt.ApplicationModal)

        popup.register_buttonPrev.setIcon(QIcon('Assets/FuncIcons/icon_arrow_prev'))
        popup.register_buttonConfirmPart1_NextToPart2.setIcon(QIcon('Assets/FuncIcons/icon_arrow_next'))

        # Connect 'Next to Part 2' button
        next_btn = popup.findChild(QPushButton, "register_buttonConfirmPart1_NextToPart2")
        if next_btn:
            next_btn.clicked.connect(lambda: self.show_register_citizen_part_02_popup(popup))

        def setup_radio_button_groups_01():
            # Sex
            radio_sex = QButtonGroup(popup)
            radio_male = popup.findChild(QRadioButton, "radioButton_male")
            radio_female = popup.findChild(QRadioButton, "radioButton_female")
            if radio_male and radio_female:
                radio_sex.addButton(radio_male)
                radio_sex.addButton(radio_female)

        setup_radio_button_groups_01()

        # Upload and capture image setup
        upload_button = popup.findChild(QPushButton, "uploadButton")
        capture_button = popup.findChild(QPushButton, "captureButton")
        image_label = popup.findChild(QLabel, "imageLabel")

        if upload_button:
            upload_button.setIcon(QIcon("Assets/Icons/icon_upload_image.svg"))
        if capture_button:
            capture_button.setIcon(QIcon("Assets/Icons/icon_camera.svg"))

        # Update interviewer info
        update_date_label(popup.interviewer_dateofvisit)
        popup.interviewer_emp_name.setText(self.emp_first_name)

        def upload_image():
            file_path, _ = QFileDialog.getOpenFileName(popup, "Select an Image", "",
                                                       "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
            if file_path:
                pixmap = QPixmap(file_path)
                image_label.setPixmap(pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio))

        def capture_photo():
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open webcam")
                return

            ret, frame = cap.read()
            cap.release()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                image_label.setPixmap(pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio))
            else:
                print("Error: Failed to capture image")

        if upload_button:
            upload_button.clicked.connect(upload_image)
        if capture_button:
            capture_button.clicked.connect(capture_photo)

        popup.show()

    # ==================================

    def show_register_citizen_part_02_popup(self, part_one_popup):
        print("-- Register New Citizen Profile Part 2")
        popup = load_popup("UI/PopUp/Screen_CitizenProfiles/register_citizen_part_02.ui", self)
        popup.setWindowTitle("Register New Citizen - Part 2")
        popup.setWindowModality(Qt.ApplicationModal)
        part_one_popup.close()

        popup.register_buttonReturnToPart1_FromPart2.setIcon(QIcon('Assets/FuncIcons/icon_arrow_prev'))
        popup.register_buttonConfirmPart2_NextToPart3.setIcon(QIcon('Assets/FuncIcons/icon_arrow_next'))

        # Update interviewer info
        update_date_label(popup.interviewer_dateofvisit)
        popup.interviewer_emp_name.setText(self.emp_first_name)

        def setup_radio_button_groups_02():
            # Government Worker
            radio_gov = QButtonGroup(popup)
            gov_yes = popup.findChild(QRadioButton, "radioButton_IsGov_Yes")
            gov_no = popup.findChild(QRadioButton, "radioButton_IsGov_No")
            if gov_yes and gov_no:
                radio_gov.addButton(gov_yes)
                radio_gov.addButton(gov_no)

            # Philhealth Member
            radio_phil = QButtonGroup(popup)
            phil_yes = popup.findChild(QRadioButton, "radioButton_IsPhilMem_Yes")
            phil_no = popup.findChild(QRadioButton, "radioButton_IsPhilMem_No")
            if phil_yes and phil_no:
                radio_phil.addButton(phil_yes)
                radio_phil.addButton(phil_no)

        setup_radio_button_groups_02()

        # Go to Part 3
        next_btn = popup.findChild(QPushButton, "register_buttonConfirmPart2_NextToPart3")
        if next_btn:
            next_btn.clicked.connect(lambda: self.show_register_citizen_part_03_popup(popup))

        # Return to Part 1
        back_btn = popup.findChild(QPushButton, "register_buttonReturnToPart1_FromPart2")
        if back_btn:
            back_btn.clicked.connect(lambda: self.show_register_citizen_part_01_popup_and_close(popup))

        popup.show()

    # ==================================

    def show_register_citizen_part_01_popup_and_close(self, current_popup):
        current_popup.close()
        self.show_register_citizen_part_01_popup()

    # ==================================

    def show_register_citizen_part_03_popup(self, part_two_popup):
        print("-- Register New Citizen Profile Part 3")
        popup = load_popup("UI/PopUp/Screen_CitizenProfiles/register_citizen_part_03.ui", self)
        popup.setWindowTitle("Register New Citizen - Part 3")
        popup.setWindowModality(Qt.ApplicationModal)
        part_two_popup.close()

        popup.register_buttonReturnToPart2_FromPart3.setIcon(QIcon('Assets/FuncIcons/icon_arrow_prev'))
        popup.register_buttonConfirmPart3_SaveForm.setIcon(QIcon('Assets/FuncIcons/icon_confirm'))

        # Update interviewer info
        update_date_label(popup.interviewer_dateofvisit)
        popup.interviewer_emp_name.setText(self.emp_first_name)

        def setup_radio_button_groups_03():
            # Student
            radio_student = QButtonGroup(popup)
            student_yes = popup.findChild(QRadioButton, "radioButton_IsStudent_Yes")
            student_no = popup.findChild(QRadioButton, "radioButton_IsStudent_No")
            if student_yes and student_no:
                radio_student.addButton(student_yes)
                radio_student.addButton(student_no)

            # Family Planning
            radio_famplan = QButtonGroup(popup)
            famplan_yes = popup.findChild(QRadioButton, "radioButton_IsFamPlan_Yes")
            famplan_no = popup.findChild(QRadioButton, "radioButton_IsFamPlan_No")
            if student_yes and student_no:
                radio_famplan.addButton(famplan_yes)
                radio_famplan.addButton(famplan_no)

            # PWD
            radio_pwd = QButtonGroup(popup)
            pwd_yes = popup.findChild(QRadioButton, "register_citizen_IsPWD_Yes")
            pwd_no = popup.findChild(QRadioButton, "register_citizen_IsPWD_No")
            if pwd_yes and pwd_no:
                radio_pwd.addButton(pwd_yes)
                radio_pwd.addButton(pwd_no)

            # Registered Voter
            radio_voter = QButtonGroup(popup)
            vote_yes = popup.findChild(QRadioButton, "register_citizen_RegVote_Yes")
            vote_no = popup.findChild(QRadioButton, "register_citizen_RegVote_No")
            if vote_yes and vote_no:
                radio_voter.addButton(vote_yes)
                radio_voter.addButton(vote_no)

            # Deceased
            radio_deceased = QButtonGroup(popup)
            deceased_yes = popup.findChild(QRadioButton, "register_citizen_Deceased_Yes")
            deceased_no = popup.findChild(QRadioButton, "register_citizen_Deceased_No")
            if deceased_yes and deceased_no:
                radio_deceased.addButton(deceased_yes)
                radio_deceased.addButton(deceased_no)

            # Indigenous Group
            radio_indigenous = QButtonGroup(popup)
            ind_yes = popup.findChild(QRadioButton, "register_citizen_IndGroup_Yes")
            ind_no = popup.findChild(QRadioButton, "register_citizen_IndGroup_No")
            if ind_yes and ind_no:
                radio_indigenous.addButton(ind_yes)
                radio_indigenous.addButton(ind_no)

        setup_radio_button_groups_03()

        # Save final form with confirmation
        save_btn = popup.findChild(QPushButton, "register_buttonConfirmPart3_SaveForm")
        if save_btn:
            def confirm_and_save():
                reply = QMessageBox.question(
                    popup,
                    "Confirm Registration",
                    "Are you sure you want to register this citizen?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    print("-- Form Submitted")
                    QMessageBox.information(popup, "Success", "Citizen successfully registered!")
                    popup.close()

            save_btn.clicked.connect(confirm_and_save)

        # Return to Part 2
        back_btn = popup.findChild(QPushButton, "register_buttonReturnToPart2_FromPart3")
        if back_btn:
            back_btn.clicked.connect(lambda: self.show_register_citizen_part_02_popup_and_close(popup))

        popup.show()

    # ==================================

    def show_register_citizen_part_02_popup_and_close(self, current_popup):
        current_popup.close()
        self.show_register_citizen_part_02_popup(current_popup)

    # ==================================

    # PLEASE ADD FUNCTIONALITY ARI NA MO SAVE ANG CHANGES NYA BASTA
    def save_filter_options(self, popup):
        print("Filter options saved.")
        self.filter_options_changed = False  # Reset the change flag
        popup.close()

    # ===============================================================================================

    def setup_statistics_ui(self):
        """Setup the statistics UI layout."""
        self.setFixedSize(1350, 850)  # Set size for statistics screen
        self.setWindowTitle("MaPro: Statistics")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.statistics_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.statistics_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.statistics_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
            self.statistics_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.statistics_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
            self.statistics_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
            self.statistics_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

            self.statistics_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.statistics_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
            self.statistics_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.statistics_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.statistics_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
            # self.statistics_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics) # UNNECESSARY
            self.statistics_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
            self.statistics_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
            self.statistics_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

            # Set Images for the Statistics Categories
            self.statistics_screen.statistics_ButtonDemographic.setIcon(QIcon('Assets/Images/img_demographic.png'))
            self.statistics_screen.statistics_ButtonGeographic.setIcon(QIcon('Assets/Images/img_geographic.png'))
            self.statistics_screen.statistics_ButtonHousehold.setIcon(QIcon('Assets/Images/img_household.png'))
            self.statistics_screen.statistics_ButtonSocioEconomic.setIcon(QIcon('Assets/Images/img_socioeconomic.png'))
            self.statistics_screen.statistics_ButtonVoters.setIcon(QIcon('Assets/Images/img_voters.png'))
            self.statistics_screen.statistics_ButtonHealth.setIcon(QIcon('Assets/Images/img_health.png'))
            self.statistics_screen.statistics_ButtonJobs.setIcon(QIcon('Assets/Images/img_jobs.png'))
            self.statistics_screen.statistics_ButtonGroups.setIcon(QIcon('Assets/Images/img_groups.png'))

            self.statistics_screen.statistics_ButtonDemographic.clicked.connect(self.goto_demographics)
            self.statistics_screen.statistics_ButtonGeographic.clicked.connect(self.goto_geographics)
            self.statistics_screen.statistics_ButtonHousehold.clicked.connect(self.goto_household)
            self.statistics_screen.statistics_ButtonSocioEconomic.clicked.connect(self.goto_socioeco)
            self.statistics_screen.statistics_ButtonVoters.clicked.connect(self.goto_voters)
            self.statistics_screen.statistics_ButtonHealth.clicked.connect(self.goto_health)
            self.statistics_screen.statistics_ButtonJobs.clicked.connect(self.goto_jobs)
            self.statistics_screen.statistics_ButtonGroups.clicked.connect(self.goto_groups)

            # Connect logout button
            self.statistics_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.statistics_initialized = True

    # ===============================================================================================

    def setup_institutions_ui(self):
        """Setup the institutions UI layout."""
        self.setFixedSize(1350, 850)  # Set size for business screen
        self.setWindowTitle("MaPro: Institutions")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.institutions_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.institutions_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.institutions_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.institutions_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
            self.institutions_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.institutions_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
            self.institutions_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
            self.institutions_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

            self.institutions_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.institutions_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
            self.institutions_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            self.institutions_screen.inst_ButtonCategory_Business.setIcon(QIcon('Assets/Images/img_category_business.png'))
            self.institutions_screen.inst_ButtonCategory_Infrastructure.setIcon(QIcon('Assets/Images/img_category_infrastructure.png'))

            # Connect navbar buttons
            self.institutions_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.institutions_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
            self.institutions_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            # self.institutions.screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
            self.institutions_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
            self.institutions_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

            # self.institutions_screen.inst_ButtonCategory_Business.clicked.connect()
            # self.institutions_screen.inst_ButtonCategory_Infrastructure.clicked.connect()

            # Connect logout button
            self.institutions_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.institutions_initialized = True

    # ===============================================================================================

    def setup_transactions_ui(self):
        """Setup the schedules UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MaPro: Transactions")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.transactions_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.transactions_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.transactions_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.transactions_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
            self.transactions_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.transactions_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
            self.transactions_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
            self.transactions_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

            self.transactions_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.transactions_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
            self.transactions_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            # Connect navbar buttons
            self.transactions_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.transactions_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
            self.transactions_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.transactions_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
            # self.transactions_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
            self.transactions_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

            # Connect logout button
            self.transactions_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.transactions_initialized = True

    # ===============================================================================================

    def setup_history_records_ui(self):
        """Setup the history records UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MaPro: History Records")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.history_records_initialized:  # Ensure connections are made only once
            # Set images and icons for the navbar
            self.history_records_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
            self.history_records_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
            self.history_records_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
            self.history_records_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
            self.history_records_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
            self.history_records_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
            self.history_records_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord.svg'))

            self.history_records_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
            self.history_records_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
            self.history_records_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

            self.history_records_screen.hisrec_Button_CitizenHistory.setIcon(QIcon('Assets/Images/img_history_citizen.png'))
            self.history_records_screen.hisrec_Button_MedicalHistory.setIcon(QIcon('Assets/Images/img_history_medical.png'))
            self.history_records_screen.hisrec_Button_SettlementHistory.setIcon(QIcon('Assets/Images/img_history_settlement.png'))

            # Connect navbar buttons
            self.history_records_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
            self.history_records_screen.nav_buttonCitizenPanel.clicked.connect(self.goto_citizen_panel)
            self.history_records_screen.nav_buttonStatistics.clicked.connect(self.goto_statistics)
            self.history_records_screen.nav_buttonInstitutions.clicked.connect(self.goto_institutions)
            self.history_records_screen.nav_buttonTransactions.clicked.connect(self.goto_transactions)
            # self.history_records_screen.nav_buttonHistoryRecords.clicked.connect(self.goto_history_records)

            # Connect logout button
            self.history_records_screen.logout_buttonLogout.clicked.connect(self.logout_button_clicked)

            self.history_records_initialized = True

    # ===============================================================================================

    def setup_demographics_ui(self):
        """Setup the Demographics UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MaPro: Statistics > Demographics")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_demo_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_demo_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))
            self.statistics_demo_screen.icon_male.setIcon(QIcon('Assets/Icons/icon_male.png'))
            self.statistics_demo_screen.icon_female.setIcon(QIcon('Assets/Icons/icon_female.png'))

            # Return Button
            self.statistics_demo_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_demo_initialized = True

    # ===============================================================================================

    def setup_geographic_ui(self):
        """Setup the Geographic UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MaPro: Statistics > Geographic")
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
        self.setWindowTitle("MaPro: Statistics > Household")
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
        self.setWindowTitle("MaPro: Statistics > Socio-Economic")
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
        self.setWindowTitle("MaPro: Statistics > Voters")
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
        self.setWindowTitle("MaPro: Statistics > Health")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_health_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_health_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_health_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_health_initialized = True

    # ===============================================================================================

    def setup_job_ui(self):
        """Setup the Job UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MaPro: Statistics > Jobs")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_jobs_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_jobs_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_jobs_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_jobs_initialized = True

    # ===============================================================================================

    def setup_group_ui(self):
        """Setup the Groups UI layout."""
        self.setFixedSize(1350, 850)  # Set size for schedules screen
        self.setWindowTitle("MaPro: Statistics > Groups")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        if not self.statistics_groups_initialized:  # Ensure connections are made only once

            # Set images and icons
            self.statistics_groups_screen.btn_returnToStatisticsPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))

            # Return Button
            self.statistics_groups_screen.btn_returnToStatisticsPage.clicked.connect(self.goto_statistics)

            self.statistics_groups_initialized = True

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

    def goto_citizen_panel(self):
        """Handle navigation to citizen panel screen."""
        print("-- Navigating to Citizen Panel")
        self.setup_citizen_panel_ui()  # Ensure citizen panel is set up
        self.stack.setCurrentIndex(1)  # Switch to citizen panel screen

    def goto_statistics(self):
        """Handle navigation to statistics screen."""
        print("-- Navigating to Statistics")
        self.setup_statistics_ui()  # Ensure statistics is set up
        self.stack.setCurrentIndex(2)  # Switch to statistics screen

    def goto_institutions(self):
        """Handle navigation to Institutions screen."""
        print("-- Navigating to Institutions")
        self.setup_institutions_ui()  # Ensure Institutions is set up
        self.stack.setCurrentIndex(3)  # Switch to Institutions screen

    def goto_transactions(self):
        """Handle navigation to Transactions screen."""
        print("-- Navigating to Transactions")
        self.setup_transactions_ui()  # Ensure Transactions is set up
        self.stack.setCurrentIndex(4)  # Switch to Transactions screen

    def goto_history_records(self):
        """Handle navigation to History Records screen."""
        print("-- Navigating to History Records")
        self.setup_history_records_ui()  # Ensure History Records is set up
        self.stack.setCurrentIndex(5)  # Switch to History Records screen

    def goto_demographics(self):
        """Handle navigation to demographic screen."""
        print("-- Navigating to Statistics > Demographics")
        self.setup_demographics_ui()  # Ensure Demographics is set up
        self.stack.setCurrentIndex(6)  # Switch to Demographics screen

    def goto_geographics(self):
        """Handle navigation to geographic screen."""
        print("-- Navigating to Statistics > Geographics")
        self.setup_geographic_ui()  # Ensure Geographics is set up
        self.stack.setCurrentIndex(7)  # Switch to Geographics screen

    def goto_household(self):
        """Handle navigation to household screen."""
        print("-- Navigating to Statistics > Household")
        self.setup_household_ui()  # Ensure Household is set up
        self.stack.setCurrentIndex(8)  # Switch to Household screen

    def goto_socioeco(self):
        """Handle navigation to socio-economic screen."""
        print("-- Navigating to Statistics > Socio-Economic")
        self.setup_socioeco_ui()  # Ensure Socio-Economic is set up
        self.stack.setCurrentIndex(9)  # Switch to Socio-Economic screen

    def goto_voters(self):
        """Handle navigation to voters screen."""
        print("-- Navigating to Statistics > Voters")
        self.setup_voters_ui()  # Ensure Voters is set up
        self.stack.setCurrentIndex(10)  # Switch to Voters screen

    def goto_health(self):
        """Handle navigation to health screen."""
        print("-- Navigating to Statistics > Health")
        self.setup_health_ui()  # Ensure Health is set up
        self.stack.setCurrentIndex(11)  # Switch to Health screen

    def goto_jobs(self):
        """Handle navigation to jobs screen."""
        print("-- Navigating to Statistics > Jobs")
        self.setup_job_ui()  # Ensure Jobs is set up
        self.stack.setCurrentIndex(12)  # Switch to Jobs screen

    def goto_groups(self):
        """Handle navigation to groups screen."""
        print("-- Navigating to Statistics > Groups")
        self.setup_group_ui()  # Ensure Groups is set up
        self.stack.setCurrentIndex(13)  # Switch to Groups screen

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