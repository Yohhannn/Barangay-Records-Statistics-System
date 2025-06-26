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
from database import Database


class CitizenBinController(BaseFileController):
    def __init__(self, login_window, emp_first_name, sys_user_id, user_role, stack):
        super().__init__(login_window, emp_first_name, sys_user_id)
        self.selected_citizen_id = None
        self.user_role = user_role

        # INITIALIZE OBJECTS NEEDED

        self.stack = stack
        self.model = CitizenModel()
        self.view = CitizenView(self)
        print(self.sys_user_id)

        self.cp_citizenbin_screen = self.load_ui("Resources/UIs/AdminPages/TrashBin/BinCitizens/bin_cp_citizenprofile.ui")
        self.setup_citizenbin_ui(self.cp_citizenbin_screen)
        self.load_citizen_data()


            # PART 2
            #     'reviewer_name': self.part1_popup.register_household_ReviewedBy.text().strip(),
            #     'date_of_visit': self.part1_popup.register_household_date_DOV.date().toString("yyyy-MM-dd"),
            #     'water_id': self.part1_popup.register_household_comboBox_WaterSource.currentData(),
            #     'toilet_id': self.part1_popup.register_household_comboBox_ToiletType.currentData(),
            #     'sitio_id': self.part1_popup.register_household_comboBox_Sitio.currentData()

            # SAVE FOR LATER

        # self.part1_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_01.ui")
        # self.view.show_register_citizen_part_01_popup(self.part1_popup)

        # self.view.setup_citizen_panel_ui(self.cp_citizenbin_screen)
        self.center_on_screen()

        # Store references needed for navigation
        self.login_window = login_window
        self.emp_first_name = emp_first_name
        # self.stacked_widget = QStackedWidget()

    #
    #
    # POP UP UI INITIALIZATION
    #
    #







    def setup_citizenbin_ui(self, ui_screen):
        self.cp_citizenbin_screen = ui_screen

        ui_screen.setFixedSize(1350, 850)
        ui_screen.setWindowTitle("MaPro: Citizen Profile")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
        # ui_screen.btn_returnToCitizenPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        ui_screen.cp_CitizenName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        ui_screen.cp_citizen_button_restore.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
            # ui_screen.profileList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))
        ui_screen.btn_returnToTrashBinPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        ui_screen.btn_returnToTrashBinPage.clicked.connect(self.goto_trashbin)
        # ui_screen.cp_citizen_button_update.clicked.connect(self.show_update_citizen_part_01_initialize)
        ui_screen.cp_tableView_List_RegCitizens.cellClicked.connect(self.handle_row_click_citizen)
        ui_screen.cp_CitizenName_buttonSearch.clicked.connect(self.perform_citizen_search)

        ui_screen.cp_citizen_button_restore.clicked.connect(self.restore_selected_citizen)
        # ui_screen.cp_citizen_button_remove.clicked.connect(self.handle_remove_citizen)




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
    WHERE C.CTZ_IS_DELETED = TRUE
    ORDER BY C.CTZ_ID DESC
    LIMIT 50;
            """)
            rows = cursor.fetchall()
            self.rows = rows

            table = self.cp_citizenbin_screen.cp_tableView_List_RegCitizens
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
            QMessageBox.critical(self.cp_citizenbin_screen, "Database Error", str(e))
        finally:
            if connection:
                connection.close()


    def handle_row_click_citizen(self, row, column):
        table = self.cp_citizenbin_screen.cp_tableView_List_RegCitizens
        selected_item = table.item(row, 0)
        if not selected_item:
            return

        selected_id = selected_item.text()
        self.selected_citizen_id = selected_id  # Store selected ID here

        for record in self.rows:
            if str(record[0]) == selected_id:
                self.cp_citizenbin_screen.cp_displayCItizenID.setText(str(record[0]))
                self.cp_citizenbin_screen.cp_displayLastName.setText(record[1])
                self.cp_citizenbin_screen.cp_displayFirstName.setText(record[2])
                self.cp_citizenbin_screen.cp_displayMiddleName.setText(record[3] or "None")
                self.cp_citizenbin_screen.cp_displaySuffix.setText(record[4] or "None")
                self.cp_citizenbin_screen.cp_displaySitio.setText(record[5])
                self.cp_citizenbin_screen.display_DateUpdated.setText(record[6])

                dob = record[7]
                if dob:
                    try:
                        today = date.today()
                        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                        self.cp_citizenbin_screen.cp_displayAge.setText(
                            dob.strftime('%B %d, %Y | ') + str(age) + " years old")
                    except Exception:
                        self.cp_citizenbin_screen.cp_displayAge.setText("")
                else:
                    self.cp_citizenbin_screen.cp_displayAge.setText("")

                self.cp_citizenbin_screen.cp_displayCivilStatus.setText(
                    "Male | " + record[9] if record[8] == 'M' else "Female | " + record[9])
                self.cp_citizenbin_screen.cp_displayEmail.setText(record[10] or "None")
                self.cp_citizenbin_screen.cp_displayContactNum.setText(record[11] or "None")
                self.cp_citizenbin_screen.cp_displayPlaceOfBirth.setText(record[12] or "None")
                self.cp_citizenbin_screen.cp_displayFullAddress.setText(record[13] or "None")
                self.cp_citizenbin_screen.cp_displaySocioEcoStatus.setText(record[14] or "None")
                self.cp_citizenbin_screen.cp_displayNHTSNum.setText(record[15] or "None")
                self.cp_citizenbin_screen.cp_displayEmploymentStatus.setText(record[16] or "None")
                self.cp_citizenbin_screen.cp_displayOccupation.setText(record[17] or "None")
                self.cp_citizenbin_screen.cp_displayGovWorker.setText("Yes" if record[18] == True else "No")
                self.cp_citizenbin_screen.cp_displayHouseholdID.setText(str(record[19]) if record[19] else "")
                self.cp_citizenbin_screen.cp_displayRelationship.setText(record[20] or "None")
                self.cp_citizenbin_screen.cp_displayPhilCat.setText(record[21] or "None")
                self.cp_citizenbin_screen.cp_displayPhilID.setText(record[32] or "None")
                self.cp_citizenbin_screen.cp_displayMembershipType.setText(record[22] or "None")
                self.cp_citizenbin_screen.cp_displayReligion.setText(record[23] or "None")
                self.cp_citizenbin_screen.cp_displayBloodType.setText(record[24] or "None")
                self.cp_citizenbin_screen.cp_displayStudent.setText("Yes" if record[25] == True else "No")
                self.cp_citizenbin_screen.cp_displaySchoolName.setText(record[26] or "None")
                self.cp_citizenbin_screen.cp_displayEducationalAttainment.setText(record[27] or "None")
                self.cp_citizenbin_screen.cp_display_health_classification.setText(record[28] or "None")
                self.cp_citizenbin_screen.cp_displayRegisteredVoter.setText("Yes" if record[29] == True else "No")
                self.cp_citizenbin_screen.cp_displayDeceased.setText("Yes" if record[30] == True else "No")
                self.cp_citizenbin_screen.cp_displayPartOfIndigenousGroup.setText("Yesss" if record[31] == True else "No")
                self.cp_citizenbin_screen.display_DateEncoded.setText(record[33] or "None")
                self.cp_citizenbin_screen.display_EncodedBy.setText(record[34] or "None")
                self.cp_citizenbin_screen.display_DateUpdated.setText(record[35] or "None")
                self.cp_citizenbin_screen.display_UpdatedBy.setText(record[36] or "None")
                self.cp_citizenbin_screen.cp_displayReasonOfDeath.setText(record[37] or "None")
                self.cp_citizenbin_screen.cp_displayDoD.setText(record[38] or "None")
                # --- Family Planning Info ---
                # Safely extract family planning fields
                fam_plan_method = str(record[41]) if len(record) > 41 and record[41] is not None else "None"
                fam_plan_status = str(record[42]) if len(record) > 42 and record[42] is not None else "None"
                fam_plan_start = record[39] if len(record) > 39 else None
                fam_plan_end = record[40] if len(record) > 40 else None

                # Set method and status (always strings)
                self.cp_citizenbin_screen.cp_displayFamPlanMethod.setText(fam_plan_method)
                self.cp_citizenbin_screen.cp_displayFamPlanStatus.setText(fam_plan_status)

                # Format dates if valid
                self.cp_citizenbin_screen.display_DateStarted.setText(
                    fam_plan_start.strftime("%B %d, %Y") if isinstance(fam_plan_start, date) else "None"
                )
                self.cp_citizenbin_screen.display_DateEnded.setText(
                    fam_plan_end.strftime("%B %d, %Y") if isinstance(fam_plan_end, date) else "None"
                )
                break

    def restore_selected_citizen(self):
        if not self.selected_citizen_id:
            QMessageBox.warning(self.cp_citizenbin_screen, "No Selection", "Please select a citizen to restore.")
            return

        confirm = QMessageBox.question(
            self.cp_citizenbin_screen,
            "Confirm Restore",
            f"Are you sure you want to restore citizen with ID: {self.selected_citizen_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            connection = None
            try:
                connection = Database()
                cursor = connection.cursor
                # Update CTZ_IS_DELETED to FALSE
                cursor.execute("SET LOCAL app.current_user_id TO %s", (str(self.sys_user_id),))
                cursor.execute("""
                    UPDATE CITIZEN
                    SET CTZ_IS_DELETED = FALSE
                    WHERE CTZ_ID = %s
                """, (self.selected_citizen_id,))
                connection.commit()

                QMessageBox.information(self.cp_citizenbin_screen, "Success", "Citizen restored successfully.")

                # Reload the citizen data to reflect changes
                self.load_citizen_data()
                self.clear_display_fields()  # Optional: clear profile display after restore

            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self.cp_citizenbin_screen, "Database Error", str(e))
            finally:
                if connection:
                    connection.close()


    def perform_citizen_search(self):
        search_text = self.cp_citizenbin_screen.cp_CitizenName_fieldSearch.text().strip()

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
            WHERE C.CTZ_IS_DELETED = TRUE
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

            table = self.cp_citizenbin_screen.cp_tableView_List_RegCitizens
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
            QMessageBox.critical(self.cp_citizenbin_screen, "Database Error", str(e))
        finally:
            if db:
                db.close()


    def clear_display_fields(self):
        screen = self.cp_citizenbin_screen
        display_widgets = [
            screen.cp_displayCItizenID,
            screen.cp_displayLastName,
            screen.cp_displayFirstName,
            screen.cp_displayMiddleName,
            screen.cp_displaySuffix,
            screen.cp_displaySitio,
            screen.display_DateUpdated,
            screen.cp_displayAge,
            screen.cp_displayCivilStatus,
            screen.cp_displayEmail,
            screen.cp_displayContactNum,
            screen.cp_displayPlaceOfBirth,
            screen.cp_displayFullAddress,
            screen.cp_displaySocioEcoStatus,
            screen.cp_displayNHTSNum,
            screen.cp_displayEmploymentStatus,
            screen.cp_displayOccupation,
            screen.cp_displayGovWorker,
            screen.cp_displayHouseholdID,
            screen.cp_displayRelationship,
            screen.cp_displayPhilCat,
            screen.cp_displayMembershipType,
            screen.cp_displayReligion,
            screen.cp_displayBloodType,
            screen.cp_displayStudent,
            screen.cp_displaySchoolName,
            screen.cp_displayEducationalAttainment,
            screen.cp_display_health_classification,
            screen.cp_displayRegisteredVoter,
            screen.cp_displayDeceased,
            screen.cp_displayPartOfIndigenousGroup,
            screen.display_DateEncoded,
            screen.display_UpdatedBy,
            screen.display_EncodedBy,
            screen.cp_displayReasonOfDeath,
            screen.cp_displayDoD,
            screen.cp_displayFamPlanMethod,
            screen.cp_displayFamPlanStatus,
            screen.display_DateStarted,
            screen.display_DateEnded,
        ]
        for widget in display_widgets:
            if isinstance(widget, QLabel):
                widget.setText("None")

    def goto_trashbin(self):
        """Handle navigation to Citizen Panel screen."""
        print("-- Navigating to Citizen Panel")
        if not hasattr(self, 'citizen_panel'):
            from Controllers.AdminController.AdminBinController import AdminBinController
            self.adminbin_panel = AdminBinController(self.login_window, self.emp_first_name, self.sys_user_id,
                                                        self.user_role, self.stack)
            self.stack.addWidget(self.adminbin_panel.trashbin_screen)

        self.stack.setCurrentWidget(self.adminbin_panel.trashbin_screen)

        # self.stack.setCurrentWidget(self.adminbin_panel.adminbin_panel_screen)
        self.setWindowTitle("MaPro: Admin Bin Panel")


