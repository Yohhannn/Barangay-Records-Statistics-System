from database import Database

class ActivityLogsModel:
    def __init__(self, sys_user_id=None):
        self.connection = Database()
        if sys_user_id is not None:
            self.connection.set_user_id(sys_user_id)

    def get_activity_logs(self):
        try:
            query = """
                SELECT
                    a.SYS_USER_ID,
                    CONCAT_WS(' ',
                              a.SYS_FNAME,
                              CASE
                                  WHEN a.SYS_MNAME IS NOT NULL AND a.SYS_MNAME <> ''
                                      THEN LEFT(a.SYS_MNAME, 1) || '.'
                                  END,
                              a.SYS_LNAME
                    ) AS FULL_NAME,
                    l.ACT_DESCRIPTION,
                    l.ACT_TIMESTAMP
                FROM
                    SYSTEM_ACTIVITY_LOG l
                        JOIN
                    SYSTEM_ACCOUNT a ON l.SYS_USER_ID = a.SYS_USER_ID
                ORDER BY
                    l.ACT_TIMESTAMP DESC;
            """
            self.connection.cursor.execute(query)
            rows = self.connection.cursor.fetchall()

            return {
                'columns': ['User Id', 'Staff Name', 'Action Made', 'Timestamp of action'],
                'data': rows
            }

        except Exception as e:
            print(f"Failed to fetch system users: {e}")
            return {'columns': [], 'data': []}

