-- Database; marigondon_profiling_db
CREATE DATABASE marigondon_profiling_db;
--

CREATE SEQUENCE SYS_USER_ID_SEQ START 1001;
CREATE TYPE role_type_enum AS ENUM(
    'Staff',
    'Admin',
    'Super Admin'
    );

CREATE TABLE SYSTEM_ACCOUNT (
                                SYS_ID SERIAL PRIMARY KEY,
                                SYS_USER_ID INT UNIQUE DEFAULT NEXTVAL('SYS_USER_ID_SEQ'),
                                SYS_PIN VARCHAR(6) NOT NULL,
                                SYS_FIRSTNAME VARCHAR(50) NOT NULL,
                                SYS_MIDDLENAME VARCHAR(50),
                                SYS_LASTNAME VARCHAR(50) NOT NULL,
                                SYS_ROLE role_type_enum NOT NULL
);



-- Table: SITIO
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
-- Table: CLASSIFICATION (Age/Risk)
CREATE TABLE CLASSIFICATION (
                                CLA_ID SERIAL PRIMARY KEY,
                                CLAG_ID INT REFERENCES CLASSIFICATION_AGE(CLAG_ID),
                                CLAH_ID INT REFERENCES CLASSIFICATION_HEALTH_RISK(CLAH_ID)
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
                                           SOEC_STATUS IN ('NHTS 4Ps', 'NHTS Non-4Ps','Non-NHTS')
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

--UNCOMMENT LATER IF NEED JUD
-- CREATE TABLE INTERVIEWER (
--                              INTER_ID SERIAL PRIMARY KEY,
--                              INTER_FNAME VARCHAR(50) NOT NULL,
--                              INTER_LNAME VARCHAR(50) NOT NULL,
--                              INTER_MNAME VARCHAR(50)
-- );
--
-- CREATE TABLE REVIEWER (
--                           REV_ID SERIAL PRIMARY KEY,
--                           REV_FNAME VARCHAR(50) NOT NULL,
--                           REV_LNAME VARCHAR(50) NOT NULL,
--                           REV_MNAME VARCHAR(50)
-- );
--
--
-- -- Table: CITIZEN_INTERVIEW
-- CREATE TABLE CITIZEN_INTERVIEW (
--                                    CIN_ID SERIAL PRIMARY KEY,
--                                    INTER_ID INT NOT NULL REFERENCES INTERVIEWER(INTER_ID),
--                                    REV_ID INT NOT NULL REFERENCES REVIEWER(REV_ID)
-- );



-- Table: HOUSEHOLD_INFO
CREATE TABLE HOUSEHOLD_INFO (
                                HH_ID SERIAL PRIMARY KEY,
                                HH_HOUSE_NUMBER VARCHAR(50) UNIQUE NOT NULL,
                                HH_ADDRESS TEXT,
                                HH_OWNERSHIP_STATUS VARCHAR(50),
                                HH_HOME_IMAGE TEXT NOT NULL,
                                HH_HOME_LINK TEXT NOT NULL,
                                HH_INTERVIEWER_NAME VARCHAR(100) NOT NULL,
                                HH_REVIEWER_NAME VARCHAR(100) NOT NULL,
                                HH_DATE_VISIT DATE NOT NULL,
                                HH_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                HH_IS_DELETED BOOLEAN DEFAULT FALSE,
                                HH_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                                HH_DELETE_REQ_REASON TEXT,
                                WATER_ID INT NOT NULL REFERENCES  WATER_SOURCE(WATER_ID),
                                TOILET_TYPE INT NOT NULL REFERENCES TOILET_TYPE(TOIL_ID),
                                SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
                                CONSTRAINT chk_valid_home_link CHECK(
                                    HH_HOME_LINK ~ 'https?://[^\s/$.?#].[^\s]*$]' AND
                                    length(HH_HOME_LINK) <= 1024 AND
                                    HH_HOME_LINK !~ '[<>''"\s]'
),
    CONSTRAINT chk_pending_delete CHECK (
        (HH_IS_PENDING_DELETE = TRUE AND HH_DELETE_REQ_REASON IS NOT NULL) OR
        (HH_IS_PENDING_DELETE = FALSE AND HH_DELETE_REQ_REASON IS NULL)
        )
);

-- Table: EDUCATIONAL_ATTAINMENT
CREATE TABLE EDUCATIONAL_ATTAINMENT (
                                        EDAT_ID SERIAL PRIMARY KEY,
                                        EDAT_LEVEL VARCHAR(100)
);

-- Table: EDUCATION_STATUS
CREATE TABLE EDUCATION_STATUS (
                                  EDU_ID SERIAL PRIMARY KEY,
                                  EDU_IS_CURRENTLY_STUDENT BOOLEAN,
                                  EDU_INSTITUTION_NAME VARCHAR(255),
                                  EDAT_ID INT REFERENCES EDUCATIONAL_ATTAINMENT(EDAT_ID)
);

-- Table: PHILHEALTH_CATEGORY
CREATE TABLE PHILHEALTH_CATEGORY (
                                     PC_ID SERIAL PRIMARY KEY,
                                     PC_CATEGORY_NAME VARCHAR(100) NOT NULL
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

CREATE SEQUENCE SYS_CTZ_ID_SEQ START 1001;

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
                         CTZ_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         CTZ_IS_DELETED BOOLEAN DEFAULT FALSE,
                         CTZ_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                         CTZ_DELETE_REQ_REASON TEXT,
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
                             ),
                         CONSTRAINT chk_pending_delete CHECK (
                             (CTZ_IS_PENDING_DELETE = FALSE) OR
                             (CTZ_IS_PENDING_DELETE = TRUE AND CTZ_DELETE_REQ_REASON IS NOT NULL)
                             )
);


