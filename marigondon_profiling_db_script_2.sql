-- Database; marigondon_profiling_db
CREATE DATABASE marigondon_profiling_db;
--
-- Table: SITIO
-- TABLES WITH NO FOREIGN KEYS
CREATE TABLE SITIO (
                       SITIO_ID SERIAL PRIMARY KEY,
                       SITIO_NAME VARCHAR(100) NOT NULL
);

CREATE TABLE CLASSIFICATION_AGE(
                                   CLAG_ID SERIAL PRIMARY KEY,
                                   CLAG_CLASSIFICATION_NAME VARCHAR(50) NOT NULL
);

CREATE TABLE CLASSIFICATION_HEALTH_RISK(
                                           CLAH_ID SERIAL PRIMARY KEY,
                                           CLAH_CLASSIFICATION_NAME VARCHAR(50) NOT NULL
);


-- Table: ETHNICITY
CREATE TABLE ETHNICITY (
                           ETH_ID SERIAL PRIMARY KEY,
                           ETH_TRIBE_NAME VARCHAR(100) NOT NULL
);

-- Table: RELIGION
CREATE TABLE RELIGION (
                          REL_ID SERIAL PRIMARY KEY,
                          REL_NAME VARCHAR(100) NOT NULL
);

-- Table: SOCIO_ECONOMIC_STATUS
CREATE TABLE SOCIO_ECONOMIC_STATUS (
                                       SOEC_ID SERIAL PRIMARY KEY,
                                       SOEC_STATUS VARCHAR(100) NOT NULL CHECK (
                                           SOEC_STATUS IN ('NHTS', 'Non-NHTS', 'Other')
                                           ),
                                       SOEC_NUMBER VARCHAR(50),
                                       CONSTRAINT chk_socio_status CHECK (
                                           (SOEC_STATUS IN ('NHTS 4Ps', 'NHTS Non-4Ps') AND SOEC_NUMBER IS NOT NULL) OR
                                           (SOEC_STATUS = 'Non-NHTS' AND SOEC_NUMBER IS NULL)
                                           )
);

CREATE TYPE blood_type_enum AS ENUM(
    'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
    );
CREATE TYPE civil_status_type AS ENUM(
    'Single', 'Married', 'Widowed', 'Separated'
    );

CREATE SEQUENCE SYS_USER_ID_SEQ START 1001;
CREATE TYPE role_type_enum AS ENUM(
    'Staff',
    'Admin',
    'Super Admin'
    );



-- Table: WATER_SOURCE
CREATE TABLE WATER_SOURCE(
                             WATER_ID SERIAL PRIMARY KEY,
                             WATER_SOURCE_NAME VARCHAR(50) NOT NULL
);

-- Table: WATER_SOURCE
CREATE TABLE TOILET_TYPE(
                            TOIL_ID SERIAL PRIMARY KEY,
                            TOIL_TYPE_NAME VARCHAR(50) NOT NULL
);

-- Table: RELATIONSHIP_TYPE
CREATE TABLE RELATIONSHIP_TYPE (
                                   RTH_ID SERIAL PRIMARY KEY,
                                   RTH_RELATIONSHIP_NAME VARCHAR(100)
);

-- Table: EDUCATIONAL_ATTAINMENT
CREATE TABLE EDUCATIONAL_ATTAINMENT (
                                        EDAT_ID SERIAL PRIMARY KEY,
                                        EDAT_LEVEL VARCHAR(100)
);



CREATE SEQUENCE SYS_CTZ_ID_SEQ START 1001;

=
-- Table: INFRASTRUCTURE_TYPE
CREATE TABLE INFRASTRUCTURE_TYPE (
                                     INFT_ID SERIAL PRIMARY KEY,
                                     INFT_TYPE_NAME VARCHAR(100) NOT NULL
);



