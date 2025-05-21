
-- CREATE DATABASE marigondon_profiling_db;

CREATE TABLE DEPARTMENT(
    DEP_ID SERIAL PRIMARY KEY,
    DEP_DEPARTMENT_NAME VARCHAR(100) NOT NULL
);

CREATE SEQUENCE SYS_USER_ID_SEQ START 1001;

CREATE TYPE role_type_enum AS ENUM(
    'Staff',
    'Admin',
    'Super Admin'
    );

CREATE TYPE permission_type_enum AS ENUM(
    'View',
    'Create',
    'Update',
    'Delete'
    );

CREATE TABLE SYSTEM_ACCOUNT (
                                SYS_ID SERIAL PRIMARY KEY,
                                SYS_USER_ID INT UNIQUE DEFAULT NEXTVAL('SYS_USER_ID_SEQ'),
                                SYS_PASSWORD VARCHAR(6) NOT NULL,
                                SYS_FNAME VARCHAR(50) NOT NULL,
                                SYS_MNAME VARCHAR(50),
                                SYS_LNAME VARCHAR(50) NOT NULL,
                                SYS_ROLE role_type_enum,
                                SYS_PERMISSION_TYPE permission_type_enum,
                                SYS_IS_ACTIVE BOOLEAN DEFAULT TRUE,
                                SYS_DATE_ENCODED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                DEP_ID INT REFERENCES DEPARTMENT(DEP_ID) ON DELETE CASCADE,
                                CONSTRAINT chk_superadmin_rule CHECK (
                                    (
                                        SYS_ROLE = 'Super Admin' AND
                                        SYS_PERMISSION_TYPE IS NULL AND
                                        DEP_ID IS NULL
                                        )
                                        OR
                                    (
                                        SYS_ROLE IN ('Admin', 'Staff') AND
                                        SYS_PERMISSION_TYPE IS NOT NULL AND
                                        DEP_ID IS NOT NULL
                                        )
                                    )

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


-- Table: HOUSEHOLD_INFO
CREATE TABLE HOUSEHOLD_INFO (
                                HH_ID SERIAL PRIMARY KEY,
                                HH_HOUSE_NUMBER VARCHAR(50) UNIQUE NOT NULL,
                                HH_ADDRESS TEXT,
                                HH_OWNERSHIP_STATUS VARCHAR(50),
                                HH_HOME_IMAGE_PATH TEXT NOT NULL,
                                HH_HOME_GOOGLE_LINK TEXT NOT NULL,
                                HH_INTERVIEWER_NAME VARCHAR(100) NOT NULL,
                                HH_REVIEWER_NAME VARCHAR(100) NOT NULL,
                                HH_DATE_VISIT DATE NOT NULL,
                                HH_LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                HH_IS_DELETED BOOLEAN DEFAULT FALSE,
                                HH_IS_PENDING_DELETE BOOLEAN DEFAULT FALSE,
                                HH_DELETE_REQ_REASON TEXT,
                                SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                                WATER_ID INT NOT NULL REFERENCES  WATER_SOURCE(WATER_ID),
                                TOILET_ID INT NOT NULL REFERENCES TOILET_TYPE(TOIL_ID),
                                SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
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
                         CTZ_DATE_OF_DEATH DATE,
                         CTZ_REASON_OF_DEATH TEXT,
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
                             ),
                         CONSTRAINT chk_is_alive CHECK (
                             (CTZ_IS_ALIVE = TRUE) OR
                             (CTZ_IS_ALIVE = FALSE AND CTZ_DATE_OF_DEATH IS NOT NULL AND CTZ_REASON_OF_DEATH IS NOT NULL)
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
                                      INFO_MNAME VARCHAR(100)
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
                                SYS_ID INT NOT NULL REFERENCES SYSTEM_ACCOUNT(SYS_ID),
                                INFT_ID INT NOT NULL REFERENCES INFRASTRUCTURE_TYPE(INFT_ID),
                                INFO_ID INT REFERENCES INFRASTRUCTURE_OWNER(INFO_ID),
                                SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
                                CONSTRAINT chk_access_type CHECK (
                                    (INF_ACCESS_TYPE = 'Private' AND INFO_ID IS NOT NULL) OR
                                    (INF_ACCESS_TYPE = 'Public' AND INFO_ID IS NOT NULL)
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
                               SITIO_ID INT NOT NULL REFERENCES SITIO(SITIO_ID),
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
    'Declined'
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

--AUTO UPDATE LAST UPDATED
CREATE OR REPLACE FUNCTION update_last_updated_citizen()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.CTZ_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_citizen_last_updated
    BEFORE UPDATE ON CITIZEN
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_citizen();



CREATE OR REPLACE FUNCTION update_last_updated_household()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.HH_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_household_last_updated
    BEFORE UPDATE ON HOUSEHOLD_INFO
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_household();



CREATE OR REPLACE FUNCTION update_last_updated_infrastructure()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.INF_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_infrastructure_last_updated
    BEFORE UPDATE ON INFRASTRUCTURE
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_infrastructure();



CREATE OR REPLACE FUNCTION update_last_updated_business()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.BS_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_business_last_updated
    BEFORE UPDATE ON BUSINESS_INFO
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_business();



CREATE OR REPLACE FUNCTION update_last_updated_transaction()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.TL_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_transaction_last_updated
    BEFORE UPDATE ON TRANSACTION_LOG
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_transaction();



CREATE OR REPLACE FUNCTION update_last_updated_medical()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.MH_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_medical_last_updated
    BEFORE UPDATE ON MEDICAL_HISTORY
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_medical();



CREATE OR REPLACE FUNCTION update_last_updated_citizen_history()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.CIHI_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_citizen_history_last_updated
    BEFORE UPDATE ON CITIZEN_HISTORY
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_citizen_history();



CREATE OR REPLACE FUNCTION update_last_updated_settlement()
    RETURNS TRIGGER AS $$
BEGIN
    NEW.SETT_LAST_UPDATED = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_settlement_last_updated
    BEFORE UPDATE ON MEDICAL_HISTORY
    FOR EACH ROW
EXECUTE FUNCTION update_last_updated_settlement();



--INSERTS


-- SUPER ADMIN
INSERT INTO SYSTEM_ACCOUNT(SYS_PASSWORD, SYS_FNAME, SYS_MNAME, SYS_LNAME, SYS_ROLE)
VALUES
    (000001, 'Ian','Neko', 'Majica','Super Admin');

INSERT INTO WATER_SOURCE(WATER_SOURCE_NAME)
VALUES
    ('Level 1 - Point Source'),
    ('Level 2 - Communal Faucet'),
    ('Level 3 - Individual Connection'),
    ('Others');

INSERT INTO TOILET_TYPE (TOIL_TYPE_NAME)
VALUES
    ('A - Pour/flush type connected to septic tank'),
    ('B - Pour/flush toilet connected to Sewerage System '),
    ('C - Ventilated Pit (VIP) latrine'),
    ('D - Water-sealed toilet'),
    ('E - Overhung latrine'),
    ('F - Open pit latrine'),
    ('E - G - Without toilet');

INSERT INTO SITIO(SITIO_NAME)
VALUES
        ('Sitio Uno'),
        ('Sitio Dos'),
        ('Sitio Tres');


INSERT INTO DEPARTMENT (DEP_DEPARTMENT_NAME)
VALUES
    ('Barangay Administration'),
    ('Health Services'),
    ('Social Welfare'),
    ('Public Safety'),
    ('Engineering');

INSERT INTO SYSTEM_ACCOUNT (
    SYS_PASSWORD,
    SYS_FNAME,
    SYS_MNAME,
    SYS_LNAME,
    SYS_ROLE,
    SYS_PERMISSION_TYPE,
    DEP_ID
) VALUES
        ('000001', 'Juan', 'Dela', 'Cruz', 'Super Admin', NULL, NULL),
        ('000002', 'Maria', 'Santos', 'Reyes', 'Admin', 'Create',
        (SELECT DEP_ID FROM DEPARTMENT WHERE DEP_DEPARTMENT_NAME = 'Barangay Administration'));


INSERT INTO CLASSIFICATION_AGE (CLAG_CLASSIFICATION_NAME)
VALUES
        ('Child (0-12)'),
        ('Adolescent (13-19)'),
        ('Adult (20-59)'),
        ('Senior Citizen (60+)');

INSERT INTO CLASSIFICATION_HEALTH_RISK (CLAH_CLASSIFICATION_NAME)
VALUES
        ('None'),
        ('Pregnant'),
        ('Adolescent Pregnant'),
        ('Postpartum'),
        ('Infant'),
        ('Under 5 Years Old'),
        ('Person With Disability');

INSERT INTO CLASSIFICATION (CLAG_ID, CLAH_ID)
VALUES
        (1, 1),
        (2, 6),
        (2, 2),
        (3, 1);

INSERT INTO RELATIONSHIP_TYPE (RTH_RELATIONSHIP_NAME)
VALUES
        ('Head'),
        ('Spouse'),
        ('Son'),
        ('Daughter'),
        ('Other Relative');

INSERT INTO RELIGION (REL_NAME)
VALUES
        ('Roman Catholic'),
        ('Islam'),
        ('Protestant'),
        ('Iglesia ni Cristo');

INSERT INTO SOCIO_ECONOMIC_STATUS (SOEC_STATUS, SOEC_NUMBER)
VALUES
        ('NHTS 4Ps', '123456'),
        ('NHTS Non-4Ps', '654321'),
        ('Non-NHTS', NULL);

INSERT INTO HOUSEHOLD_INFO (
    HH_HOUSE_NUMBER,
    HH_ADDRESS,
    HH_OWNERSHIP_STATUS,
    HH_HOME_IMAGE_PATH,
    HH_HOME_GOOGLE_LINK,
    HH_INTERVIEWER_NAME,
    HH_REVIEWER_NAME,
    HH_DATE_VISIT,
    SYS_ID,
    WATER_ID,
    TOILET_ID,
    SITIO_ID
) VALUES (
             'HM-2023-001',
             '123 Purok Santan, Barangay Marigondon',
             'Owned',
             'Assets/Register/HouseholdImages\Screenshot 2023-10-10 193121.png',
             'https://www.google.com/maps/place/Shell+Robinsons+Mobility+Station+-+Galleria+Cebu+City/@10.3024076,123.9108788,19.5z/data=!4m6!3m5!1s0x33a999f29f761867:0x51e0d3123523c12a!8m2!3d10.3025851!4d123.9110295!16s%2Fg%2F11rrs0pzvl?authuser=0&entry=ttu&g_ep=EgoyMDI1MDQzMC4xIKXMDSoASAFQAw%3D%3D',
             'Juan Dela Cruz',
             'Maria Reyes',
             CURRENT_DATE,
             (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_ID = 1),
             (SELECT WATER_ID FROM WATER_SOURCE WHERE WATER_SOURCE_NAME = 'Level 3 - Individual Connection'),
             (SELECT TOIL_ID FROM TOILET_TYPE WHERE TOIL_TYPE_NAME = 'A - Pour/flush type connected to septic tank'),
             (SELECT SITIO_ID FROM SITIO WHERE SITIO_NAME = 'Sitio Uno')
         );


INSERT INTO CITIZEN (
    CTZ_FIRST_NAME,
    CTZ_MIDDLE_NAME,
    CTZ_LAST_NAME,
    CTZ_DATE_OF_BIRTH,
    CTZ_SEX,
    CTZ_CIVIL_STATUS,
    CTZ_BLOOD_TYPE,
    CTZ_PLACE_OF_BIRTH,
    SYS_ID,
    SOEC_ID,
    REL_ID,
    CLA_ID,
    RTH_ID,
    HH_ID,
    SITIO_ID
) VALUES (
             'Roberto',
             'Santos',
             'Gonzales',
             '1980-05-15',
             'M',
             'Married',
             'O+',
             'Cebu City',
             (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_ID = '1' ),
             (SELECT SOEC_ID FROM SOCIO_ECONOMIC_STATUS WHERE SOEC_STATUS = 'NHTS 4Ps'),
             (SELECT REL_ID FROM RELIGION WHERE REL_NAME = 'Roman Catholic'),
             (SELECT CLA_ID FROM CLASSIFICATION WHERE CLAG_ID = 3 AND CLAH_ID = 1),
             (SELECT RTH_ID FROM RELATIONSHIP_TYPE WHERE RTH_RELATIONSHIP_NAME = 'Head'),
             (SELECT HH_ID FROM HOUSEHOLD_INFO WHERE HH_HOUSE_NUMBER = 'HM-2023-001'),
             (SELECT SITIO_ID FROM SITIO WHERE SITIO_NAME = 'Sitio Uno')
         );

-- INFRASTRUCTURE
INSERT INTO INFRASTRUCTURE_TYPE (INFT_TYPE_NAME)
VALUES
        ('Barangay Hall'),
        ('Health Center'),
        ('Daycare Center'),
        ('Basketball Court');

INSERT INTO INFRASTRUCTURE_OWNER (INFO_LNAME, INFO_FNAME, INFO_MNAME)
VALUES
        ('Tan', 'Michael', 'C'),
        ('Lim', 'Angela', 'B'),
        ('', 'Government', '');


INSERT INTO INFRASTRUCTURE (
    INF_NAME,
    INF_ACCESS_TYPE,
    INF_DESCRIPTION,
    INF_ADDRESS_DESCRIPTION,
    INFO_ID,
    SYS_ID,
    INFT_ID,
    SITIO_ID
) VALUES
      ('Marigondon Barangay Hall',
       'Public',
       'Main government building',
       'Near the highway',
       (SELECT INFO_ID FROM INFRASTRUCTURE_OWNER WHERE INFO_FNAME = 'Government'),
       (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_ID = '1' ),
       (SELECT INFT_ID FROM INFRASTRUCTURE_TYPE WHERE INFT_TYPE_NAME = 'Barangay Hall'),
       (SELECT SITIO_ID FROM SITIO WHERE SITIO_NAME = 'Sitio Uno')),

      ('Tan Residence', 'Private', 'Private property', 'Behind the elementary school',
       (SELECT INFO_ID FROM INFRASTRUCTURE_OWNER WHERE INFO_LNAME = 'Tan' AND INFO_FNAME = 'Michael'),
       (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_ID = '1' ),
       (SELECT INFT_ID FROM INFRASTRUCTURE_TYPE WHERE INFT_TYPE_NAME = 'Barangay Hall'),
       (SELECT SITIO_ID FROM SITIO WHERE SITIO_NAME = 'Sitio Dos'));

-- BUSINESS
INSERT INTO BUSINESS_TYPE (BST_ID, BST_TYPE_NAME)
VALUES
        (1, 'Sari-sari Store'),
        (2, 'Food Stall'),
        (3, 'Repair Shop');

INSERT INTO BUSINESS_OWNER (BSO_FNAME, BSO_LNAME, BSO_MI)
VALUES
        ('Alfredo', 'Garcia', 'D'),
        ('Corazon', 'Ramos', 'M');

INSERT INTO BUSINESS_INFO (
    BS_NAME,
    BS_DESCRIPTION,
    BS_STATUS,
    BS_IS_DTI,
    BS_DTI_IMAGE,
    BS_ADDRESS,
    SITIO_ID,
    BST_ID,
    BSO_ID,
    SYS_ID
) VALUES
      ('Aling Nena''s Sari-sari', 'General merchandise store', 'ACTIVE', FALSE, NULL, '123 Purok Santan',
       (SELECT SITIO_ID FROM SITIO WHERE SITIO.SITIO_ID = '1'),
       (SELECT BST_ID FROM BUSINESS_TYPE WHERE BST_TYPE_NAME = 'Sari-sari Store'),
       (SELECT BSO_ID FROM BUSINESS_OWNER WHERE BSO_LNAME = 'Garcia'),
       (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_FNAME = 'Juan')),

      ('Marigondon Auto Repair', 'Motorcycle and bicycle repairs', 'ACTIVE', TRUE, '/dti/repair123.jpg', '456 Purok Rosas',
       (SELECT SITIO_ID FROM SITIO WHERE SITIO.SITIO_ID = '2'),
       (SELECT BST_ID FROM BUSINESS_TYPE WHERE BST_TYPE_NAME = 'Repair Shop'),
       (SELECT BSO_ID FROM BUSINESS_OWNER WHERE BSO_LNAME = 'Ramos'),
       (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_FNAME = 'Maria'));

-- HEALTH
INSERT INTO PHILHEALTH_CATEGORY (PC_CATEGORY_NAME)
VALUES
        ('Formal Economy Private'),
        ('Formal Economy Government'),
        ('Informal Economy'),
        ('NHTS'),
        ('Senior Citizen'),
        ('Indigenous People'),
        ('Unknown');

INSERT INTO PHILHEALTH (PHEA_ID_NUMBER, PHEA_MEMBERSHIP_TYPE, PC_ID)
VALUES
        ('123456789012', 'Member', (SELECT PC_ID FROM PHILHEALTH_CATEGORY WHERE PC_CATEGORY_NAME = 'Formal Economy Private')),
        ('987654321098', 'Dependent', (SELECT PC_ID FROM PHILHEALTH_CATEGORY WHERE PC_CATEGORY_NAME = 'Indigenous People'));

INSERT INTO MEDICAL_HISTORY_TYPE (MHT_TYPE_NAME)
VALUES
        ('Hypertension'),
        ('Diabetes'),
        ('Tuberculosis'),
        ('Surgery');

INSERT INTO FAMILY_PLANNING_METHOD (FPM_METHOD)
VALUES
        ('COC'),
        ('POP'),
        ('Injectables'),
        ('IUD'),
        ('Condom'),
        ('LAM'),
        ('BTL'),
        ('Implant'),
        ('SDM'),
        ('DPT'),
        ('Withdrawal'),
        ('Others');

INSERT INTO FPM_STATUS (FPMS_STATUS_NAME)
VALUES
        ('New Acceptor'),
        ('Current User'),
        ('Changing Method'),
        ('Changing Clinic'),
        ('Dropout'),
        ('Restarter');

-- EDUCATION
INSERT INTO EDUCATIONAL_ATTAINMENT (EDAT_LEVEL)
VALUES
        ('Elementary Graduate'),
        ('High School Graduate'),
        ('College Graduate');

INSERT INTO EDUCATION_STATUS (
    EDU_IS_CURRENTLY_STUDENT,
    EDU_INSTITUTION_NAME,
    EDAT_ID
) VALUES
      (TRUE, 'Marigondon Elementary School',
       (SELECT EDAT_ID FROM EDUCATIONAL_ATTAINMENT WHERE EDAT_LEVEL = 'Elementary Graduate')),

      (FALSE, 'Cebu Normal University',
       (SELECT EDAT_ID FROM EDUCATIONAL_ATTAINMENT WHERE EDAT_LEVEL = 'College Graduate'));

-- EMPLOYMENT
INSERT INTO EMPLOYMENT_STATUS (ES_STATUS_NAME)
VALUES
       ('Employed'),
       ('Unemployed'),
       ('Self-employed'),
       ('Retired');

INSERT INTO EMPLOYMENT (
    EMP_OCCUPATION,
    EMP_IS_GOV_WORKER,
    ES_ID,
    CTZ_ID
) VALUES
      ('Barangay Health Worker', TRUE,
       (SELECT ES_ID FROM EMPLOYMENT_STATUS WHERE ES_STATUS_NAME = 'Employed'),
       (SELECT CTZ_ID FROM CITIZEN WHERE CTZ_LAST_NAME = 'Gonzales')),

      ('Fish Vendor', FALSE,
       (SELECT ES_ID FROM EMPLOYMENT_STATUS WHERE ES_STATUS_NAME = 'Self-employed'),
       (SELECT CTZ_ID FROM CITIZEN WHERE CTZ_LAST_NAME = 'Gonzales'));

-- TRANSACTIONS
INSERT INTO TRANSACTION_TYPE (TT_TYPE_NAME)
VALUES
        ('Barangay Clearance'),
        ('Business Permit'),
        ('Complaint');

INSERT INTO TRANSACTION_LOG (
    TL_PURPOSE,
    TL_STATUS,
    TL_FNAME,
    TL_LANME,
    TT_ID,
    SYS_ID
) VALUES
      ('For loan application', 'Approved', 'Roberto', 'Gonzales',
       (SELECT TT_ID FROM TRANSACTION_TYPE WHERE TT_TYPE_NAME = 'Barangay Clearance'),
       (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_FNAME = 'Maria')),

      ('New sari-sari store', 'Pending', 'Alfredo', 'Garcia',
       (SELECT TT_ID FROM TRANSACTION_TYPE WHERE TT_TYPE_NAME = 'Business Permit'),
       (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_FNAME = 'Juan'));

-- COMPLAINTS
INSERT INTO COMPLAINANT (COMP_FNAME, COMP_LNAME, COMP_MNAME)
VALUES
        ('Lourdes', 'Santos', 'R'),
        ('Carlos', 'Reyes', 'M');

INSERT INTO HISTORY_TYPE (HIST_TYPE_NAME)
VALUES
       ('Complaint'),
       ('Violation');

INSERT INTO CITIZEN_HISTORY (
    CIHI_DESCRIPTION,
    HIST_ID,
    CTZ_ID,
    SYS_ID
) VALUES
    ('Noise complaint',
     (SELECT HIST_ID FROM HISTORY_TYPE WHERE HIST_TYPE_NAME = 'Complaint'),
     (SELECT CTZ_ID FROM CITIZEN WHERE CTZ_LAST_NAME = 'Gonzales'),
     (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_FNAME = 'Maria'));

INSERT INTO SETTLEMENT_LOG (
    SETT_COMPLAINT_DESCRIPTION,
    SETT_SETTLEMENT_DESCRIPTION,
    SETT_DATE_OF_SETTLEMENT,
    COMP_ID,
    CIHI_ID
) VALUES
    ('Loud karaoke at night', 'Warning issued to homeowner', CURRENT_DATE,
     (SELECT COMP_ID FROM COMPLAINANT WHERE COMP_LNAME = 'Santos'),
     (SELECT CIHI_ID FROM CITIZEN_HISTORY WHERE CIHI_DESCRIPTION = 'Noise complaint'));

-- Update citizen with education and health records
UPDATE CITIZEN SET
       EDU_ID = (SELECT EDU_ID FROM EDUCATION_STATUS WHERE EDU_INSTITUTION_NAME = 'Marigondon Elementary School'),
       PHEA_ID = (SELECT PHEA_ID FROM PHILHEALTH WHERE PHEA_ID_NUMBER = '123456789012')
WHERE CTZ_LAST_NAME = 'Gonzales';

-- Medical History
INSERT INTO MEDICAL_HISTORY (
    MH_DATE_DIAGNOSED,
    MHT_ID,
    CTZ_ID,
    SYS_ID
) VALUES
    ('2020-01-15',
     (SELECT MHT_ID FROM MEDICAL_HISTORY_TYPE WHERE MHT_TYPE_NAME = 'Hypertension'),
     (SELECT CTZ_ID FROM CITIZEN WHERE CTZ_LAST_NAME = 'Gonzales'),
     (SELECT SYS_ID FROM SYSTEM_ACCOUNT WHERE SYS_FNAME = 'Maria'));

-- Family Planning
INSERT INTO FAMILY_PLANNING (
    FP_START_DATE,
    FP_END_DATE,
    CTZ_ID,
    FPMS_STATUS,
    FPM_METHOD
) VALUES
    ('2021-06-01', NULL,
     (SELECT CTZ_ID FROM CITIZEN WHERE CTZ_LAST_NAME = 'Gonzales'),
     (SELECT FPMS_ID FROM FPM_STATUS WHERE FPMS_STATUS_NAME = 'Current User'),
     (SELECT FPM_ID FROM FAMILY_PLANNING_METHOD WHERE FPM_METHOD = 'Condom'));

--
-- SELECT
--     INF.INF_ID,
--     INF.INF_NAME,
--     INF.INF_ACCESS_TYPE,
--     INF.INF_DATE_ENCODED,
--     CONCAT(IO.INFO_FNAME, ' ',COALESCE(NULLIF(LEFT(IO.INFO_MNAME, 1), '') || '. ', ''), IO.INFO_LNAME) AS INFRASTRUCTURE_OWNER,
--     IT.INFT_TYPE_NAME,
--     INF.INF_ADDRESS_DESCRIPTION,
--     S.SITIO_NAME,
--     INF.INF_DESCRIPTION
-- FROM INFRASTRUCTURE INF
-- JOIN INFRASTRUCTURE_OWNER IO ON INF.INFO_ID = IO.INFO_ID
-- JOIN INFRASTRUCTURE_TYPE IT ON INF.INFT_ID=IT.INFT_ID
-- JOIN SITIO S ON INF.SITIO_ID = S.SITIO_ID;
