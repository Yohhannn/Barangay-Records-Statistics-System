from datetime import date

import cv2
from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QMessageBox, QPushButton, QLabel, QFileDialog,
                               QButtonGroup, QRadioButton, QTableWidgetItem)
from PySide6.QtGui import QPixmap, QIcon, Qt, QImage
from PySide6.QtWidgets import QMessageBox, QPushButton, QFileDialog, QButtonGroup, QRadioButton, QStackedWidget
from Controllers.BaseFileController import BaseFileController
from Models.CitizenModel import CitizenModel
from Views.CitizenPanel.CitizenView import CitizenView
from Utils.util_popup import load_popup
from database import Database


class CitizenController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_citizen_id = None
        self.user_role = user_role

        # INITIALIZE OBJECTS NEEDED
        self.indig_group = None
        self.deceased_group = None
        self.voter_group = None
        self.pwd_group = None
        self.fam_plan_group = None
        self.student_group = None
        self.gov_group = None
        self.sex_group = None
        self.stack = stack
        self.model = CitizenModel()
        self.view = CitizenView(self)
        print(self.sys_user_id)

        self.cp_profile_screen = self.load_ui("Resources/UIs/MainPages/CitizenPanelPages/cp_citizenprofile.ui")
        self.view.setup_profile_ui(self.cp_profile_screen)
        self.load_citizen_data()

        # self.part1_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_01.ui")
        # self.view.show_register_citizen_part_01_popup(self.part1_popup)

        # self.view.setup_citizen_panel_ui(self.cp_profile_screen)
        self.center_on_screen()
        self.citizen_data = {}
        self.part1_popup = None
        self.part2_popup = None
        self.part3_popup = None
        self.part1_popup_update = None
        self.part2_popup_update = None
        self.part3_popup_update = None

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

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT fpm_id, fpm_method FROM family_planning_method ORDER BY fpm_method ASC;")
            results = cursor.fetchall()

            combo = self.part3_popup.register_citizen_comboBox_FamilyPlanningMethod
            for fpm_id, fpm_method in results:
                combo.addItem(fpm_method, fpm_id)

        except Exception as e:
            print(f"Failed to load fpm meyhofd: {e}")
        finally:
            db.close()

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT fpms_id, fpms_status_name FROM fpm_status ORDER BY fpms_status_name ASC;")
            results = cursor.fetchall()

            combo = self.part3_popup.register_citizen_comboBox_FamPlanStatus
            for fpms_id, fpms_status_name in results:
                combo.addItem(fpms_status_name, fpms_id)

        except Exception as e:
            print(f"Failed to load fpm status: {e}")
        finally:
            db.close()

        self.gov_group = QButtonGroup()
        self.sex_group = QButtonGroup()

        self.sex_group.addButton(self.part1_popup.radioButton_male)
        self.sex_group.addButton(self.part1_popup.radioButton_female)

        self.gov_group.addButton(self.part2_popup.radioButton_IsGov_Yes)
        self.gov_group.addButton(self.part2_popup.radioButton_IsGov_No)

        self.student_group = QButtonGroup()
        self.fam_plan_group = QButtonGroup()
        self.pwd_group = QButtonGroup()
        self.voter_group = QButtonGroup()
        self.deceased_group = QButtonGroup()
        self.indig_group = QButtonGroup()

        self.student_group.addButton(self.part3_popup.radioButton_IsStudent_Yes)
        self.student_group.addButton(self.part3_popup.radioButton_IsStudent_No)

        # self.fam_plan_group.addButton(self.part3_popup.radioButton_IsFamPlan_Yes)
        # self.fam_plan_group.addButton(self.part3_popup.radioButton_IsFamPlan_No)

        # self.pwd_group.addButton(self.part3_popup.register_citizen_IsPWD_Yes)
        # self.pwd_group.addButton(self.part3_popup.register_citizen_IsPWD_No)

        self.voter_group.addButton(self.part3_popup.register_citizen_RegVote_Yes)
        self.voter_group.addButton(self.part3_popup.register_citizen_RegVote_No)

        # initialize data
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT sitio_id, sitio_name FROM sitio ORDER BY sitio_name ASC;")
            results = cursor.fetchall()

            combo = self.part1_popup.register_citizen_comboBox_Sitio
            combo.clear()
            for sitio_id, sitio_name in results:
                combo.addItem(sitio_name, sitio_id)

        except Exception as e:
            print(f"Failed to load sitios: {e}")
        finally:
            db.close()
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
        try:
            db = Database()
            cursor = db.get_cursor()
            # During setup (show_update_citizen_part_02_initialize or wherever you're filling the combo box):
            cursor.execute(
                "SELECT rth_id, rth_relationship_name FROM relationship_type ORDER BY rth_relationship_name ASC;")
            results = cursor.fetchall()

            combo = self.part2_popup.register_citizen_comboBox_Relationship
            combo.clear()
            for rth_id, rth_name in results:
                combo.addItem(rth_name, rth_id)  # ✅ Binds display text and rth_id as userData


        except Exception as e:
            print(f"Failed to load sitios: {e}")
        finally:
            db.close()
        self.part2_popup.show()

        # self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
        # self.part2_popup.register_citizen_HouseholdID.setText('test')

        # if hasattr(self, 'citizen_data'):
        self.part2_popup.exec_()
        # self.restore_part2_data()

    def show_register_citizen_part_03_initialize(self):
        print("-- Register New Citizen Part 3 Popup")
        self.part3_popup.show()

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute(
                "SELECT clah_id, clah_classification_name FROM classification_health_risk ORDER BY clah_classification_name ASC;")
            results = cursor.fetchall()

            combo = self.part3_popup.register_citizen_health_classification
            combo.clear()
            for clah_id, clah_classification_name in results:
                combo.addItem(clah_classification_name, clah_id)

        except Exception as e:
            print(f"Failed to load classitiofat: {e}")
        finally:
            db.close()

        self.deceased_group.addButton(self.part3_popup.register_citizen_Deceased_Yes)
        self.deceased_group.addButton(self.part3_popup.register_citizen_Deceased_No)

        # self.indig_group.addButton(self.part3_popup.register_citizen_IndGroup_Yes)
        # self.indig_group.addButton(self.part3_popup.register_citizen_IndGroup_No)

        # self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
        # self.part2_popup.register_citizen_HouseholdID.setText('test')

        # if hasattr(self, 'citizen_data'):
        self.part3_popup.exec_()
        # self.restore_part3_data()

        # DATA INTERACTION PART 1

    def show_update_citizen_part_01_initialize(self):
        print("-- Update Citizen Part 1 Popup")
        if not self.selected_citizen_id:
            QMessageBox.warning(self.cp_profile_screen, "No Citizen Selected",
                                "Please select a citizen from the table first.")
            return
        self.part1_popup_update = self.view.show_update_citizen_part_01_popup(self)
        self.part2_popup_update = self.view.show_update_citizen_part_02_popup(self)
        self.part3_popup_update = self.view.show_update_citizen_part_03_popup(self)

        self.gov_group = QButtonGroup()
        self.sex_group = QButtonGroup()

        self.sex_group.addButton(self.part1_popup_update.radioButton_male)
        self.sex_group.addButton(self.part1_popup_update.radioButton_female)

        self.gov_group.addButton(self.part2_popup_update.radioButton_IsGov_Yes)
        self.gov_group.addButton(self.part2_popup_update.radioButton_IsGov_No)

        self.student_group = QButtonGroup()
        self.fam_plan_group = QButtonGroup()
        self.pwd_group = QButtonGroup()

        self.voter_group = None
        self.deceased_group = None
        self.indig_group = None

        self.voter_group = QButtonGroup()
        self.deceased_group = QButtonGroup()
        self.indig_group = QButtonGroup()

        self.student_group.addButton(self.part3_popup_update.radioButton_IsStudent_Yes)
        self.student_group.addButton(self.part3_popup_update.radioButton_IsStudent_No)

        # self.fam_plan_group.addButton(self.part3_popup_update.radioButton_IsFamPlan_Yes)
        # self.fam_plan_group.addButton(self.part3_popup_update.radioButton_IsFamPlan_No)

        # self.pwd_group.addButton(self.part3_popup_update.register_citizen_IsPWD_Yes)
        # self.pwd_group.addButton(self.part3_popup_update.register_citizen_IsPWD_No)

        self.deceased_group.addButton(self.part3_popup_update.register_citizen_Deceased_Yes)
        self.deceased_group.addButton(self.part3_popup_update.register_citizen_Deceased_No)

        self.indig_group.addButton(self.part3_popup_update.register_citizen_IndGroup_Yes)
        self.indig_group.addButton(self.part3_popup_update.register_citizen_IndGroup_No)

        self.voter_group.addButton(self.part3_popup_update.register_citizen_RegVote_Yes)
        self.voter_group.addButton(self.part3_popup_update.register_citizen_RegVote_No)

        # initialize data
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT sitio_id, sitio_name FROM sitio ORDER BY sitio_name ASC;")
            results = cursor.fetchall()

            combo = self.part1_popup_update.register_citizen_comboBox_Sitio
            combo.clear()
            for sitio_id, sitio_name in results:
                combo.addItem(sitio_name, sitio_id)

        except Exception as e:
            print(f"Failed to load sitios: {e}")
        finally:
            db.close()
        # self.stacked_widget.addWidget(self.part1_popup)
        # self.stacked_widget.addWidget(self.part2_popup)
        #
        # self.stacked_widget.setCurrentIndex(0)
        # if hasattr(self, 'citizen_data'):
        #     self.restore_part1_data()
        self.load_citizen_data_for_update()
        # self.load_citizen_part2_data_for_update()
        self.part1_popup_update.show()

        # self.part2_popup.close()
        print("test")

    def show_update_citizen_part_02_initialize(self):
        print("-- Update Citizen Part 2 Popup")

        # Populate Relationship ComboBox
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute(
                "SELECT rth_id, rth_relationship_name FROM relationship_type ORDER BY rth_relationship_name ASC;"
            )
            results = cursor.fetchall()

            combo = self.part2_popup_update.register_citizen_comboBox_Relationship
            combo.clear()
            for rth_id, rth_relationship_name in results:
                combo.addItem(rth_relationship_name, rth_id)  # ✅ Properly bind ID to item


            # Populate Philhealth Category ComboBox
            cursor.execute("SELECT pc_id, pc_category_name FROM philhealth_category ORDER BY pc_category_name ASC;")
            results = cursor.fetchall()
            combo_philcat = self.part2_popup_update.register_citizen_comboBox_PhilCat
            # combo_philcat.clear()
            for pc_id, pc_category_name in results:
                combo_philcat.addItem(pc_category_name, pc_id)

            # Populate Membership Type ComboBox
            # membership_types = ["Member", "Dependent", "Non-Member"]
            # combo_memtype = self.part2_popup_update.register_citizen_comboBox_PhilMemType
            # combo_memtype.clear()
            # for mem_type in membership_types:
            #     combo_memtype.addItem(mem_type)

        except Exception as e:
            print(f"Failed to initialize Part 2 popup: {e}")
        finally:
            db.close()

        # Load data after populating combos
        # self.load_citizen_part2_data_for_update()
        self.part2_popup_update.show()
        # self.part2_popup_update.exec_()

    def show_update_citizen_part_03_initialize(self):
        print("-- Update Citizen Part 3 Popup")
        self.part3_popup_update.show()

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute(
                "SELECT clah_id, clah_classification_name FROM classification_health_risk ORDER BY clah_classification_name ASC;")
            results = cursor.fetchall()

            combo = self.part3_popup_update.register_citizen_health_classification
            # combo.clear()
            for clah_id, clah_classification_name in results:
                combo.addItem(clah_classification_name, clah_id)



        except Exception as e:
            print(f"Failed to load classitiofat: {e}")
        finally:
            db.close()

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT fpm_id, fpm_method FROM family_planning_method ORDER BY fpm_method ASC;")
            results = cursor.fetchall()

            combo = self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod
            for fpm_id, fpm_method in results:
                combo.addItem(fpm_method, fpm_id)

        except Exception as e:
            print(f"Failed to load fpm meyhofd: {e}")
        finally:
            db.close()

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT fpms_id, fpms_status_name FROM fpm_status ORDER BY fpms_status_name ASC;")
            results = cursor.fetchall()

            combo = self.part3_popup_update.register_citizen_comboBox_FamPlanStatus
            for fpms_id, fpms_status_name in results:
                combo.addItem(fpms_status_name, fpms_id)

        except Exception as e:
            print(f"Failed to load fpm status: {e}")
        finally:
            db.close()

        # self.deceased_group.addButton(self.part3_popup_update.register_citizen_Deceased_Yes)
        # self.deceased_group.addButton(self.part3_popup_update.register_citizen_Deceased_No)
        #
        # # self.indig_group.addButton(self.part3_popup_update.register_citizen_IndGroup_Yes)
        # # self.indig_group.addButton(self.part3_popup_update.register_citizen_IndGroup_No)

        # self.part2_popup = self.view.show_register_citizen_part_02_popup(self)
        # self.part2_popup.register_citizen_HouseholdID.setText('test')

        # if hasattr(self, 'citizen_data'):
        # self.load_citizen_part3_data_for_update()

        self.part3_popup_update.exec_()
        # self.restore_part3_data()

        # DATA INTERACTION PART 1

    def get_form_data_update(self):
        sex = 'M' if self.part1_popup_update.radioButton_male.isChecked() else 'F'
        gov_worker = self.part2_popup_update.radioButton_IsGov_Yes.isChecked()
        is_student = self.update_radio_button_student_result() == 'Yes'
        indigenous_group = self.update_radio_button_indig_result() == 'Yes'
        registered_voter = self.update_radio_button_voter_result() == 'Yes'
        is_alive = self.update_radio_button_deceased_result() != 'Yes'
        relationship = self.part2_popup_update.register_citizen_comboBox_Relationship.currentText().strip()

        return {
            # Part 1
            'first_name': self.part1_popup_update.register_citizen_firstname.text().strip(),
            'middle_name': self.part1_popup_update.register_citizen_middlename.text().strip(),
            'last_name': self.part1_popup_update.register_citizen_lastname.text().strip(),
            'suffix': self.part1_popup_update.register_citizen_suffix.text().strip(),
            'birth_date': self.part1_popup_update.register_citizen_date_dob.date().toString("yyyy-MM-dd"),
            'sex': sex,
            'civil_status': self.part1_popup_update.register_citizen_comboBox_CivilStatus.currentText().strip(),
            'birth_place': self.part1_popup_update.register_citizen_Pob.text().strip(),
            'blood_type': self.part1_popup_update.register_citizen_comboBox_BloodType.currentText().strip(),
            'email': self.part1_popup_update.register_citizen_Email.text().strip(),
            'contact_number': self.part1_popup_update.register_citizen_ContactNumber.text().strip(),
            'sitio_id': self.part1_popup_update.register_citizen_comboBox_Sitio.currentData(),
            # Assuming currentData() returns sitio_id
            'religion': self.part1_popup_update.register_citizen_comboBox_Religion.currentText().strip(),

            # Part 2
            'socioeco_status': self.part2_popup_update.register_citizen_comboBox_SocEcoStat.currentText().strip(),
            'nhts_number': self.part2_popup_update.register_citizen_NHTSNum.text().strip(),
            'household_id': self.part2_popup_update.register_citizen_HouseholdID.text().strip(),
            'relationship_name': relationship,
            # Assume currentData() gives rth_id
            'employment_status': self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.currentText().strip(),
            'occupation': self.part2_popup_update.register_citizen_Occupation.text().strip(),
            'gov_worker': gov_worker,
            'philhealth_category': self.part2_popup_update.register_citizen_comboBox_PhilCat.currentText().strip(),
            'membership_type': self.part2_popup_update.register_citizen_comboBox_PhilMemType.currentText().strip(),
            'philhealth_id': self.part2_popup_update.register_citizen_PhilhealthID.text().strip(),

            # Part 3
            'is_student': is_student,
            'school_name': self.part3_popup_update.register_citizen_SchoolName.text().strip(),
            'educational_level': self.part3_popup_update.register_citizen_comboBox_EducationalLevel.currentText().strip(),
            'fp_method': self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.currentText().strip(),
            'fp_status': self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.currentText().strip(),
            'start_date': self.part3_popup_update.register_citizen_start_date.date().toString("yyyy-MM-dd") or None,
            'end_date': self.part3_popup_update.register_citizen_end_date.date().toString("yyyy-MM-dd") or None,
            'health_classification': self.part3_popup_update.register_citizen_health_classification.currentText().strip(),
            'indigenous_group': indigenous_group,
            'reason_of_death': self.part3_popup_update.register_citizen_ReasonOfDeath.toPlainText().strip(),
            'date_of_death': self.part3_popup_update.register_citizen_death_date.date().toString("yyyy-MM-dd") or None,
            'registered_voter': registered_voter,
            'is_alive': is_alive
        }

    def get_form_data(self):
        return {
            # PART 1
            'first_name': self.part1_popup.register_citizen_firstname.text().strip(),  # REQUIRED
            'middle_name': self.part1_popup.register_citizen_middlename.text().strip() or "None",
            'last_name': self.part1_popup.register_citizen_lastname.text().strip(),  # REQUIRED
            'suffix': self.part1_popup.register_citizen_suffix.text().strip() or "None",

            'civil_status': self.part1_popup.register_citizen_comboBox_CivilStatus.currentText().strip(),  # REQUIRED
            'birth_date': self.part1_popup.register_citizen_date_dob.date().toString("yyyy-MM-dd"),  # REQUIRED

            'religion': self.part1_popup.register_citizen_comboBox_Religion.currentText().strip(),  # REQUIRED

            'blood_type': self.part1_popup.register_citizen_comboBox_BloodType.currentText().strip() or "None",
            'sex': self.radio_button_sex_result(),
            # 'Male' if self.part1_popup.radioButton_male.isChecked(), 'Female' if self.part1_popup.radioButton_female.isChecked(), # REQUIRED

            'contact_number': self.part1_popup.register_citizen_ContactNumber.text().strip() or "None",
            'email_address': self.part1_popup.register_citizen_Email.text().strip() or "None",

            'sitio': self.part1_popup.register_citizen_comboBox_Sitio.currentText().strip(),  # REQUIRED
            'place_of_birth': self.part1_popup.register_citizen_Pob.text().strip() or "None",

            # APRT 2
            # PART 2

            # socio info
            'socio_eco_status': self.part2_popup.register_citizen_comboBox_SocEcoStat.currentText().strip(),
            'nhts_number': self.part2_popup.register_citizen_NHTSNum.text().strip(),

            # house hold info
            'household_id': self.part2_popup.register_citizen_HouseholdID.text().strip(),
            'relationship': self.part2_popup.register_citizen_comboBox_Relationship.currentText().strip(),

            # work information

            'employment_status': self.part2_popup.register_citizen_comboBox_EmploymentStatus.currentText().strip(),
            'occupation': self.part2_popup.register_citizen_Occupation.text().strip(),
            'gov_worker': self.radio_button_gov_worker_result(),
            'phil_category': self.part2_popup.register_citizen_comboBox_PhilCat.currentText().strip(),
            'phil_id': self.part2_popup.register_citizen_PhilID.text().strip() or "None",
            'membership_type': self.part2_popup.register_citizen_comboBox_PhilMemType.currentText().strip(),

            # PART 3
            'is_student': self.radio_button_student_result(),
            'school_name': self.part3_popup.register_citizen_SchoolName.text().strip(),
            'educ_level': self.part3_popup.register_citizen_comboBox_EducationalLevel.currentText().strip(),
            # 'has_fam_plan': self.radio_button_fam_plan_result(),
            'fam_plan_method': self.part3_popup.register_citizen_comboBox_FamilyPlanningMethod.currentText().strip(),
            'fam_plan_stat': self.part3_popup.register_citizen_comboBox_FamPlanStatus.currentText().strip(),
            'fam_plan_start_date': self.part3_popup.register_citizen_start_date.date().toString("yyyy-MM-dd"),
            'fam_plan_end_date': self.part3_popup.register_citizen_end_date.date().toString("yyyy-MM-dd"),
            'health_class': self.part3_popup.register_citizen_health_classification.currentText().strip(),
            'is_voter': self.radio_button_voter_result(),
            'is_indig': self.radio_button_indig_result(),
            'is_deceased': self.radio_button_deceased_result(),
            'reason_of_death': self.part3_popup.register_citizen_ReasonOfDeath.toPlainText().strip(),
            'date_of_death': self.part3_popup.register_citizen_death_date.date().toString("yyyy-MM-dd")  # REQUIRED

        }

    def get_form_data_update(self):
        sex = 'M' if self.part1_popup_update.radioButton_male.isChecked() else 'F'
        gov_worker = self.part2_popup_update.radioButton_IsGov_Yes.isChecked()
        is_student = self.update_radio_button_student_result() == 'Yes'
        indigenous_group = self.update_radio_button_indig_result() == 'Yes'
        registered_voter = self.update_radio_button_voter_result() == 'Yes'
        is_alive = self.update_radio_button_deceased_result() != 'Yes'

        return {
            # Part 1
            'first_name': self.part1_popup_update.register_citizen_firstname.text().strip(),
            'middle_name': self.part1_popup_update.register_citizen_middlename.text().strip(),
            'last_name': self.part1_popup_update.register_citizen_lastname.text().strip(),
            'suffix': self.part1_popup_update.register_citizen_suffix.text().strip(),
            'birth_date': self.part1_popup_update.register_citizen_date_dob.date().toString("yyyy-MM-dd"),
            'sex': sex,
            'civil_status': self.part1_popup_update.register_citizen_comboBox_CivilStatus.currentText().strip(),
            'birth_place': self.part1_popup_update.register_citizen_Pob.text().strip(),
            'blood_type': self.part1_popup_update.register_citizen_comboBox_BloodType.currentText().strip(),
            'email': self.part1_popup_update.register_citizen_Email.text().strip(),
            'contact_number': self.part1_popup_update.register_citizen_ContactNumber.text().strip(),
            'sitio_id': self.part1_popup_update.register_citizen_comboBox_Sitio.currentData(),
            # Assuming currentData() returns sitio_id
            'religion': self.part1_popup_update.register_citizen_comboBox_Religion.currentText().strip(),

            # Part 2
            'socioeco_status': self.part2_popup_update.register_citizen_comboBox_SocEcoStat.currentText().strip(),
            'nhts_number': self.part2_popup_update.register_citizen_NHTSNum.text().strip(),
            'household_id': self.part2_popup_update.register_citizen_HouseholdID.text().strip(),
            'relationship_id': self.part2_popup_update.register_citizen_comboBox_Relationship.currentData(),
            # Assume currentData() gives rth_id
            'employment_status': self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.currentText().strip(),
            'occupation': self.part2_popup_update.register_citizen_Occupation.text().strip(),
            'gov_worker': gov_worker,
            'philhealth_category': self.part2_popup_update.register_citizen_comboBox_PhilCat.currentText().strip(),
            'membership_type': self.part2_popup_update.register_citizen_comboBox_PhilMemType.currentText().strip(),
            'philhealth_id': self.part2_popup_update.register_citizen_PhilID.text().strip(),

            # Part 3
            'is_student': is_student,
            'school_name': self.part3_popup_update.register_citizen_SchoolName.text().strip(),
            'educational_level': self.part3_popup_update.register_citizen_comboBox_EducationalLevel.currentText().strip(),
            'fp_method': self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.currentText().strip(),
            'fp_status': self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.currentText().strip(),
            'start_date': self.part3_popup_update.register_citizen_start_date.date().toString("yyyy-MM-dd") or None,
            'end_date': self.part3_popup_update.register_citizen_end_date.date().toString("yyyy-MM-dd") or None,
            'health_classification': self.part3_popup_update.register_citizen_health_classification.currentText().strip(),
            'indigenous_group': indigenous_group,
            'reason_of_death': self.part3_popup_update.register_citizen_ReasonOfDeath.toPlainText().strip(),
            'date_of_death': self.part3_popup_update.register_citizen_death_date.date().toString("yyyy-MM-dd") or None,
            'registered_voter': registered_voter,
            'is_alive': is_alive
        }

    # def get_form_data_part_2(self):
    #     return{
    #         # PART 2
    #
    #         # socio info
    #         'socio_eco_status': self.part2_popup.register_citizen_comboBox_SocEcoStat.currentText().strip(),
    #         'nhts_number': self.part2_popup.register_citizen_NHTSNum.text().strip(),
    #
    #         # house hold info
    #         'household_id': self.part2_popup.register_citizen_HouseholdID.text().strip(),
    #         'relationship': self.part2_popup.register_citizen_comboBox_Relationship.currentText().strip(),
    #         'other_relationship': self.part2_popup.register_citizen_HouseholdRelationshipOther.text().strip(),
    #
    #         # work information
    #
    #         'employment_status': self.part2_popup.register_citizen_comboBox_EmploymentStatus.currentText().strip(),
    #         'occupation': self.part2_popup.register_citizen_Occupation.text().strip(),
    #         'gov_worker': self.radio_button_gov_worker_result(),
    #         'phil_member': self.radio_button_phil_member_result(),
    #         'phil_category': self.part2_popup.register_citizen_comboBox_PhilCat.currentText().strip(),
    #         'phil_id': self.part2_popup.register_citizen_PhilID.text().strip(),
    #         'membership_type': self.part2_popup.register_citizen_comboBox_PhilMemType.currentText().strip()
    #     }

    from datetime import date
    # from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

    from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
    from datetime import date

    def load_citizen_data(self):
        connection = None
        try:
            connection = Database()
            cursor = connection.cursor
            cursor.execute("""
    SELECT DISTINCT ON (C.CTZ_ID)
        C.CTZ_ID, --0
        C.CTZ_LAST_NAME,
        C.CTZ_FIRST_NAME,
        C.CTZ_MIDDLE_NAME,
        C.CTZ_SUFFIX,
        S.SITIO_NAME, --5
        TO_CHAR(C.CTZ_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS LAST_UPDATED,
        C.CTZ_DATE_OF_BIRTH,
        C.CTZ_SEX,
        C.CTZ_CIVIL_STATUS,
        COALESCE(CON.CON_EMAIL, '') AS EMAIL, --10
        COALESCE(CON.CON_PHONE, '') AS CONTACT_NUM,
        C.CTZ_PLACE_OF_BIRTH,
        HH.HH_ADDRESS,
        SES.SOEC_STATUS,
        SES.SOEC_NUMBER, --15
        ES.ES_STATUS_NAME AS EMPLOYMENT_STATUS,
        EMP.EMP_OCCUPATION AS OCCUPATION,
        EMP.EMP_IS_GOV_WORKER,
        HH.HH_ID, --19
        RT.RTH_RELATIONSHIP_NAME AS RELATIONSHIP_NAME,
        PHC.PC_CATEGORY_NAME AS PHILHEALTH_CATEGORY_NAME,
        PH.PHEA_MEMBERSHIP_TYPE, --22
        R.REL_NAME AS RELIGION,
        C.CTZ_BLOOD_TYPE,
        EDU.EDU_IS_CURRENTLY_STUDENT AS IS_STUDENT,
        EDU.EDU_INSTITUTION_NAME AS SCHOOL_NAME, --26
        EDAT.EDAT_LEVEL AS EDUCATIONAL_ATTAINMENT, --27
        CHR.CLAH_CLASSIFICATION_NAME AS CLASSIFICATION_HEALTH_RISK_NAME, --28
        C.CTZ_IS_REGISTERED_VOTER, --29
        NOT C.CTZ_IS_ALIVE AS IS_DECEASED, --30
        C.CTZ_IS_IP,
        PH.PHEA_ID_NUMBER,
        TO_CHAR(C.CTZ_DATE_ENCODED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_ENCODED_FORMATTED, --33

        CASE 
            WHEN SA.SYS_FNAME IS NULL THEN 'System'
            ELSE SA.SYS_FNAME || ' ' || COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') || SA.SYS_LNAME
        END AS ENCODED_BY, --34

        TO_CHAR(C.CTZ_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED_FORMATTED, --35

        CASE 
            WHEN SUA.SYS_FNAME IS NULL THEN 'System'
            ELSE SUA.SYS_FNAME || ' ' || COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') || SUA.SYS_LNAME
        END AS LAST_UPDATED_BY_NAME, --36

        C.CTZ_REASON_OF_DEATH, --37
        TO_CHAR(C.CTZ_DATE_OF_DEATH, 'FMMonth FMDD, YYYY'), --38
        FP.fp_start_date AS FAM_PLAN_START_DATE,
        FP.fp_end_date AS FAM_PLAN_END_DATE,
        FPM.FPM_METHOD AS FAM_PLAN_METHOD,
        FPS.FPMS_STATUS_NAME AS FAM_PLAN_STATUS

    FROM CITIZEN C
    LEFT JOIN CONTACT CON ON C.CON_ID = CON.CON_ID
    LEFT JOIN EMPLOYMENT EMP ON C.CTZ_ID = EMP.CTZ_ID
    LEFT JOIN EMPLOYMENT_STATUS ES ON EMP.ES_ID = ES.ES_ID
    JOIN SITIO S ON C.SITIO_ID = S.SITIO_ID
    JOIN HOUSEHOLD_INFO HH ON C.HH_ID = HH.HH_ID
    LEFT JOIN SOCIO_ECONOMIC_STATUS SES ON C.SOEC_ID = SES.SOEC_ID
    LEFT JOIN RELATIONSHIP_TYPE RT ON C.RTH_ID = RT.RTH_ID
    LEFT JOIN PHILHEALTH PH ON C.PHEA_ID = PH.PHEA_ID
    LEFT JOIN PHILHEALTH_CATEGORY PHC ON PH.PC_ID = PHC.PC_ID
    LEFT JOIN RELIGION R ON C.REL_ID = R.REL_ID
    LEFT JOIN EDUCATION_STATUS EDU ON C.EDU_ID = EDU.EDU_ID
    LEFT JOIN EDUCATIONAL_ATTAINMENT EDAT ON EDU.EDAT_ID = EDAT.EDAT_ID
    LEFT JOIN CLASSIFICATION_HEALTH_RISK CHR ON C.CLAH_ID = CHR.CLAH_ID
    LEFT JOIN SYSTEM_ACCOUNT SA ON C.ENCODED_BY_SYS_ID = SA.SYS_USER_ID
    LEFT JOIN SYSTEM_ACCOUNT SUA ON C.LAST_UPDATED_BY_SYS_ID = SUA.SYS_USER_ID
    LEFT JOIN FAMILY_PLANNING FP ON C.CTZ_ID = FP.CTZ_ID
    LEFT JOIN FAMILY_PLANNING_METHOD FPM ON FP.FPM_METHOD = FPM.FPM_ID
    LEFT JOIN FPM_STATUS FPS ON FP.FPMS_STATUS = FPS.FPMS_ID
    WHERE C.CTZ_IS_DELETED = FALSE
    ORDER BY C.CTZ_ID DESC
    LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.rows = rows

            table = self.cp_profile_screen.cp_tableView_List_RegCitizens
            table.setRowCount(len(rows))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["ID", "Family Name", "First Name", "Sitio", "Last Updated"])

            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 150)
            table.setColumnWidth(3, 150)
            table.setColumnWidth(4, 200)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[5], row_data[6]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.cp_profile_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()

    # def load_citizen_part2_data_for_update(self):
    #     if not self.selected_citizen_id:
    #         QMessageBox.warning(self.part2_popup_update, "No Selection", "No citizen selected for update.")
    #         return
    #
    #     try:
    #         db = Database()
    #         cursor = db.get_cursor()
    #
    #         query = """
    #             SELECT
    #                 hh.HH_ID,
    #                 c.rth_id,
    #                 ses.soec_number,
    #                 ses.SOEC_STATUS AS SocioEconomic_Status,
    #                 emp.ES_ID,
    #                 emp.EMP_OCCUPATION AS Occupation,
    #                 emp.EMP_IS_GOV_WORKER AS Is_Government_Worker,
    #                 ph.phea_id_number AS Philhealth_ID,
    #                 ph.phea_membership_type AS Membership_Type,
    #                 ph.pc_id AS Philhealth_Category
    #             FROM Citizen c
    #             LEFT JOIN HOUSEHOLD_INFO hh ON c.hh_id = hh.hh_id
    #             LEFT JOIN SOCIO_ECONOMIC_STATUS ses ON c.soec_id = ses.soec_id
    #             LEFT JOIN EMPLOYMENT emp ON c.CTZ_ID = emp.CTZ_ID
    #             LEFT JOIN PHILHEALTH ph ON c.phea_id = ph.phea_id
    #             WHERE c.CTZ_ID = %s;
    #         """
    #
    #         cursor.execute(query, (self.selected_citizen_id,))
    #         result = cursor.fetchone()
    #
    #         if result:
    #             (
    #                 household_id,
    #                 relationship_id,
    #                 nhts_number,
    #                 socioeco_status,
    #                 es_id,
    #                 occupation,
    #                 gov_worker,
    #                 phil_id,
    #                 membership_type,
    #                 phil_category
    #             ) = result
    #
    #             # --- Household ID ---
    #             self.part2_popup_update.register_citizen_HouseholdID.setText(str(household_id) if household_id else "")
    #
    #             # --- Relationship ComboBox ---
    #             index = self.part2_popup_update.register_citizen_comboBox_Relationship.findData(relationship_id)
    #             if index >= 0:
    #                 self.part2_popup_update.register_citizen_comboBox_Relationship.setCurrentIndex(index)
    #
    #             # --- NHTS Number ---
    #             self.part2_popup_update.register_citizen_NHTSNum.setText(nhts_number or "")
    #
    #             # --- Socioeconomic Status ---
    #             index_se = self.part2_popup_update.register_citizen_comboBox_SocEcoStat.findText(socioeco_status or "")
    #             if index_se >= 0:
    #                 self.part2_popup_update.register_citizen_comboBox_SocEcoStat.setCurrentIndex(index_se)
    #
    #             # --- Employment Status ---
    #             index_emp = self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.findData(es_id)
    #             if index_emp >= 0:
    #                 self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.setCurrentIndex(index_emp)
    #
    #             # --- Occupation ---
    #             self.part2_popup_update.register_citizen_Occupation.setText(occupation or "")
    #
    #             # --- Government Worker Radio Buttons ---
    #             if gov_worker == 'Yes':
    #                 self.part2_popup_update.radioButton_IsGov_Yes.setChecked(True)
    #             elif gov_worker == 'No':
    #                 self.part2_popup_update.radioButton_IsGov_No.setChecked(True)
    #
    #             # --- Philhealth Category ComboBox ---
    #             index_phil_cat = self.part2_popup_update.register_citizen_comboBox_PhilCat.findText(phil_category or "")
    #             if index_phil_cat >= 0:
    #                 self.part2_popup_update.register_citizen_comboBox_PhilCat.setCurrentIndex(index_phil_cat)
    #
    #             # --- Philhealth ID LineEdit ---
    #             self.part2_popup_update.register_citizen_PhilID.setText(phil_id or "")
    #
    #             # --- Membership Type ComboBox ---
    #             index_mem = self.part2_popup_update.register_citizen_comboBox_PhilMemType.findText(
    #                 membership_type or "")
    #             if index_mem >= 0:
    #                 self.part2_popup_update.register_citizen_comboBox_PhilMemType.setCurrentIndex(index_mem)
    #
    #     except Exception as e:
    #         print("Error loading citizen Part 2 data:", e)
    #         QMessageBox.critical(self.part2_popup_update, "Database Error", f"Failed to load Part 2 citizen data: {e}")
    #     finally:
    #         db.close()

    # def load_citizen_part3_data_for_update(self):
    #     if not self.selected_citizen_id:
    #         QMessageBox.warning(self.part3_popup_update, "No Selection", "No citizen selected for update.")
    #         return
    #
    #     try:
    #         db = Database()
    #         cursor = db.get_cursor()
    #
    #         query = """
    #         SELECT
    #             edu.EDU_IS_CURRENTLY_STUDENT AS Is_Student,
    #             edu.EDU_INSTITUTION_NAME AS School_Name,
    #             ea.EDAT_LEVEL AS Educational_Level,
    #
    #             fp.FPM_METHOD AS Fam_Plan_Method,
    #             fp.FPMS_STATUS AS Fam_Plan_Status,
    #             fp.FP_START_DATE AS Fam_Start_Date,
    #             fp.FP_END_DATE AS Fam_End_Date,
    #
    #             clah.clah_classification_name AS Health_Class,
    #             c.CTZ_IS_REGISTERED_VOTER AS Is_Voter,
    #             c.IS_INDIGENOUS AS Is_Indig,
    #             c.IS_DECEASED AS Is_Deceased,
    #             c.REASON_OF_DEATH AS Reason_Of_Death,
    #             c.DATE_OF_DEATH AS Date_Of_Death
    #         FROM Citizen c
    #         LEFT JOIN EDUCATION_STATUS edu ON c.edu_id = edu.edu_id
    #         LEFT JOIN EDUCATIONAL_ATTAINMENT ea ON edu.EDAT_ID = ea.EDAT_ID
    #         LEFT JOIN FAMILY_PLANNING fp ON c.CTZ_ID = fp.CTZ_ID
    #         LEFT JOIN classification_health_risk clah ON c.clah_id = clah.clah_id
    #         WHERE c.CTZ_ID = %s;
    #         """
    #
    #         cursor.execute(query, (self.selected_citizen_id,))
    #         result = cursor.fetchone()
    #
    #         if result:
    #             (
    #                 is_student,
    #                 school_name,
    #                 educational_level,
    #                 fam_plan_method,
    #                 fam_plan_status,
    #                 fam_start_date,
    #                 fam_end_date,
    #                 health_class,
    #                 is_voter,
    #                 is_indig,
    #                 is_deceased,
    #                 reason_of_death,
    #                 date_of_death
    #             ) = result
    #
    #             # Set Student Radio Buttons
    #             if is_student == 'Yes':
    #                 self.part3_popup_update.register_citizen_IsStudent_Yes.setChecked(True)
    #             elif is_student == 'No':
    #                 self.part3_popup_update.register_citizen_IsStudent_No.setChecked(True)
    #
    #             # School Name
    #             self.part3_popup_update.register_citizen_SchoolName.setText(school_name or "")
    #
    #             # Educational Level Combo Box
    #             index_edu = self.part3_popup_update.register_citizen_comboBox_EducationalLevel.findText(
    #                 educational_level or "")
    #             if index_edu >= 0:
    #                 self.part3_popup_update.register_citizen_comboBox_EducationalLevel.setCurrentIndex(index_edu)
    #
    #             # Family Planning Method
    #             index_fam_plan = self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.findText(
    #                 fam_plan_method or "")
    #             if index_fam_plan >= 0:
    #                 self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.setCurrentIndex(
    #                     index_fam_plan)
    #
    #             # Family Planning Status
    #             index_fam_stat = self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.findText(
    #                 fam_plan_status or "")
    #             if index_fam_stat >= 0:
    #                 self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.setCurrentIndex(index_fam_stat)
    #
    #             # Family Plan Dates
    #             if fam_start_date:
    #                 start_date = QDate.fromString(fam_start_date, "yyyy-MM-dd")
    #                 self.part3_popup_update.register_citizen_start_date.setDate(start_date)
    #             if fam_end_date:
    #                 end_date = QDate.fromString(fam_end_date, "yyyy-MM-dd")
    #                 self.part3_popup_update.register_citizen_end_date.setDate(end_date)
    #
    #             # Health Classification
    #             index_health = self.part3_popup_update.register_citizen_health_classification.findText(
    #                 health_class or "")
    #             if index_health >= 0:
    #                 self.part3_popup_update.register_citizen_health_classification.setCurrentIndex(index_health)
    #
    #             # Voter Radio Buttons
    #             if is_voter == 'Yes':
    #                 self.part3_popup_update.register_citizen_RegVote_Yes.setChecked(True)
    #             elif is_voter == 'No':
    #                 self.part3_popup_update.register_citizen_RegVote_No.setChecked(True)
    #
    #             # Indigenous Group Radio Buttons
    #             if is_indig == 'Yes':
    #                 self.part3_popup_update.register_citizen_IndGroup_Yes.setChecked(True)
    #             elif is_indig == 'No':
    #                 self.part3_popup_update.register_citizen_IndGroup_No.setChecked(True)
    #
    #             # Deceased Radio Buttons
    #             if is_deceased == 'Yes':
    #                 self.part3_popup_update.register_citizen_Deceased_Yes.setChecked(True)
    #                 # Enable death-related fields
    #                 self.part3_popup_update.register_citizen_ReasonOfDeath.setPlainText(reason_of_death or "")
    #                 if date_of_death:
    #                     dod = QDate.fromString(date_of_death, "yyyy-MM-dd")
    #                     self.part3_popup_update.register_citizen_death_date.setDate(dod)
    #             else:
    #                 self.part3_popup_update.register_citizen_Deceased_No.setChecked(True)
    #                 # Optionally disable death-related fields
    #                 self.part3_popup_update.register_citizen_ReasonOfDeath.setPlainText("")
    #                 self.part3_popup_update.register_citizen_death_date.setDate(QDate.currentDate())
    #
    #     except Exception as e:
    #         print("Error loading citizen Part 3 data:", e)
    #         QMessageBox.critical(self.part3_popup_update, "Database Error", f"Failed to load Part 3 citizen data: {e}")
    #     finally:
    #         db.close()

    def handle_row_click_citizen(self, row, column):
        table = self.cp_profile_screen.cp_tableView_List_RegCitizens
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()
        self.selected_citizen_id = selected_id  # Store selected ID here

        for record in self.rows:
            if str(record[0]) == selected_id:
                self.cp_profile_screen.cp_displayCItizenID.setText(str(record[0]))
                self.cp_profile_screen.cp_displayLastName.setText(record[1])
                self.cp_profile_screen.cp_displayFirstName.setText(record[2])
                self.cp_profile_screen.cp_displayMiddleName.setText(record[3] or "None")
                self.cp_profile_screen.cp_displaySuffix.setText(record[4] or "None")
                self.cp_profile_screen.cp_displaySitio.setText(record[5])
                self.cp_profile_screen.display_DateUpdated.setText(record[6])

                dob = record[7]
                if dob:
                    try:
                        today = date.today()
                        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                        self.cp_profile_screen.cp_displayAge.setText(
                            dob.strftime('%B %d, %Y | ') + str(age) + " years old")
                    except Exception:
                        self.cp_profile_screen.cp_displayAge.setText("")
                else:
                    self.cp_profile_screen.cp_displayAge.setText("")

                self.cp_profile_screen.cp_displayCivilStatus.setText(
                    "Male | " + record[9] if record[8] == 'M' else "Female | " + record[9])
                self.cp_profile_screen.cp_displayEmail.setText(record[10] or "None")
                self.cp_profile_screen.cp_displayContactNum.setText(record[11] or "None")
                self.cp_profile_screen.cp_displayPlaceOfBirth.setText(record[12] or "None")
                self.cp_profile_screen.cp_displayFullAddress.setText(record[13] or "None")
                self.cp_profile_screen.cp_displaySocioEcoStatus.setText(record[14] or "None")
                self.cp_profile_screen.cp_displayNHTSNum.setText(record[15] or "None")
                self.cp_profile_screen.cp_displayEmploymentStatus.setText(record[16] or "None")
                self.cp_profile_screen.cp_displayOccupation.setText(record[17] or "None")
                self.cp_profile_screen.cp_displayGovWorker.setText("Yes" if record[18] == True else "No")
                self.cp_profile_screen.cp_displayHouseholdID.setText(str(record[19]) if record[19] else "")
                self.cp_profile_screen.cp_displayRelationship.setText(record[20] or "None")
                self.cp_profile_screen.cp_displayPhilCat.setText(record[21] or "None")
                self.cp_profile_screen.cp_displayPhilID.setText(record[32] or "None")
                self.cp_profile_screen.cp_displayMembershipType.setText(record[22] or "None")
                self.cp_profile_screen.cp_displayReligion.setText(record[23] or "None")
                self.cp_profile_screen.cp_displayBloodType.setText(record[24] or "None")
                self.cp_profile_screen.cp_displayStudent.setText("Yes" if record[25] == True else "No")
                self.cp_profile_screen.cp_displaySchoolName.setText(record[26] or "None")
                self.cp_profile_screen.cp_displayEducationalAttainment.setText(record[27] or "None")
                self.cp_profile_screen.cp_display_health_classification.setText(record[28] or "None")
                self.cp_profile_screen.cp_displayRegisteredVoter.setText("Yes" if record[29] == True else "No")
                self.cp_profile_screen.cp_displayDeceased.setText("Yes" if record[30] == True else "No")
                self.cp_profile_screen.cp_displayPartOfIndigenousGroup.setText("Yesss" if record[31] == True else "No")
                self.cp_profile_screen.display_DateEncoded.setText(record[33] or "None")
                self.cp_profile_screen.display_EncodedBy.setText(record[34] or "None")
                self.cp_profile_screen.display_DateUpdated.setText(record[35] or "None")
                self.cp_profile_screen.display_UpdatedBy.setText(record[36] or "None")
                self.cp_profile_screen.cp_displayReasonOfDeath.setText(record[37] or "None")
                self.cp_profile_screen.cp_displayDoD.setText(record[38] or "None")
                # --- Family Planning Info ---
                # Safely extract family planning fields
                fam_plan_method = str(record[41]) if len(record) > 41 and record[41] is not None else "None"
                fam_plan_status = str(record[42]) if len(record) > 42 and record[42] is not None else "None"
                fam_plan_start = record[39] if len(record) > 39 else None
                fam_plan_end = record[40] if len(record) > 40 else None

                # Set method and status (always strings)
                self.cp_profile_screen.cp_displayFamPlanMethod.setText(fam_plan_method)
                self.cp_profile_screen.cp_displayFamPlanStatus.setText(fam_plan_status)

                # Format dates if valid
                self.cp_profile_screen.display_DateStarted.setText(
                    fam_plan_start.strftime("%B %d, %Y") if isinstance(fam_plan_start, date) else "None"
                )
                self.cp_profile_screen.display_DateEnded.setText(
                    fam_plan_end.strftime("%B %d, %Y") if isinstance(fam_plan_end, date) else "None"
                )
                break

    #
    # BUTTON FUNCTIONS
    #

    def perform_citizen_search(self):
        search_text = self.cp_profile_screen.cp_CitizenName_fieldSearch.text().strip()

        if not search_text:
            # If search field is empty, reload all citizens
            self.load_citizen_data()
            return

        query = """
            SELECT DISTINCT ON (C.CTZ_ID)
                C.CTZ_ID,
                C.CTZ_LAST_NAME,
                C.CTZ_FIRST_NAME,
                C.CTZ_MIDDLE_NAME,
                C.CTZ_SUFFIX,
                S.SITIO_NAME,
                TO_CHAR(C.CTZ_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS LAST_UPDATED
            FROM CITIZEN C
            JOIN SITIO S ON C.SITIO_ID = S.SITIO_ID
            WHERE C.CTZ_IS_DELETED = FALSE
              AND (
                  CAST(C.CTZ_ID AS TEXT) ILIKE %s OR
                  C.CTZ_LAST_NAME ILIKE %s OR
                  C.CTZ_FIRST_NAME ILIKE %s OR
                  S.SITIO_NAME ILIKE %s
              )
            ORDER BY C.CTZ_ID, COALESCE(C.CTZ_LAST_UPDATED, C.CTZ_DATE_ENCODED) DESC
            LIMIT 50;
        """

        try:
            db = Database()
            cursor = db.get_cursor()
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()

            table = self.cp_profile_screen.cp_tableView_List_RegCitizens
            table.setRowCount(len(rows))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["ID", "Family Name", "First Name", "Sitio", "Last Updated"])
            table.setColumnWidth(0, 50)
            table.setColumnWidth(1, 150)
            table.setColumnWidth(2, 150)
            table.setColumnWidth(3, 150)
            table.setColumnWidth(4, 200)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate([row_data[0], row_data[1], row_data[2], row_data[5], row_data[6]]):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self.cp_profile_screen, "Database Error", str(e))
        finally:
            if db:
                db.close()

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

    def radio_button_student_result(self):
        if self.part3_popup.radioButton_IsStudent_Yes.isChecked():
            student = 'Yes'
        elif self.part3_popup.radioButton_IsStudent_No.isChecked():
            student = 'No'
        else:
            student = ''
        return student

    def radio_button_pwd_result(self):
        if self.part3_popup.register_citizen_IsPWD_Yes.isChecked():
            pwd = 'Yes'
        elif self.part3_popup.register_citizen_IsPWD_No.isChecked():
            pwd = 'No'
        else:
            pwd = ''
        return pwd

    def radio_button_voter_result(self):
        if self.part3_popup.register_citizen_RegVote_Yes.isChecked():
            voter = 'Yes'
        elif self.part3_popup.register_citizen_RegVote_No.isChecked():
            voter = 'No'
        else:
            voter = ''
        return voter

    def radio_button_deceased_result(self):
        if self.part3_popup.register_citizen_Deceased_Yes.isChecked():
            deceased = 'Yes'
        elif self.part3_popup.register_citizen_Deceased_No.isChecked():
            deceased = 'No'
        else:
            deceased = ''
        return deceased

    def radio_button_indig_result(self):
        if self.part3_popup.register_citizen_IndGroup_Yes.isChecked():
            indig = 'Yes'
        elif self.part3_popup.register_citizen_IndGroup_No.isChecked():
            indig = 'No'
        else:
            indig = ''
        return indig

    def update_radio_button_sex_result(self):
        if self.part1_popup_update.radioButton_male.isChecked():
            sex_value = 'Male'
        elif self.part1_popup_update.radioButton_female.isChecked():
            sex_value = 'Female'
        else:
            sex_value = ''
        return sex_value

    def update_radio_button_gov_worker_result(self):
        if self.part2_popup_update.radioButton_IsGov_Yes.isChecked():
            gov_worker = 'Yes'
        elif self.part2_popup_update.radioButton_IsGov_No.isChecked():
            gov_worker = 'No'
        else:
            gov_worker = ''
        return gov_worker

    def update_radio_button_phil_member_result(self):
        if self.part2_popup_update.radioButton_IsPhilMem_Yes.isChecked():
            phil_member = 'Yes'
        elif self.part2_popup_update.radioButton_IsPhilMem_No.isChecked():
            phil_member = 'No'
        else:
            phil_member = ''
        return phil_member

    def update_radio_button_student_result(self):
        if self.part3_popup_update.radioButton_IsStudent_Yes.isChecked():
            student = 'Yes'
        elif self.part3_popup_update.radioButton_IsStudent_No.isChecked():
            student = 'No'
        else:
            student = ''
        return student

    def update_radio_button_pwd_result(self):
        if self.part3_popup_update.register_citizen_IsPWD_Yes.isChecked():
            pwd = 'Yes'
        elif self.part3_popup_update.register_citizen_IsPWD_No.isChecked():
            pwd = 'No'
        else:
            pwd = ''
        return pwd

    def update_radio_button_voter_result(self):
        if self.part3_popup_update.register_citizen_RegVote_Yes.isChecked():
            voter = 'Yes'
        elif self.part3_popup_update.register_citizen_RegVote_No.isChecked():
            voter = 'No'
        else:
            voter = ''
        return voter

    def update_radio_button_deceased_result(self):
        if self.part3_popup_update.register_citizen_Deceased_Yes.isChecked():
            deceased = 'Yes'
        elif self.part3_popup_update.register_citizen_Deceased_No.isChecked():
            deceased = 'No'
        else:
            deceased = ''
        return deceased

    def update_radio_button_indig_result(self):
        if self.part3_popup_update.register_citizen_IndGroup_Yes.isChecked():
            indig = 'Yes'
        elif self.part3_popup_update.register_citizen_IndGroup_No.isChecked():
            indig = 'No'
        else:
            indig = ''
        return indig

    def validate_part1_fields(self, popup):
        form_data_part_1 = self.get_form_data()
        errors_part_1 = []
        print(form_data_part_1)

        # First name validation
        if not form_data_part_1['first_name']:
            errors_part_1.append("First name is required.")
            self.part1_popup.register_citizen_firstname.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.part1_popup.register_citizen_firstname.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Last name validation
        if not form_data_part_1['last_name']:
            errors_part_1.append("Last name is required.")
            self.part1_popup.register_citizen_lastname.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.part1_popup.register_citizen_lastname.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Check if first name + last name already exist in the database
        if form_data_part_1['first_name'] and form_data_part_1['last_name']:
            try:
                db = Database()
                cursor = db.get_cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM citizen 
                    WHERE C.CTZ_IS_DELETED = FALSE AND LOWER(ctz_first_name) = LOWER(%s) AND LOWER(ctz_last_name) = LOWER(%s)
                """, (form_data_part_1['first_name'], form_data_part_1['last_name']))
                result = cursor.fetchone()
                if result[0] > 0:
                    errors_part_1.append("A citizen with the same first and last name already exists.")
                    self.part1_popup.register_citizen_firstname.setStyleSheet(
                        "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                    )
                    self.part1_popup.register_citizen_lastname.setStyleSheet(
                        "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                    )
            except Exception as e:
                print(f"Error checking duplicate name: {e}")
            finally:
                db.close()

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
        else:
            self.part1_popup.register_citizen_comboBox_Religion.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
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
            self.part1_popup.close()
            self.show_register_citizen_part_02_initialize()

    def validate_part3_fields(self):
        form_data_part_3 = self.get_form_data()
        errors_part_3 = []
        # STUDENT / SCHOOL / EDUC LEVELL
        if not form_data_part_3['is_student']:
            errors_part_3.append("Student is required.")
            self.part3_popup.radioButton_IsStudent_Yes.setStyleSheet("color: red")
            self.part3_popup.radioButton_IsStudent_No.setStyleSheet("color: red")

        else:

            self.part3_popup.radioButton_IsStudent_Yes.setStyleSheet("color: rgb(18, 18, 18)")
            self.part3_popup.radioButton_IsStudent_No.setStyleSheet("color: rgb(18, 18, 18)")

        # if not form_data_part_3['has_fam_plan']:
        #     errors_part_3.append("Family Planning is required.")
        #     self.part3_popup.radioButton_IsFamPlan_Yes.setStyleSheet("color: red")
        #     self.part3_popup.radioButton_IsFamPlan_No.setStyleSheet("color: red")
        # elif form_data_part_3['has_fam_plan'] == 'Yes':
        if not form_data_part_3['fam_plan_method']:
            errors_part_3.append("Family Method is required.")
            self.part3_popup.register_citizen_comboBox_FamilyPlanningMethod.setStyleSheet(
                'border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')
        else:
            self.part3_popup.register_citizen_comboBox_FamilyPlanningMethod.setStyleSheet(
                'border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')
        if not form_data_part_3['fam_plan_stat']:
            errors_part_3.append("Family Status is required.")
            self.part3_popup.register_citizen_comboBox_FamPlanStatus.setStyleSheet(
                'border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')
        else:
            self.part3_popup.register_citizen_comboBox_FamPlanStatus.setStyleSheet(
                'border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')
        # else:
        #     form_data_part_3['fam_plan_method'] = 'N/A'
        #     form_data_part_3['fam_plan_stat'] = 'N/A'
        #     self.part3_popup.radioButton_IsFamPlan_Yes.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.part3_popup.radioButton_IsFamPlan_No.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.part3_popup.register_citizen_comboBox_FamPlanStatus.setStyleSheet(
        #         'border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')
        #     self.part3_popup.register_citizen_comboBox_FamilyPlanningMethod.setStyleSheet(
        #         'border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')

        if not form_data_part_3['is_voter']:
            errors_part_3.append("Voter is required.")
            self.part3_popup.register_citizen_RegVote_Yes.setStyleSheet("color: red")
            self.part3_popup.register_citizen_RegVote_No.setStyleSheet("color: red")
        else:
            self.part3_popup.register_citizen_RegVote_Yes.setStyleSheet("color: rgb(18, 18, 18)")
            self.part3_popup.register_citizen_RegVote_No.setStyleSheet("color: rgb(18, 18, 18)")

        if not form_data_part_3['is_deceased']:
            errors_part_3.append("Deceased is required.")
            self.part3_popup.register_citizen_Deceased_Yes.setStyleSheet("color: red")
            self.part3_popup.register_citizen_Deceased_No.setStyleSheet("color: red")
        elif form_data_part_3['is_deceased'] == 'Yes' and not form_data_part_3['reason_of_death']:
            errors_part_3.append("Reason of Death is required.")
            self.part3_popup.register_citizen_Deceased_Yes.setStyleSheet("color: rgb(18, 18, 18)")
            self.part3_popup.register_citizen_Deceased_No.setStyleSheet("color: rgb(18, 18, 18)")
            self.part3_popup.register_citizen_ReasonOfDeath.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        else:
            self.part3_popup.register_citizen_Deceased_Yes.setStyleSheet("color: rgb(18, 18, 18)")
            self.part3_popup.register_citizen_Deceased_No.setStyleSheet("color: rgb(18, 18, 18)")
            self.part3_popup.register_citizen_ReasonOfDeath.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")
            form_data_part_3['reason_of_death'] = "None"
        if not form_data_part_3['is_indig']:
            errors_part_3.append("Indigenous Group is required.")
            self.part3_popup.register_citizen_IndGroup_Yes.setStyleSheet("color: red")
            self.part3_popup.register_citizen_IndGroup_No.setStyleSheet("color: red")
        else:
            self.part3_popup.register_citizen_IndGroup_Yes.setStyleSheet("color: rgb(18, 18, 18)")
            self.part3_popup.register_citizen_IndGroup_No.setStyleSheet("color: rgb(18, 18, 18)")
        if not form_data_part_3['health_class']:
            errors_part_3.append("Health Classification is required.")
            self.part3_popup.register_citizen_health_classification.setStyleSheet(
                'border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')
        else:
            self.part3_popup.register_citizen_health_classification.setStyleSheet(
                'border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)')

        if errors_part_3:
            self.view.show_error_message(errors_part_3)
        else:
            self.confirm_and_save()

        print(form_data_part_3)
        # if not form_data_part_1['sex']:
        #     errors_part_1.append("Sex is required.")
        #     self.part1_popup.radioButton_female.setStyleSheet("color: red")
        #     self.part1_popup.radioButton_male.setStyleSheet("color: red")
        # else:
        #     self.part1_popup.radioButton_female.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.part1_popup.radioButton_male.setStyleSheet("color: rgb(18, 18, 18)")

    def validate_part2_fields(self):
        form_data_part_2 = self.get_form_data()
        errors_part_2 = []

        # Socio Economic Status & NHTS Number
        if not form_data_part_2['socio_eco_status']:
            errors_part_2.append("Socio Economic Status is required.")
            self.part2_popup.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        elif form_data_part_2['socio_eco_status'] in ['NHTS 4Ps', 'NHTS Non-4Ps']:
            if not form_data_part_2['nhts_number']:
                errors_part_2.append("NHTS Number is required.")
                self.part2_popup.register_citizen_NHTSNum.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            else:
                self.part2_popup.register_citizen_NHTSNum.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            self.part2_popup.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            form_data_part_2['nhts_number'] = "None"
            self.part2_popup.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
            self.part2_popup.register_citizen_NHTSNum.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Employment Status
        if not form_data_part_2['employment_status']:
            errors_part_2.append("Employment Status is required.")
            self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        elif form_data_part_2['employment_status'] in ['Employed', 'Retired', 'Self Employed']:
            if not form_data_part_2['occupation']:
                errors_part_2.append("Occupation is required.")
                self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
                self.part2_popup.register_citizen_Occupation.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            else:
                self.part2_popup.register_citizen_Occupation.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
        else:
            form_data_part_2['occupation'] = "None"
            self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
            self.part2_popup.register_citizen_Occupation.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # Household ID (Existence Check)
        if not form_data_part_2['household_id']:
            errors_part_2.append("Household ID is required.")
            self.part2_popup.register_citizen_HouseholdID.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT 1 FROM household_info WHERE HH_IS_DELETED = FALSE AND hh_id = %s",
                           (form_data_part_2['household_id'],))
            result = cursor.fetchone()
            if not result:
                errors_part_2.append("Household ID does not exist.")
                self.part2_popup.register_citizen_HouseholdID.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            else:
                self.part2_popup.register_citizen_HouseholdID.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )

        # Relationship
        if not form_data_part_2['relationship']:
            errors_part_2.append("Relationship is required.")
            self.part2_popup.register_citizen_comboBox_Relationship.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        else:
            self.part2_popup.register_citizen_comboBox_Relationship.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # Philhealth Member
        if not form_data_part_2['phil_category']:
            errors_part_2.append("Philhealth Category is required.")
            self.part2_popup.register_citizen_comboBox_PhilCat.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part2_popup.register_citizen_comboBox_PhilCat.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
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
        # elif not form_data_part_2['phil_member']:
        #     errors_part_2.append("Philhealth Member is required.")
        #     self.part2_popup.radioButton_IsPhilMem_Yes.setStyleSheet("color: red")
        #     self.part2_popup.radioButton_IsPhilMem_No.setStyleSheet("color: red")

        # if not form_data_part_1['sex']:
        #     errors_part_1.append("Sex is required.")
        #     self.part1_popup.radioButton_female.setStyleSheet("color: red")
        #     self.part1_popup.radioButton_male.setStyleSheet("color: red")
        # else:
        #     self.part1_popup.radioButton_female.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.part1_popup.radioButton_male.setStyleSheet("color: rgb(18, 18, 18)")
        # else:
        #     self.part2_popup.radioButton_IsPhilMem_Yes.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.part2_popup.radioButton_IsPhilMem_No.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.part2_popup.register_citizen_comboBox_PhilCat.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)")
        #     self.part2_popup.register_citizen_comboBox_PhilMemType.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)")
        #     self.part2_popup.register_citizen_PhilID.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
        #     )

        # if not form_data_part_1['sex']:
        #     errors_part_1.append("Sex is required.")
        #     self.part1_popup.radioButton_female.setStyleSheet("color: red")
        #     self.part1_popup.radioButton_male.setStyleSheet("color: red")
        # else:
        #     self.part1_popup.radioButton_female.setStyleSheet("color: rgb(18, 18, 18)")
        #     self.part1_popup.radioButton_male.setStyleSheet("color: rgb(18, 18, 18)")

        if form_data_part_2['employment_status'] == 'Unemployed':
            form_data_part_2['gov_worker'] = 'No'
            self.part2_popup.radioButton_IsGov_Yes.setStyleSheet("color: rgb(18, 18, 18)")
            self.part2_popup.radioButton_IsGov_No.setStyleSheet("color: rgb(18, 18, 18)")

        elif not form_data_part_2['gov_worker']:
            errors_part_2.append("Government Worker is required.")
            self.part2_popup.radioButton_IsGov_Yes.setStyleSheet("color: red")
            self.part2_popup.radioButton_IsGov_No.setStyleSheet("color: red")
        else:
            self.part2_popup.radioButton_IsGov_Yes.setStyleSheet("color: rgb(18, 18, 18)")
            self.part2_popup.radioButton_IsGov_No.setStyleSheet("color: rgb(18, 18, 18)")

        print(form_data_part_2)

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

    def update_validate_part1_fields(self):
        errors = []

        # Get field values directly from widgets
        first_name = self.part1_popup_update.register_citizen_firstname.text().strip()
        last_name = self.part1_popup_update.register_citizen_lastname.text().strip()
        suffix = self.part1_popup_update.register_citizen_suffix.text().strip()
        dob = self.part1_popup_update.register_citizen_date_dob.date()
        selected_sex_button = self.sex_group.checkedButton()
        # First Name Validation
        if not first_name:
            errors.append("First name is required.")
            self.part1_popup_update.register_citizen_firstname.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        else:
            self.part1_popup_update.register_citizen_firstname.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")

        # Last Name Validation
        if not last_name:
            errors.append("Last name is required.")
            self.part1_popup_update.register_citizen_lastname.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        else:
            self.part1_popup_update.register_citizen_lastname.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")

        # DOB Validation (Optional but should be valid)
        if not dob.isValid():
            errors.append("Date of birth is invalid.")
            self.part1_popup_update.register_citizen_date_dob.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        else:
            self.part1_popup_update.register_citizen_date_dob.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")

        # Sex Validation
        if not selected_sex_button:
            errors.append("Sex is required.")
            self.part1_popup_update.radioButton_male.setStyleSheet("color: red")
            self.part1_popup_update.radioButton_female.setStyleSheet("color: red")
        else:
            self.part1_popup_update.radioButton_male.setStyleSheet("color: rgb(18, 18, 18)")
            self.part1_popup_update.radioButton_female.setStyleSheet("color: rgb(18, 18, 18)")

        # Civil Status
        civil_status = self.part1_popup_update.register_citizen_comboBox_CivilStatus.currentText()
        if not civil_status:
            errors.append("Civil status is required.")
            self.part1_popup_update.register_citizen_comboBox_CivilStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        else:
            self.part1_popup_update.register_citizen_comboBox_CivilStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")

        if errors:
            self.view.show_error_message(errors)
        else:
            self.part1_popup_update.close()
            self.show_update_citizen_part_02_initialize()
        # if errors:
        #     self.view.show_error_message(errors)
        #     return False
        # return True

    def update_validate_part2_fields(self):
        errors = []

        # Get form data from widgets
        socio_eco_status = self.part2_popup_update.register_citizen_comboBox_SocEcoStat.currentText().strip()
        nhts_number = self.part2_popup_update.register_citizen_NHTSNum.text().strip()
        household_id = self.part2_popup_update.register_citizen_HouseholdID.text().strip()
        relationship = self.part2_popup_update.register_citizen_comboBox_Relationship.currentText().strip()
        emp_status = self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.currentText().strip()
        occupation = self.part2_popup_update.register_citizen_Occupation.text().strip()
        phil_category = self.part2_popup_update.register_citizen_comboBox_PhilCat.currentText().strip()
        membership_type = self.part2_popup_update.register_citizen_comboBox_PhilMemType.currentText().strip()

        # --- Socio Economic Status Validation ---
        if not socio_eco_status:
            errors.append("Socio Economic Status is required.")
            self.part2_popup_update.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part2_popup_update.register_citizen_comboBox_SocEcoStat.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # --- NHTS Number Validation (only if applicable) ---
        if socio_eco_status in ['NHTS 4Ps', 'NHTS Non-4Ps']:
            if not nhts_number:
                errors.append("NHTS Number is required.")
                self.part2_popup_update.register_citizen_NHTSNum.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            else:
                self.part2_popup_update.register_citizen_NHTSNum.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
        else:
            self.part2_popup_update.register_citizen_NHTSNum.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # --- Household ID Validation ---
        if not household_id:
            errors.append("Household ID is required.")
            self.part2_popup_update.register_citizen_HouseholdID.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        else:
            self.part2_popup_update.register_citizen_HouseholdID.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # --- Relationship Validation ---
        if not relationship:
            errors.append("Relationship is required.")
            self.part2_popup_update.register_citizen_comboBox_Relationship.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part2_popup_update.register_citizen_comboBox_Relationship.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # --- Employment Status & Occupation ---
        if not emp_status:
            errors.append("Employment status is required.")
            self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )
        elif emp_status in ['Employed', 'Retired', 'Self Employed']:
            if not occupation:
                errors.append("Occupation is required.")
                self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
                )
                self.part2_popup_update.register_citizen_Occupation.setStyleSheet(
                    "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
            else:
                self.part2_popup_update.register_citizen_Occupation.setStyleSheet(
                    "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
                )
        else:
            self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
            self.part2_popup_update.register_citizen_Occupation.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
            )

        # --- Philhealth Category Validation ---
        if not phil_category:
            errors.append("Philhealth Category is required.")
            self.part2_popup_update.register_citizen_comboBox_PhilCat.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part2_popup_update.register_citizen_comboBox_PhilCat.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # --- Membership Type Validation ---
        if not membership_type:
            errors.append("Membership Type is required.")
            self.part2_popup_update.register_citizen_comboBox_PhilMemType.setStyleSheet(
                "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )
        else:
            self.part2_popup_update.register_citizen_comboBox_PhilMemType.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
            )

        # Show errors if any
        if errors:
            self.view.show_error_message(errors)
            return False
        else:
            self.part2_popup_update.close()
            self.show_update_citizen_part_03_initialize()
            return True
        # if not occupation:
        #     errors.append("Occupation is required.")
        #     self.part2_popup_update.register_citizen_Occupation.setStyleSheet(
        #         "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        # else:
        #     self.part2_popup_update.register_citizen_Occupation.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")

        # if not form_data_part_2['employment_status']:
        #     errors_part_2.append("Employment Status is required.")
        #     self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
        #         "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
        #     )
        # elif form_data_part_2['employment_status'] in ['Employed', 'Retired', 'Self Employed']:
        #     if not form_data_part_2['occupation']:
        #         errors_part_2.append("Occupation is required.")
        #         self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
        #             "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
        #         )
        #         self.part2_popup.register_citizen_Occupation.setStyleSheet(
        #             "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff"
        #         )
        #     else:
        #         self.part2_popup.register_citizen_Occupation.setStyleSheet(
        #             "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
        #         )
        # else:
        #     form_data_part_2['occupation'] = "None"
        #     self.part2_popup.register_citizen_comboBox_EmploymentStatus.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: rgb(239, 239, 239)"
        #     )
        #     self.part2_popup.register_citizen_Occupation.setStyleSheet(
        #             "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff"
        #         )
        # if not monthly_income:
        #     errors.append("Monthly income is required.")
        #     self.part2_popup_update.register_citizen_MonthlyIncome.setStyleSheet(
        #         "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        # elif not monthly_income.replace('.', '', 1).isdigit():
        #     errors.append("Monthly income must be a number.")
        #     self.part2_popup_update.register_citizen_MonthlyIncome.setStyleSheet(
        #         "border: 1px solid red; border-radius: 5px; padding: 5px; background-color: #f2efff")
        # else:
        #     self.part2_popup_update.register_citizen_MonthlyIncome.setStyleSheet(
        #         "border: 1px solid gray; border-radius: 5px; padding: 5px; background-color: #f2efff")

    def update_validate_part3_fields(self):
        errors = []

        # # Student
        # student = self.update_radio_button_student_result()
        # if not student:
        #     errors.append("Student status is required.")
        #     self.part3_popup_update.register_citizen_IsStudent_Yes.setStyleSheet("color: red")
        #     self.part3_popup_update.register_citizen_IsStudent_No.setStyleSheet("color: red")
        # else:
        #     self.part3_popup_update.register_citizen_IsStudent_Yes.setStyleSheet("color: black")
        #     self.part3_popup_update.register_citizen_IsStudent_No.setStyleSheet("color: black")

        # Voter
        # voter = self.update_radio_button_voter_result()
        # if not voter:
        #     errors.append("Voter status is required.")
        #     self.part3_popup_update.register_citizen_RegVote_Yes.setStyleSheet("color: red")
        #     self.part3_popup_update.register_citizen_RegVote_No.setStyleSheet("color: red")
        # else:
        #     self.part3_popup_update.register_citizen_RegVote_Yes.setStyleSheet("color: black")
        #     self.part3_popup_update.register_citizen_RegVote_No.setStyleSheet("color: black")
        #
        # # Deceased
        # deceased = self.update_radio_button_deceased_result()
        # if not deceased:
        #     errors.append("Deceased status is required.")
        #     self.part3_popup_update.register_citizen_Deceased_Yes.setStyleSheet("color: red")
        #     self.part3_popup_update.register_citizen_Deceased_No.setStyleSheet("color: red")
        # else:
        #     self.part3_popup_update.register_citizen_Deceased_Yes.setStyleSheet("color: black")
        #     self.part3_popup_update.register_citizen_Deceased_No.setStyleSheet("color: black")

        if errors:
            self.view.show_error_message(errors)
            return False
        else:
            self.confirm_and_save_update()

        return True

    def confirm_and_save_update(self):

        if not self.selected_citizen_id:
            QMessageBox.warning(self.part3_popup_update, "No Citizen Selected", "Please select a citizen to update.")
            return

        form_data = self.get_form_data_update()
        print('mao nani', form_data['relationship_id'])

        confirm = QMessageBox.question(
            self.part3_popup_update,
            "Confirm Update",
            "Are you sure you want to update this citizen’s information?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            db = Database()
            cursor = db.get_cursor()

            # 1. Update CITIZEN
            cursor.execute("""
                UPDATE citizen SET
                    ctz_first_name = %s,
                    ctz_middle_name = %s,
                    ctz_last_name = %s,
                    ctz_suffix = %s,
                    ctz_date_of_birth = %s,
                    ctz_sex = %s,
                    ctz_civil_status = %s,
                    ctz_place_of_birth = %s,
                    ctz_blood_type = %s,
                    sitio_id = %s,
                    rel_id = (SELECT rel_id FROM religion WHERE rel_name = %s LIMIT 1),
                    ctz_is_ip = %s,
                    ctz_is_registered_voter = %s,
                    ctz_is_alive = %s,
                    ctz_reason_of_death = %s,
                    ctz_date_of_death = %s,
                    soec_id = (SELECT soec_id FROM socio_economic_status WHERE soec_status = %s LIMIT 1),
                    hh_id = %s,
                    rth_id = %s,
                    clah_id = (SELECT clah_id FROM classification_health_risk WHERE clah_classification_name = %s LIMIT 1),
                    last_updated_by_sys_id = %s,
                    ctz_last_updated = CURRENT_TIMESTAMP
                WHERE ctz_id = %s
            """, (
                form_data['first_name'], form_data['middle_name'], form_data['last_name'],
                form_data['suffix'], form_data['birth_date'], form_data['sex'],
                form_data['civil_status'], form_data['birth_place'], form_data['blood_type'],
                form_data['sitio_id'], form_data['religion'], form_data['indigenous_group'],
                form_data['registered_voter'], form_data['is_alive'], form_data['reason_of_death'],
                form_data['date_of_death'], form_data['socioeco_status'],
                form_data['household_id'], form_data['relationship_id'],
                form_data['health_classification'], self.sys_user_id, self.selected_citizen_id
            ))
            # 2. Update CONTACT
            cursor.execute("""
                UPDATE contact SET
                    con_email = %s,
                    con_phone = %s
                WHERE con_id = (SELECT con_id FROM citizen WHERE ctz_id = %s)
            """, (
                form_data['email'], form_data['contact_number'], self.selected_citizen_id
            ))

            # 3. Update EMPLOYMENT
            cursor.execute("""
                UPDATE employment SET
                    emp_occupation = %s,
                    emp_is_gov_worker = %s,
                    es_id = (SELECT es_id FROM employment_status WHERE es_status_name = %s LIMIT 1)
                WHERE ctz_id = %s
            """, (
                form_data['occupation'], form_data['gov_worker'],
                form_data['employment_status'], self.selected_citizen_id
            ))

            # 4. Update PHILHEALTH
            cursor.execute("""
                UPDATE philhealth SET
                    phea_id_number = %s,
                    phea_membership_type = %s,
                    pc_id = (SELECT pc_id FROM philhealth_category WHERE pc_category_name = %s LIMIT 1)
                WHERE phea_id = (SELECT phea_id FROM citizen WHERE ctz_id = %s)
            """, (
                form_data['philhealth_id'], form_data['membership_type'],
                form_data['philhealth_category'], self.selected_citizen_id
            ))

            # 5. Update EDUCATION_STATUS
            cursor.execute("""
                UPDATE education_status SET
                    edu_is_currently_student = %s,
                    edu_institution_name = %s,
                    edat_id = (SELECT edat_id FROM educational_attainment WHERE edat_level = %s LIMIT 1)
                WHERE edu_id = (SELECT edu_id FROM citizen WHERE ctz_id = %s)
            """, (
                form_data['is_student'], form_data['school_name'],
                form_data['educational_level'], self.selected_citizen_id
            ))

            # 6. Update FAMILY_PLANNING
            cursor.execute("""
                UPDATE family_planning SET
                    fpm_method = (SELECT fpm_id FROM family_planning_method WHERE fpm_method = %s LIMIT 1),
                    fpms_status = (SELECT fpms_id FROM fpm_status WHERE fpms_status_name = %s LIMIT 1),
                    fp_start_date = %s,
                    fp_end_date = %s
                WHERE ctz_id = %s
            """, (
                form_data['fp_method'], form_data['fp_status'],
                form_data['start_date'], form_data['end_date'],
                self.selected_citizen_id
            ))

            db.commit()

            QMessageBox.information(self.part3_popup_update, "Success", "Citizen information updated successfully.")

            self.part1_popup_update.close()
            self.part2_popup_update.close()
            self.part3_popup_update.close()
            self.load_citizen_data()

        except Exception as e:
            print(f"Error during update: {e}")
            QMessageBox.critical(self.part3_popup_update, "Update Error", f"An error occurred:\n{e}")
        finally:
            db.close()

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
        file_path, _ = QFileDialog.getOpenFileName(self.part1_popup, "Select an Image", "",
                                                   "General_Images (*.png *.jpg *.jpeg *.bmp *.gif)")
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
            self.part2_popup.register_citizen_HouseholdID.setText(self.get_form_data()['household_id'])
        if 'relationship' in self.citizen_data:
            index = self.part2_popup.register_citizen_comboBox_Relationship.findText(self.citizen_data['relationship'])
            if index >= 0:
                self.part2_popup.register_citizen_comboBox_Relationship.setCurrentIndex(index)

    def return_to_part1_from_part2(self):
        # self.save_part2_data()
        print(self.get_form_data())
        self.part2_popup.close()
        self.part1_popup.show()

    def return_to_part2_from_part3(self):
        # self.save_part2_data()
        # print(self.get_form_data_part_3())
        self.part3_popup.close()
        self.part2_popup.show()

    def update_return_to_part1_from_part2(self):
        # self.save_part2_data()
        # print(self.get_form_data())
        self.part2_popup_update.close()
        self.part1_popup_update.show()

    def update_return_to_part2_from_part3(self):
        # self.save_part2_data()
        # print(self.get_form_data_part_3())
        self.part3_popup_update.close()
        self.part2_popup_update.show()

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

    #
    # def setup_radio_button_groups_02(self):
    #     gov_worker = QButtonGroup(self.part2_popup)
    #     gov_worker_yes = self.part2_popup.findChild(QRadioButton, "radioButton_IsGov_Yes")
    #     gov_worker_no = self.part2_popup.findChild(QRadioButton, "radioButton_IsGov_No")
    #     if gov_worker_yes and gov_worker_no:
    #         gov_worker.addButton(gov_worker_yes)
    #         gov_worker.addButton(gov_worker_no)
    #
    #     phil_member = QButtonGroup(self.part2_popup)
    #     phil_member_yes = self.part2_popup.findChild(QRadioButton, "radioButton_IsPhilMem_Yes")
    #     phil_member_no = self.part2_popup.findChild(QRadioButton, "radioButton_IsPhilMem_No")
    #     if phil_member_yes and phil_member_no:
    #         phil_member.addButton(phil_member_yes)
    #         phil_member.addButton(phil_member_no)

    #
    #
    # CITIZEN CREATE PART 3
    #
    #

    # def show_register_citizen_part_03_popup(self, part_two_popup):
    #     part_two_popup.close()
    #     self.part3_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_03.ui", self)
    #     self.part3_popup.setWindowTitle("Register New Citizen - Part 3")
    #     self.part3_popup.setWindowModality(Qt.ApplicationModal)
    #     self.part3_popup.setFixedSize(self.part3_popup.size())
    #     self.part3_popup.register_buttonReturnToPart2_FromPart3.setIcon(QIcon('Resources/Icons/FuncIcons/icon_arrow_prev'))
    #     self.part3_popup.register_buttonConfirmPart3_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm'))
    #     if hasattr(self, 'citizen_data'):
    #         self.restore_part3_data()
    #     # self.setup_radio_button_groups_03()
    #     save_btn = self.part3_popup.findChild(QPushButton, "register_buttonConfirmPart3_SaveForm")
    #     if save_btn:
    #         save_btn.clicked.connect(self.confirm_and_save)
    #     back_btn = self.part3_popup.findChild(QPushButton, "register_buttonReturnToPart2_FromPart3")
    #
    #     if back_btn:
    #         back_btn.clicked.connect(self.return_to_part2_from_part3)
    #     self.part3_popup.show()

    # DATA INTERACTION PART 3

    # def update_setup_radio_button_groups_03(self):
    #     radio_student = QButtonGroup(self.part3_popup)
    #     student_yes = self.part3_popup.findChild(QRadioButton, "radioButton_IsStudent_Yes")
    #     student_no = self.part3_popup.findChild(QRadioButton, "radioButton_IsStudent_No")
    #     if student_yes and student_no:
    #         radio_student.addButton(student_yes)
    #         radio_student.addButton(student_no)
    #
    #     radio_famplan = QButtonGroup(self.part3_popup)
    #     famplan_yes = self.part3_popup.findChild(QRadioButton, "radioButton_IsFamPlan_Yes")
    #     famplan_no = self.part3_popup.findChild(QRadioButton, "radioButton_IsFamPlan_No")
    #     if famplan_yes and famplan_no:
    #         radio_famplan.addButton(famplan_yes)
    #         radio_famplan.addButton(famplan_no)
    #
    #     radio_pwd = QButtonGroup(self.part3_popup)
    #     pwd_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_IsPWD_Yes")
    #     pwd_no = self.part3_popup.findChild(QRadioButton, "register_citizen_IsPWD_No")
    #     if pwd_yes and pwd_no:
    #         radio_pwd.addButton(pwd_yes)
    #         radio_pwd.addButton(pwd_no)
    #
    #     radio_voter = QButtonGroup(self.part3_popup)
    #     vote_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_RegVote_Yes")
    #     vote_no = self.part3_popup.findChild(QRadioButton, "register_citizen_RegVote_No")
    #     if vote_yes and vote_no:
    #         radio_voter.addButton(vote_yes)
    #         radio_voter.addButton(vote_no)
    #
    #     radio_deceased = QButtonGroup(self.part3_popup)
    #     deceased_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_Deceased_Yes")
    #     deceased_no = self.part3_popup.findChild(QRadioButton, "register_citizen_Deceased_No")
    #     if deceased_yes and deceased_no:
    #         radio_deceased.addButton(deceased_yes)
    #         radio_deceased.addButton(deceased_no)
    #
    #     radio_indigenous = QButtonGroup(self.part3_popup)
    #     ind_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_IndGroup_Yes")
    #     ind_no = self.part3_popup.findChild(QRadioButton, "register_citizen_IndGroup_No")
    #     if ind_yes and ind_no:
    #         radio_indigenous.addButton(ind_yes)
    #         radio_indigenous.addButton(ind_no)

    # GENERAL FUNCTION PART 3

    #
    #
    # def setup_radio_button_groups_03(self):
    #     radio_student = QButtonGroup(self.part3_popup)
    #     student_yes = self.part3_popup.findChild(QRadioButton, "radioButton_IsStudent_Yes")
    #     student_no = self.part3_popup.findChild(QRadioButton, "radioButton_IsStudent_No")
    #     if student_yes and student_no:
    #         radio_student.addButton(student_yes)
    #         radio_student.addButton(student_no)
    #
    #     radio_famplan = QButtonGroup(self.part3_popup)
    #     famplan_yes = self.part3_popup.findChild(QRadioButton, "radioButton_IsFamPlan_Yes")
    #     famplan_no = self.part3_popup.findChild(QRadioButton, "radioButton_IsFamPlan_No")
    #     if famplan_yes and famplan_no:
    #         radio_famplan.addButton(famplan_yes)
    #         radio_famplan.addButton(famplan_no)
    #
    #     radio_pwd = QButtonGroup(self.part3_popup)
    #     pwd_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_IsPWD_Yes")
    #     pwd_no = self.part3_popup.findChild(QRadioButton, "register_citizen_IsPWD_No")
    #     if pwd_yes and pwd_no:
    #         radio_pwd.addButton(pwd_yes)
    #         radio_pwd.addButton(pwd_no)
    #
    #     radio_voter = QButtonGroup(self.part3_popup)
    #     vote_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_RegVote_Yes")
    #     vote_no = self.part3_popup.findChild(QRadioButton, "register_citizen_RegVote_No")
    #     if vote_yes and vote_no:
    #         radio_voter.addButton(vote_yes)
    #         radio_voter.addButton(vote_no)
    #
    #     radio_deceased = QButtonGroup(self.part3_popup)
    #     deceased_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_Deceased_Yes")
    #     deceased_no = self.part3_popup.findChild(QRadioButton, "register_citizen_Deceased_No")
    #     if deceased_yes and deceased_no:
    #         radio_deceased.addButton(deceased_yes)
    #         radio_deceased.addButton(deceased_no)
    #
    #     radio_indigenous = QButtonGroup(self.part3_popup)
    #     ind_yes = self.part3_popup.findChild(QRadioButton, "register_citizen_IndGroup_Yes")
    #     ind_no = self.part3_popup.findChild(QRadioButton, "register_citizen_IndGroup_No")
    #     if ind_yes and ind_no:
    #         radio_indigenous.addButton(ind_yes)
    #         radio_indigenous.addButton(ind_no)

    def confirm_and_save(self):
        reply = QMessageBox.question(
            self.part3_popup,
            "Confirm Registration",
            "Are you sure you want to register this citizen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        print("-- Form Submitted")

        # Get form data
        form_data = self.get_form_data()
        if not form_data:
            QMessageBox.critical(self.part3_popup, "Error", "No data to save.")
            return

        db = Database()
        connection = db.conn
        cursor = connection.cursor()

        # --- GET rth_id FROM RELATIONSHIP_TYPE ---
        relationship_name = form_data['relationship']
        cursor.execute("SELECT rth_id FROM relationship_type WHERE rth_relationship_name = %s", (relationship_name,))
        rth_result = cursor.fetchone()

        if not rth_result:
            raise Exception(f"Relationship '{relationship_name}' not found in relationship_type table.")
        rth_id = rth_result[0]

        # --- Validate/Insert CLASSIFICATION_HEALTH_RISK ---
        health_class = form_data.get('health_class')
        clah_id = None

        if health_class not in ['None', '', None]:
            cursor.execute("SELECT clah_id FROM classification_health_risk WHERE clah_classification_name = %s",
                           (health_class,))
            clah_result = cursor.fetchone()
            if not clah_result:
                raise Exception(f"Health classification '{health_class}' not found.")
            clah_id = clah_result[0]

        try:
            # --- Validate & Insert CONTACT ---
            email = form_data['email_address']
            phone = form_data['contact_number']

            contact_query = """
                INSERT INTO contact (con_email, con_phone)
                VALUES (%s, %s)
                RETURNING con_id;
            """
            cursor.execute(contact_query, (email, phone))
            contact_result = cursor.fetchone()
            if not contact_result:
                raise Exception("Failed to insert into CONTACT table")
            contact_id = contact_result[0]

            # --- Validate SITIO ---
            cursor.execute("SELECT sitio_id FROM sitio WHERE sitio_name = %s", (form_data['sitio'],))
            sitio_result = cursor.fetchone()
            if not sitio_result:
                raise Exception(f"Sitio '{form_data['sitio']}' not found in database.")
            sitio_id = sitio_result[0]

            # --- Validate/Insert EDUCATION_LEVEL ---
            edu_level = form_data['educ_level']
            edat_id = None
            if edu_level not in ['None', '', None]:
                cursor.execute("SELECT edat_id FROM educational_attainment WHERE edat_level = %s", (edu_level,))
                edu_level_result = cursor.fetchone()
                if not edu_level_result:
                    raise Exception(f"Educational level '{edu_level}' not found.")
                edat_id = edu_level_result[0]

            # --- Insert EDUCATION_STATUS ---
            cursor.execute("""
                INSERT INTO education_status (edu_is_currently_student, edu_institution_name, edat_id)
                VALUES (%s, %s, %s)
                RETURNING edu_id;
            """, (
                True if form_data['is_student'] == 'Yes' else False,
                form_data['school_name'] if form_data['school_name'] not in ['', 'None'] else None,
                edat_id
            ))
            edu_result = cursor.fetchone()
            if not edu_result:
                raise Exception("Failed to insert into EDUCATION_STATUS")
            edu_id = edu_result[0]

            # --- Insert SOCIO_ECONOMIC_STATUS ---
            socio_status = form_data['socio_eco_status']
            nhts_num = form_data['nhts_number'] if socio_status in ['NHTS 4Ps', 'NHTS Non-4Ps'] else None

            cursor.execute("""
                INSERT INTO socio_economic_status (soec_status, soec_number)
                VALUES (%s, %s)
                RETURNING soec_id;
            """, (socio_status, nhts_num))
            soec_result = cursor.fetchone()
            if not soec_result:
                raise Exception("Failed to insert into SOCIO_ECONOMIC_STATUS")
            soec_id = soec_result[0]

            # --- Validate RELIGION ---
            religion = form_data['religion']
            cursor.execute("SELECT rel_id FROM religion WHERE rel_name = %s", (religion,))
            rel_result = cursor.fetchone()
            if not rel_result:
                cursor.execute("INSERT INTO religion (rel_name) VALUES (%s) RETURNING rel_id", (religion,))
                rel_insert_result = cursor.fetchone()
                if not rel_insert_result:
                    raise Exception("Failed to insert new religion")
                rel_id = rel_insert_result[0]
            else:
                rel_id = rel_result[0]

            # --- Validate PHILHEALTH CATEGORY ---
            phil_category = form_data['phil_category']
            cursor.execute("SELECT pc_id FROM philhealth_category WHERE pc_category_name = %s", (phil_category,))
            pc_result = cursor.fetchone()
            if not pc_result:
                raise Exception(f"Philhealth category '{phil_category}' not found.")
            pc_id = pc_result[0]

            # --- Insert PHILHEALTH ---
            phil_id = form_data['phil_id'].strip() if form_data['phil_id'] and form_data['phil_id'].strip() else None
            membership_type = form_data['membership_type']
            phil_category = pc_id  # Already retrieved earlier

            # Always insert PHILHEALTH if category & membership type are present
            if not membership_type:
                raise Exception("Membership type cannot be empty")

            cursor.execute("""
                INSERT INTO philhealth (phea_id_number, pc_id, phea_membership_type)
                VALUES (%s, %s, %s)
                RETURNING phea_id;
            """, (phil_id, phil_category, membership_type))

            phea_result = cursor.fetchone()
            if not phea_result:
                raise Exception("Failed to insert into PHILHEALTH")
            phea_id = phea_result[0]

            # --- Insert CITIZEN ---
            # --- Insert CITIZEN ---
            citizen_query = """
            INSERT INTO citizen (
                ctz_first_name, ctz_middle_name, ctz_last_name, ctz_suffix,
                ctz_date_of_birth, ctz_sex, ctz_civil_status, ctz_place_of_birth,
                ctz_blood_type, ctz_is_registered_voter, ctz_is_alive, ctz_date_of_death,
                ctz_reason_of_death, ctz_date_encoded, con_id, sitio_id, edu_id, soec_id,
                phea_id, rel_id, rth_id, hh_id, encoded_by_sys_id, last_updated_by_sys_id,
                clah_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING ctz_id;
            """

            date_of_death = form_data['date_of_death'] if form_data['is_deceased'] == 'Yes' else None
            reason_of_death = form_data['reason_of_death'] if form_data['is_deceased'] == 'Yes' else None
            is_alive = not (form_data['is_deceased'] == 'Yes')

            cursor.execute(citizen_query, (
                form_data['first_name'],
                form_data['middle_name'] or None,
                form_data['last_name'],
                form_data['suffix'] or None,
                form_data['birth_date'],
                'M' if form_data['sex'] == 'Male' else 'F',
                form_data['civil_status'],
                form_data['place_of_birth'],
                form_data['blood_type'] or None,
                True if form_data['is_voter'] == 'Yes' else False,
                is_alive,
                date_of_death,
                reason_of_death,
                contact_id,
                sitio_id,
                edu_id,
                soec_id,
                phea_id,
                rel_id,
                rth_id,
                int(form_data['household_id']),
                self.sys_user_id,
                self.sys_user_id,
                clah_id  # ✅ Now properly included
            ))
            citizen_result = cursor.fetchone()
            if not citizen_result:
                raise Exception("Failed to insert into CITIZEN")
            citizen_id = citizen_result[0]

            # --- FAMILY PLANNING INSERTION ---
            fam_plan_method = form_data.get('fam_plan_method')
            fam_plan_stat = form_data.get('fam_plan_stat')

            if fam_plan_method not in ['None', '', None] and fam_plan_stat not in ['None', '', None]:
                # Retrieve FPM_ID from family_planning_method
                cursor.execute("SELECT FPM_ID FROM family_planning_method WHERE FPM_METHOD = %s", (fam_plan_method,))
                fpm_result = cursor.fetchone()
                if not fpm_result:
                    raise Exception(f"Family planning method '{fam_plan_method}' not found.")
                fpm_id = fpm_result[0]

                # Retrieve FPMS_ID from fpm_status
                cursor.execute("SELECT FPMS_ID FROM fpm_status WHERE FPMS_STATUS_NAME = %s", (fam_plan_stat,))
                fpms_result = cursor.fetchone()
                if not fpms_result:
                    raise Exception(f"Family planning status '{fam_plan_stat}' not found.")
                fpms_id = fpms_result[0]

                fp_start_date = form_data.get('fam_plan_start_date')
                fp_end_date = form_data.get('fam_plan_end_date')

                # Use citizen_id here, NOT ctz_id
                cursor.execute("""
                    INSERT INTO family_planning (
                        FP_START_DATE, FP_END_DATE, CTZ_ID, FPMS_STATUS, FPM_METHOD
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    fp_start_date,
                    fp_end_date,
                    citizen_id,  # ← Correct variable
                    fpms_id,
                    fpm_id
                ))
            else:
                print("-- Skipping Family Planning insertion due to missing data")

            # --- Insert EMPLOYMENT ---
            employment_status = form_data['employment_status']
            cursor.execute("SELECT es_id FROM employment_status WHERE es_status_name = %s", (employment_status,))
            es_result = cursor.fetchone()
            if not es_result:
                raise Exception(f"Employment status '{employment_status}' not found")
            es_id = es_result[0]

            cursor.execute("""
                INSERT INTO employment (emp_occupation, emp_is_gov_worker, es_id, ctz_id)
                VALUES (%s, %s, %s, %s);
            """, (
                form_data['occupation'],
                True if form_data['gov_worker'] == 'Yes' else False,
                es_id,
                citizen_id
            ))

            # --- Commit transaction ---
            connection.commit()
            QMessageBox.information(self.part3_popup, "Success", "Citizen successfully registered!")

            # Close popup and refresh UI
            self.part3_popup.close()
            self.load_citizen_data()

        except Exception as e:
            connection.rollback()
            QMessageBox.critical(self.part3_popup, "Database Error", f"Failed to register citizen: {e}")
        finally:
            cursor.close()
            connection.close()

    def handle_remove_citizen(self):
        if not getattr(self, 'selected_citizen_id', None):
            QMessageBox.warning(self.cp_profile_screen, "No Selection", "Please select a citizen to remove.")
            return

        citizen_id = self.selected_citizen_id

        citizen_id = self.selected_citizen_id

        confirm = QMessageBox.question(
            self.cp_profile_screen,
            "Confirm Deletion",
            f"Are you sure you want to delete citizen with ID {citizen_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("""
                UPDATE citizen
                SET ctz_is_deleted = TRUE
                WHERE ctz_id = %s;
            """, (citizen_id,))
            db.conn.commit()
            QMessageBox.information(self.cp_profile_screen, "Success", f"Citizen {citizen_id} has been deleted.")
            self.load_citizen_data()  # Refresh table
            delattr(self, 'selected_citizen_id')  # Clear selection
        except Exception as e:
            db.conn.rollback()
            QMessageBox.critical(self.cp_profile_screen, "Database Error", f"Failed to delete citizen: {str(e)}")
        finally:
            db.close()

    def load_citizen_data_for_update(self):


        if not self.selected_citizen_id:
            QMessageBox.warning(self.part1_popup_update, "No Selection", "No citizen selected for update.")
            return
        print(self.selected_citizen_id)

        try:
            db = Database()
            cursor = db.get_cursor()

            # === PART 1 DATA ===
            query_part1 = """
                SELECT 
                    c.ctz_first_name, c.ctz_middle_name, c.ctz_last_name, c.ctz_suffix,
                    c.ctz_date_of_birth, c.ctz_sex, c.ctz_civil_status, c.ctz_place_of_birth,
                    c.ctz_blood_type, 
                    co.con_email, co.con_phone,
                    s.sitio_name,
                    c.ctz_is_registered_voter, c.ctz_is_alive, c.ctz_reason_of_death,
                    c.ctz_date_of_death,
                    r.rel_name
                FROM citizen c
                LEFT JOIN contact co ON c.con_id = co.con_id
                LEFT JOIN sitio s ON c.sitio_id = s.sitio_id
                LEFT JOIN religion r ON c.rel_id = r.rel_id
                WHERE c.ctz_id = %s;
            """
            cursor.execute(query_part1, (self.selected_citizen_id,))
            result = cursor.fetchone()
            print("testeweqwqewewq", result)

            if result:
                print("Fetched citizen data:", result)

                # Populate Part 1 Fields
                self.part1_popup_update.register_citizen_firstname.setText(result[0])
                self.part1_popup_update.register_citizen_middlename.setText(result[1] or "")
                self.part1_popup_update.register_citizen_lastname.setText(result[2])
                self.part1_popup_update.register_citizen_suffix.setText(result[3] or "")

                # DOB
                from PySide6.QtCore import QDate
                if result[4]:  # Only if the date exists
                    dob = QDate(result[4].year, result[4].month, result[4].day)
                    if dob.isValid():
                        self.part1_popup_update.register_citizen_date_dob.setDate(dob)
                    else:
                        QMessageBox.critical(self.part1_popup_update, "Date Error",
                                             f"Invalid date of birth: {result[4]}")
                else:
                    # Optionally reset the date edit field or skip
                    self.part1_popup_update.register_citizen_date_dob.setDate(QDate.currentDate())  # or setDateToNull()

                # Sex
                if result[5] == 'M':
                    self.part1_popup_update.radioButton_male.setChecked(True)
                else:
                    self.part1_popup_update.radioButton_female.setChecked(True)

                # Civil Status
                index = self.part1_popup_update.register_citizen_comboBox_CivilStatus.findText(result[6])
                if index >= 0:
                    self.part1_popup_update.register_citizen_comboBox_CivilStatus.setCurrentIndex(index)

                # Place of Birth
                self.part1_popup_update.register_citizen_Pob.setText(result[7] or "")

                # Blood Type
                self.part1_popup_update.register_citizen_comboBox_BloodType.setCurrentText(result[8] or "")

                # Email & Contact
                self.part1_popup_update.register_citizen_Email.setText(result[9] or "")
                self.part1_popup_update.register_citizen_ContactNumber.setText(result[10] or "")

                # Sitio
                self.part1_popup_update.register_citizen_comboBox_Sitio.setCurrentText(result[11])

                # Religion
                self.part1_popup_update.register_citizen_comboBox_Religion.setCurrentText(result[16])

                # # Voter
                # self.part3_popup_update.register_citizen_RegVote_Yes.setChecked(result[12])
                # self.part3_popup_update.register_citizen_RegVote_No.setChecked(not result[12])
                #
                # # # Deceased
                # # is_deceased = 1 if result[13] is not None else 0
                # # self.part3_popup_update.register_citizen_Deceased_Yes.setChecked(is_deceased == 1)
                # # self.part3_popup_update.register_citizen_Deceased_No.setChecked(is_deceased != 1)
                # #
                # # # Reason of death
                # # self.part3_popup_update.register_citizen_ReasonOfDeath.setPlainText(result[14] or "")
                #
                # # Voter
                # self.part3_popup_update.register_citizen_Deceased_Yes.setChecked(Treu)
                # self.part3_popup_update.register_citizen_Deceased_No.setChecked(not result[13])
                # print(result[13])
                #
                #
                # from PySide6.QtCore import QDate
                # # For Date of Death
                # if result[15]:  # ctz_date_of_death
                #     dod = QDate(result[15].year, result[15].month, result[15].day)
                #     if dod.isValid():
                #         self.part3_popup_update.register_citizen_death_date.setDate(dod)
                #     else:
                #         QMessageBox.critical(self.part3_popup_update, "Date Error",
                #                              f"Invalid date of death: {result[15]}")
                # else:
                #     self.part3_popup_update.register_citizen_death_date.clear()  # or set to default
                # Date of Death
                # if result[15]:
                #     dod = QDate.fromString(result[15], "yyyy-MM-dd")
                #     self.part3_popup_update.register_citizen_death_date.setDate(dod)

            # === PART 2 DATA ===
            query_part2 = """
                SELECT 
                    ses.soec_status,
                    ses.soec_number,
                    hh.hh_id,
                    rth.rth_relationship_name,
                    es.es_status_name,
                    emp.emp_occupation,
                    emp.emp_is_gov_worker,
                    phc.pc_category_name,
                    ph.phea_membership_type,
                    ph.phea_id_number
                FROM citizen c
                LEFT JOIN socio_economic_status ses ON c.soec_id = ses.soec_id
                LEFT JOIN household_info hh ON c.hh_id = hh.hh_id
                LEFT JOIN relationship_type rth ON c.rth_id = rth.rth_id
                LEFT JOIN employment emp ON c.ctz_id = emp.ctz_id
                LEFT JOIN employment_status es ON emp.es_id = es.es_id
                LEFT JOIN philhealth ph ON c.phea_id = ph.phea_id
                LEFT JOIN philhealth_category phc ON ph.pc_id = phc.pc_id
                WHERE c.ctz_id = %s;
            """
            cursor.execute(query_part2, (self.selected_citizen_id,))
            result_part2 = cursor.fetchone()

            if result_part2:
                print("Fetched Part 2 citizen data:", result_part2)

                # Socioeconomic Status
                sosocioeco_status = result_part2[0]
                index_se = self.part2_popup_update.register_citizen_comboBox_SocEcoStat.findText(
                    sosocioeco_status or "")
                if index_se >= 0:
                    self.part2_popup_update.register_citizen_comboBox_SocEcoStat.setCurrentIndex(index_se)

                # NHTS Number
                nhts_number = result_part2[1] or ""
                self.part2_popup_update.register_citizen_NHTSNum.setText(nhts_number)

                # Household ID
                household_id = result_part2[2]
                self.part2_popup_update.register_citizen_HouseholdID.setText(str(household_id) if household_id else "")

                # Relationship
                print('yawa', result_part2[3])
                # Now set the index safely
                relationship_name = result_part2[3]  # This should be the string like "Head"
                combo = self.part2_popup_update.register_citizen_comboBox_Relationship
                index = combo.findText(relationship_name or "", Qt.MatchFixedString)

                if index >= 0:
                    combo.setCurrentIndex(index)
                else:
                    print(f"[Debug] Relationship '{relationship_name}' not found in ComboBox items.")

                # Employment Status
                employment_status = result_part2[4]
                index_emp = self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.findText(
                    employment_status or "")
                if index_emp >= 0:
                    self.part2_popup_update.register_citizen_comboBox_EmploymentStatus.setCurrentIndex(index_emp)

                # Occupation
                occupation = result_part2[5] or ""
                self.part2_popup_update.register_citizen_Occupation.setText(occupation)

                # Government Worker (Yes/No)
                gov_worker = result_part2[6]
                if gov_worker is True:
                    self.part2_popup_update.radioButton_IsGov_Yes.setChecked(True)
                elif gov_worker is False:
                    self.part2_popup_update.radioButton_IsGov_No.setChecked(True)

                # Philhealth Category
                phil_category = result_part2[7] or ""
                self.part2_popup_update.register_citizen_comboBox_PhilCat.setCurrentText(phil_category)

                # Membership Type
                membership_type = result_part2[8] or ""
                self.part2_popup_update.register_citizen_comboBox_PhilMemType.setCurrentText(membership_type)

                phil_id = result_part2[9] if result_part2[9] not in (None, "None") else ""
                self.part2_popup_update.register_citizen_PhilID.setText(phil_id)

            # === PART 3 DATA ===
            query_part3 = """
                SELECT 
                    edu.edu_is_currently_student,
                    edu.edu_institution_name,
                    ea.edat_level,
                    fpm.fpm_method,
                    fps.fpms_status_name,
                    fp.fp_start_date,
                    fp.fp_end_date,
                    clah.clah_classification_name,
                    c.ctz_is_ip,
                    c.ctz_reason_of_death,
                    c.ctz_date_of_death,
                    c.ctz_is_registered_voter, c.ctz_is_alive
                FROM citizen c
                LEFT JOIN education_status edu ON c.edu_id = edu.edu_id
                LEFT JOIN educational_attainment ea ON edu.edat_id = ea.edat_id
                LEFT JOIN family_planning fp ON c.ctz_id = fp.ctz_id
                LEFT JOIN family_planning_method fpm ON fpm.fpm_id = fp.fpm_method
                LEFT JOIN fpm_status fps ON fp.fpms_status = fps.fpms_id
                LEFT JOIN classification_health_risk clah ON c.clah_id = clah.clah_id
                WHERE c.ctz_id = %s;
            """

            cursor.execute(query_part3, (self.selected_citizen_id,))
            result_part3 = cursor.fetchone()

            if result_part3:
                print("Fetched Part 3 citizen data:", result_part3)

                # Student (Yes/No)
                is_student = result_part3[0]
                if is_student is not None:
                    self.part3_popup_update.radioButton_IsStudent_Yes.setChecked(is_student)
                    self.part3_popup_update.radioButton_IsStudent_No.setChecked(not is_student)

                # School Name
                school_name = result_part3[1] or ""
                self.part3_popup_update.register_citizen_SchoolName.setText(school_name)

                # Educational Level
                educ_level = result_part3[2] or ""
                index_edu = self.part3_popup_update.register_citizen_comboBox_EducationalLevel.findText(educ_level)
                if index_edu >= 0:
                    self.part3_popup_update.register_citizen_comboBox_EducationalLevel.setCurrentIndex(index_edu)

                # # Health Classification
                # health_class = result_part3[7] or ""
                # index_health = self.part3_popup_update.register_citizen_health_classification.findText(health_class)
                # if index_health >= 0:
                #     self.part3_popup_update.register_citizen_health_classification.setCurrentIndex(index_health)
                #
                # print("Available FP Methods:", [
                #     self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.itemText(i)
                #     for i in range(self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.count())
                # ])
                #
                # print("Available FP Statuses:", [
                #     self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.itemText(i)
                #     for i in range(self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.count())
                # ])

                try:
                    db = Database()
                    cursor = db.get_cursor()
                    cursor.execute("SELECT fpm_id, fpm_method FROM family_planning_method ORDER BY fpm_method ASC;")
                    results = cursor.fetchall()

                    combo = self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod
                    for fpm_id, fpm_method in results:
                        combo.addItem(fpm_method, fpm_id)

                except Exception as e:
                    print(f"Failed to load fpm meyhofd: {e}")
                finally:
                    db.close()

                try:
                    db = Database()
                    cursor = db.get_cursor()
                    cursor.execute("SELECT fpms_id, fpms_status_name FROM fpm_status ORDER BY fpms_status_name ASC;")
                    results = cursor.fetchall()

                    combo = self.part3_popup_update.register_citizen_comboBox_FamPlanStatus
                    for fpms_id, fpms_status_name in results:
                        combo.addItem(fpms_status_name, fpms_id)

                except Exception as e:
                    print(f"Failed to load fpm status: {e}")
                finally:
                    db.close()
                # Family Planning Method
                fam_plan_method = result_part3[3] or "-- None --"
                index_fam_method = self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.findText(
                    fam_plan_method)
                if index_fam_method >= 0:
                    self.part3_popup_update.register_citizen_comboBox_FamilyPlanningMethod.setCurrentIndex(
                        index_fam_method)
                else:
                    # Optional fallback or warning
                    print(f"[DEBUG] FP Method '{fam_plan_method}' not found in combo box")

                # Family Planning Status
                fam_plan_status = result_part3[4] or "-- None --"
                index_fam_stat = self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.findText(
                    fam_plan_status)
                if index_fam_stat >= 0:
                    self.part3_popup_update.register_citizen_comboBox_FamPlanStatus.setCurrentIndex(index_fam_stat)
                else:
                    print(f"[DEBUG] FP Status '{fam_plan_status}' not found in combo box")

                from PySide6.QtCore import QDate
                # FP Start Date
                if result_part3[5]:
                    sd = QDate(result_part3[5].year, result_part3[5].month, result_part3[5].day)
                    if sd.isValid():
                        self.part3_popup_update.register_citizen_start_date.setDate(sd)
                    else:
                        QMessageBox.critical(self.part3_popup_update, "Date Error",
                                             f"Invalid start date: {result_part3[5]}")
                else:
                    self.part3_popup_update.register_citizen_start_date.clear()

                # FP End Date
                if result_part3[6]:
                    ed = QDate(result_part3[6].year, result_part3[6].month, result_part3[6].day)
                    if ed.isValid():
                        self.part3_popup_update.register_citizen_end_date.setDate(ed)
                    else:
                        QMessageBox.critical(self.part3_popup_update, "Date Error",
                                             f"Invalid end date: {result_part3[6]}")
                else:
                    self.part3_popup_update.register_citizen_end_date.clear()

                # if result_part3[5]:
                #     start_date = QDate.fromString(result_part3[5], "yyyy-MM-dd")
                #     self.part3_popup_update.register_citizen_start_date.setDate(start_date)

                # FP End Date
                # from PySide6.QtCore import QDate
                #
                # ed = QDate(result[6].year, result[6].month, result[6].day)
                # if not ed.isValid():
                #     QMessageBox.critical(self.part3_popup_update, "Date Error", f"Invalid date format: {result[4]}")
                # else:
                #     self.part3_popup_update.register_citizen_end_date.setDate(ed)

                # if result_part3[6]:
                #     end_date = QDate.fromString(result_part3[6], "yyyy-MM-dd")
                #     self.part3_popup_update.register_citizen_end_date.setDate(end_date)

                # Health Classification
                health_class = result_part3[7] or ""
                index_health = self.part3_popup_update.register_citizen_health_classification.findText(health_class)
                if index_health >= 0:
                    self.part3_popup_update.register_citizen_health_classification.setCurrentIndex(index_health)

                # Indigenous Group
                is_indigenous = result_part3[8]
                if is_indigenous is not None:
                    self.part3_popup_update.register_citizen_IndGroup_Yes.setChecked(is_indigenous)
                    self.part3_popup_update.register_citizen_IndGroup_No.setChecked(not is_indigenous)

                print("is indig", is_indigenous)

                # Reason of Death
                reason_of_death = result_part3[9] or ""
                self.part3_popup_update.register_citizen_ReasonOfDeath.setPlainText(reason_of_death)

                # Date of Death
                # if result_part3[10]:
                #     dod = QDate.fromString(result_part3[10], "yyyy-MM-dd")
                #     self.part3_popup_update.register_citizen_death_date.setDate(dod)

                # FP End Date
                if result_part3[10]:
                    ed = QDate(result_part3[10].year, result_part3[10].month, result_part3[10].day)
                    if ed.isValid():
                        self.part3_popup_update.register_citizen_death_date.setDate(ed)
                    else:
                        QMessageBox.critical(self.part3_popup_update, "Date Error",
                                             f"Invalid end date: {result_part3[10]}")
                else:
                    self.part3_popup_update.register_citizen_death_date.clear()

                is_voter = result_part3[11]
                if is_voter is not None:
                    self.part3_popup_update.register_citizen_RegVote_Yes.setChecked(is_voter)
                    self.part3_popup_update.register_citizen_RegVote_No.setChecked(not is_voter)

                is_alive = result_part3[12]
                if is_alive is not None:
                    self.part3_popup_update.register_citizen_Deceased_Yes.setChecked(not is_alive)
                    self.part3_popup_update.register_citizen_Deceased_No.setChecked(is_alive)





        except Exception as e:
            print("Error loading citizen data:", e)
            QMessageBox.critical(self.part1_popup_update, "Database Error", f"Failed to load citizen data: {e}")
        finally:
            db.close()

    def goto_citizen_panel(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.UserController.CitizenPanelController import CitizenPanelController
            self.citizen_panel = CitizenPanelController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                        self.user_role, self.stack)
            self.stack.addWidget(self.citizen_panel.citizen_panel_screen)

        self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)

        # self.stack.setCurrentWidget(self.citizen_panel.citizen_panel_screen)
        self.setWindowTitle("MaPro: Citizen Panel")