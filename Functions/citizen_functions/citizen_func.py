import cv2
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QLabel, QButtonGroup, QRadioButton
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class citizen_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.citizen_panel_screen = self.load_ui("UI/MainPages/citizenpanel.ui")
        self.setup_ui()
        self.center_on_screen()

    def setup_ui(self):
        """Setup the citizen panel UI layout."""
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Citizen Panel")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))

        # Set images and icons for the navbar
        self.citizen_panel_screen.nav_imageLogo.setPixmap(QPixmap("Assets/Images/logo_brgyClear.png"))
        self.citizen_panel_screen.nav_buttonDashboard.setIcon(QIcon('Assets/Icons/icon_dashboard.svg'))
        self.citizen_panel_screen.nav_buttonCitizenPanel.setIcon(QIcon('Assets/Icons/icon_citizenpanel.svg'))
        self.citizen_panel_screen.nav_buttonStatistics.setIcon(QIcon('Assets/Icons/icon_statistics.svg'))
        self.citizen_panel_screen.nav_buttonInstitutions.setIcon(QIcon('Assets/Icons/icon_institutions.svg'))
        self.citizen_panel_screen.nav_buttonTransactions.setIcon(QIcon('Assets/Icons/icon_transaction.svg'))
        self.citizen_panel_screen.nav_buttonHistoryRecords.setIcon(QIcon('Assets/Icons/icon_historyrecord_closed.svg'))

        self.citizen_panel_screen.nav_buttonAdminPanel.setIcon(QIcon('Assets/Icons/icon_adminoverview_off.svg'))
        self.citizen_panel_screen.nav_buttonActivityLogs.setIcon(QIcon('Assets/Icons/icon_activitylogs_off.svg'))
        self.citizen_panel_screen.nav_isLocked.setIcon(QIcon('Assets/Icons/icon_isLocked.svg'))

        # Set Icons
        self.citizen_panel_screen.profileList_buttonRegister.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
        self.citizen_panel_screen.profileList_buttonRegisterHousehold.setIcon(QIcon('Assets/FuncIcons/icon_household.svg'))
        self.citizen_panel_screen.profileList_buttonDelete.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))
        self.citizen_panel_screen.profileList_buttonUpdate.setIcon(QIcon('Assets/FuncIcons/icon_edit.svg'))
        self.citizen_panel_screen.profileList_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
        self.citizen_panel_screen.profileList_buttonFilter.setIcon(QIcon('Assets/FuncIcons/icon_filter.svg'))

        # Connect buttons
        self.citizen_panel_screen.nav_buttonDashboard.clicked.connect(self.goto_dashboard)
        self.citizen_panel_screen.profileList_buttonFilter.clicked.connect(self.show_filter_popup)
        self.citizen_panel_screen.profileList_buttonRegister.clicked.connect(self.show_register_citizen_part_01_popup)

    def goto_dashboard(self):
        """Return to dashboard screen"""
        self.stack.setCurrentIndex(0)
        self.setWindowTitle("MaPro: Dashboard")

    def show_filter_popup(self):
        print("-- Navigating to Profile List > Filter Options")
        popup = load_popup("UI/PopUp/Screen_CitizenProfiles/filteroptions.ui", self)
        popup.setWindowTitle("Filter Options")
        popup.setWindowModality(Qt.ApplicationModal)
        popup.show()

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

    def show_register_citizen_part_01_popup_and_close(self, current_popup):
        current_popup.close()
        self.show_register_citizen_part_01_popup()

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
            if famplan_yes and famplan_no:
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

    def show_register_citizen_part_02_popup_and_close(self, current_popup):
        current_popup.close()
        self.show_register_citizen_part_02_popup(current_popup)