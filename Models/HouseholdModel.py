import os
import shutil
from database import Database


class HouseholdModel:
    def __init__(self, sys_user_id):
        pass

    def save_household_data(self, household_data, sys_user_id):
        db = Database()
        connection = db.conn
        cursor = connection.cursor()


        cursor.execute("SELECT sitio_id FROM sitio WHERE sitio_name = %s", (household_data['sitio_id'],))
        sitio_result = cursor.fetchone()
        if not sitio_result:
            raise Exception(f"Sitio '{household_data['sitio_id']}' not found in database.")
        sitio_id = sitio_result[0]


        cursor.execute("SELECT toil_id FROM toilet_type WHERE toil_type_name = %s", (household_data['toilet_id'],))
        toilet_type_result = cursor.fetchone()
        if not toilet_type_result:
            raise Exception(f"Sitio '{household_data['toilet_id']}' not found in database.")
        toil_id = toilet_type_result[0]

        cursor.execute("SELECT water_id FROM water_source WHERE water_source_name = %s", (household_data['water_id'],))
        water_source_result = cursor.fetchone()
        if not water_source_result:
            raise Exception(f"Sitio '{household_data['water_id']}' not found in database.")
        water_id = water_source_result[0]



        try:
            connection = Database()
            cursor = connection.cursor

            query = """
                INSERT INTO HOUSEHOLD_INFO (
                    HH_HOUSE_NUMBER,
                    HH_ADDRESS,
                    HH_OWNERSHIP_STATUS,
                    HH_HOME_GOOGLE_LINK,
                    HH_HOME_IMAGE_PATH,
                    HH_INTERVIEWER_NAME,
                    HH_REVIEWER_NAME,
                    HH_DATE_VISIT,
                    encoded_by_sys_id,
                    last_updated_by_sys_id,
                    hh_date_encoded,
                    WATER_ID,
                    TOILET_ID,
                    SITIO_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
            """
            # HH_HOUSE_NUMBER,
            # HH_ADDRESS,
            # HH_OWNERSHIP_STATUS,
            # HH_HOME_IMAGE_PATH,
            # HH_HOME_GOOGLE_LINK,
            # HH_INTERVIEWER_NAME,
            # HH_REVIEWER_NAME,
            # HH_DATE_VISIT,
            # SYS_ID,
            # WATER_ID,
            # TOILET_ID,
            # SITIO_ID
            cursor.execute(query, (
                household_data['house_number'],
                household_data['home_address'],
                household_data['ownership_status'],
                household_data['home_google_link'],
                household_data['home_image_path'],
                household_data['interviewer_name'],
                household_data['reviewer_name'],
                household_data['date_of_visit'],
                sys_user_id,
                sys_user_id,
                water_id,
                toil_id,
                sitio_id
            ))
            connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