-- Table: FAMILY_PLANNING_METHOD
CREATE TABLE FAMILY_PLANNING_METHOD (
                                        FPM_ID SERIAL PRIMARY KEY,
                                        FPM_METHOD VARCHAR(100)
);

-- Table: FPM_STATUS
CREATE TABLE FPM_STATUS (
                            FPMS_ID SERIAL PRIMARY KEY,
                            FPMS_STATUS_NAME VARCHAR(100)
);


--
-- -- Table: BUSINESS_ADDRESS
-- CREATE TABLE BUSINESS_ADDRESS (
--     BA_ID SERIAL PRIMARY KEY,
--     BA_POSTAL_CODE VARCHAR(20),
--     BA_PROVINCE VARCHAR(100),
--     BA_MUNICIPALITY VARCHAR(100),
--     BA_BARANGAY VARCHAR(100),
--     BA_SITIO_PUROK VARCHAR(100),
--     BA_STREET VARCHAR(255)
-- );
--
CREATE TABLE BUSINESS_OWNER(
                               BSO_ID SERIAL PRIMARY KEY,
                               BSO_FNAME VARCHAR(50) NOT NULL,
                               BSO_LNAME VARCHAR(50) NOT NULL,
                               BSO_MI CHAR(1)
);

CREATE TABLE BUSINESS_TYPE(
                              BST_ID INT PRIMARY KEY,
                              BST_TYPE_NAME VARCHAR(100) NOT NULL
);

CREATE TYPE business_status_enum AS ENUM(
    'ACTIVE',
    'INACTIVE',
    'CLOSED',
    'SUSPENDED'
    );
--

-- Table: EMPLOYMENT_STATUS
CREATE TABLE EMPLOYMENT_STATUS (
                                   ES_ID SERIAL PRIMARY KEY,
                                   ES_STATUS_NAME VARCHAR(100)
);

-- Table: TRANSACTION_TYPE
CREATE TABLE TRANSACTION_TYPE (
                                  TT_ID SERIAL PRIMARY KEY,
                                  TT_TYPE_NAME VARCHAR(100) NOT NULL
);

CREATE TYPE transaction_status_enum AS ENUM(
    'Pending',
    'Approved',
    'Rejected'
    );


CREATE TYPE action_type_enum AS ENUM (
    'INSERT',
    'UPDATE',
    'DELETE',
    'LOGIN',
    'LOGOUT'
    );


-- Table: MEDICAL_HISTORY_TYPE
CREATE TABLE MEDICAL_HISTORY_TYPE(
                                     MHT_ID SERIAL PRIMARY KEY,
                                     MHT_TYPE_NAME VARCHAR(100) NOT NULL
);

-- Table: PHILHEALTH_CATEGORY
CREATE TABLE PHILHEALTH_CATEGORY (
                                     PC_ID SERIAL PRIMARY KEY,
                                     PC_CATEGORY_NAME VARCHAR(100) NOT NULL
);

-- Table: HISTORY_TYPE
CREATE TABLE HISTORY_TYPE (
                              HIST_ID SERIAL PRIMARY KEY,
                              HIST_TYPE_NAME VARCHAR(100) NOT NULL
);


CREATE TABLE COMPLAINANT(
                            COMP_ID SERIAL PRIMARY KEY,
                            COMP_FNAME VARCHAR(50) NOT NULL,
                            COMP_LNAME VARCHAR(50) NOT NULL,
                            COMP_MI CHAR(1)
);


-- TABLES WITH FOREIGN KEYS

-- Table: BARANGAY_EMPLOYEE

