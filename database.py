import psycopg2
from passlib.hash import bcrypt
class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="marigondon_profiling_db",
                user="postgres",
                password="123jp"
            )
            self.cursor = self.conn.cursor()
            print("Database Connected Successfully!")
        except Exception as e:
            print(f"Database Connection Failed: {e}")

        self.sys_user_id = 0

    def close(self):
        if self.cursor:
            self.cursor.close()
            print("Cursor closed successfully!")
        if self.conn:
            self.conn.close()
            print("Database Connection Closed Successfully!")

    def commit(self):
        try:
            self.conn.commit()
            print("Transaction committed successfully!")
            return True
        except Exception as e:
            print(f"Commit failed: {e}")
            self.conn.rollback()  # Rollback in case of error
            return False

    def get_cursor(self):
        return self.cursor

    def set_user_id(self, user_id):
        if user_id is not None:
            self.sys_user_id = str(user_id)
            print(f"Database user ID set to: {self.sys_user_id}")  # Debug

    def execute_with_user(self, query, params=None):
        try:
            # Set the user context if available
            if self.sys_user_id:
                set_user_query = "SET LOCAL app.current_user_id TO %s"
                self.cursor.execute(set_user_query, (self.sys_user_id,))
                print(f"Setting app.current_user_id to: {self.sys_user_id}")  # Debug

            # Execute the main query
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

        except Exception as e:
            self.conn.rollback()
            print(f"Error in execute_with_user: {e}")  # Debug
            raise

    # This is for hashing plaintext passwords in the database
    def hash_plaintext_passwords(self):
        try:
            # Fetch all user IDs and passwords
            self.cursor.execute("SELECT SYS_USER_ID, SYS_PASSWORD FROM SYSTEM_ACCOUNT")
            users = self.cursor.fetchall()

            for user_id, password in users:
                # Skip if already hashed
                if password.startswith('$2b$') or password.startswith('$2a$'):
                    continue

                # Hash the plaintext password
                hashed_password = bcrypt.hash(password)

                self.cursor.execute(
                    "UPDATE SYSTEM_ACCOUNT SET SYS_PASSWORD = %s WHERE SYS_USER_ID = %s",
                    (hashed_password, user_id)
                )

            print(f"User passwords are all hashed and updated.")

            self.commit()

        except Exception as e:
            print(f"Error hashing passwords: {e}")
            self.conn.rollback()

if __name__ == "__main__":
    db = Database()
    db.hash_plaintext_passwords()
    db.close()