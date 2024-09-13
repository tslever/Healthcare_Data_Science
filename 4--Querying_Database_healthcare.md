# Querying Database healthcare

Created on 09/12/2024 by Tom Lever

Updated on 09/12/2024 by Tom Lever


1.  Consider an SQL Server database with tables departments, encounters, patients, and providers.
    
    Table departments has columns Department_Key of type tinyint, Department_ID of type time, and Department_Name of type nvarchar.
    
    Table encounters has columns Encounter_Key of type smallint, Encounter_Type_Description of type nvarchar, Encounter_Type of type nvarchar, Encounter_Patient_Class of ype nvarchar, Encounter_Patient_Status of type nvarchar, Encounter_ED_Disposition of type nvarchar, Encounter_Status of type nvarchar, Encounter_Appointment_Date of type datetime2, Encounter_Admit_Date of type nvarchar, Encounter_Discharge_Date of type nvarchar, Patient_Key of type smallint, Encounter_Provider_Key of type smallint, and Encounter_Department_Key of type tinyint.
    
    Table patients has columns Patient_Key of type smallint, Patient_Medical_Record_Number_Alias of type smallint, Patient_Birth_Date of type date, Patient_Gender of type nvarchar, Patient_Address_State of type nvarchar, and PCP_Provider_Key of type smallint.
    
    Table providers has columns Provider_Key of type smallint, Provider_Name of type nvarchar, Provider_Type of type nvarchar, Provider_Credential of type nvarchar, and Provider_Department_Key of type tinyint. All rows in table providers with value in column Provider_Department_Key of 21 are provided below.
    
    |Provider_Key|Provider_Name|Provider_Type|Provider_Credential|Provider_Department_Key|
    |---|---|---|---|---|
    |360|MATGRE|Physician|MD|21|
    |378|WENWES|Physician|MD|21|
    |605|CARRHE|Nurse Practitioner|NP|21|
    |606|SARWAL|Nurse Practitioner|NP|21|
    
    It is September 12, 2023. Your clinic (Department_Key = 21, MEDICAL ASSOCIATES) is planning for the start of the next flu season on October 1, 2023.
    
    a.  How many total patients are there per provider (PCP, primary care provider) at your department?

        Assume that providers MATGRE, WENWES, CARRHE, and SARWAL are all Primary Care Providers associated with department with department key 21 and department name "MEDICAL ASSOCIATES".
        
        ```
        SELECT
            Provider_Key,
            Provider_Name,
            COUNT(Patient_Key) AS Count_Of_Patients
        FROM providers
        LEFT JOIN patients
        ON PCP_Provider_Key = Provider_Key
        WHERE Provider_Department_Key = 21
        GROUP BY
            Provider_Key,
            Provider_Name;
        ```
        
        |Provider_Key|Provider_Name|Count_Of_Patients|
        |---|---|---|
        |605|CARRHE|4|
        |360|MATGRE|6|
        |606|SARWAL|1|
        |378|WENWES|5|
    
    b.  A different flu shot is needed depending on age:
        
        |Name Of Flu Shot|Minimum Age (y)|Maximum Age (y)|Dose (mL)|
        |---|---|---|---|
        |Flucelvax Quadrivalent|0.5|17|0.5|
        |Flublok Quadrivalent|18|64|0.5|
        |Fluzone High-Dose Quadrivalent|65|infinity|0.7|
        
        How many of each flu shot types will be needed for each Primary Care Provider at your clinic with department key 21 and department name MEDICAL ASSOCIATES?

        ```
        DROP TABLE IF EXISTS #Table_Of_Information_Re_Providers_And_Patients;
        DROP TABLE IF EXISTS #Table_Of_Information_Re_Providers_Patients_And_Flu_Shots;

        DECLARE @String_Representing_Date_Of_Start_Of_Flu_Season DATE = '2023-10-01';

        CREATE TABLE #Table_Of_Information_Re_Providers_And_Patients (
            Provider_Key INT,
            Provider_Name VARCHAR(255),
            Patient_Key INT,
            Patient_Birth_Date DATE,
            Age FLOAT
        );

        INSERT INTO #Table_Of_Information_Re_Providers_And_Patients
        SELECT 
            Provider_Key,
            Provider_Name,
            Patient_Key,
            Patient_Birth_Date,
            DATEDIFF(day, Patient_Birth_Date, @String_Representing_Date_Of_Start_Of_Flu_Season) / 365.25 AS Age
        FROM providers
        INNER JOIN patients
        ON Provider_Key = PCP_Provider_Key
        WHERE Provider_Department_Key = 21;

        CREATE TABLE #Table_Of_Information_Re_Providers_Patients_And_Flu_Shots (
            Provider_Key INT,
            Provider_Name VARCHAR(255),
            Patient_Key INT,
            Age FLOAT,
            Type_Of_Flu_Shot VARCHAR(255)
        );

        INSERT INTO #Table_Of_Information_Re_Providers_Patients_And_Flu_Shots
        SELECT
            Provider_Key,
            Provider_Name,
            Patient_Key,
            Age,
            CASE 
                WHEN Age >= 0.5 AND Age < 18 THEN 'Flucelvax Quadrivalent'
                WHEN Age >= 18 AND Age < 65 THEN 'Flublok Quadrivalent'
                WHEN Age >= 65 THEN 'Fluzone High-Dose Quadrivalent'
                ELSE 'Unknown'
            END AS Type_Of_Flu_Shot
        FROM #Table_Of_Information_Re_Providers_And_Patients;

        SELECT
            Provider_Name,
            Type_Of_Flu_Shot,
            COUNT(Patient_Key) AS Number_Of_Flu_Shots
        FROM #Table_Of_Information_Re_Providers_Patients_And_Flu_Shots
        GROUP BY
            Provider_Name,
            Type_Of_Flu_Shot
        ORDER BY
            Provider_Name,
            Type_Of_Flu_Shot;

        DROP TABLE #Table_Of_Information_Re_Providers_And_Patients;
        DROP TABLE #Table_Of_Information_Re_Providers_Patients_And_Flu_Shots;
        ```
        
        |Provider_Name|Type_Of_Flu_Shot|Number_Of_Flu_Shots|
        |---|---|---|
        |CARRHE|Flublok Quadrivalent|2|
        |CARRHE|Fluzone High-Dose Quadrivalent|2|
        |MATGRE|Flublok Quadrivalent|3|
        |MATGRE|Fluzone High-Dose Quadrivalent|3|
        |SARWAL|Fluzone High-Dose Quadrivalent|1|
        |WENWES|Flublok Quadrivalent|3|
        |WENWES|Flucelvax Quadrivalent|2|