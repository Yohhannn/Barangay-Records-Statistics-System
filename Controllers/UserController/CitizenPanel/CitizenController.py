import cv2
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QButtonGroup, QRadioButton, QStackedWidget
from Controllers.BaseFileController import BaseFileController
from Models.CitizenModel import CitizenModel
from Views.CitizenPanel.CitizenView import CitizenView
from Utils.util_popup import load_popup

class CitizenController(BaseFileController):
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)

        # INITIALIZE OBJECTS NEEDED
        self.stack = stack
        self.model = CitizenModel()
        self.view = CitizenView(self)


        self.cp_profile_screen = self.load_ui("Resources/UIs/MainPages/CitizenPanelPages/cp_citizenprofile.ui")
        self.view.setup_profile_ui(self.cp_profile_screen)


        # self.part1_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_01.ui")
        # self.view.show_register_citizen_part_01_popup(self.part1_popup)

        # self.view.setup_citizen_panel_ui(self.cp_profile_screen)
        self.center_on_screen()
        self.citizen_data = {}
        self.part1_popup = None
        self.part2_popup = None
        self.part3_popup = None

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        # self.stacked_widget = QStackedWidget()



    #
    #
    # POP UP UI INITIALIZATION
    #
    #

    def show_register_citizen_part_01_initialize(self):
        print("-- Register New Citizen Part 1 Popup")
        self.part1_popup = self.view.show_register_citizen_part_01_popup(self)
        self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
        self.part3_popup = self.view.show_register_citizen_part_03_popup(self)
        # self.stacked_widget.addWidget(self.part1_popup)
        # self.stacked_widget.addWidget(self.part2_popup)
        #
        # self.stacked_widget.setCurrentIndex(0)
        # if hasattr(self, 'citizen_data'):
        #     self.restore_part1_data()
        self.part1_popup.show()
        # self.part2_popup.close()
        print("test")


    def show_register_citizen_part_02_initialize(self):
        print("-- Register New Citizen Part 2 Popup")
        self.part2_popup.show()
        # self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
        # self.part2_popup.register_citizen_HouseholdID.setText('test')


        # if hasattr(self, 'citizen_data'):
        self.part2_popup.exec_()
        # self.restore_part2_data()

    def show_register_citizen_part_03_initialize(self):
        print("-- Register New Citizen Part 3 Popup")
        self.part3_popup.show()
        # self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
        # self.part2_popup.register_citizen_HouseholdID.setText('test')

        # if hasattr(self, 'citizen_data'):
        self.part3_popup.exec_()
        # self.restore_part3_data()

        # DATA INTERACTION PART 1

    def get_form_data_part_1(self):
        return{
        #PART 1
            'first_name': self.part1_popup.register_citizen_firstname.text().strip(), # REQUIRED
            'middle_name': self.part1_popup.register_citizen_middlename.text().strip(),
            'last_name': self.part1_popup.register_citizen_lastname.text().strip(), # REQUIRED
            'suffix': self.part1_popup.register_citizen_suffix.text().strip(),

            'civil_status': self.part1_popup.register_citizen_comboBox_CivilStatus.currentText().strip(), # REQUIRED
            'birth_date': self.part1_popup.register_citizen_date_dob.date().toString("yyyy-MM-dd"), # REQUIRED

            'religion': self.part1_popup.register_citizen_comboBox_Religion.currentText().strip(), # REQUIRED
            'religion_others': self.part1_popup.register_citizen_religion_others.text().strip(), # REQUIRED

            'blood_type': self.part1_popup.register_citizen_comboBox_BloodType.currentText().strip(),
            'sex': self.radio_button_sex_result(),  #'Male' if self.part1_popup.radioButton_male.isChecked(), 'Female' if self.part1_popup.radioButton_female.isChecked(), # REQUIRED

            'contact_number': self.part1_popup.register_citizen_ContactNumber.text().strip(),
            'email_address': self.part1_popup.register_citizen_Email.text().strip(),

            'sitio': self.part1_popup.register_citizen_comboBox_Sitio.currentText().strip(), # REQUIRED
            'place_of_birth': self.part1_popup.register_citizen_Pob.text().strip(),
            'full_address': self.part1_popup.register_citizen_FullAddress.toPlainText()
        }

    def get_form_data_part_2(self):
        return{
            # PART 2

            # socio info
            'socio_eco_status': self.part2_popup.register_citizen_comboBox_SocEcoStat.currentText().strip(),
            'nhts_number': self.part2_popup.register_citizen_NHTSNum.text().strip(),

            # house hold info
            'household_id': self.part2_popup.register_citizen_HouseholdID.text().strip(),
            'relationship': self.part2_popup.register_citizen_comboBox_Relationship.currentText().strip(),
            'other_relationship': self.part2_popup.register_citizen_HouseholdRelationshipOther.text().strip(),

            # work information

            'employment_status': self.part2_popup.register_citizen_comboBox_EmploymentStatus.currentText().strip(),
            'occupation': self.part2_popup.register_citizen_Occupation.text().strip(),
            'gov_worker': self.radio_button_gov_worker_result(),
            'phil_member': self.radio_button_phil_member_result(),
            'phil_category': self.part2_popup.register_citizen_comboBox_PhilCat.currentText().strip(),
            'phil_id': self.part2_popup.register_citizen_PhilID.text().strip(),
            'membership_type': self.part2_popup.register_citizen_comboBox_PhilMemType.currentText().strip()
        }


    #
    # BUTTON FUNCTIONS
    #



    def radio_button_sex_result(self):
        if self.part1_popup.radioButton_male.isChecked():
            sex_value = 'Male'
        elif self.part1_popup.radioButton_female.isChecked():
            sex_value = 'Female'
        else:
            sex_value = ''
        return sex_value

    def radio_button_gov_worker_result(self):
        if self.part2_popup.radioButton_IsGov_Yes.isChecked():
            gov_worker = 'Yes'
        elif self.part2_popup.radioButton_IsGov_No.isChecked():
            gov_worker = 'No'
        else:
            gov_worker = ''
        return gov_worker


    def radio_button_phil_member_result(self):
        if self.part2_popup.radioButton_IsPhilMem_Yes.isChecked():
            phil_member = 'Yes'
        elif self.part2_popup.radioButton_IsPhilMem_No.isChecked():
            phil_member = 'No'
        else:
            phil_member = ''
        return phil_member


    def validate_part1_fields(self, popup):
        form_data_part_1 = self.get_form_data_part_1()
        errors_part_1 = []
        print(form_data_part_1)

        if not form_data_part_1['first_name']:
            errors_part_1.append("First name is required.")
            self.part1_popup.register_citizen_firstname.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.part1_popup.register_citizen_firstname.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if not form_data_part_1['last_name']:
            errors_part_1.append("Last name is required.")
            self.part1_popup.register_citizen_lastname.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.part1_popup.register_citizen_lastname.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if not form_data_part_1['civil_status']:
            errors_part_1.append("Civil status is required.")
            self.part1_popup.register_citizen_comboBox_CivilStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part1_popup.register_citizen_comboBox_CivilStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        if not form_data_part_1['religion']:
            errors_part_1.append("Religion is required.")
            self.part1_popup.register_citizen_comboBox_Religion.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        elif form_data_part_1['religion'] == 'Others':
            if not form_data_part_1['religion_others']:
                errors_part_1.append("Religion is required.")
                self.part1_popup.register_citizen_religion_others.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
                self.part1_popup.register_citizen_comboBox_Religion.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
            else:
                self.part1_popup.register_citizen_religion_others.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
                self.part1_popup.register_citizen_comboBox_Religion.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
        else:
            self.part1_popup.register_citizen_comboBox_Religion.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
            self.part1_popup.register_citizen_religion_others.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        if not form_data_part_1['sex']:
            errors_part_1.append("Sex is required.")
            self.part1_popup.radioButton_female.setStyleSheet("color: red")
            self.part1_popup.radioButton_male.setStyleSheet("color: red")
        else:
            self.part1_popup.radioButton_female.setStyleSheet("color: rgb(18, 18, 18)")
            self.part1_popup.radioButton_male.setStyleSheet("color: rgb(18, 18, 18)")
        if not form_data_part_1['sitio']:
            errors_part_1.append("Sitio is required.")
            self.part1_popup.register_citizen_comboBox_Sitio.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part1_popup.register_citizen_comboBox_Sitio.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        if errors_part_1:
            self.view.show_error_message(errors_part_1)
        else:
            # self.save_part1_data()
            self.part1_popup.close()
            # self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
            #
            # self.part2_popup.show()
            self.show_register_citizen_part_02_initialize()
            # self.show_register_citizen_part_02_initialize()

    def validate_part2_fields(self):
        form_data_part_2 = self.get_form_data_part_2()
        errors_part_2 = []
        print(form_data_part_2)

        if not form_data_part_2['socio_eco_status']:
            errors_part_2.append("Socio Economic Status is required.")
            self.part2_popup.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        elif form_data_part_2['socio_eco_status'] == 'NHTS 4Ps' or form_data_part_2['socio_eco_status'] == 'NHTS Non-4Ps':
            if not form_data_part_2['nhts_number']:
                errors_part_2.append("NHTS Number is required.")
                self.part2_popup.register_citizen_NHTSNum.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
                self.part2_popup.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
            else:
                self.part2_popup.register_citizen_NHTSNum.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
                self.part2_popup.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
        else:
            self.part2_popup.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
            self.part2_popup.register_citizen_NHTSNum.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if not form_data_part_2['employment_status']:
            errors_part_2.append("Employment Status is required.")
            self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )


        if not form_data_part_2['household_id']:
            errors_part_2.append("Household ID is required.")
            self.part2_popup.register_citizen_HouseholdID.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.part2_popup.register_citizen_HouseholdID.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if not form_data_part_2['relationship']:
            errors_part_2.append("Relationship is required.")
            self.part2_popup.register_citizen_comboBox_Relationship.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        elif form_data_part_2['relationship'] == 'Others':
            if not form_data_part_2['other_relationship']:
                errors_part_2.append("Relationship is required.")
                self.part2_popup.register_citizen_HouseholdRelationshipOther.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
                self.part2_popup.register_citizen_comboBox_Relationship.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
            else:
                self.part2_popup.register_citizen_HouseholdRelationshipOther.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
                self.part2_popup.register_citizen_comboBox_Relationship.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
        else:
            self.part2_popup.register_citizen_comboBox_Relationship.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
            self.part2_popup.register_citizen_HouseholdRelationshipOther.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        if not form_data_part_2['employment_status']:
            errors_part_2.append("Employment Status is required.")
            self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )


        if form_data_part_2['phil_member'] == 'Yes':
            if not form_data_part_2['phil_category']:
                errors_part_2.append("Philhealth Category is required.")
                self.part2_popup.register_citizen_comboBox_PhilCat.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
            else:
                self.part2_popup.register_citizen_comboBox_PhilCat.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
            if not form_data_part_2['phil_id']:
                errors_part_2.append("Philhealth ID is required.")
                self.part2_popup.register_citizen_PhilID.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            else:
                self.part2_popup.register_citizen_PhilID.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            if not form_data_part_2['membership_type']:
                errors_part_2.append("Membership Type is required.")
                self.part2_popup.register_citizen_comboBox_PhilMemType.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
            else:
                self.part2_popup.register_citizen_comboBox_PhilMemType.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )



        if errors_part_2:
            self.view.show_error_message(errors_part_2)
        else:
            # self.save_part1_data()
            self.part2_popup.close()
            # self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
            #
            # self.part2_popup.show()
            self.show_register_citizen_part_03_initialize()
            # self.show_register_citizen_part_02_initialize()


    # def save_part1_data(self):
    #     self.citizen_data.update(self.get_form_data_part_1())


            # 'first_name': popup.register_citizen_firstname.text().strip(),
            # 'last_name': popup.register_citizen_lastname.text().strip(),
            # 'civil_status': popup.register_citizen_comboBox_CivilStatus.currentText(),
            # 'dob': popup.register_citizen_date_dob.date().toString("yyyy-MM-dd"),
            # 'gender': 'Male' if popup.radioButton_male.isChecked() else 'Female',
            # 'image': popup.imageLabel.pixmap()
    #
    # def save_part1_data(self):
    #     self.citizen_data.update({
    #         'first_name': self.part1_popup.register_citizen_firstname.text().strip(),
    #         'last_name': self.part1_popup.register_citizen_lastname.text().strip(),
    #         'civil_status': self.part1_popup.register_citizen_comboBox_CivilStatus.currentText(),
    #         'dob': self.part1_popup.register_citizen_date_dob.date().toString("yyyy-MM-dd"),
    #         'gender': 'Male' if self.part1_popup.radioButton_male.isChecked() else 'Female',
    #         'image': self.part1_popup.imageLabel.pixmap()
    #     })
    #
    # def restore_part1_data(self):
    #     if 'first_name' in self.citizen_data:
    #         self.part1_popup.register_citizen_firstname.setText(self.citizen_data['first_name'])
    #     if 'last_name' in self.citizen_data:
    #         self.part1_popup.register_citizen_lastname.setText(self.citizen_data['last_name'])
    #     if 'civil_status' in self.citizen_data:
    #         index = self.part1_popup.register_citizen_comboBox_CivilStatus.findText(self.citizen_data['civil_status'])
    #         if index >= 0:
    #             self.part1_popup.register_citizen_comboBox_CivilStatus.setCurrentIndex(index)
    #     if 'dob' in self.citizen_data:
    #         from PySide6.QtCore import QDate
    #         date = QDate.fromString(self.citizen_data['dob'], "yyyy-MM-dd")
    #         self.part1_popup.register_citizen_date_dob.setDate(date)
    #     if 'gender' in self.citizen_data:
    #         if self.citizen_data['gender'] == 'Male':
    #             self.part1_popup.radioButton_male.setChecked(True)
    #         else:
    #             self.part1_popup.radioButton_female.setChecked(True)
    #     if 'image' in self.citizen_data and self.citizen_data['image']:
    #         self.part1_popup.imageLabel.setPixmap(self.citizen_data['image'])


        # GENERAL FUNCTION PART 1



    def setup_image_handlers(self, popup):
        popup.uploadButton.setIcon(QIcon("Resources/Icons/General_Icons/icon_upload_image.svg"))
        popup.captureButton.setIcon(QIcon("Resources/Icons/General_Icons/icon_camera.svg"))
        popup.uploadButton.clicked.connect(lambda: self.upload_image(popup.imageLabel))
        popup.captureButton.clicked.connect(lambda: self.capture_photo(popup.imageLabel))

    def upload_image(self, image_label):
        file_path, _ = QFileDialog.getOpenFileName(self.part1_popup, "Select an Image", "", "General_Images (*.png *.jpg *.jpeg *.bmp *.gif)")
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
    #
    # def show_register_citizen_part_02_initialize(self):
    #     self.part1_popup.close()
    #     print("-- Register New Citizen Part 2 Popup")
    #     self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
    #     # if hasattr(self, 'citizen_data'):
    #     #     self.restore_part2_data()
    #     self.part2_popup.exec_()









    # DATA INTERACTION PART 2



    def restore_part2_data(self):
        if 'household_id' in self.citizen_data:
            self.part2_popup.register_citizen_HouseholdID.setText(self.get_form_data_part_2()['household_id'])
        if 'relationship' in self.citizen_data:
            index = self.part2_popup.register_citizen_comboBox_Relationship.findText(self.citizen_data['relationship'])
            if index >= 0:
                self.part2_popup.register_citizen_comboBox_Relationship.setCurrentIndex(index)

    def return_to_part1_from_part2(self):
        # self.save_part2_data()
        print(self.get_form_data_part_2())
        self.part2_popup.close()
        self.part1_popup.show()
    def return_to_part2_from_part3(self):
        # self.save_part2_data()
        # print(self.get_form_data_part_3())
        self.part3_popup.close()
        self.part2_popup.show()


    # def save_part2_data(self):
    #     self.citizen_data.update({
    #         'household_id': self.part2_popup.register_citizen_HouseholdID.text().strip(),
    #         'relationship': self.part2_popup.register_citizen_comboBox_Relationship.currentText(),
    #     })


        # if not self.part1_popup.register_citizen_lastname.text().strip():
        #     self.part1_popup.register_citizen_lastname.setStyleSheet(
        #         "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
        #     )
        #     errors.append("Last name is required")
        # else:
        #     self.part1_popup.register_citizen_lastname.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
        #     )
        #
        # if self.part1_popup.register_citizen_comboBox_CivilStatus.currentIndex() == -1:
        #     self.part1_popup.register_citizen_comboBox_CivilStatus.setStyleSheet(
        #         "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
        #     )
        #     errors.append("Civil status is required")
        # else:
        #     self.part1_popup.register_citizen_comboBox_CivilStatus.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
        #     )


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



    #
    #
    # CITIZEN CREATE PART 3
    #
    #





    def show_register_citizen_part_03_popup(self, part_two_popup):
        part_two_popup.close()
        self.part3_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_03.ui", self)
        self.part3_popup.setWindowTitle("Register New Citizen - Part 3")
        self.part3_popup.setWindowModality(Qt.ApplicationModal)
        self.part3_popup.setFixedSize(self.part3_popup.size())
        self.part3_popup.register_buttonReturnToPart2_FromPart3.setIcon(QIcon('Resources/Icons/FuncIcons/icon_arrow_prev'))
        self.part3_popup.register_buttonConfirmPart3_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm'))
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



    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

        # self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")