-- Table: SYSTEM_ACCOUNT
CREATE TABLE SYSTEM_ACCOUNT (
                                SYS_ID SERIAL PRIMARY KEY,
                                SYS_USER_ID INT UNIQUE DEFAULT NEXTVAL('SYS_USER_ID_SEQ'),
                                SYS_PIN VARCHAR(6) NOT NULL,
                                SYS_ROLE_NAME role_type_enum NOT NULL,
                                SYS_IS_ACTIVE BOOLEAN DEFAULT TRUE,
                                SYS_DATE_ENCODED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                BE_ID INT,
                                CONSTRAINT FK_BE FOREIGN KEY (BE_ID) REFERENCES BARANGAY_EMPLOYEE(BE_ID) ON DELETE SET NULL,
                                CONSTRAINT chk_role_type CHECK (
                                    (SYS_ROLE_NAME = 'Super Admin' AND BE_ID IS NULL) OR
                                    (SYS_ROLE_NAME = 'Staff' AND BE_ID IS NOT NULL) OR
                                    (SYS_ROLE_NAME = 'Admin' AND BE_ID IS NOT NULL)
                                    )
);


CREATE TABLE BARANGAY_EMPLOYEE (
                                   BE_ID SERIAL PRIMARY KEY,
                                   BE_POSITION VARCHAR(100) NOT NULL,
                                   BE_START_DATE DATE NOT NULL,
                                   BE_END_DATE DATE,
                                   CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID)
);

-- Table: CITIZEN
CREATE TABLE CITIZEN (
                         CTZ_ID SERIAL PRIMARY KEY,
                         CTZ_UUID INT UNIQUE DEFAULT NEXTVAL('SYS_CTZ_ID_SEQ'),
                         CTZ_FIRST_NAME VARCHAR(100) NOT NULL,
                         CTZ_MIDDLE_NAME VARCHAR(100),
                         CTZ_LAST_NAME VARCHAR(100) NOT NULL,
                         CTZ_SUFFIX VARCHAR(10),
                         CTZ_DATE_OF_BIRTH DATE NOT NULL,
                         CTZ_SEX CHAR(1) NOT NULL CHECK(
                             CTZ_SEX IN ('M', 'F')
                             ),
                         CTZ_CIVIL_STATUS civil_status_type NOT NULL,
                         CTZ_BLOOD_TYPE blood_type_enum,
                         CTZ_IS_ALIVE BOOLEAN DEFAULT TRUE,
                         CTZ_IS_REGISTERED_VOTER BOOLEAN DEFAULT FALSE,
                         CTZ_IS_IP BOOLEAN DEFAULT FALSE,
                         CTZ_PLACE_OF_BIRTH TEXT NOT NULL,
                         CTZ_DATE_ENCODED DATE DEFAULT CURRENT_DATE,
                         SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                         EDU_ID INT REFERENCES EDUCATION_STATUS(EDU_ID),
                         SOEC_ID INT NOT NULL REFERENCES SOCIO_ECONOMIC_STATUS(SOEC_ID),
                         PHEA_ID INT REFERENCES PHILHEALTH(PHEA_ID),
                         REL_ID INT REFERENCES RELIGION(REL_ID),
                         ETH_ID INT REFERENCES ETHNICITY(ETH_ID),
                         CLA_ID INT NOT NULL REFERENCES CLASSIFICATION(CLA_ID),
                         RTH_ID INT NOT NULL REFERENCES RELATIONSHIP_TYPE(RTH_ID),
                         HH_ID INT NOT NULL REFERENCES HOUSEHOLD_INFO(HH_ID),
                         SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
                         CONSTRAINT chk_ethnicity CHECK(
                             (CTZ_IS_IP = TRUE AND ETH_ID IS NOT NULL) OR
                             (CTZ_IS_IP = FALSE AND ETH_ID IS NULL)
                             )
);





-- Table: SETTLEMENT_LOG
CREATE TABLE SETTLEMENT_LOG(
                               SETT_ID SERIAL PRIMARY KEY,
                               SETT_COMPLAINT_DESCRIPTION TEXT NOT NULL,
                               SETT_SETTLEMENT_DESCRIPTION TEXT NOT NULL,
                               COMP_ID INT NOT NULL REFERENCES COMPLAINANT(COMP_ID),
                               CIHI_ID INT NOT NULL REFERENCES CITIZEN_HISTORY(CIHI_ID)
);


