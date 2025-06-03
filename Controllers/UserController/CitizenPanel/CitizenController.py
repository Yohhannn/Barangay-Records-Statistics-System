from datetime import date

import cv2
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
    def __init__(self, login_window, emp_first_name, stack):
        super().__init__(login_window, emp_first_name)

        # INITIALIZE OBJECTS NEEDED
        self.stack = stack
        self.model = CitizenModel()
        self.view = CitizenView(self)


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


    def get_form_data(self):
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
            'full_address': self.part1_popup.register_citizen_FullAddress.toPlainText(),

            # APRT 2
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
    from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

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

    -- ENCODED BY
    CASE 
        WHEN SA.SYS_FNAME IS NULL THEN 'System'
        ELSE SA.SYS_FNAME || ' ' ||
             COALESCE(LEFT(SA.SYS_MNAME, 1) || '. ', '') ||
             SA.SYS_LNAME
    END AS ENCODED_BY, --34

    TO_CHAR(C.CTZ_LAST_UPDATED, 'FMMonth FMDD, YYYY | FMHH:MI AM') AS DATE_UPDATED_FORMATTED, --35

    -- LAST UPDATED BY (moved to 36)
    CASE 
        WHEN SUA.SYS_FNAME IS NULL THEN 'System'
        ELSE SUA.SYS_FNAME || ' ' ||
             COALESCE(LEFT(SUA.SYS_MNAME, 1) || '. ', '') ||
             SUA.SYS_LNAME
    END AS LAST_UPDATED_BY_NAME --36

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

-- Join for ENCODED_BY
LEFT JOIN SYSTEM_ACCOUNT SA ON C.ENCODED_BY_SYS_ID = SA.SYS_ID

-- Join for LAST_UPDATED_BY
LEFT JOIN SYSTEM_ACCOUNT SUA ON C.LAST_UPDATED_BY_SYS_ID = SUA.SYS_ID

WHERE C.CTZ_IS_DELETED = FALSE
ORDER BY C.CTZ_ID, COALESCE(C.CTZ_LAST_UPDATED, C.CTZ_DATE_ENCODED) DESC
LIMIT 20;


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

    def handle_row_click_citizen(self, row, column):
        table = self.cp_profile_screen.cp_tableView_List_RegCitizens
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()

        for record in self.rows:
            if str(record[0]) == selected_id:
                self.cp_profile_screen.cp_displayCItizenID.setText(str(record[0]))
                self.cp_profile_screen.cp_displayLastName.setText(record[1])
                self.cp_profile_screen.cp_displayFirstName.setText(record[2])
                self.cp_profile_screen.cp_displayMiddleName.setText(record[3] or "N/A")
                self.cp_profile_screen.cp_displaySuffix.setText(record[4] or "N/A")
                self.cp_profile_screen.cp_displaySitio.setText(record[5])
                self.cp_profile_screen.display_DateUpdated.setText(record[6])

                dob = record[7]
                if dob:
                    try:
                        # self.cp_profile_screen.cp_displayDOB.setText(dob.strftime('%B %d, %Y'))
                        today = date.today()
                        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                        self.cp_profile_screen.cp_displayAge.setText(dob.strftime('%B %d, %Y | ') + str(age) + " years old")
                    except Exception:
                        # self.cp_profile_screen.cp_displayDOB.setText(str(dob))
                        self.cp_profile_screen.cp_displayAge.setText("")
                else:
                    # self.cp_profile_screen.cp_displayDOB.setText("")
                    self.cp_profile_screen.cp_displayAge.setText("")

                # self.cp_profile_screen.cp_displaySex.setText("Male | " + record[9] if record[8] == 'M' else "Female | " + record[9])
                self.cp_profile_screen.cp_displayCivilStatus.setText("Male | " + record[9] if record[8] == 'M' else "Female | " + record[9])
                self.cp_profile_screen.cp_displayEmail.setText(record[10] or "N/A")
                self.cp_profile_screen.cp_displayContactNum.setText(record[11] or "N/A")
                self.cp_profile_screen.cp_displayPlaceOfBirth.setText(record[12] or "N/A")
                self.cp_profile_screen.cp_displayFullAddress.setText(record[13] or "N/A")
                self.cp_profile_screen.cp_displaySocioEcoStatus.setText(record[14] or "N/A")
                self.cp_profile_screen.cp_displayNHTSNum.setText(record[15] or "N/A")
                self.cp_profile_screen.cp_displayEmploymentStatus.setText(record[16] or "N/A")
                self.cp_profile_screen.cp_displayOccupation.setText(record[17] or "N/A")
                self.cp_profile_screen.cp_displayGovWorker.setText("Yes" if record[18] == True else "No")
                self.cp_profile_screen.cp_displayHouseholdID.setText(str(record[19]) if record[19] else "")
                self.cp_profile_screen.cp_displayRelationship.setText(record[20] or "N/A")
                self.cp_profile_screen.cp_displayPhilCat.setText(record[21] or "N/A")
                self.cp_profile_screen.cp_displayPhilID.setText(record[32] or "N/A")
                self.cp_profile_screen.cp_displayMembershipType.setText(record[22] or "N/A")
                self.cp_profile_screen.cp_displayPhilMem.setText("Yes" if record[23] else "No")
                self.cp_profile_screen.cp_displayReligion.setText(record[23] or "N/A")
                self.cp_profile_screen.cp_displayBloodType.setText(record[24] or "N/A")
                self.cp_profile_screen.cp_displayStudent.setText("Yes" if record[25] == True else "No")
                self.cp_profile_screen.cp_displaySchoolName.setText(record[26] or "N/A")
                self.cp_profile_screen.cp_displayEducationalAttainment.setText(record[27] or "N/A")
                self.cp_profile_screen.cp_displayPWD.setText("No | None" if record[28] == "None" else "Yes" + " | " + record[28]  )
                self.cp_profile_screen.cp_displayRegisteredVoter.setText("Yes" if record[29] == True else "No")
                self.cp_profile_screen.cp_displayDeceased.setText("Yes" if record[30] == True else "No")
                self.cp_profile_screen.cp_displayPartOfIndigenousGroup.setText("Yes" if record[31] == True else "No")
                self.cp_profile_screen.display_DateEncoded.setText(record[33] or "N/A")
                self.cp_profile_screen.display_EncodedBy.setText(record[34] or "N/A")
                self.cp_profile_screen.display_DateUpdated.setText(record[35] or "N/A")
                self.cp_profile_screen.display_UpdatedBy.setText(record[36] or "N/A")
                print(record[31])
                print(record[34])
                break

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
        form_data_part_1 = self.get_form_data()
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
        form_data_part_2 = self.get_form_data()
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