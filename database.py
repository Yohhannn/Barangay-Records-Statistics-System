import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="marigondon_profiling_db",
                user="postgres",
                password=""
            )
            self.cursor = self.conn.cursor()
            print("Database Connected Successfully!")
        except Exception as e:
            print(f"Database Connection Failed: {e}")

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

if __name__ == "__main__":
    db = Database()