-- Table: CONTACT
CREATE TABLE CONTACT (
                         CON_ID SERIAL PRIMARY KEY,
                         CON_PHONE VARCHAR(20) UNIQUE NOT NULL,
                         CON_EMAIL VARCHAR(100) UNIQUE NOT NULL,
                         CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID)
);

-- Table: INFRASTRUCTURE_TYPE
CREATE TABLE INFRASTRUCTURE_TYPE (
                                     INFT_ID SERIAL PRIMARY KEY,
                                     INFT_TYPE_NAME VARCHAR(100) NOT NULL
);

-- Table: INFRASTRUCTURE_OWNER
CREATE TABLE INFRASTRUCTURE_OWNER (
                                      INFO_ID SERIAL PRIMARY KEY,
                                      INFO_LNAME VARCHAR(100) NOT NULL,
                                      INFO_FNAME VARCHAR(100) NOT NULL,
                                      INFO_MNAME VARCHAR(100),
                                      CTZ_ID INT REFERENCES CITIZEN(CTZ_ID)
);

-- Table: INFRASTRUCTURE
CREATE TABLE INFRASTRUCTURE (
                                INF_ID SERIAL PRIMARY KEY,
                                INF_NAME VARCHAR(100) NOT NULL,
                                INF_ACCESS_TYPE VARCHAR(10) NOT NULL CHECK ( INF_ACCESS_TYPE IN ('Public', 'Private')),
                                INF_DESCRIPTION TEXT,
                                INF_ADDRESS_DESCRIPTION TEXT,
                                INF_DATE_ENCODED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                INF_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                INF_IS_DELETED BOOLEAN DEFAULT FALSE,
                                INF_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                                INF_DELETE_REQ_REASON TEXT,
                                INFT_ID INT NOT NULL REFERENCES INFRASTRUCTURE_TYPE(INFT_ID),
                                INFO_ID INT REFERENCES INFRASTRUCTURE_OWNER(INFO_ID),
                                SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
                                CONSTRAINT chk_access_type CHECK (
                                    (INF_ACCESS_TYPE = 'Private' AND INFO_ID IS NOT NULL) OR
                                    (INF_ACCESS_TYPE = 'Public' AND INFO_ID IS NULL)
                                    ),
                                CONSTRAINT chk_pending_delete CHECK (
                                    (INF_IS_PENDING_DELETE = FALSE) OR
                                    (INF_IS_PENDING_DELETE = TRUE AND INF_DELETE_REQ_REASON IS NOT NULL)
                                    )
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

-- Table: FAMILY_PLANNING
CREATE TABLE FAMILY_PLANNING (
                                 FP_ID SERIAL PRIMARY KEY,
                                 FP_START_DATE DATE,
                                 FP_END_DATE DATE,
                                 CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID),
                                 FPMS_STATUS INT NOT NULL REFERENCES FPM_STATUS(FPMS_ID),
                                 FPM_METHOD INT NOT NULL REFERENCES FAMILY_PLANNING_METHOD(FPM_ID)
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
                               BS_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               BS_IS_DELETED BOOLEAN DEFAULT FALSE,
                               BS_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                               BS_DELETE_REQ_REASON TEXT,
                               BST_ID INT NOT NULL REFERENCES BUSINESS_TYPE(BST_ID),
                               BSO_ID INT NOT NULL REFERENCES BUSINESS_OWNER(BSO_ID),
                               SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                               CONSTRAINT chk_is_dti CHECK(
                                   (BS_IS_DTI = TRUE AND BS_DTI_IMAGE IS NOT NULL) OR
                                   (BS_IS_DTI = FALSE AND BS_DTI_IMAGE IS NULL)
                                   ),
                               CONSTRAINT chk_pending_delete CHECK (
                                   (BS_IS_PENDING_DELETE = FALSE) OR
                                   (BS_IS_PENDING_DELETE = TRUE AND BS_DELETE_REQ_REASON IS NOT NULL)
                                   )
);



