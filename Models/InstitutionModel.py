import os
import shutil
from database import Database


class InstitutionsModel:
    def __init__(self):
        self.image_path = None

    def save_household_data(self, household_data):
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
                    WATER_ID,
                    TOILET_ID,
                    SITIO_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                household_data['house_number'],
                household_data['home_address'],
                household_data['ownership_status'],
                household_data['home_google_link'],
                household_data['home_image_path'],
                household_data['interviewer_name'],
                household_data['reviewer_name'],
                household_data['date_of_visit'],
                household_data['water_id'],
                household_data['toilet_id'],
                household_data['sitio_id']
            ))
            connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

    def save_image(self, file_path, target_folder="Assets/Register/HouseholdImages"):
        if not file_path:
            return None

        os.makedirs(target_folder, exist_ok=True)
        image_filename = os.path.basename(file_path)
        target_path = os.path.join(target_folder, image_filename)
        shutil.copy(file_path, target_path)
        self.image_path = target_path
        return target_path