from database import Database

class HouseholdModel:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.get_cursor()

    def get_household_stat_per_sitio(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    s.SITIO_NAME AS "Sitio Name",
                    COUNT(DISTINCT h.HH_ID) AS "Total Households",
                    CASE 
                        WHEN COUNT(DISTINCT h.HH_ID) > 0 THEN
                            ROUND(COUNT(c.CTZ_ID) FILTER (WHERE c.CTZ_SEX = 'M')::numeric / COUNT(DISTINCT h.HH_ID), 2)
                        ELSE 0 
                    END AS "Avg Male/Household",
                    CASE 
                        WHEN COUNT(DISTINCT h.HH_ID) > 0 THEN
                            ROUND(COUNT(c.CTZ_ID) FILTER (WHERE c.CTZ_SEX = 'F')::numeric / COUNT(DISTINCT h.HH_ID), 2)
                        ELSE 0 
                    END AS "Avg Female/Household",
                    CASE 
                        WHEN COUNT(DISTINCT h.HH_ID) > 0 THEN
                            ROUND(COUNT(c.CTZ_ID)::numeric / COUNT(DISTINCT h.HH_ID), 2)
                        ELSE 0 
                    END AS "Avg Members/Household"
                FROM SITIO s
                LEFT JOIN HOUSEHOLD_INFO h 
                    ON h.SITIO_ID = s.SITIO_ID 
                    AND h.HH_IS_DELETED = FALSE
                    AND h.HH_LAST_UPDATED ::date BETWEEN %s AND %s
                LEFT JOIN CITIZEN c 
                    ON c.HH_ID = h.HH_ID 
                    AND c.CTZ_IS_DELETED = FALSE 
                    AND c.CTZ_IS_ALIVE = TRUE
                GROUP BY s.SITIO_NAME
                ORDER BY s.SITIO_NAME;
            """, (from_date, to_date))

            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            return {"columns": columns, "data": results}

        except Exception as e:
            print(f"[ERROR] Failed to fetch household stats: {e}")
            return {"columns": [], "data": []}

    def get_highest_lowest_total_households(self, from_date, to_date):
        try:
            self.cursor.execute("""
                WITH sitio_households AS (
                    SELECT
                        s.SITIO_NAME,
                        COUNT(h.HH_ID) AS total_households
                    FROM
                        SITIO s
                            LEFT JOIN HOUSEHOLD_INFO h ON h.SITIO_ID = s.SITIO_ID
                            AND h.HH_IS_DELETED = FALSE
                            AND h.HH_LAST_UPDATED ::date BETWEEN %s AND %s
                    GROUP BY
                        s.SITIO_NAME
                ),
                     highest AS (
                         SELECT * FROM sitio_households ORDER BY total_households DESC LIMIT 1
                     ),
                     lowest AS (
                         SELECT * FROM sitio_households ORDER BY total_households ASC LIMIT 1
                     )
                SELECT * FROM highest
                UNION ALL
                SELECT * FROM lowest;
            """, (from_date, to_date))

            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return {"columns": columns, "data": results}
        except Exception as e:
            print(f"[ERROR] Failed to fetch household stats: {e}")
            return []

    def get_household_ownership_status(self, from_date, to_date):
        try:
            self.cursor.execute("""
                WITH OWNERSHIP_STATUS AS (
                    SELECT unnest(enum_range(NULL::house_ownership_status)) AS ownership_status
                )
                SELECT
                    OS.OWNERSHIP_STATUS AS HH_OWNERSHIP_STATUS,
                    COALESCE(COUNT(hh.HH_ID), 0) AS total_households
                FROM
                    OWNERSHIP_STATUS OS
                        LEFT JOIN
                    HOUSEHOLD_INFO hh ON hh.HH_OWNERSHIP_STATUS = OS.OWNERSHIP_STATUS 
                    AND hh.HH_IS_DELETED = FALSE 
                    AND hh.HH_LAST_UPDATED ::date BETWEEN %s AND %s
                GROUP BY
                    OS.OWNERSHIP_STATUS 
                ORDER BY
                    OS.OWNERSHIP_STATUS ;
            """, (from_date, to_date))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch household ownership status: {e}")
            return []

    def get_household_water_source(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT 
                    ws.WATER_SOURCE_NAME,
                    COALESCE(COUNT(hh.HH_ID), 0) AS total_households
                FROM 
                    WATER_SOURCE ws
                LEFT JOIN 
                    HOUSEHOLD_INFO hh ON hh.WATER_ID = ws.WATER_ID AND hh.HH_IS_DELETED = FALSE
                    AND hh.HH_IS_DELETED = FALSE
                    AND hh.HH_LAST_UPDATED ::date BETWEEN %s AND %s
                GROUP BY 
                    ws.WATER_SOURCE_NAME
                ORDER BY
                    ws.WATER_SOURCE_NAME;
            """,(from_date, to_date))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch household water source: {e}")
            return []
