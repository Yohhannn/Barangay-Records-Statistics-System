from database import Database

class EducationModel:
    def __init__(self):
        self.connection = Database()
        self.cursor = self.connection.get_cursor()

    def get_total_students_and_not(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT
                    SUM(CASE WHEN es.EDU_IS_CURRENTLY_STUDENT = TRUE THEN 1 ELSE 0 END) AS total_currently_studying,
                    SUM(CASE WHEN es.EDU_IS_CURRENTLY_STUDENT = FALSE OR es.EDU_IS_CURRENTLY_STUDENT IS NULL THEN 1 ELSE 0 END) AS total_not_currently_studying
                FROM CITIZEN c
                    LEFT JOIN EDUCATION_STATUS es ON c.EDU_ID = es.EDU_ID
                WHERE c.CTZ_IS_DELETED = FALSE 
                    AND c.CTZ_IS_ALIVE = TRUE
                    AND c.CTZ_LAST_UPDATED::date BETWEEN %s AND %s;
            """, (from_date, to_date))

            return self.cursor.fetchone()

        except Exception as e:
            print(f"ERROR: Failed to fetch students and not data: {e}")
            return []

    def get_all_educational_attainment_stats(self, to_date):
        try:
            self.cursor.execute("""
                SELECT 
                    ea.EDAT_LEVEL AS attainment,
                    COUNT(c.CTZ_ID) AS count
                FROM 
                    EDUCATIONAL_ATTAINMENT ea
                LEFT JOIN 
                    EDUCATION_STATUS es ON ea.EDAT_ID = es.EDAT_ID
                LEFT JOIN 
                    CITIZEN c ON es.EDU_ID = c.EDU_ID
                        AND c.CTZ_IS_DELETED = FALSE
                        AND c.CTZ_IS_ALIVE = TRUE
                        AND c.CTZ_DATE_OF_BIRTH::date <= %s
                GROUP BY 
                    ea.EDAT_ID, ea.EDAT_LEVEL
                ORDER BY
                    CASE ea.EDAT_LEVEL
                        WHEN 'No Formal Education' THEN 1
                        WHEN 'Kindergarten' THEN 2
                        WHEN 'Elementary Undergraduate' THEN 3
                        WHEN 'Elementary Graduate' THEN 4
                        WHEN 'Junior High School Undergraduate' THEN 5
                        WHEN 'Senior High School Undergraduate' THEN 6
                        WHEN 'Senior High School Graduate' THEN 7
                        WHEN 'Vocational/Technical Graduate' THEN 8
                        WHEN 'College Undergraduate' THEN 9
                        WHEN 'College Graduate' THEN 10
                        WHEN 'Postgraduate' THEN 11
                        ELSE 12
                    END;
            """, (to_date,))

            return self.cursor.fetchall()

        except Exception as e:
            print(f"Error fetching all educational attainment stats: {e}")
            return []

