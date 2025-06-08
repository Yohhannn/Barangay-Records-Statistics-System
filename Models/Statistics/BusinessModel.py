from database import Database

class BusinessModel:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.get_cursor()

    def get_business_stat_per_sitio(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    s.SITIO_NAME AS "Sitio",
                    COUNT(CASE WHEN bs.BS_STATUS = 'Active' THEN 1 END) AS "Active",
                    COUNT(CASE WHEN bs.BS_STATUS = 'Inactive' THEN 1 END) AS "Inactive",
                    COUNT(CASE WHEN bs.BS_STATUS = 'Closed' THEN 1 END) AS "Closed",
                    COUNT(CASE WHEN bs.BS_STATUS = 'Suspended' THEN 1 END) AS "Suspended"
                FROM
                    SITIO s
                        LEFT JOIN
                    BUSINESS_INFO bs ON s.SITIO_ID = bs.SITIO_ID
                                     AND bs.BS_IS_DELETED = FALSE
                                     AND bs.BS_LAST_UPDATED::date BETWEEN %s AND %s
                GROUP BY
                    s.SITIO_NAME
                ORDER BY
                    s.SITIO_NAME;
            """, (from_date, to_date))

            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            return {"columns": columns, "data": results}

        except Exception as e:
            print(f"[ERROR] Failed to fetch business stats: {e}")
            return {"columns": [], "data": []}


    def get_active_business_type(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT bt.BST_TYPE_NAME,
                        COUNT(BS_ID) AS active_count
                FROM BUSINESS_TYPE bt
                LEFT JOIN BUSINESS_INFO bs on bt.BST_ID = bs.BST_ID
                    AND BS.BS_STATUS = 'Active'
                    AND bs.BS_IS_DELETED = FALSE
                    AND bs.BS_LAST_UPDATED::date BETWEEN %s AND %s
                GROUP BY bt.BST_TYPE_NAME;
            """, (from_date, to_date))

            return self.cursor.fetchall()

        except Exception as e:
            print(f"Error fetching active business type data: {e}")
            return []

