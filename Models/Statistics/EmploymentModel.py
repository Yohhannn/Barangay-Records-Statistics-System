from database import Database

class EmploymentModel:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.get_cursor()

    def get_employment_data_per_sitio(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    s.SITIO_NAME AS "Sitio",
                    COUNT(CASE WHEN es.ES_STATUS_NAME = 'Employed' THEN 1 END) AS "Employed",
                    COUNT(CASE WHEN es.ES_STATUS_NAME = 'Unemployed' THEN 1 END) AS "Unemployed",
                    COUNT(CASE WHEN es.ES_STATUS_NAME = 'Self-employed' THEN 1 END) AS "Self-employed",
                    COUNT(CASE WHEN es.ES_STATUS_NAME = 'Not in Labor Force' THEN 1 END) AS "Not in Labor Force"
                FROM
                    SITIO s
                        LEFT JOIN
                    CITIZEN c ON s.SITIO_ID = c.SITIO_ID
                        AND c.CTZ_IS_DELETED = FALSE
                        AND c.CTZ_IS_ALIVE = TRUE
                        AND c.CTZ_LAST_UPDATED BETWEEN %s AND %s
                        LEFT JOIN
                    EMPLOYMENT e ON c.CTZ_ID = e.CTZ_ID
                        LEFT JOIN
                    EMPLOYMENT_STATUS es ON e.ES_ID = es.ES_ID
                GROUP BY
                    s.SITIO_NAME
                ORDER BY
                    s.SITIO_NAME;
            """, (from_date, to_date))

            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return {"columns": columns, "data": results}
        except Exception as e:
            print(f"[ERROR] Failed to fetch employment stat: {e}")
            return []


    def get_total_gov_nongov_worker(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    COUNT(e.EMP_ID) FILTER (WHERE e.EMP_IS_GOV_WORKER = TRUE) AS "Governement Worker",
                    COUNT(e.EMP_ID) FILTER (WHERE e.EMP_IS_GOV_WORKER = FALSE) AS "Non-Governement Worker"
                FROM
                    EMPLOYMENT e
                        LEFT JOIN CITIZEN c ON e.CTZ_ID = c.CTZ_ID
                WHERE c.CTZ_IS_DELETED = FALSE
                        AND c.CTZ_IS_ALIVE = TRUE
                        AND c.CTZ_LAST_UPDATED::date BETWEEN %s AND %s;
            """, (from_date, to_date))

            return self.cursor.fetchone()

        except Exception as e:
            print(f"ERROR: Failed to fetch total government and non-government worker data: {e}")
            return []

    def get_overall_employment_stats(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    COUNT(e.EMP_ID) FILTER (WHERE es.ES_STATUS_NAME = 'Employed') AS "Employed",
                    COUNT(e.EMP_ID) FILTER (WHERE es.ES_STATUS_NAME = 'Unemployed') AS "Unemployed",
                    COUNT(e.EMP_ID) FILTER (WHERE es.ES_STATUS_NAME = 'Self-Employed') AS "Self-Employed",
                    COUNT(e.EMP_ID) FILTER (WHERE es.ES_STATUS_NAME = 'Not in Labor Force') AS "Not in Labor Force"
                FROM
                    EMPLOYMENT e
                        LEFT JOIN CITIZEN c ON e.CTZ_ID = c.CTZ_ID
                        LEFT JOIN EMPLOYMENT_STATUS es ON e.ES_ID = es.ES_ID
                WHERE       c.CTZ_IS_DELETED = FALSE
                            AND c.CTZ_IS_ALIVE = TRUE
                            AND C.CTZ_LAST_UPDATED::date BETWEEN %s AND %s;
            """, (from_date, to_date))
            return self.cursor.fetchone()

        except Exception as e:
            print(f"Error fetching all educational attainment stats: {e}")
            return []