-- Table: EMPLOYMENT_STATUS
CREATE TABLE EMPLOYMENT_STATUS (
                                   ES_ID SERIAL PRIMARY KEY,
                                   ES_STATUS_NAME VARCHAR(100)
);

-- Table: EMPLOYMENT
CREATE TABLE EMPLOYMENT (
                            EMP_ID SERIAL PRIMARY KEY,
                            EMP_OCCUPATION VARCHAR(100) NOT NULL,
                            EMP_IS_GOV_WORKER BOOLEAN DEFAULT FALSE,
                            ES_ID INT REFERENCES EMPLOYMENT_STATUS(ES_ID),
                            CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID)
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

-- Table: TRANSACTION_LOG
CREATE TABLE TRANSACTION_LOG (
                                 TL_ID SERIAL PRIMARY KEY,
                                 TL_DATE_REQUESTED DATE DEFAULT CURRENT_DATE,
                                 TL_PURPOSE VARCHAR(150) NOT NULL,
                                 TL_STATUS transaction_status_enum,
                                 TL_FNAME VARCHAR(50) NOT NULL,
                                 TL_LANME VARCHAR(50) NOT NULL,
                                 TL_DATE_ENCODED DATE DEFAULT CURRENT_DATE,
                                 TL_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                 TL_IS_DELETED BOOLEAN DEFAULT FALSE,
                                 TL_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                                 TL_DELETE_REQ_REASON TEXT,
                                 TT_ID INT NOT NULL REFERENCES TRANSACTION_TYPE(TT_ID),
                                 SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                                 CONSTRAINT chk_pending_delete CHECK (
                                     (TL_IS_PENDING_DELETE = FALSE) OR
                                     (TL_IS_PENDING_DELETE = TRUE AND TL_DELETE_REQ_REASON IS NOT NULL)
                                     )
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

-- Table: MEDICAL_HISTORY
CREATE TABLE MEDICAL_HISTORY (
                                 MH_ID SERIAL PRIMARY KEY,
                                 MH_DATE_DIAGNOSED DATE,
                                 MH_DATE_ENCODED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                 MH_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                 MH_IS_DELETED BOOLEAN DEFAULT FALSE,
                                 MH_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                                 MH_DELETE_REQ_REASON TEXT,
                                 MHT_ID INT NOT NULL REFERENCES MEDICAL_HISTORY_TYPE(MHT_ID),
                                 CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID),
                                 SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                                 CONSTRAINT chk_pending_delete CHECK (
                                     (MH_IS_PENDING_DELETE = FALSE) OR
                                     (MH_IS_PENDING_DELETE = TRUE AND MH_DELETE_REQ_REASON IS NOT NULL)
                                     )
);



