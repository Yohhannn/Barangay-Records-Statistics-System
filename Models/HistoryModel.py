import os
import shutil
from database import Database

class HistoryModel:
    def __init__(self):
        self.image_path = None


    def save_citizen_data(self, citizen_data):
        pass

    def save_image(self, file_path, target_folder="Assets/Register/CitizenProfileImages"):
        if not file_path:
            return None

        os.makedirs(target_folder, exist_ok=True)
        image_filename = os.path.basename(file_path)
        target_path = os.path.join(target_folder, image_filename)
        shutil.copy(file_path, target_path)
        self.image_path = target_path
        return target_path