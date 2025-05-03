import cv2
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog, QButtonGroup, QRadioButton, QComboBox, QLineEdit

from Functions.base_file_func import base_file_func
from Utils.utils_datetime import update_date_label
from Utils.util_popup import load_popup

class citizen_profile_func(base_file_func):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)
        self.stack = stack
        self.cp_profile_screen = self.load_ui("UI/MainPages/CitizenPanelPages/cp_citizenprofile.ui")
        self.setup_profile_ui()
        self.center_on_screen()
        self.citizen_data = {}
        self.part1_popup = None
        self.part2_popup = None
        self.part3_popup = None

    def setup_profile_ui(self):
        self.setFixedSize(1350, 850)
        self.setWindowTitle("MaPro: Citizen Profile")
        self.setWindowIcon(QIcon("Assets/AppIcons/appicon_active_u.ico"))
        self.cp_profile_screen.btn_returnToCitizenPanelPage.setIcon(QIcon('Assets/FuncIcons/img_return.png'))
        self.cp_profile_screen.cp_CitizenName_buttonSearch.setIcon(QIcon('Assets/FuncIcons/icon_search_w.svg'))
        self.cp_profile_screen.cp_citizen_button_register.setIcon(QIcon('Assets/FuncIcons/icon_add.svg'))
        self.cp_profile_screen.cp_citizen_button_update.setIcon(QIcon('Assets/FuncIcons/icon_edit.svg'))
        self.cp_profile_screen.cp_citizen_button_remove.setIcon(QIcon('Assets/FuncIcons/icon_del.svg'))
        self.cp_profile_screen.profileList_buttonFilter.setIcon(QIcon('Assets/FuncIcons/icon_filter.svg'))
        self.cp_profile_screen.btn_returnToCitizenPanelPage.clicked.connect(self.goto_citizen_panel)
        self.cp_profile_screen.cp_citizen_button_register.clicked.connect(self.show_register_citizen_part_01_popup)




    #
    #
    # CITIZEN CREATE PART 1
    #
    #


    def show_register_citizen_part_01_popup(self):
        self.part1_popup = load_popup("UI/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_01.ui", self)
        self.part1_popup.setWindowTitle("Register New Citizen")
        self.part1_popup.setWindowModality(Qt.ApplicationModal)
        self.part1_popup.setFixedSize(self.part1_popup.size())
        self.part1_popup.register_buttonPrev.setIcon(QIcon('Assets/FuncIcons/icon_arrow_prev'))
        self.part1_popup.register_buttonConfirmPart1_NextToPart2.setIcon(QIcon('Assets/FuncIcons/icon_arrow_next'))
        self.part1_popup.register_buttonConfirmPart1_NextToPart2.clicked.connect(self.validate_part1_fields)
        self.setup_radio_button_groups_01(self.part1_popup)
        self.setup_image_handlers(self.part1_popup)
        if hasattr(self, 'citizen_data'):
            self.restore_part1_data()
        self.part1_popup.exec_()


        # DATA INTERACTION PART 1

    def restore_part1_data(self):
        if 'first_name' in self.citizen_data:
            self.part1_popup.register_citizen_firstname.setText(self.citizen_data['first_name'])
        if 'last_name' in self.citizen_data:
            self.part1_popup.register_citizen_lastname.setText(self.citizen_data['last_name'])
        if 'civil_status' in self.citizen_data:
            index = self.part1_popup.register_citizen_comboBox_CivilStatus.findText(self.citizen_data['civil_status'])
            if index >= 0:
                self.part1_popup.register_citizen_comboBox_CivilStatus.setCurrentIndex(index)
        if 'dob' in self.citizen_data:
            from PySide6.QtCore import QDate
            date = QDate.fromString(self.citizen_data['dob'], "yyyy-MM-dd")
            self.part1_popup.register_citizen_date_dob.setDate(date)
        if 'gender' in self.citizen_data:
            if self.citizen_data['gender'] == 'Male':
                self.part1_popup.radioButton_male.setChecked(True)
            else:
                self.part1_popup.radioButton_female.setChecked(True)
        if 'image' in self.citizen_data and self.citizen_data['image']:
            self.part1_popup.imageLabel.setPixmap(self.citizen_data['image'])

    def validate_part1_fields(self):
        errors = []
        if not self.part1_popup.register_citizen_firstname.text().strip():
            errors.append("First name is required")
        if not self.part1_popup.register_citizen_lastname.text().strip():
            errors.append("Last name is required")
        if self.part1_popup.register_citizen_comboBox_CivilStatus.currentIndex() == -1:
            errors.append("Civil status is required")
        if not self.part1_popup.register_citizen_date_dob.date().isValid():
            errors.append("Valid date of birth is required")
        if not (self.part1_popup.radioButton_male.isChecked() or self.part1_popup.radioButton_female.isChecked()):
            errors.append("Gender selection is required")
        if errors:
            QMessageBox.warning(self.part1_popup, "Incomplete Form", "Please complete all required fields:\n\n• " + "\n• ".join(errors))
            self.highlight_missing_fields01(errors)
        else:
            self.save_part1_data()
            self.show_register_citizen_part_02_popup(self.part1_popup)

    def save_part1_data(self):
        self.citizen_data.update({
            'first_name': self.part1_popup.register_citizen_firstname.text().strip(),
            'last_name': self.part1_popup.register_citizen_lastname.text().strip(),
            'civil_status': self.part1_popup.register_citizen_comboBox_CivilStatus.currentText(),
            'dob': self.part1_popup.register_citizen_date_dob.date().toString("yyyy-MM-dd"),
            'gender': 'Male' if self.part1_popup.radioButton_male.isChecked() else 'Female',
            'image': self.part1_popup.imageLabel.pixmap()
        })

        # GENERAL FUNCTION PART 1


    def setup_radio_button_groups_01(self, popup):
        # self.sex_group = QButtonGroup(popup)
        # self.sex_group.addButton(popup.radioButton_male) OLLD DO NNOT TOUCH!
        # self.sex_group.addButton(popup.radioButton_female)

        sex_group = QButtonGroup(self.part1_popup)

        male_yes = self.part1_popup.findChild(QRadioButton, "radioButton_IsMale_Yes")
        male_no = self.part1_popup.findChild(QRadioButton, "radioButton_IsMale_No")

        if male_yes and male_no:
            sex_group.addButton(male_yes)
            sex_group.addButton(male_no)

    def highlight_missing_fields01(self, errors):
        if "First name is required" in errors:
            self.part1_popup.register_citizen_firstname.setStyleSheet("border: 1px solid red;")
        if "Last name is required" in errors:
            self.part1_popup.register_citizen_lastname.setStyleSheet("border: 1px solid red;")
        if "Civil status is required" in errors:
            self.part1_popup.register_citizen_comboBox_CivilStatus.setStyleSheet("border: 1px solid red;")
        if "Valid date of birth is required" in errors:
            self.part1_popup.register_citizen_date_dob.setStyleSheet("border: 1px solid red;")
        if "Gender selection is required" in errors:
            self.part1_popup.radioButton_male.setStyleSheet("color: red;")
            self.part1_popup.radioButton_female.setStyleSheet("color: red;")

    def setup_image_handlers(self, popup):
        popup.uploadButton.setIcon(QIcon("Assets/Icons/icon_upload_image.svg"))
        popup.captureButton.setIcon(QIcon("Assets/Icons/icon_camera.svg"))
        popup.uploadButton.clicked.connect(lambda: self.upload_image(popup.imageLabel))
        popup.captureButton.clicked.connect(lambda: self.capture_photo(popup.imageLabel))

    def upload_image(self, image_label):
        file_path, _ = QFileDialog.getOpenFileName(self.part1_popup, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            pixmap = QPixmap(file_path)
            image_label.setPixmap(pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio))

    def capture_photo(self, image_label):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.warning(self.part1_popup, "Error", "Could not open webcam")
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



    #
    #
    # CITIZEN CREATE PART 2
    #
    #



    def show_register_citizen_part_02_popup(self, part_one_popup):
        part_one_popup.close()
        self.part2_popup = load_popup("UI/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_02.ui", self)
        self.part2_popup.setWindowTitle("Register New Citizen - Part 2")
        self.part2_popup.setWindowModality(Qt.ApplicationModal)
        self.part2_popup.setFixedSize(self.part2_popup.size())
        self.part2_popup.register_buttonReturnToPart1_FromPart2.setIcon(QIcon('Assets/FuncIcons/icon_arrow_prev'))
        self.part2_popup.register_buttonConfirmPart2_NextToPart3.setIcon(QIcon('Assets/FuncIcons/icon_arrow_next'))
        self.part2_popup.register_buttonConfirmPart2_NextToPart3.clicked.connect(self.validate_part2_fields)
        self.part2_popup.register_buttonReturnToPart1_FromPart2.clicked.connect(self.return_to_part1_from_part2)
        if hasattr(self, 'citizen_data'):
            self.restore_part2_data()
        self.setup_radio_button_groups_02()
        self.part2_popup.exec_()






    # DATA INTERACTION PART 2



    def restore_part2_data(self):
        if 'household_id' in self.citizen_data:
            self.part2_popup.register_citizen_HouseholdID.setText(self.citizen_data['household_id'])
        if 'relationship' in self.citizen_data:
            index = self.part2_popup.register_citizen_comboBox_Relationship.findText(self.citizen_data['relationship'])
            if index >= 0:
                self.part2_popup.register_citizen_comboBox_Relationship.setCurrentIndex(index)

    def return_to_part1_from_part2(self):
        self.save_part2_data()
        self.part2_popup.close()
        self.show_register_citizen_part_01_popup()

    def save_part2_data(self):
        self.citizen_data.update({
            'household_id': self.part2_popup.register_citizen_HouseholdID.text().strip(),
            'relationship': self.part2_popup.register_citizen_comboBox_Relationship.currentText(),
        })

    def validate_part2_fields(self):
        errors2 = []
        if not self.part2_popup.register_citizen_HouseholdID.text().strip():
            errors2.append("HouseHold ID is required")
        if self.part2_popup.register_citizen_comboBox_Relationship.currentIndex() == -1:
            errors2.append("Relationship is required")
        if errors2:
            QMessageBox.warning(self.part2_popup, "Incomplete Form", "Please complete all required fields:\n\n• " + "\n• ".join(errors2))
            self.highlight_missing_fields02(errors2)
        else:
            self.save_part2_data()
            # self.highlight_missing_fields02(errors2)
            self.show_register_citizen_part_03_popup(self.part2_popup)





    # GENERAL FUCNTION PART 2


    def highlight_missing_fields02(self, errors2):
        if "HouseHold ID is required" in errors2:
            self.part2_popup.register_citizen_HouseholdID.setStyleSheet("border: 1px solid red;")
        if "Relationship is required" in errors2:
            self.part2_popup.register_citizen_comboBox_Relationship.setStyleSheet("border: 1px solid red;")

    def setup_radio_button_groups_02(self):
        gov_worker = QButtonGroup(self.part2_popup)
        gov_worker_yes = self.part2_popup.findChild(QRadioButton, "radioButton_IsGov_Yes")
        gov_worker_no = self.part2_popup.findChild(QRadioButton, "radioButton_IsGov_No")
        if gov_worker_yes and gov_worker_no:
            gov_worker.addButton(gov_worker_yes)
            gov_worker.addButton(gov_worker_no)

        phil_member = QButtonGroup(self.part2_popup)
        phil_member_yes = self.part2_popup.findChild(QRadioButton, "radioButton_IsPhilMem_Yes")
        phil_member_no = self.part2_popup.findChild(QRadioButton, "radioButton_IsPhilMem_No")
        if phil_member_yes and phil_member_no:
            phil_member.addButton(phil_member_yes)
            phil_member.addButton(phil_member_no)



    def highlight_missing_fields01(self, errors):
        if "First name is required" in errors:
            self.part1_popup.register_citizen_firstname.setStyleSheet("border: 1px solid red;")
        if "Last name is required" in errors:
            self.part1_popup.register_citizen_lastname.setStyleSheet("border: 1px solid red;")
        if "Civil status is required" in errors:
            self.part1_popup.register_citizen_comboBox_CivilStatus.setStyleSheet("border: 1px solid red;")
        if "Valid date of birth is required" in errors:
            self.part1_popup.register_citizen_date_dob.setStyleSheet("border: 1px solid red;")
        if "Gender selection is required" in errors:
            self.part1_popup.radioButton_male.setStyleSheet("color: red;")
            self.part1_popup.radioButton_female.setStyleSheet("color: red;")


    #
    #
    # CITIZEN CREATE PART 3
    #
    #





    def show_register_citizen_part_03_popup(self, part_two_popup):
        part_two_popup.close()
        self.part3_popup = load_popup("UI/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_03.ui", self)
        self.part3_popup.setWindowTitle("Register New Citizen - Part 3")
        self.part3_popup.setWindowModality(Qt.ApplicationModal)
        self.part3_popup.setFixedSize(self.part3_popup.size())
        self.part3_popup.register_buttonReturnToPart2_FromPart3.setIcon(QIcon('Assets/FuncIcons/icon_arrow_prev'))
        self.part3_popup.register_buttonConfirmPart3_SaveForm.setIcon(QIcon('Assets/FuncIcons/icon_confirm'))
        if hasattr(self, 'citizen_data'):
            self.restore_part3_data()
        self.setup_radio_button_groups_03()
        save_btn = self.part3_popup.findChild(QPushButton, "register_buttonConfirmPart3_SaveForm")
        if save_btn:
            save_btn.clicked.connect(self.confirm_and_save)
        back_btn = self.part3_popup.findChild(QPushButton, "register_buttonReturnToPart2_FromPart3")
        if back_btn:
            back_btn.clicked.connect(self.return_to_part2_from_part3)
        self.part3_popup.exec_()




    # DATA INTERACTION PART 3




    def restore_part3_data(self):
        pass



    # GENERAL FUNCTION PART 3



    def setup_radio_button_groups_03(self):
        radio_student = QButtonGroup(self.part3_popup)
        student_yes = self.part3_popup.findChild(QRadioButton, "radioButton_IsStudent_Yes")
        student_no = self.part3_popup.findChild(QRadioButton, "radioButton_IsStudent_No")
        if student_yes and student_no:
            radio_student.addButton(student_yes)
            radio_student.addButton(student_no)

        radio_famplan = QButtonGroup(self.part3_popup)
        famplan_yes = self.part3_popup.findChild(QRadioButton, "radioButton_IsFamPlan_Yes")
        famplan_no = self.part3_popup.findChild(QRadioButton, "radioButton_IsFamPlan_No")
        if famplan_yes and famplan_no:
            radio_famplan.addButton(famplan_yes)
            radio_famplan.addButton(famplan_no)

        radio_pwd = QButtonGroup(self.part3_popup)
        pwd_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_IsPWD_Yes")
        pwd_no = self.part3_popup.findChild(QRadioButton, "register_citizen_IsPWD_No")
        if pwd_yes and pwd_no:
            radio_pwd.addButton(pwd_yes)
            radio_pwd.addButton(pwd_no)

        radio_voter = QButtonGroup(self.part3_popup)
        vote_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_RegVote_Yes")
        vote_no = self.part3_popup.findChild(QRadioButton, "register_citizen_RegVote_No")
        if vote_yes and vote_no:
            radio_voter.addButton(vote_yes)
            radio_voter.addButton(vote_no)

        radio_deceased = QButtonGroup(self.part3_popup)
        deceased_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_Deceased_Yes")
        deceased_no = self.part3_popup.findChild(QRadioButton, "register_citizen_Deceased_No")
        if deceased_yes and deceased_no:
            radio_deceased.addButton(deceased_yes)
            radio_deceased.addButton(deceased_no)

        radio_indigenous = QButtonGroup(self.part3_popup)
        ind_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_IndGroup_Yes")
        ind_no = self.part3_popup.findChild(QRadioButton, "register_citizen_IndGroup_No")
        if ind_yes and ind_no:
            radio_indigenous.addButton(ind_yes)
            radio_indigenous.addButton(ind_no)

    def confirm_and_save(self):
        reply = QMessageBox.question(self.part3_popup, "Confirm Registration", "Are you sure you want to register this citizen?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("-- Form Submitted")
            QMessageBox.information(self.part3_popup, "Success", "Citizen successfully registered!")
            self.citizen_data = {}
            self.part3_popup.close()

    def return_to_part2_from_part3(self):
        self.part3_popup.close()
        self.show_register_citizen_part_02_popup(self.part3_popup)

    def goto_citizen_panel(self):
        if not hasattr(self, 'citizen_panel'):
            from Functions.Main.Citizen_Panel.citizen_func import citizen_func
            self.citizen_panel = citizen_func(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)
        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")