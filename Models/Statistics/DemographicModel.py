from database import Database

class DemographicModel:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.get_cursor()

    def get_sex_counts(self):
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE CTZ_SEX = 'M') AS male,
                    COUNT(*) FILTER (WHERE CTZ_SEX = 'F') AS female
                FROM CITIZEN
                WHERE CTZ_IS_ALIVE = TRUE
            """)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[ERROR] Failed to fetch gender counts: {e}")
            return (0, 0)  # Default values in case of failure

    def get_age_group_counts(self):
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 0 AND 13),
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 14 AND 17),
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 18 AND 25),
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 26 AND 35),
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) BETWEEN 36 AND 59),
                    COUNT(*) FILTER (WHERE EXTRACT(YEAR FROM AGE(current_date, CTZ_DATE_OF_BIRTH)) >= 60)
                FROM CITIZEN
                WHERE CTZ_IS_ALIVE = TRUE;
            """)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[ERROR] Failed to fetch age group counts: {e}")
            return (0, 0, 0, 0, 0, 0)

    def get_civil_status_distribution(self):
        query = """
        SELECT 
            CTZ_CIVIL_STATUS,
            COUNT(*) FILTER (WHERE CTZ_SEX = 'M') AS male_count,
            COUNT(*) FILTER (WHERE CTZ_SEX = 'F') AS female_count,
            COUNT(*) AS total_count
        FROM citizen
        WHERE CTZ_IS_ALIVE = TRUE
        GROUP BY CTZ_CIVIL_STATUS
        ORDER BY CTZ_CIVIL_STATUS ASC;
        """
        try:
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            return results
        except Exception as e:
            print(f"[ERROR] Failed to fetch civil status data: {e}")
            return []

    def get_voter_statistics(self):
        try:
            self.cursor.execute("""
                SELECT
                    -- Age groups among registered voters
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
                WHERE CTZ_IS_ALIVE = TRUE;
            """)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[ERROR] Failed to fetch voter statistics: {e}")
            return (0,) * 11  # Return 11 zeros as default

    def get_socio_economic_distribution(self):
        query = """
            SELECT
                COUNT(*) AS total
            FROM
                CITIZEN c
            LEFT JOIN
                SOCIO_ECONOMIC_STATUS s ON c.CTZ_SOCIO_ECONOMIC_ID = s.SOEC_ID
            WHERE
                c.CTZ_IS_ALIVE = TRUE
            GROUP BY
                s.SOEC_STATUS
            ORDER BY
                s.SOEC_STATUS;
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch socio-economic data: {e}")
            return []

    def get_religion_distribution(self):
        try:
            self.cursor.execute("""
                SELECT 
                    COUNT(*) AS total
                FROM 
                    CITIZEN c
                JOIN
                    RELIGION r ON c.CTZ_RELIGION_ID = r.REL_ID
                WHERE 
                    c.CTZ_IS_ALIVE = TRUE
                GROUP BY 
                    r.REL_NAME
                ORDER BY 
                    religion;
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR] Failed to fetch religion distribution: {e}")
            return []

    def close(self):
        self.db.close()
