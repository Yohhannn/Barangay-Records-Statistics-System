import psycopg2


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host = "localhost",
                database = "",
                user = "postgres",
                password = ""
            )
            self.cursor = self.conn.cursor()
            print("Database Connected Successfully!")
        except Exception as e:
            print(f"Database Connection Failed: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
            print("cursor closed successfully!")
        if self.conn:
            self.conn.close()
            print("Database Connection Closed Successfully!")

if __name__ == "__main__":
    db = Database()
