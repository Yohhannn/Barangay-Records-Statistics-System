from database import Database

class DemographicModel:
    def __init__(self):
        self.connection = Database()
        self.cursor = self.connection.get_cursor()

    def get_population_counts(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE CTZ_SEX = 'M' AND CTZ_IS_ALIVE = TRUE) AS male,
                    COUNT(*) FILTER (WHERE CTZ_SEX = 'F' AND CTZ_IS_ALIVE = TRUE) AS female,
                    COUNT(*) FILTER (WHERE CTZ_IS_IP = TRUE AND CTZ_IS_ALIVE = TRUE) as ip_count,
                    COUNT(*) FILTER (WHERE CTZ_IS_ALIVE = FALSE) AS deceased
                FROM (
                    SELECT * FROM CITIZEN
                    WHERE CTZ_LAST_UPDATED BETWEEN %s AND %s
                    AND CTZ_IS_DELETED = FALSE
                ) AS filtered_citizens
            """, (from_date, to_date))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[ERROR] Failed to fetch population counts: {e}")
            return (0, 0, 0, 0)

    def get_age_group_counts(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 0 AND 2) as "Infant",
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 3 AND 12) as "Child",
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 13 AND 17) as "Teen",
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 18 AND 24) as "Young Adult",
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 25 AND 39) as "Adult",
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 40 AND 59) as "Middle Aged",
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) >= 60) as "Senior"
                FROM CITIZEN
                WHERE CTZ_IS_ALIVE = TRUE 
                AND CTZ_LAST_UPDATED BETWEEN %s AND %s 
                AND CTZ_IS_DELETED = FALSE;
            """, (from_date, to_date))

            return self.cursor.fetchone()
        except Exception as e:
            print(f"[ERROR] Failed to fetch age group counts: {e}")
            return 0, 0, 0, 0, 0, 0

    def get_civil_status_distribution(self, from_date, to_date):
        try:
            self.cursor.execute("""
            SELECT 
                CTZ_CIVIL_STATUS,
                COUNT(*) FILTER (WHERE CTZ_SEX = 'M') AS male_count,
                COUNT(*) FILTER (WHERE CTZ_SEX = 'F') AS female_count,
                COUNT(*) AS total_count
            FROM citizen
            WHERE CTZ_IS_ALIVE = TRUE
            AND CTZ_LAST_UPDATED BETWEEN %s AND %s 
            AND CTZ_IS_DELETED = FALSE
            GROUP BY CTZ_CIVIL_STATUS;
            """, (from_date, to_date))

            results = self.db.cursor.fetchall()
            return results
        except Exception as e:
            print(f"[ERROR] Failed to fetch civil status data: {e}")
            return []

    def get_voter_statistics(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE AND EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 15 AND 17) AS age_15_17,
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE AND EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 18 AND 25) AS age_18_25,
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE AND EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 26 AND 35) AS age_26_35,
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE AND EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 36 AND 59) AS age_36_59,
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE AND EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) >= 60) AS age_60_above,

                    -- Total registered & unregistered
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE) AS total_registered,
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = FALSE) AS total_unregistered,

                    -- Male & Female registered voters
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE AND CTZ_SEX = 'M') AS male_voters,
                    COUNT(*) FILTER (WHERE CTZ_IS_REGISTERED_VOTER = TRUE AND CTZ_SEX = 'F') AS female_voters

                FROM CITIZEN
                WHERE CTZ_IS_ALIVE = TRUE 
                AND CTZ_LAST_UPDATED BETWEEN %s AND %s 
                AND CTZ_IS_DELETED = FALSE;
            """, (from_date, to_date))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[ERROR] Failed to fetch voter statistics: {e}")
            return (0,) * 11

    def get_socio_economic_distribution(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    s.SOEC_STATUS, COUNT(*) AS total
                FROM
                    CITIZEN c
                LEFT JOIN
                    SOCIO_ECONOMIC_STATUS s ON c.SOEC_ID = s.SOEC_ID
                WHERE
                    c.CTZ_IS_ALIVE = TRUE
                AND c.CTZ_LAST_UPDATED BETWEEN %s AND %s 
                AND c.CTZ_IS_DELETED = FALSE
                GROUP BY
                    s.SOEC_STATUS;
            """, (from_date, to_date))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch socio-economic data: {e}")
            return []

    def get_religion_distribution(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT 
                    r.REL_NAME AS religion,
                    COUNT(*) AS total
                FROM 
                    CITIZEN c
                JOIN
                    RELIGION r ON c.REL_ID = r.REL_ID
                WHERE 
                    c.CTZ_IS_ALIVE = TRUE
                AND c.CTZ_LAST_UPDATED BETWEEN %s AND %s 
                AND c.CTZ_IS_DELETED = FALSE
                GROUP BY 
                    r.REL_NAME;
            """, (from_date, to_date))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch religion distribution: {e}")
            return []

    def close(self):
        self.db.close()