-- Table: CLASSIFICATION (Age/Risk)
CREATE TABLE CLASSIFICATION (
                                CLA_ID SERIAL PRIMARY KEY,
                                CLAG_ID INT REFERENCES CLASSIFICATION_AGE(CLAG_ID),
                                CLAH_ID INT REFERENCES CLASSIFICATION_HEALTH_RISK(CLAH_ID)
);

-- Table: HOUSEHOLD_INFO
CREATE TABLE HOUSEHOLD_INFO (
                                HH_ID SERIAL PRIMARY KEY,
                                HH_HOUSE_NUMBER VARCHAR(50) UNIQUE NOT NULL,
                                HH_ADDRESS TEXT,
                                HH_OWNERSHIP_STATUS VARCHAR(50),
                                HH_HOME_IMAGE TEXT NOT NULL,
                                HH_HOME_LINK TEXT NOT NULL,
                                WATER_ID INT NOT NULL REFERENCES  WATER_SOURCE(WATER_ID),
                                TOILET_TYPE INT NOT NULL REFERENCES TOILET_TYPE(TOIL_ID),
                                SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
                                CONSTRAINT chk_valid_home_link CHECK(
                                    HH_HOME_LINK ~ 'https?://[^\s/$.?#].[^\s]*$]' AND
                                    length(HH_HOME_LINK) <= 1024 AND
                                    HH_HOME_LINK !~ '[<>''"\s]'
                                    )
);

-- Table: EDUCATION_STATUS
CREATE TABLE EDUCATION_STATUS (
                                  EDU_ID SERIAL PRIMARY KEY,
                                  EDU_IS_CURRENTLY_STUDENT BOOLEAN,
                                  EDU_INSTITUTION_NAME VARCHAR(255),
                                  EDAT_ID INT REFERENCES EDUCATIONAL_ATTAINMENT(EDAT_ID)
);

-- Table: CITIZEN_HISTORY
CREATE TABLE CITIZEN_HISTORY (
                                 CIHI_ID SERIAL PRIMARY KEY,
                                 CIHI_DESCRIPTION VARCHAR(100) NOT NULL,
                                 CIHI_DATE_ENCODED DATE DEFAULT CURRENT_DATE,
                                 HIST_ID INT NOT NULL REFERENCES HISTORY_TYPE(HIST_ID),
                                 CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID),
                                 SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID)
);

-- Table: PHILHEALTH
CREATE TABLE PHILHEALTH (
                            PHEA_ID SERIAL PRIMARY KEY,
                            PHEA_ID_NUMBER VARCHAR(50) UNIQUE NOT NULL,
                            PHEA_MEMBERSHIP_TYPE VARCHAR(50) CHECK(
                                PHEA_MEMBERSHIP_TYPE IN (
                                                         'Member',
                                                         'Dependent'
                                    )
                                ),
                            PC_ID INT NOT NULL REFERENCES PHILHEALTH_CATEGORY(PC_ID)
);


-- Table: CONTACT
CREATE TABLE CONTACT (
                         CON_ID SERIAL PRIMARY KEY,
                         CON_PHONE VARCHAR(20) UNIQUE NOT NULL,
                         CON_EMAIL VARCHAR(100) UNIQUE NOT NULL,
                         CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID)
);

-- Table: INFRASTRUCTURE_OWNER
CREATE TABLE INFRASTRUCTURE_OWNER (
                                      INFO_ID SERIAL PRIMARY KEY,
                                      INFO_LAST_NAME VARCHAR(100) NOT NULL,
                                      INFO_FIRST_NAME VARCHAR(100) NOT NULL,
                                      INFO_MI VARCHAR(100),
                                      CTZ_ID INT REFERENCES CITIZEN(CTZ_ID)
);


