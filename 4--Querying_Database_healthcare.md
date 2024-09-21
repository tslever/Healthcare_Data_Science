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

2.  We consider a patient to be an active patient if they had two or more encounters.

    a.  How many active patients are in each of the following age groups?
        
    |Name|Minimum Age (years)|Maximum Age (years)|
    |---|---|---|
    |Age Group 1|0|17|
    |Age Group 2|18|64|
    |Age Group 3|65|infinity|
    
    ```
    WITH

        Table_Of_Keys_Of_Active_Patients AS (
            SELECT Patient_Key
            FROM encounters
            GROUP BY Patient_Key
            HAVING COUNT(Encounter_Key) >= 2
        ),

        Table_Of_Keys_And_Ages_Of_Active_Patients AS (
            SELECT
                Table_Of_Keys_Of_Active_Patients.Patient_Key,
                DATEDIFF(day, Patient_Birth_Date, GETDATE()) / 365.25 AS Age
            FROM Table_Of_Keys_Of_Active_Patients
            JOIN patients
            ON Table_Of_Keys_Of_Active_Patients.Patient_Key = patients.Patient_Key
        ),

        Table_Of_Keys_And_Age_Groups_Of_Active_Patients AS (
            SELECT
                Patient_Key,
                CASE
                    WHEN Age >= 0 AND AGE < 18 THEN 'Age Group 1'
                    WHEN Age >= 18 AND Age < 65 THEN 'Age Group 2'
                    WHEN Age >= 65 THEN 'Age Group 3'
                END AS Age_Group
            FROM Table_Of_Keys_And_Ages_Of_Active_Patients
        )

    SELECT
        Age_Group,
        COUNT(Patient_Key) AS Number_Of_Active_Patients
    FROM Table_Of_Keys_And_Age_Groups_Of_Active_Patients
    GROUP BY Age_Group;
    ```
    
    |Age_Group|Number_Of_Active_Patients|
    |---|---|
    |Age Group 1|6|
    |Age Group 2|45|
    |Age Group 3|18|

    b.  Which Primary Care Providers in which departments have the largest number of active patients? To answer this question, provide a rank ordered list for each department with number of active patients (descending) for each Primary Care Provider.
    
    ```
    WITH
        Table_Of_Keys_Of_Active_Patients AS (
            SELECT Patient_Key
            FROM encounters
            GROUP BY Patient_Key
            HAVING COUNT(*) >= 2
        ),

        Table_Of_Keys_Of_Providers_And_Active_Patients AS (
            SELECT
                PCP_Provider_Key,
                patients.Patient_Key
            FROM patients
            INNER JOIN Table_Of_Keys_Of_Active_Patients
            ON patients.Patient_Key = Table_Of_Keys_Of_Active_Patients.Patient_Key
        ),

        Table_Of_Keys_Of_Providers_And_Numbers_Of_Active_Patients AS (
            SELECT
                PCP_Provider_Key,
                COUNT(DISTINCT Patient_Key) AS Number_of_Active_Patients
            FROM Table_Of_Keys_Of_Providers_And_Active_Patients
            GROUP BY PCP_Provider_Key
        )

    SELECT
        Department_Key,
        Department_Name,
        Provider_Key,
        Provider_Name,
        Number_of_Active_Patients,
        RANK() OVER (
            PARTITION BY Department_Key
            ORDER BY Number_of_Active_Patients DESC
        ) AS Rank_In_Department
    FROM Table_Of_Keys_Of_Providers_And_Numbers_Of_Active_Patients
    INNER JOIN providers
    ON PCP_Provider_Key = Provider_Key
    INNER JOIN departments
    ON Provider_Department_Key = Department_Key
    ORDER BY
        Department_Key ASC,
        Rank_In_Department DESC;
    ```
    
    |Department_Key|Department_Name|Provider_Key|Provider_Name|Number_of_Active_Patients|Rank_In_Department|
    |---|---|---|---|---|---|
    |1|Unknown|58|KEVMCC|1|2|
    |1|Unknown|128|JOCSCH|1|2|
    |1|Unknown|203|EVAPRI|1|2|
    |1|Unknown|380|GHONON|1|2|
    |1|Unknown|431|PRONON|1|2|
    |1|Unknown|476|JASPER|1|2|
    |1|Unknown|513|ALLCHU|1|2|
    |1|Unknown|702|NOUNK|1|2|
    |1|Unknown|758|PAMREY|1|2|
    |1|Unknown|1|NONON|1|2|
    |1|Unknown|6|UVACLI|3|1|
    |4|FAMILY MEDICINE|492|THOALB|1|1|
    |11|CLINIC C|752|MARBAD|1|1|
    |18|PEDIATRICS|780|CHRASH|1|1|
    |19|MEDICAL ASSOCIATES|237|JASERN|1|7|
    |19|MEDICAL ASSOCIATES|247|JUSELK|1|7|
    |19|MEDICAL ASSOCIATES|251|AVNSHA|1|7|
    |19|MEDICAL ASSOCIATES|742|NATPHA|1|7|
    |19|MEDICAL ASSOCIATES|716|BRAPOD|1|7|
    |19|MEDICAL ASSOCIATES|481|IRAHEL|1|7|
    |19|MEDICAL ASSOCIATES|166|ALELAV|1|7|
    |19|MEDICAL ASSOCIATES|167|SARACE|1|7|
    |19|MEDICAL ASSOCIATES|169|FRAMOR|1|7|
    |19|MEDICAL ASSOCIATES|173|REBBRO|1|7|
    |19|MEDICAL ASSOCIATES|176|HEAFRA|1|7|
    |19|MEDICAL ASSOCIATES|182|KATFOR|1|7|
    |19|MEDICAL ASSOCIATES|114|POOPAT|1|7|
    |19|MEDICAL ASSOCIATES|115|VARKAV|1|7|
    |19|MEDICAL ASSOCIATES|117|ANUGUD|1|7|
    |19|MEDICAL ASSOCIATES|119|ADAPUR|1|7|
    |19|MEDICAL ASSOCIATES|157|EMIBRZ|1|7|
    |19|MEDICAL ASSOCIATES|165|KENMIC|1|7|
    |19|MEDICAL ASSOCIATES|91|KATGUI|1|7|
    |19|MEDICAL ASSOCIATES|95|AISCAM|1|7|
    |19|MEDICAL ASSOCIATES|99|CLAHUM|1|7|
    |19|MEDICAL ASSOCIATES|105|BREMUL|1|7|
    |19|MEDICAL ASSOCIATES|106|EMMTRA|1|7|
    |19|MEDICAL ASSOCIATES|113|SHIHAN|1|7|
    |19|MEDICAL ASSOCIATES|57|JEAENG|1|7|
    |19|MEDICAL ASSOCIATES|80|AKUBOA|1|7|
    |19|MEDICAL ASSOCIATES|84|CHAMOR|1|7|
    |19|MEDICAL ASSOCIATES|85|EMIMIN|1|7|
    |19|MEDICAL ASSOCIATES|88|EMIMIT|1|7|
    |19|MEDICAL ASSOCIATES|89|CARCHE|1|7|
    |19|MEDICAL ASSOCIATES|379|EVAHEA|2|2|
    |19|MEDICAL ASSOCIATES|534|ELILYO|2|2|
    |19|MEDICAL ASSOCIATES|720|ASHBOL|2|2|
    |19|MEDICAL ASSOCIATES|750|ABHRAV|2|2|
    |19|MEDICAL ASSOCIATES|753|DAVCAL|2|2|
    |19|MEDICAL ASSOCIATES|347|BETJAE|4|1|
    |25|PEDIATRICS|418|ELISCH|1|1|
    |27|FAMILY MEDICINE|352|STEHEI|1|1|
    |36|FAMILY MEDICINE|671|GRESTR|2|1|
    |100|PRIMARY CARE|596|DANTYL|1|1|
    |101|PRIMARY CARE|211|KAIALT|1|1|
    |106|PEDIATRICS|174|REBHU|1|1|
    |117|PRIMARY CARE|484|AMAGON|1|1|
    |128|FAMILY MEDICINE|191|SADGIR|1|1|

