from database import Database

class ManageAccountsModel:
    def __init__(self, sys_user_id=None):
        self.connection = Database()
        if sys_user_id is not None:
            self.connection.set_user_id(sys_user_id)

    def save_new_account_data(self, account_data):
        try:
            query = """
                INSERT INTO SYSTEM_ACCOUNT (
                    SYS_FNAME,
                    SYS_LNAME,
                    SYS_MNAME,
                    SYS_PASSWORD,
                    SYS_ROLE
                ) VALUES (%s, %s, %s, %s, %s)
            """
            self.connection.execute_with_user(query, (
                account_data['first_name'],
                account_data['last_name'],
                account_data['middle_name'],
                account_data['user_password'],
                account_data['role']
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False



    def get_system_users(self):
        try:
            query = """
                SELECT
                    SYS_USER_ID,
                    COALESCE(SYS_LNAME, '') || ', ' ||
                    COALESCE(SYS_FNAME, '') ||
                    CASE
                        WHEN SYS_MNAME IS NOT NULL AND SYS_MNAME <> ''
                            THEN ' ' || SYS_MNAME
                        ELSE ''
                    END AS full_name,
                    SYS_ROLE,
                    SYS_IS_ACTIVE,
                    SYS_DATE_ENCODED::date AS date_encoded
                FROM SYSTEM_ACCOUNT
                WHERE SYS_ROLE != 'Super Admin'
                AND SYS_IS_DELETED = FALSE
                ORDER BY SYS_LNAME, SYS_FNAME;
            """
            self.connection.cursor.execute(query)
            rows = self.connection.cursor.fetchall()

            return {
                'columns': ['User_ID', 'Full Name', 'Role', 'Is Active', 'Date Encoded'],
                'data': rows
            }

        except Exception as e:
            print(f"Failed to fetch system users: {e}")
            return {'columns': [], 'data': []}

    def soft_delete_account_data(self, account_data):
        try:
            query = """
                UPDATE SYSTEM_ACCOUNT
                SET SYS_IS_DELETED = TRUE
                WHERE SYS_USER_ID = %s
                    AND SYS_ROLE != 'Super Admin';
            """
            self.connection.execute_with_user(query, (
                account_data['user_id'],
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