-- Table: INFRASTRUCTURE
CREATE TABLE INFRASTRUCTURE (
                                INF_ID SERIAL PRIMARY KEY,
                                INF_NAME VARCHAR(100) NOT NULL,
                                INF_ACCESS_TYPE VARCHAR(10) NOT NULL CHECK ( INF_ACCESS_TYPE IN ('Public', 'Private')),
                                INF_DESCRIPTION TEXT,
                                INF_ADDRESS_DESCRIPTION TEXT,
                                INF_DATE_REGISTERED DATE NOT NULL,
                                INFT_ID INT NOT NULL REFERENCES INFRASTRUCTURE_TYPE(INFT_ID),
                                INFO_ID INT REFERENCES INFRASTRUCTURE_OWNER(INFO_ID),
                                SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
                                CONSTRAINT chk_access_type CHECK (
                                    (INF_ACCESS_TYPE = 'Private' AND INFO_ID IS NOT NULL) OR
                                    (INF_ACCESS_TYPE = 'Public' AND INFO_ID IS NULL)
                                    )
);

-- Table: FAMILY_PLANNING
CREATE TABLE FAMILY_PLANNING (
                                 FP_ID SERIAL PRIMARY KEY,
                                 FP_START_DATE DATE,
                                 FP_END_DATE DATE,
                                 CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID),
                                 FPMS_STATUS INT NOT NULL REFERENCES FPM_STATUS(FPMS_ID),
                                 FPM_METHOD INT NOT NULL REFERENCES FAMILY_PLANNING_METHOD(FPM_ID)
);

-- Table: BUSINESS_INFO
CREATE TABLE BUSINESS_INFO (
                               BS_ID SERIAL PRIMARY KEY,
                               BS_NAME VARCHAR(100) NOT NULL,
                               BS_DESCRIPTION TEXT NOT NULL,
                               BS_STATUS business_status_enum NOT NULL,
                               BS_IS_DTI BOOLEAN NOT NULL,
                               BS_DTI_IMAGE TEXT,
                               BS_ADDRESS TEXT NOT NULL,
                               BS_DATE_ENCODED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               BST_ID INT NOT NULL REFERENCES BUSINESS_TYPE(BST_ID),
                               BSO_ID INT NOT NULL REFERENCES BUSINESS_OWNER(BSO_ID),
                               SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                               CONSTRAINT chk_is_dti CHECK(
                                   (BS_IS_DTI = TRUE AND BS_DTI_IMAGE IS NOT NULL) OR
                                   (BS_IS_DTI = FALSE AND BS_DTI_IMAGE IS NULL)
                                   )
);

-- Table: EMPLOYMENT
CREATE TABLE EMPLOYMENT (
                            EMP_ID SERIAL PRIMARY KEY,
                            EMP_OCCUPATION VARCHAR(100) NOT NULL,
                            EMP_IS_GOV_WORKER BOOLEAN DEFAULT FALSE,
                            ES_ID INT REFERENCES EMPLOYMENT_STATUS(ES_ID),
                            CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID)
);


-- Table: TRANSACTION_LOG
CREATE TABLE TRANSACTION_LOG (
                                 TL_ID SERIAL PRIMARY KEY,
                                 TL_DATE_REQUESTED DATE DEFAULT CURRENT_DATE,
                                 TL_PURPOSE VARCHAR(150) NOT NULL,
                                 TL_STATUS transaction_status_enum,
                                 TL_FNAME VARCHAR(50) NOT NULL,
                                 TL_LANME VARCHAR(50) NOT NULL,
                                 TL_DATE_ENCODED DATE DEFAULT CURRENT_DATE,
                                 TT_ID INT NOT NULL REFERENCES TRANSACTION_TYPE(TT_ID),
                                 SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID)
);


-- Table: CITIZEN_INTERVIEW
CREATE TABLE CITIZEN_INTERVIEW (
                                   CIN_ID SERIAL PRIMARY KEY,
                                   CIN_DATE_INTERVIEWED DATE,
                                   CIN_DATE_REVIEWED DATE,
                                   BE_INTERVIEWER_ID INT NOT NULL REFERENCES BARANGAY_EMPLOYEE(BE_ID),
                                   BE_REVIEWER_ID INT REFERENCES BARANGAY_EMPLOYEE(BE_ID),
                                   CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID)
);