-- Table: HISTORY_TYPE
CREATE TABLE HISTORY_TYPE (
                              HIST_ID SERIAL PRIMARY KEY,
                              HIST_TYPE_NAME VARCHAR(100) NOT NULL
);

-- Table: CITIZEN_HISTORY
CREATE TABLE CITIZEN_HISTORY (
                                 CIHI_ID SERIAL PRIMARY KEY,
                                 CIHI_DESCRIPTION VARCHAR(100) NOT NULL,
                                 CIHI_DATE_ENCODED DATE DEFAULT CURRENT_DATE,
                                 CIHI_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                 CIHI_IS_DELETED BOOLEAN DEFAULT FALSE,
                                 CIHI_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                                 CIHI_DELETE_REQ_REASON TEXT,
                                 HIST_ID INT NOT NULL REFERENCES HISTORY_TYPE(HIST_ID),
                                 CTZ_ID INT NOT NULL REFERENCES CITIZEN(CTZ_ID),
                                 SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                                 CONSTRAINT chk_pending_delete CHECK (
                                     (CIHI_IS_PENDING_DELETE = FALSE) OR
                                     (CIHI_IS_PENDING_DELETE = TRUE AND CIHI_DELETE_REQ_REASON IS NOT NULL)
                                     )
);


CREATE TABLE COMPLAINANT(
                            COMP_ID SERIAL PRIMARY KEY,
                            COMP_FNAME VARCHAR(50) NOT NULL,
                            COMP_LNAME VARCHAR(50) NOT NULL,
                            COMP_MNAME VARCHAR(50)
);

-- Table: SETTLEMENT_LOG
CREATE TABLE SETTLEMENT_LOG(
                               SETT_ID SERIAL PRIMARY KEY,
                               SETT_COMPLAINT_DESCRIPTION TEXT NOT NULL,
                               SETT_SETTLEMENT_DESCRIPTION TEXT NOT NULL,
                               SETT_DATE_OF_SETTLEMENT DATE NOT NULL,
                               SETT_DATE_ENCODED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               SETT_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               SETT_IS_DELETED BOOLEAN DEFAULT FALSE,
                               SETT_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                               SETT_DELETE_REQ_REASON TEXT,
                               COMP_ID INT NOT NULL REFERENCES COMPLAINANT(COMP_ID),
                               CIHI_ID INT NOT NULL REFERENCES CITIZEN_HISTORY(CIHI_ID),
                               CONSTRAINT chk_pending_delete CHECK (
                                   (SETT_IS_PENDING_DELETE = FALSE) OR
                                   (SETT_IS_PENDING_DELETE = TRUE AND SETT_DELETE_REQ_REASON IS NOT NULL)
                                   )
);



--TRIGGER FUNCTIONS

--SAMPLE
CREATE OR REPLACE FUNCTION update_last_updated()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.hh_last_updated = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_last_updated
    BEFORE UPDATE ON HOUSEHOLD_INFO
    FOR EACH ROW
    EXECUTE FUNCTION update_last_updated();

CREATE TRIGGER set_last_updated
    BEFORE UPDATE ON CITIZEN
    FOR EACH ROW
    EXECUTE FUNCTION update_last_updated();



--INSERTS

-- INSERT SYSTEM_ACCOUNT
INSERT INTO SYSTEM_ACCOUNT (SYS_USER_ID, SYS_PIN, SYS_FIRSTNAME, SYS_MIDDLENAME, SYS_LASTNAME, SYS_ROLE)
VALUES (2,123,Joehanes,)