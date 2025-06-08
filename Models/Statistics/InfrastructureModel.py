from database import Database

class InfrastructureModel:
    def __init__(self):
        self.connection = Database()
        self.cursor = self.connection.get_cursor()

    def get_total_sitio_infrastructure(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    s.SITIO_NAME AS "Sitio Name",
                    COUNT(CASE WHEN i.INF_ACCESS_TYPE = 'Public' THEN 1 END) AS "Public",
                    COUNT(CASE WHEN i.INF_ACCESS_TYPE = 'Private' THEN 1 END) AS "Private",
                    COUNT(i.INF_ID) AS "Total Infrastructure"
                FROM
                    SITIO s
                LEFT JOIN INFRASTRUCTURE i ON i.SITIO_ID = s.SITIO_ID
                        AND i.INF_IS_DELETED = FALSE
                        AND i.INF_LAST_UPDATED::date BETWEEN %s AND %s
                GROUP BY
                    s.SITIO_NAME
                ORDER BY
                    s.SITIO_NAME;
            """, (from_date, to_date))

            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return {"columns": columns, "data": results}

        except Exception as e:
            print(f"ERROR: Failed to fetch infrastructure data per sitio: {e}")
            return []


    def get_total_infrastructure_type(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    it.INFT_TYPE_NAME as "Infrastructure Type",
                    COUNT(CASE WHEN i.INF_ACCESS_TYPE = 'Public' THEN 1 END) as "Public",
                    COUNT(CASE WHEN i.INF_ACCESS_TYPE = 'Private' THEN 1 END) as "Private",
                    COUNT(i.INF_ID) as "Total Infrastructure"
                
                FROM INFRASTRUCTURE_TYPE it
                    LEFT JOIN INFRASTRUCTURE i on it.INFT_ID = i.INFT_ID
                        AND i.INF_IS_DELETED = FALSE
                        AND i.INF_LAST_UPDATED::date BETWEEN %s AND %s
                
                GROUP BY it.INFT_TYPE_NAME
                
                ORDER BY "Total Infrastructure" DESC;
            """, (from_date, to_date))

            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return {"columns": columns, "data": results}

        except Exception as e:
            print(f"ERROR: Failed to fetch infrastructure types: {e}")
            return []


    def get_total_infrastructures(self,from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                       COUNT(CASE WHEN INF_ACCESS_TYPE = 'Public' THEN 1 END) as "Public",
                       COUNT(CASE WHEN INF_ACCESS_TYPE = 'Private' THEN 1 END) as "Private",
                       COUNT(INF_ID) as "Total Infrastructure"
                FROM INFRASTRUCTURE
                WHERE INF_IS_DELETED = FALSE
                     AND INF_LAST_UPDATED::date BETWEEN %s AND %s;

            """, (from_date, to_date))

            return self.cursor.fetchone()

        except Exception as e:
            print(f"Error fetching all educational attainment stats: {e}")
            return []