-- Table: SYSTEM_ACTIVITY_LOG
CREATE TABLE SYSTEM_ACTIVITY_LOG (
                                     ACT_ID SERIAL PRIMARY KEY,
                                     ACT_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                     ACT_ACTION_TYPE action_type_enum NOT NULL,
                                     ACT_TABLE_NAME VARCHAR(50) NOT NULL,
                                     ACT_ENTITY_ID INT NOT NULL,
                                     ACT_DESCRIPTION TEXT,
                                     SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID)

);

-- Table: MEDICAL_HISTORY
CREATE TABLE MEDICAL_HISTORY (
                                 MH_ID SERIAL PRIMARY KEY,
                                 MH_DATE_DIAGNOSED DATE,
                                 MH_DATE_ENCODED DATE DEFAULT CURRENT_DATE,
                                 MHT_ID INT NOT NULL REFERENCES MEDICAL_HISTORY_TYPE(MHT_ID),
                                 CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID),
                                 SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID)
);


-- TRIGGER FUNCTIONS

CREATE OR REPLACE FUNCTION is_reproductive_age_female(dob DATE, sex CHAR(1))
    RETURNS BOOLEAN AS $$
BEGIN
    RETURN sex = 'F' AND
           EXTRACT(YEAR FROM AGE(dob)) BETWEEN 15 AND 49;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_reproductive_age_trigger()
    RETURNS TRIGGER AS $$
DECLARE
    dob DATE;
    sex CHAR(1);
BEGIN
    SELECT CTZ_DATE_OF_BIRTH, CTZ_SEX INTO dob, sex
    FROM CITIZEN WHERE CTZ_ID = NEW.CTZ_ID;

    IF NOT is_reproductive_age_female(dob, sex) THEN
        RAISE EXCEPTION 'Citizen is not a female of reproductive age (15-49).';
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_is_reproductive_age
    BEFORE INSERT OR UPDATE ON FAMILY_PLANNING
    FOR EACH ROW
EXECUTE FUNCTION check_reproductive_age_trigger();





--INSERTS

-- SUPER ADMIN

INSERT INTO SYSTEM_ACCOUNT(
    SYS_USER_ID, SYS_PIN, SYS_ROLE_NAME, SYS_IS_ACTIVE, BE_ID
) VALUES
      (00001,'000000', 'Super Admin', TRUE,NULL),
      (00002,'000000', 'Super Admin', TRUE,NULL),
      (00003,'000000', 'Super Admin', TRUE,NULL);










--
--
-- INSERT INTO CITIZEN (
--     CTZ_ID, CTZ_FIRST_NAME, CTZ_LAST_NAME, CTZ_DATE_OF_BIRTH, CTZ_SEX, CTZ_IS_ALIVE, CTZ_IS_REGISTERED_VOTER
-- ) VALUES
--       (1,'John', 'Cena', '2000-08-21', 'Male', TRUE, TRUE),
--       (2,'Ryan', 'Bang', '1999-08-21', 'Male', TRUE, TRUE);
--
-- INSERT INTO BARANGAY_EMPLOYEE (
--     BE_ID, BE_POSITION, BE_START_DATE, CTZ_ID
-- ) VALUES
--       (1,'Data Encoder', '2024-02-15', 1),
--       (2,'Data Encoder', '2024-02-15', 2);
--
-- INSERT INTO SYSTEM_ACCOUNT (
--     SYS_PIN, SYS_IS_ADMIN, SYS_IS_ACTIVE, BE_ID
-- ) VALUES
--       ('000002', TRUE, TRUE, 1),
--       ('000003', TRUE, TRUE, 2);
--

