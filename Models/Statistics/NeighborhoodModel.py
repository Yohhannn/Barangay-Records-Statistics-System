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

                    -- Using FILTER for cleaner conditional aggregations
                    COUNT(*) FILTER (WHERE c.CTZ_SEX = 'M') AS "No. of Male",
                    COUNT(*) FILTER (WHERE c.CTZ_SEX = 'F') AS "No. of Female",
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(c.CTZ_DATE_OF_BIRTH)) >= 60) AS "No. of Seniors",
                    COUNT(*) FILTER (WHERE ch.CLAH_CLASSIFICATION_NAME = 'Person With Disability') AS "No. of PWD",
                    COUNT(*) FILTER (WHERE c.CTZ_IS_REGISTERED_VOTER = TRUE) AS "No. of Voters",

                    -- Total population
                    COUNT(*) AS "Total Population"

                FROM 
                    CITIZEN c
                JOIN 
                    SITIO s ON c.SITIO_ID = s.SITIO_ID
                LEFT JOIN 
                    CLASSIFICATION cl ON c.CLA_ID = cl.CLA_ID
                LEFT JOIN 
                    CLASSIFICATION_HEALTH_RISK ch ON cl.CLAH_ID = ch.CLAH_ID
                WHERE 
                    c.CTZ_LAST_UPDATED BETWEEN %s AND %s 
                    AND c.CTZ_IS_DELETED = FALSE
                    AND c.CTZ_IS_ALIVE = TRUE
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

    def get_highest_and_lowest_population_sitios(self, from_date, to_date):
        try:
            self.cursor.execute("""
                WITH sitio_population AS (
                    SELECT 
                        s.SITIO_NAME,
                        COUNT(*) AS total_population
                    FROM 
                        CITIZEN c
                    JOIN 
                        SITIO s ON c.SITIO_ID = s.SITIO_ID
                    WHERE 
                        c.CTZ_LAST_UPDATED BETWEEN %s AND %s 
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

