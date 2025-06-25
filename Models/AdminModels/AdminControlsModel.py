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

    def update_sitio_name(self, sitio_id, new_name):
        try:
            query = """
                UPDATE SITIO
                SET SITIO_NAME = %s
                WHERE SITIO_ID = %s AND SITIO_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (new_name, sitio_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating sitio name: {e}")
            return False


    def get_sitio_name_by_id(self, sitio_id, raw=False):
        try:
            query = """
                SELECT SITIO_NAME
                FROM SITIO
                WHERE SITIO_ID = %s AND SITIO_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (sitio_id,))
            result = self.connection.cursor.fetchone()
            if not result:
                return None
            return result if raw else result[0]
        except Exception as e:
            print(f"Error fetching sitio name: {e}")
            return None if not raw else []

    def get_sitio_names(self):
        try:
            query = """
                SELECT
                    SITIO_ID,
                    SITIO_NAME
                FROM SITIO
                WHERE SITIO_IS_DELETED = FALSE;
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


    def get_infrastructure_types(self):
        try:
            query = """
                SELECT
                    INFT_ID,
                    INFT_TYPE_NAME
                FROM INFRASTRUCTURE_TYPE
                WHERE INFT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query)
            rows = self.connection.cursor.fetchall()

            return {
                'columns': ['Infrastructure type ID', 'Infrastructure Type Name'],
                'data': rows
            }

        except Exception as e:
            print(f"Failed to fetch system users: {e}")
            return {'columns': [], 'data': []}

    def save_new_infrastructure_type(self, infra_data):
        try:
            query = """
                INSERT INTO INFRASTRUCTURE_TYPE (
                    INFT_TYPE_NAME
                ) VALUES (%s)
            """
            self.connection.execute_with_user(query, (
                infra_data['infra_name'],
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

    def update_infrastructure_type(self, infra_id, new_name):
        try:
            query = """
                UPDATE INFRASTRUCTURE_TYPE
                SET INFT_TYPE_NAME = %s
                WHERE INFT_ID = %s AND INFT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (new_name, infra_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating Infrastructure type name: {e}")
            return False

    def get_infrastructure_type_by_id(self, infra_id, raw=False):
        try:
            query = """
                SELECT INFT_TYPE_NAME
                FROM INFRASTRUCTURE_TYPE
                WHERE INFT_ID = %s AND INFT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (infra_id,))
            result = self.connection.cursor.fetchone()
            if not result:
                return None
            return result if raw else result[0]
        except Exception as e:
            print(f"Error fetching Infrastructure type name: {e}")
            return None if not raw else []

    def get_transaction_types(self):
        try:
            query = """
                SELECT
                    TT_ID,
                    TT_TYPE_NAME
                FROM TRANSACTION_TYPE
                WHERE TT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query)
            rows = self.connection.cursor.fetchall()

            return {
                'columns': ['Transaction type ID', 'Transaction Type Name'],
                'data': rows
            }

        except Exception as e:
            print(f"Failed to fetch system users: {e}")
            return {'columns': [], 'data': []}

    def save_new_transaction_type(self, transaction_data):
        try:
            query = """
                INSERT INTO TRANSACTION_TYPE (
                    TT_TYPE_NAME
                ) VALUES (%s);
            """
            self.connection.execute_with_user(query, (
                transaction_data['transaction_name'],
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

    def update_transaction_type(self, transaction_id, new_name):
        try:
            query = """
                UPDATE TRANSACTION_TYPE
                SET TT_TYPE_NAME = %s
                WHERE TT_ID = %s AND TT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (new_name, transaction_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating Transaction type name: {e}")
            return False

    def get_transaction_type_by_id(self, transaction_id, raw=False):
        try:
            query = """
                SELECT TT_TYPE_NAME
                FROM TRANSACTION_TYPE
                WHERE TT_ID = %s AND TT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (transaction_id,))
            result = self.connection.cursor.fetchone()
            if not result:
                return None
            return result if raw else result[0]
        except Exception as e:
            print(f"Error fetching Transaction type name: {e}")
            return None if not raw else []



    def get_history_types(self):
        try:
            query = """
                SELECT
                    HIST_ID,
                    HIST_TYPE_NAME
                FROM HISTORY_TYPE
                WHERE HIST_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query)
            rows = self.connection.cursor.fetchall()

            return {
                'columns': ['History type ID', 'History Type Name'],
                'data': rows
            }

        except Exception as e:
            print(f"Failed to fetch system users: {e}")
            return {'columns': [], 'data': []}

    def save_new_history_type(self, history_data):
        try:
            query = """
                INSERT INTO HISTORY_TYPE (
                    HIST_TYPE_NAME
                ) VALUES (%s);
            """
            self.connection.execute_with_user(query, (
                history_data['history_name'],
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

    def update_history_type(self, history_id, new_name):
        try:
            query = """
                UPDATE HISTORY_TYPE
                SET HIST_TYPE_NAME = %s
                WHERE HIST_ID = %s AND HIST_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (new_name, history_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating History type name: {e}")
            return False

    def get_history_type_by_id(self, history_id, raw=False):
        try:
            query = """
                SELECT HIST_TYPE_NAME
                FROM HISTORY_TYPE
                WHERE HIST_ID = %s AND HIST_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (history_id,))
            result = self.connection.cursor.fetchone()
            if not result:
                return None
            return result if raw else result[0]
        except Exception as e:
            print(f"Error fetching History type name: {e}")
            return None if not raw else []



    def get_medical_types(self):
        try:
            query = """
                SELECT
                    MHT_ID,
                    MHT_TYPE_NAME
                FROM MEDICAL_HISTORY_TYPE
                WHERE MHT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query)
            rows = self.connection.cursor.fetchall()

            return {
                'columns': ['Medical type ID', 'Medical Type Name'],
                'data': rows
            }

        except Exception as e:
            print(f"Failed to fetch system users: {e}")
            return {'columns': [], 'data': []}

    def save_new_medical_type(self, medical_data):
        try:
            query = """
                INSERT INTO MEDICAL_HISTORY_TYPE (
                    MHT_TYPE_NAME
                ) VALUES (%s);
            """
            self.connection.execute_with_user(query, (
                medical_data['medical_name'],
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

    def update_medical_type(self, medical_id, new_name):
        try:
            query = """
                UPDATE MEDICAL_HISTORY_TYPE
                SET MHT_TYPE_NAME = %s
                WHERE MHT_ID = %s AND MHT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (new_name, medical_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating Medical History type name: {e}")
            return False

    def get_medical_type_by_id(self, medical_id, raw=False):
        try:
            query = """
                SELECT MHT_TYPE_NAME
                FROM MEDICAL_HISTORY_TYPE
                WHERE MHT_ID = %s AND MHT_IS_DELETED = FALSE;
            """
            self.connection.cursor.execute(query, (medical_id,))
            result = self.connection.cursor.fetchone()
            if not result:
                return None
            return result if raw else result[0]
        except Exception as e:
            print(f"Error fetching Medical History type name: {e}")
            return None if not raw else []


    def soft_delete_sitio_data(self, sitio_id):
        try:
            query = """
                UPDATE SITIO
                SET SITIO_IS_DELETED = TRUE
                WHERE SITIO_ID = %s;
            """
            self.connection.execute_with_user(query, (sitio_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error(sitio):", e)
            return False

    def soft_delete_infrastructure_data(self, infrastructure_id):
        try:
            query = """
                UPDATE INFRASTRUCTURE_TYPE
                SET INFT_IS_DELETED = TRUE
                WHERE INFT_ID = %s;
            """
            self.connection.execute_with_user(query, (infrastructure_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error(Infrastructure):", e)
            return False

    def soft_delete_transaction_type(self, transaction_type_id):
        try:
            query = """
                UPDATE TRANSACTION_TYPE
                SET TT_IS_DELETED = TRUE
                WHERE TT_ID = %s;
            """
            self.connection.execute_with_user(query, (transaction_type_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error(Transaction Type):", e)
            return False

    def soft_delete_history_type(self, history_type_id):
        try:
            query = """
                UPDATE HISTORY_TYPE
                SET HIST_IS_DELETED = TRUE
                WHERE HIST_ID = %s;
            """
            self.connection.execute_with_user(query, (history_type_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error(History type):", e)
            return False

    def soft_delete_medical_hist_type(self, med_hist_id):
        try:
            query = """
                UPDATE MEDICAL_HISTORY_TYPE
                SET MHT_IS_DELETED = TRUE
                WHERE MHT_ID = %s;
            """
            self.connection.execute_with_user(query, (med_hist_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error(Medical history type):", e)
            return False

    # def handle_citizen_id_search(self):
    #     citizen_id = self.popup.record_citizenIDANDsearch.text().strip()
    #     if not citizen_id:
    #         self.popup.display_citizenFullName.setText("None")
    #         return
    #
    #     connection = None
    #     try:
    #         connection = Database()
    #         cursor = connection.cursor
    #
    #         # Query to fetch citizen by ID
    #         query = """
    #                 SELECT CTZ_FIRST_NAME, CTZ_LAST_NAME
    #                 FROM CITIZEN
    #                 WHERE CTZ_ID = %s \
    #                   AND CTZ_IS_DELETED = FALSE; \
    #                 """
    #         cursor.execute(query, (citizen_id,))
    #         result = cursor.fetchone()
    #
    #         if result:
    #             full_name = f"{result[0]} {result[1]}"
    #             self.popup.display_citizenFullName.setText(full_name)
    #         else:
    #             self.popup.display_citizenFullName.setText("Not Found")
    #
    #     except Exception as e:
    #         QMessageBox.critical(self.popup, "Database Error", str(e))
    #     finally:
    #         if connection:
    #             connection.close()