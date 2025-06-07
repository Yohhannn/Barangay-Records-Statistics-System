from PySide6.QtGui import QPixmap, QIcon, Qt
from Utils.util_popup import load_popup
from PySide6.QtWidgets import QMessageBox

from Utils.util_widget import load_ui_widget
from database import Database


class CitizenView:
    def __init__(self, controller):
        self.controller = controller
      #  self.popup = None
        self.part1_popup = None
        self.part2_popup = None
        self.part3_popup = None
      #   self.setWindowModality(Qt.ApplicationModal)
      #   self.setFixedSize(750, 600)  # Adjust as needed
      #  self.profile_screen = None
        self.cp_profile_screen = None




    def show_error_message(self, errors):
        QMessageBox.warning(self.part1_popup, "Incomplete Form",
                            "Please complete all required fields:\n\n• " + "\n• ".join(errors))




        # return self.part1_popup
    def show_register_citizen_part_01_popup(self, parent):
        self.part1_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_01.ui", parent)
        # self.stack.addWidget(self.part1_popup)
        self.part1_popup.setWindowTitle("Register New Citizen")
        self.part1_popup.setWindowModality(Qt.ApplicationModal)
        self.part1_popup.setFixedSize(self.part1_popup.size())
        self.part1_popup.register_buttonPrev.setIcon(QIcon('Resources/Icons/FuncIcons/icon_arrow_prev'))
        self.part1_popup.register_buttonConfirmPart1_NextToPart2.setIcon(QIcon('Resources/Icons/FuncIcons/icon_arrow_next'))
        self.part1_popup.register_buttonConfirmPart1_NextToPart2.clicked.connect(self.controller.validate_part1_fields)

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT rel_id, rel_name FROM religion ORDER BY rel_name ASC;")
            results = cursor.fetchall()

            combo = self.part1_popup.register_citizen_comboBox_Religion
            combo.clear()
            for rel_id, rel_name in results:
                combo.addItem(rel_name, rel_id)

        except Exception as e:
            print(f"Failed to load religion : {e}")
        finally:
            db.close()
        # self.setup_image_handlers(self.part1_popup)
        # if hasattr(self, 'citizen_data'):
        #     self.restore_part1_data()
        # self.part1_popup.exec_()

        return self.part1_popup

    def show_register_citizen_part_02_popup(self, parent):
        # part_one_popup.close()
        self.part2_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_02.ui", parent)
        self.part2_popup.setWindowTitle("Register New Citizen - Part 2")
        self.part2_popup.setWindowModality(Qt.ApplicationModal)
        self.part2_popup.setFixedSize(self.part2_popup.size())
        self.part2_popup.register_buttonReturnToPart1_FromPart2.setIcon(QIcon('Resources/Icons/FuncIcons/icon_arrow_prev'))
        self.part2_popup.register_buttonConfirmPart2_NextToPart3.setIcon(QIcon('Resources/Icons/FuncIcons/icon_arrow_next'))
        self.part2_popup.register_buttonConfirmPart2_NextToPart3.clicked.connect(self.controller.validate_part2_fields)
        self.part2_popup.register_buttonReturnToPart1_FromPart2.clicked.connect(self.controller.return_to_part1_from_part2)
        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT es_id, es_status_name FROM employment_status ORDER BY es_status_name ASC;")
            results = cursor.fetchall()

            combo = self.part2_popup.register_citizen_comboBox_EmploymentStatus
            combo.clear()
            for es_id, es_status_name in results:
                combo.addItem(es_status_name, es_id)

        except Exception as e:
            print(f"Failed to load employment status: {e}")
        finally:
            db.close()


        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT pc_id, pc_category_name FROM philhealth_category ORDER BY pc_category_name ASC;")
            results = cursor.fetchall()

            combo = self.part2_popup.register_citizen_comboBox_PhilCat
            combo.clear()
            for pc_id, pc_category_name in results:
                combo.addItem(pc_category_name, pc_id)

        except Exception as e:
            print(f"Failed to load philhealth categopry name: {e}")
        finally:
            db.close()
        # self.part2_popup.exec_()

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT pc_id, pc_category_name FROM philhealth_category ORDER BY pc_category_name ASC;")
            results = cursor.fetchall()

            combo = self.part2_popup.register_citizen_comboBox_PhilCat
            combo.clear()
            for pc_id, pc_category_name in results:
                combo.addItem(pc_category_name, pc_id)

        except Exception as e:
            print(f"Failed to load philhealth categopry name: {e}")
        finally:
            db.close()

        return self.part2_popup
 #return_to_part1_from_part2
    def show_register_citizen_part_03_popup(self, parent):
        # part_two_popup.close()
        self.part3_popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenCitizenProfile/register_citizen_part_03.ui", parent)
        self.part3_popup.setWindowTitle("Register New Citizen - Part 3")
        self.part3_popup.setWindowModality(Qt.ApplicationModal)
        self.part3_popup.setFixedSize(self.part3_popup.size())
        self.part3_popup.register_buttonReturnToPart2_FromPart3.setIcon(QIcon('Resources/Icons/FuncIcons/icon_arrow_prev'))
        self.part3_popup.register_buttonConfirmPart3_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm'))
        self.part3_popup.register_buttonConfirmPart3_SaveForm.clicked.connect(self.controller.validate_part3_fields)
        self.part3_popup.register_buttonReturnToPart2_FromPart3.clicked.connect(self.controller.return_to_part2_from_part3)

        # if hasattr(self, 'citizen_data'):
        #     self.restore_part3_data()
        # self.setup_radio_button_groups_03()
        # save_btn = self.part3_popup.findChild(QPushButton, "register_buttonConfirmPart3_SaveForm")
        # if save_btn:
        #     save_btn.clicked.connect(self.confirm_and_save)
        # back_btn = self.part3_popup.findChild(QPushButton, "register_buttonReturnToPart2_FromPart3")
        # if back_btn:
        #     back_btn.clicked.connect(self.return_to_part2_from_part3)
        # self.part3_popup.exec_()

        try:
            db = Database()
            cursor = db.get_cursor()
            cursor.execute("SELECT edat_id, edat_level FROM EDUCATIONAL_ATTAINMENT ORDER BY edat_level ASC;")
            results = cursor.fetchall()

            combo = self.part3_popup.register_citizen_comboBox_EducationalLevel
            combo.clear()
            for edat_id, educational_attainment in results:
                combo.addItem(educational_attainment, edat_id)

        except Exception as e:
            print(f"Failed to load educ atainment: {e}")
        finally:
            db.close()


        return self.part3_popup

    def setup_profile_ui(self, ui_screen):
        self.cp_profile_screen = ui_screen
        ui_screen.setFixedSize(1350, 850)
        ui_screen.setWindowTitle("MaPro: Citizen Profile")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))
        ui_screen.btn_returnToCitizenPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        ui_screen.cp_CitizenName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        ui_screen.cp_citizen_button_register.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        ui_screen.cp_citizen_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        ui_screen.cp_citizen_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        ui_screen.profileList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))
        ui_screen.btn_returnToCitizenPanelPage.clicked.connect(self.controller.goto_citizen_panel)
        ui_screen.cp_citizen_button_register.clicked.connect(self.controller.show_register_citizen_part_01_initialize)
        ui_screen.cp_tableView_List_RegCitizens.cellClicked.connect(self.controller.handle_row_click_citizen)
        ui_screen.cp_CitizenName_buttonSearch.clicked.connect(self.controller.perform_citizen_search)

        # PART 2
        #     'reviewer_name': self.part1_popup.register_household_ReviewedBy.text().strip(),
        #     'date_of_visit': self.part1_popup.register_household_date_DOV.date().toString("yyyy-MM-dd"),
        #     'water_id': self.part1_popup.register_household_comboBox_WaterSource.currentData(),
        #     'toilet_id': self.part1_popup.register_household_comboBox_ToiletType.currentData(),
        #     'sitio_id': self.part1_popup.register_household_comboBox_Sitio.currentData()


        # SAVE FOR LATER
   #     self.stack = stack
    #    self.profile_screen = self.load_ui("Resources/UIs/MainPages/citizenpanel.ui")
    #    self.center_on_screen()

    # def setup_citizen_profile_sub_panel_ui(self, ui_screen):
    #     self.cp_citizen_screen = ui_screen
    # #    ui_screen.register_buttonConfirmPart1_NextToPart2.setIcon(QIcon('Resources/FuncIcons/icon_arrow_next'))
