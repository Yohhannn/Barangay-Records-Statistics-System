from database import Database

class AdminControlsModel:
    def __init__(self, sys_user_id=None):
        self.connection = Database()
        if sys_user_id is not None:
            self.connection.set_user_id(sys_user_id)

    def save_new_sitio_data(self, account_data):
        try:
            query = """
                INSERT INTO SITIO (
                    SITIO_NAME
                ) VALUES (%s)
            """
            self.connection.execute_with_user(query, (
                account_data['sitio_name'],
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

    def get_sitio_names(self):
        try:
            query = """
                SELECT
                    SITIO_ID,
                    SITIO_NAME
                FROM SITIO
                ORDER BY SITIO_NAME
            """
            self.connection.cursor.execute(query)
            rows = self.connection.cursor.fetchall()

            return {
                'columns': ['Sitio ID', 'Sitio Name'],
                'data': rows
            }

        except Exception as e:
            print(f"Failed to fetch system users: {e}")
            return {'columns': [], 'data': []}