3.  Encounter Department Key 43 corresponds to department "EMERGENCY DEPT". Which Primary Care Providers have patients with the most encounters with Encounter Department Key 43? Provide a rank ordered (descending) list.

    ```
    WITH Table_Of_Number_Of_Encounters_With_Emergency_Department_By_Department_And_Provider AS (
        SELECT 
            Department_Key,
            Department_Name,
            Provider_Key,
            Provider_Name,
            COUNT(Provider_Key) AS Number_Of_Encounters_With_Emergency_Department
        FROM patients
        INNER JOIN encounters
        ON patients.Patient_Key = encounters.Patient_Key
        INNER JOIN providers
        ON PCP_Provider_Key = Provider_Key
        INNER JOIN departments
        ON Provider_Department_Key = Department_Key
        WHERE Encounter_Department_Key = 43
        GROUP BY
            Department_Key,
            Department_Name,
            Provider_Key,
            Provider_Name
    )

    SELECT
        Department_Key,
        Department_Name,
        Provider_Key,
        Provider_Name,
        Number_Of_Encounters_With_Emergency_Department,
        RANK() OVER (
            PARTITION BY Department_Key
            ORDER BY Number_Of_Encounters_With_Emergency_Department DESC
        ) AS Rank_In_Department
    FROM Table_Of_Number_Of_Encounters_With_Emergency_Department_By_Department_And_Provider
    ORDER BY
        Department_Key ASC,
        Rank_In_Department DESC;
    ```

    |Department_Key|Department_Name|Provider_Key|Provider_Name|Number_Of_Encounters_With_Emergency_Department|Rank_In_Department|
    |---|---|---|---|---|---|
    |1|Unknown|731|CAMSIM|1|36|
    |1|Unknown|739|KEVMCC|1|36|
    |1|Unknown|760|MARMEN|1|36|
    |1|Unknown|761|COLMER|1|36|
    |1|Unknown|762|JEADAV|1|36|
    |1|Unknown|764|KRYPOR|1|36|
    |1|Unknown|765|KATMIK|1|36|
    |1|Unknown|771|TIFPOW|1|36|
    |1|Unknown|775|GREMAL|1|36|
    |1|Unknown|776|RICMIL|1|36|
    |1|Unknown|779|STESHA|1|36|
    |1|Unknown|782|STEMUM|1|36|
    |1|Unknown|697|KELGOO|1|36|
    |1|Unknown|617|CHRMAN|1|36|
    |1|Unknown|619|HARCRA|1|36|
    |1|Unknown|17|DARNIG|1|36|
    |1|Unknown|25|MELBON|1|36|
    |1|Unknown|26|MORCLI|1|36|
    |1|Unknown|27|TANCUS|1|36|
    |1|Unknown|30|JULHIL|1|36|
    |1|Unknown|48|PATPLE|1|36|
    |1|Unknown|51|HALBLA|1|36|
    |1|Unknown|52|DAVSUY|1|36|
    |1|Unknown|53|TIMPOW|1|36|
    |1|Unknown|56|NATOWE|1|36|
    |1|Unknown|7|PEDCLI|1|36|
    |1|Unknown|8|LAUNUR|1|36|
    |1|Unknown|9|KATBAR|1|36|
    |1|Unknown|11|AHGBOL|1|36|
    |1|Unknown|65|HCHCLI|1|36|
    |1|Unknown|68|MICRIC|1|36|
    |1|Unknown|74|JOHWIT|1|36|
    |1|Unknown|120|SARYOW|1|36|
    |1|Unknown|123|MICMCC|1|36|
    |1|Unknown|125|DANSAW|1|36|
    |1|Unknown|126|RUSSAW|1|36|
    |1|Unknown|60|LAUGIB|1|36|
    |1|Unknown|2|CENHEA|1|36|
    |1|Unknown|3|STUFAM|1|36|
    |1|Unknown|132|CAIBUL|1|36|
    |1|Unknown|133|GRIBOU|1|36|
    |1|Unknown|137|LATSHI|1|36|
    |1|Unknown|141|FARDET|1|36|
    |1|Unknown|143|NATMUR|1|36|
    |1|Unknown|150|ROBSTO|1|36|
    |1|Unknown|321|CHRCRA|1|36|
    |1|Unknown|323|KBMEMR|1|36|
    |1|Unknown|324|JIMADC|1|36|
    |1|Unknown|327|RAYMAR|1|36|
    |1|Unknown|328|GREBRA|1|36|
    |1|Unknown|329|JENSAR|1|36|
    |1|Unknown|207|KEVVOL|1|36|
    |1|Unknown|201|LARTRI|1|36|
    |1|Unknown|307|LOUCLI|1|36|
    |1|Unknown|308|COMCLI|1|36|
    |1|Unknown|309|UVACLI|1|36|
    |1|Unknown|311|HARHEA|1|36|
    |1|Unknown|312|CVICLI|1|36|
    |1|Unknown|313|DOWFAM|1|36|
    |1|Unknown|317|LOUHAN|1|36|
    |1|Unknown|318|KIYASA|1|36|
    |1|Unknown|319|AMYCOO|1|36|
    |1|Unknown|283|ROBMIC|1|36|
    |1|Unknown|284|MARMAY|1|36|
    |1|Unknown|285|RICBRA|1|36|
    |1|Unknown|289|MINSHA|1|36|
    |1|Unknown|291|PAINOL|1|36|
    |1|Unknown|293|CARBOE|1|36|
    |1|Unknown|294|VISPAT|1|36|
    |1|Unknown|302|MICPAD|1|36|
    |1|Unknown|303|PEDCLI|1|36|
    |1|Unknown|305|FRECLI|1|36|
    |1|Unknown|218|THOWOL|1|36|
    |1|Unknown|219|ARTLAN|1|36|
    |1|Unknown|220|LAUBAB|1|36|
    |1|Unknown|221|YASKHA|1|36|
    |1|Unknown|226|STEALD|1|36|
    |1|Unknown|259|HAKDAG|1|36|
    |1|Unknown|261|SCOYOU|1|36|
    |1|Unknown|263|JAMPLE|1|36|
    |1|Unknown|264|RANSAM|1|36|
    |1|Unknown|265|BREBRA|1|36|
    |1|Unknown|275|MATGIE|1|36|
    |1|Unknown|669|WILMIX|1|36|
    |1|Unknown|672|CATBOI|1|36|
    |1|Unknown|580|BLUCLI|1|36|
    |1|Unknown|587|MONKAN|1|36|
    |1|Unknown|597|MARHOB|1|36|
    |1|Unknown|602|EVAPRY|1|36|
    |1|Unknown|604|MARHAN|1|36|
    |1|Unknown|627|MERQUA|1|36|
    |1|Unknown|631|KARPOE|1|36|
    |1|Unknown|633|CHRHEC|1|36|
    |1|Unknown|635|RANBAK|1|36|
    |1|Unknown|641|RENFIS|1|36|
    |1|Unknown|646|PETNIS|1|36|
    |1|Unknown|652|CHACOL|1|36|
    |1|Unknown|661|UVACLI|1|36|
    |1|Unknown|662|ANTMAR|1|36|
    |1|Unknown|665|ELIKOS|1|36|
    |1|Unknown|679|SHAMIL|1|36|
    |1|Unknown|685|JAMLAG|1|36|
    |1|Unknown|686|TARABE|1|36|
    |1|Unknown|687|WARCLI|1|36|
    |1|Unknown|688|RANLAN|1|36|
    |1|Unknown|690|ROBRAM|1|36|
    |1|Unknown|693|DONLEE|1|36|
    |1|Unknown|694|KRIDAL|1|36|
    |1|Unknown|705|ADAARN|1|36|
    |1|Unknown|706|ARTTIC|1|36|
    |1|Unknown|707|TEOBRO|1|36|
    |1|Unknown|711|DUNMAC|1|36|
    |1|Unknown|713|INECAR|1|36|
    |1|Unknown|714|CHERAO|1|36|
    |1|Unknown|718|MARWAR|1|36|
    |1|Unknown|721|PAMMAN|1|36|
    |1|Unknown|722|WILMAL|1|36|
    |1|Unknown|724|TALSEN|1|36|
    |1|Unknown|727|MICMAR|1|36|
    |1|Unknown|729|CINFEE|1|36|
    |1|Unknown|473|SPRFAM|1|36|
    |1|Unknown|488|PAUMAX|1|36|
    |1|Unknown|489|SENCLI|1|36|
    |1|Unknown|491|VACLI|1|36|
    |1|Unknown|499|NANLUT|1|36|
    |1|Unknown|501|AMBYOD|1|36|
    |1|Unknown|331|ADAHOL|1|36|
    |1|Unknown|430|PROCOM|1|36|
    |1|Unknown|507|BRIEAS|1|36|
    |1|Unknown|510|PAUJOH|1|36|
    |1|Unknown|513|ALLCHU|1|36|
    |1|Unknown|514|BLUTEL|1|36|
    |1|Unknown|516|CURJAN|1|36|
    |1|Unknown|539|GREGEL|1|36|
    |1|Unknown|541|SHEHIG|1|36|
    |1|Unknown|543|ANDHAW|1|36|
    |1|Unknown|546|LOAKLI|1|36|
    |1|Unknown|547|VICSUL|1|36|
    |1|Unknown|552|ALTMIR|1|36|
    |1|Unknown|557|MARGAR|1|36|
    |1|Unknown|566|STEGRI|1|36|
    |1|Unknown|335|VERGUA|1|36|
    |1|Unknown|338|DEBBAB|1|36|
    |1|Unknown|342|VALHOS|1|36|
    |1|Unknown|344|UVACLI|1|36|
    |1|Unknown|355|KURELW|1|36|
    |1|Unknown|374|ANDWAL|1|36|
    |1|Unknown|432|PHYUVA|1|36|
    |1|Unknown|433|CVINUR|1|36|
    |1|Unknown|435|ARCLOR|1|36|
    |1|Unknown|436|PIECLI|1|36|
    |1|Unknown|437|KAIBEI|1|36|
    |1|Unknown|446|BRUCAM|1|36|
    |1|Unknown|447|DAVCAM|1|36|
    |1|Unknown|451|BERFOC|1|36|
    |1|Unknown|453|DAVCHE|1|36|
    |1|Unknown|459|ELIPIC|1|36|
    |1|Unknown|460|MICSTY|1|36|
    |1|Unknown|461|EUGROB|1|36|
    |1|Unknown|462|DEIDON|1|36|
    |1|Unknown|465|DAVGRE|1|36|
    |1|Unknown|330|LORBAL|2|15|
    |1|Unknown|470|SHEDAV|2|15|
    |1|Unknown|673|ANNKLE|2|15|
    |1|Unknown|622|STESUL|2|15|
    |1|Unknown|570|EDWHAR|2|15|
    |1|Unknown|666|JOSGRE|2|15|
    |1|Unknown|667|MARWHI|2|15|
    |1|Unknown|276|ANNABR|2|15|
    |1|Unknown|277|A.TRU|2|15|
    |1|Unknown|151|JOHCLI|2|15|
    |1|Unknown|203|EVAPRI|2|15|
    |1|Unknown|320|CARARM|2|15|
    |1|Unknown|58|KEVMCC|2|15|
    |1|Unknown|62|ANNROA|2|15|
    |1|Unknown|49|MORNEW|2|15|
    |1|Unknown|15|RICMUL|2|15|
    |1|Unknown|16|PEDCLI|2|15|
    |1|Unknown|332|JAMHUT|2|15|
    |1|Unknown|613|JAYGIL|2|15|
    |1|Unknown|696|KATHED|2|15|
    |1|Unknown|730|TABDAV|2|15|
    |1|Unknown|334|LINPER|3|12|
    |1|Unknown|380|GHONON|3|12|
    |1|Unknown|506|ALABRO|3|12|
    |1|Unknown|217|PAUWIS|4|11|
    |1|Unknown|128|JOCSCH|5|8|
    |1|Unknown|306|FLUCOR|5|8|
    |1|Unknown|793|TEMPCP|5|8|
    |1|Unknown|431|PRONON|6|7|
    |1|Unknown|343|NONSEL|9|6|
    |1|Unknown|702|NOUNK|14|5|
    |1|Unknown|6|UVACLI|18|4|
    |1|Unknown|5|UVACLI|23|3|
    |1|Unknown|794|ownUnk|33|2|
    |1|Unknown|1|NONON|42|1|
    |3|CLINIC A|575|REBMUL|1|2|
    |3|CLINIC A|684|CHRTIE|2|1|
    |4|FAMILY MEDICINE|583|CORPAR|2|4|
    |4|FAMILY MEDICINE|524|KATDEG|3|2|
    |4|FAMILY MEDICINE|595|DONLAN|3|2|
    |4|FAMILY MEDICINE|492|THOALB|4|1|
    |5|HEM ONC EAST|463|RICHAL|1|1|
    |11|CLINIC C|257|LINCAR|1|2|
    |11|CLINIC C|387|KATJAF|1|2|
    |11|CLINIC C|563|KIMDOW|1|2|
    |11|CLINIC C|589|SIMLEH|1|2|
    |11|CLINIC C|660|MARZAY|1|2|
    |11|CLINIC C|752|MARBAD|4|1|
    |15|CARDIOLOGY|350|CHASAU|1|1|
    |15|CARDIOLOGY|373|JAMBER|1|1|
    |18|PEDIATRICS|780|CHRASH|4|1|
    |19|MEDICAL ASSOCIATES|91|KATGUI|1|14|
    |19|MEDICAL ASSOCIATES|93|ELLGOL|1|14|
    |19|MEDICAL ASSOCIATES|94|GRISON|1|14|
    |19|MEDICAL ASSOCIATES|95|AISCAM|1|14|
    |19|MEDICAL ASSOCIATES|99|CLAHUM|1|14|
    |19|MEDICAL ASSOCIATES|101|CALGEN|1|14|
    |19|MEDICAL ASSOCIATES|106|EMMTRA|1|14|
    |19|MEDICAL ASSOCIATES|108|BENFUL|1|14|
    |19|MEDICAL ASSOCIATES|110|JOHWIS|1|14|
    |19|MEDICAL ASSOCIATES|115|VARKAV|1|14|
    |19|MEDICAL ASSOCIATES|117|ANUGUD|1|14|
    |19|MEDICAL ASSOCIATES|481|IRAHEL|1|14|
    |19|MEDICAL ASSOCIATES|534|ELILYO|1|14|
    |19|MEDICAL ASSOCIATES|618|JOALEE|1|14|
    |19|MEDICAL ASSOCIATES|654|ROBGOO|1|14|
    |19|MEDICAL ASSOCIATES|742|NATPHA|1|14|
    |19|MEDICAL ASSOCIATES|790|CYNLI|1|14|
    |19|MEDICAL ASSOCIATES|85|EMIMIN|1|14|
    |19|MEDICAL ASSOCIATES|783|ZACBOG|1|14|
    |19|MEDICAL ASSOCIATES|155|AMBROB|1|14|
    |19|MEDICAL ASSOCIATES|159|TALMAH|1|14|
    |19|MEDICAL ASSOCIATES|160|JAMNGO|1|14|
    |19|MEDICAL ASSOCIATES|165|KENMIC|1|14|
    |19|MEDICAL ASSOCIATES|166|ALELAV|1|14|
    |19|MEDICAL ASSOCIATES|171|ABDAGH|1|14|
    |19|MEDICAL ASSOCIATES|176|HEAFRA|1|14|
    |19|MEDICAL ASSOCIATES|177|THOHIL|1|14|
    |19|MEDICAL ASSOCIATES|181|VIKZEL|1|14|
    |19|MEDICAL ASSOCIATES|183|JACFRI|1|14|
    |19|MEDICAL ASSOCIATES|235|GORSMI|1|14|
    |19|MEDICAL ASSOCIATES|238|MACFRA|1|14|
    |19|MEDICAL ASSOCIATES|247|JUSELK|1|14|
    |19|MEDICAL ASSOCIATES|254|HANLAI|1|14|
    |19|MEDICAL ASSOCIATES|347|BETJAE|1|14|
    |19|MEDICAL ASSOCIATES|80|AKUBOA|1|14|
    |19|MEDICAL ASSOCIATES|230|SAMCHA|2|4|
    |19|MEDICAL ASSOCIATES|119|ADAPUR|2|4|
    |19|MEDICAL ASSOCIATES|789|ANDVIP|2|4|
    |19|MEDICAL ASSOCIATES|391|PPREY|2|4|
    |19|MEDICAL ASSOCIATES|745|BENWIS|2|4|
    |19|MEDICAL ASSOCIATES|747|LYDBUS|2|4|
    |19|MEDICAL ASSOCIATES|748|STESCH|2|4|
    |19|MEDICAL ASSOCIATES|750|ABHRAV|2|4|
    |19|MEDICAL ASSOCIATES|751|BENROB|2|4|
    |19|MEDICAL ASSOCIATES|89|CARCHE|2|4|
    |19|MEDICAL ASSOCIATES|84|CHAMOR|3|2|
    |19|MEDICAL ASSOCIATES|57|JEAENG|3|2|
    |19|MEDICAL ASSOCIATES|753|DAVCAL|4|1|
    |21|MEDICAL ASSOCIATES|605|CARRHE|1|3|
    |21|MEDICAL ASSOCIATES|378|WENWES|3|2|
    |21|MEDICAL ASSOCIATES|360|MATGRE|4|1|
    |23|PEDIATRICS|629|ABIKUM|1|2|
    |23|PEDIATRICS|417|HEAQUI|1|2|
    |23|PEDIATRICS|419|ANNRAN|3|1|
    |24|COMMUNITY MED|376|BARPOS|1|6|
    |24|COMMUNITY MED|383|KIMBAU|1|6|
    |24|COMMUNITY MED|573|DIABAR|2|4|
    |24|COMMUNITY MED|358|MARLEP|2|4|
    |24|COMMUNITY MED|368|SUSLAU|3|2|
    |24|COMMUNITY MED|392|JOYGEI|3|2|
    |24|COMMUNITY MED|715|RACSPI|4|1|
    |25|PEDIATRICS|418|ELISCH|4|1|
    |26|CLINIC C|653|DEBADA|2|1|
    |27|FAMILY MEDICINE|523|SARSPR|1|3|
    |27|FAMILY MEDICINE|574|SARDAL|2|2|
    |27|FAMILY MEDICINE|352|STEHEI|3|1|
    |28|FAMILY MEDICINE|599|TONKIS|1|1|
    |30|SURGERY|427|BRUSCH|1|1|
    |33|OB_GYN|407|DENYOU|1|1|
    |36|FAMILY MEDICINE|87|PRICAL|1|10|
    |36|FAMILY MEDICINE|82|BRYCOC|1|10|
    |36|FAMILY MEDICINE|240|BROMIL|1|10|
    |36|FAMILY MEDICINE|252|NICLOR|1|10|
    |36|FAMILY MEDICINE|348|REBCOM|1|10|
    |36|FAMILY MEDICINE|135|ECHBUF|1|10|
    |36|FAMILY MEDICINE|229|MICCAR|1|10|
    |36|FAMILY MEDICINE|746|KARMAC|1|10|
    |36|FAMILY MEDICINE|772|MICBRI|1|10|
    |36|FAMILY MEDICINE|778|MASMOR|1|10|
    |36|FAMILY MEDICINE|349|KIMBED|2|5|
    |36|FAMILY MEDICINE|98|MANTRI|2|5|
    |36|FAMILY MEDICINE|109|MICSPR|2|5|
    |36|FAMILY MEDICINE|231|MATMIR|2|5|
    |36|FAMILY MEDICINE|83|GRETUR|2|5|
    |36|FAMILY MEDICINE|525|JERKEN|3|4|
    |36|FAMILY MEDICINE|192|MATCUR|4|1|
    |36|FAMILY MEDICINE|198|LAUHOE|4|1|
    |36|FAMILY MEDICINE|671|GRESTR|4|1|
    |38|PEDIATRICS|414|LINWAG|1|1|
    |90|FAMILY MEDICINE|362|CATCAS|1|3|
    |90|FAMILY MEDICINE|61|PRIKOH|2|2|
    |90|FAMILY MEDICINE|683|TERBAB|3|1|
    |91|CLINIC B|367|LAUARC|1|2|
    |91|CLINIC B|147|KARSTA|3|1|
    |94|PEDIATRICS|578|ANNJES|4|1|
    |95|FAMILY CARE|486|TONFIO|1|1|
    |97|PEDIATRICS|651|EVAKAR|1|1|
    |97|PEDIATRICS|689|JESSAL|1|1|
    |99|CLINIC D|369|MARPRE|1|1|
    |100|PRIMARY CARE|647|BRECAS|1|3|
    |100|PRIMARY CARE|670|CATVAR|1|3|
    |100|PRIMARY CARE|738|CARQUI|1|3|
    |100|PRIMARY CARE|372|JOHLEI|3|2|
    |100|PRIMARY CARE|596|DANTYL|5|1|
    |101|PRIMARY CARE|732|CASDIS|1|3|
    |101|PRIMARY CARE|213|MADMUR|1|3|
    |101|PRIMARY CARE|482|KHAPHA|2|2|
    |101|PRIMARY CARE|211|KAIALT|3|1|
    |103|TEEN YOUNG AD CTR|127|MONHEH|1|1|
    |103|TEEN YOUNG AD CTR|735|IREMAT|1|1|
    |103|TEEN YOUNG AD CTR|741|SERERT|1|1|
    |106|PEDIATRICS|784|ASHAKK|1|6|
    |106|PEDIATRICS|180|ASHCOM|1|6|
    |106|PEDIATRICS|421|AMYWRE|1|6|
    |106|PEDIATRICS|477|AMYBRO|1|6|
    |106|PEDIATRICS|555|SHAGUP|1|6|
    |106|PEDIATRICS|564|MICWIL|1|6|
    |106|PEDIATRICS|699|JULOWE|1|6|
    |106|PEDIATRICS|734|MICROB|1|6|
    |106|PEDIATRICS|743|ANNHAK|1|6|
    |106|PEDIATRICS|416|MARMEN|2|2|
    |106|PEDIATRICS|174|REBHU|2|2|
    |106|PEDIATRICS|744|ANDBUR|2|2|
    |106|PEDIATRICS|770|NICBYR|2|2|
    |106|PEDIATRICS|413|MEGKEE|6|1|
    |115|PRIMARY CARE|586|LISKIN|3|1|
    |116|PRIMARY CARE|763|CHRLAM|1|7|
    |116|PRIMARY CARE|529|AUDBAR|1|7|
    |116|PRIMARY CARE|356|JOHDAV|1|7|
    |116|PRIMARY CARE|698|ASHHAR|2|6|
    |116|PRIMARY CARE|346|CHRDUB|3|3|
    |116|PRIMARY CARE|359|GINENG|3|3|
    |116|PRIMARY CARE|572|AMYPOT|3|3|
    |116|PRIMARY CARE|466|ERIZAN|4|1|
    |116|PRIMARY CARE|645|ANDCHA|4|1|
    |117|PRIMARY CARE|531|MICPRO|1|2|
    |117|PRIMARY CARE|536|JENHER|1|2|
    |117|PRIMARY CARE|458|GREBAN|1|2|
    |117|PRIMARY CARE|478|JUNKIM|1|2|
    |117|PRIMARY CARE|484|AMAGON|3|1|
    |119|PRIMARY CARE|371|SCOSEA|1|1|
    |119|PRIMARY CARE|490|AMIMUN|1|1|
    |119|PRIMARY CARE|495|JENBLO|1|1|
    |120|PEDIATRICS|781|SUSSMI|1|1|
    |124|SPORTS MED|480|SIOSTA|1|1|
    |126|POPULATION HEALTH|628|PAMTET|1|1|
    |127|FAMILY MEDICINE|260|VICHAM|1|1|
    |128|FAMILY MEDICINE|191|SADGIR|2|1|