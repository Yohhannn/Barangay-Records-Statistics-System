from database import Database


class NeighborhoodModel:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.get_cursor()

    def get_data_per_sitio(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    s.SITIO_NAME AS "Sitio Name",
                    COUNT(c.CTZ_ID) FILTER (WHERE c.CTZ_SEX = 'M') AS "No. of Male",
                    COUNT(c.CTZ_ID) FILTER (WHERE c.CTZ_SEX = 'F') AS "No. of Female",
                    COUNT(c.CTZ_ID) FILTER (
                        WHERE EXTRACT(YEAR FROM AGE(c.CTZ_DATE_OF_BIRTH)) >= 60
                        ) AS "No. of Seniors",
                    COUNT(c.CTZ_ID) FILTER (
                        WHERE ch.CLAH_CLASSIFICATION_NAME = 'Person With Disability'
                        ) AS "No. of PWD",
                    COUNT(c.CTZ_ID) FILTER (WHERE c.CTZ_IS_REGISTERED_VOTER = TRUE) AS "No. of Voters",
                    COUNT(c.CTZ_ID) AS "Total Population"
                
                FROM
                    SITIO s
                        LEFT JOIN CITIZEN c
                                  ON c.SITIO_ID = s.SITIO_ID
                                      AND c.CTZ_IS_DELETED = FALSE
                                      AND c.CTZ_IS_ALIVE = TRUE
                                      AND c.CTZ_LAST_UPDATED ::date BETWEEN %s AND %s
                        LEFT JOIN CLASSIFICATION_HEALTH_RISK ch ON c.CLAH_ID = ch.CLAH_ID
                GROUP BY
                    s.SITIO_NAME
                ORDER BY
                    s.SITIO_NAME;
            """, (from_date, to_date))
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return {"columns": columns, "data": results}
        except Exception as e:
            print(f"[ERROR] Failed to fetch population counts: {e}")
            return []

    def get_sitio_count(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM SITIO;")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"[ERROR] Failed to fetch sitio count: {e}")
            return 0

    def get_highest_and_lowest_population_sitios(self, from_date, to_date):
        try:
            self.cursor.execute("""
                WITH sitio_population AS (
                    SELECT
                        s.SITIO_NAME,
                        COUNT(c.CTZ_ID) AS total_population
                    FROM
                        SITIO s
                            LEFT JOIN
                        CITIZEN c ON s.SITIO_ID = c.SITIO_ID
                            AND c.CTZ_LAST_UPDATED::date BETWEEN %s AND %s
                            AND c.CTZ_IS_DELETED = FALSE
                            AND c.CTZ_IS_ALIVE = TRUE
                    GROUP BY
                        s.SITIO_NAME
                )
                SELECT * FROM (
                                  SELECT * FROM sitio_population ORDER BY total_population DESC LIMIT 1
                              ) AS highest
                UNION ALL
                SELECT * FROM (
                                  SELECT * FROM sitio_population ORDER BY total_population ASC LIMIT 1
                              ) AS lowest;
            """, (from_date, to_date))

            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return {"columns": columns, "data": results}

        except Exception as e:
            print(f"[ERROR] Failed to fetch highest/lowest population sitios: {e}")
            return []

