from database import Database

class HealthModel:
    def __init__(self):
        self.connection = Database()
        self.cursor = self.connection.get_cursor()

    def get_health_risk_group_data(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT ch.CLAH_CLASSIFICATION_NAME, COUNT(c.CTZ_ID) AS total
                FROM CLASSIFICATION_HEALTH_RISK ch
                         LEFT JOIN CITIZEN c ON ch.CLAH_ID = c.CLAH_ID 
                         AND c.CTZ_IS_DELETED = FALSE
                         AND c.CTZ_IS_ALIVE = TRUE
                         AND c.CTZ_LAST_UPDATED::date BETWEEN %s AND %s
                GROUP BY ch.CLAH_CLASSIFICATION_NAME
                ORDER BY ch.CLAH_CLASSIFICATION_NAME;
            """, (from_date, to_date))

            return self.cursor.fetchall()

        except Exception as e:
            print(f"[ERROR] Failed to fetch health risk group stats: {e}")
            return []

    def get_blood_type_distribution(self, from_date, to_date):
        try:
            self.cursor.execute("""
                WITH all_blood_types AS (
                    SELECT unnest(enum_range(NULL::blood_type_enum)) AS blood_type
                )
                SELECT bt.blood_type, COUNT(c.CTZ_ID) AS total
                FROM all_blood_types bt
                         LEFT JOIN CITIZEN c ON c.CTZ_BLOOD_TYPE = bt.blood_type 
                            AND c.CTZ_IS_DELETED = FALSE
                            AND c.CTZ_IS_ALIVE = TRUE
                            AND c.CTZ_LAST_UPDATED::date BETWEEN %s AND %s
                GROUP BY bt.blood_type
                ORDER BY bt.blood_type;
            """, (from_date, to_date))

            return self.cursor.fetchall()

        except Exception as e:
            print(f"Error fetching blood type data: {e}")
            return []

    def get_total_gender_with_med_record(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT sex_group.sex AS gender, COUNT(DISTINCT c.CTZ_ID) AS total
                FROM (VALUES ('M'), ('F')) AS sex_group(sex)
                         LEFT JOIN CITIZEN c ON c.CTZ_SEX = sex_group.sex 
                            AND c.CTZ_IS_DELETED = FALSE
                            AND c.CTZ_IS_ALIVE = TRUE
                            AND c.CTZ_LAST_UPDATED::date BETWEEN %s AND %s
                         LEFT JOIN MEDICAL_HISTORY mh ON c.CTZ_ID = mh.CTZ_ID 
                            AND mh.MH_IS_DELETED = FALSE
                            AND mh.MH_LAST_UPDATED::date BETWEEN %s AND %s
                GROUP BY sex_group.sex
                ORDER BY sex_group.sex;
            """, (from_date, to_date, from_date, to_date))

            return self.cursor.fetchall()

        except Exception as e:
            print(f"Error fetching male and female with medical records: {e}")
            return []

    def get_philhealth_categories(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT pc.PC_CATEGORY_NAME, COUNT(c.CTZ_ID) AS total
                FROM PHILHEALTH_CATEGORY pc
                         LEFT JOIN PHILHEALTH ph ON ph.PC_ID = pc.PC_ID
                         LEFT JOIN CITIZEN c ON c.PHEA_ID = ph.PHEA_ID 
                            AND c.CTZ_IS_DELETED = FALSE
                            AND c.CTZ_IS_ALIVE = TRUE
                            AND c.CTZ_LAST_UPDATED::date BETWEEN %s AND %s                    
                GROUP BY pc.PC_CATEGORY_NAME
                ORDER BY pc.PC_CATEGORY_NAME;
            """, (from_date, to_date))

            return self.cursor.fetchall()

        except Exception as e:
            print(f"Error fetching philhealth categories: {e}")
            return []

    def get_top_5_medical_case(self, from_date, to_date):
        try:
            self.cursor.execute("""
                SELECT mht.MHT_TYPE_NAME, COUNT(mh.MHT_ID) AS total
                FROM MEDICAL_HISTORY mh
                         JOIN MEDICAL_HISTORY_TYPE mht ON mh.MHT_ID = mht.MHT_ID
                         JOIN CITIZEN c ON c.CTZ_ID = mh.CTZ_ID
                WHERE mh.MH_IS_DELETED = FALSE
                          AND c.CTZ_IS_DELETED = FALSE
                          AND c.CTZ_IS_ALIVE = TRUE
                          AND mh.MH_LAST_UPDATED::date BETWEEN %s AND %s
                GROUP BY mht.MHT_TYPE_NAME
                ORDER BY total DESC
                LIMIT 5;
            """, (from_date, to_date))

            return self.cursor.fetchall()

        except Exception as e:
            print(f"Error fetching medical case: {e}")
            return []