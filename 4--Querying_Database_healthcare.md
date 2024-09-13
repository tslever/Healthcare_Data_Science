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
            Number_of_Active_Patients
        FROM Table_Of_Keys_Of_Providers_And_Numbers_Of_Active_Patients
        INNER JOIN providers
        ON PCP_Provider_Key = Provider_Key
        INNER JOIN departments
        ON Provider_Department_Key = Department_Key
        ORDER BY
            Department_Key ASC,
            Number_of_Active_Patients DESC;
        ```
        
        |Department_Key|Department_Name|Provider_Key|Provider_Name|Number_of_Active_Patients|
        |---|---|---|---|---|
        |1|Unknown|6|UVACLI|3|
        |1|Unknown|58|KEVMCC|1|
        |1|Unknown|128|JOCSCH|1|
        |1|Unknown|203|EVAPRI|1|
        |1|Unknown|380|GHONON|1|
        |1|Unknown|431|PRONON|1|
        |1|Unknown|476|JASPER|1|
        |1|Unknown|513|ALLCHU|1|
        |1|Unknown|702|NOUNK|1|
        |1|Unknown|758|PAMREY|1|
        |1|Unknown|1|NONON|1|
        |4|FAMILY MEDICINE|492|THOALB|1|
        |11|CLINIC C|752|MARBAD|1|
        |18|PEDIATRICS|780|CHRASH|1|
        |19|MEDICAL ASSOCIATES|347|BETJAE|4|
        |19|MEDICAL ASSOCIATES|379|EVAHEA|2|
        |19|MEDICAL ASSOCIATES|534|ELILYO|2|
        |19|MEDICAL ASSOCIATES|720|ASHBOL|2|
        |19|MEDICAL ASSOCIATES|750|ABHRAV|2|
        |19|MEDICAL ASSOCIATES|753|DAVCAL|2|
        |19|MEDICAL ASSOCIATES|237|JASERN|1|
        |19|MEDICAL ASSOCIATES|247|JUSELK|1|
        |19|MEDICAL ASSOCIATES|251|AVNSHA|1|
        |19|MEDICAL ASSOCIATES|742|NATPHA|1|
        |19|MEDICAL ASSOCIATES|716|BRAPOD|1|
        |19|MEDICAL ASSOCIATES|481|IRAHEL|1|
        |19|MEDICAL ASSOCIATES|166|ALELAV|1|
        |19|MEDICAL ASSOCIATES|167|SARACE|1|
        |19|MEDICAL ASSOCIATES|169|FRAMOR|1|
        |19|MEDICAL ASSOCIATES|173|REBBRO|1|
        |19|MEDICAL ASSOCIATES|176|HEAFRA|1|
        |19|MEDICAL ASSOCIATES|182|KATFOR|1|
        |19|MEDICAL ASSOCIATES|114|POOPAT|1|
        |19|MEDICAL ASSOCIATES|115|VARKAV|1|
        |19|MEDICAL ASSOCIATES|117|ANUGUD|1|
        |19|MEDICAL ASSOCIATES|119|ADAPUR|1|
        |19|MEDICAL ASSOCIATES|157|EMIBRZ|1|
        |19|MEDICAL ASSOCIATES|165|KENMIC|1|
        |19|MEDICAL ASSOCIATES|91|KATGUI|1|
        |19|MEDICAL ASSOCIATES|95|AISCAM|1|
        |19|MEDICAL ASSOCIATES|99|CLAHUM|1|
        |19|MEDICAL ASSOCIATES|105|BREMUL|1|
        |19|MEDICAL ASSOCIATES|106|EMMTRA|1|
        |19|MEDICAL ASSOCIATES|113|SHIHAN|1|
        |19|MEDICAL ASSOCIATES|57|JEAENG|1|
        |19|MEDICAL ASSOCIATES|80|AKUBOA|1|
        |19|MEDICAL ASSOCIATES|84|CHAMOR|1|
        |19|MEDICAL ASSOCIATES|85|EMIMIN|1|
        |19|MEDICAL ASSOCIATES|88|EMIMIT|1|
        |19|MEDICAL ASSOCIATES|89|CARCHE|1|
        |25|PEDIATRICS|418|ELISCH|1|
        |27|FAMILY MEDICINE|352|STEHEI|1|
        |36|FAMILY MEDICINE|671|GRESTR|2|
        |100|PRIMARY CARE|596|DANTYL|1|
        |101|PRIMARY CARE|211|KAIALT|1|
        |106|PEDIATRICS|174|REBHU|1|
        |117|PRIMARY CARE|484|AMAGON|1|
        |128|FAMILY MEDICINE|191|SADGIR|1|

3.  Encounter Department Key 43 corresponds to department "EMERGENCY DEPT". Which Primary Care Providers have patients with the most encounters with Encounter Department Key 43? Provide a rank ordered (descending) list.

    ```
    SELECT 
        Provider_Key,
        Provider_Name,
        COUNT(Provider_Key) AS Number_Of_Encounters_With_Emergency_Department
    FROM patients
    INNER JOIN encounters
    ON patients.Patient_Key = encounters.Patient_Key
    INNER JOIN providers
    ON PCP_Provider_Key = Provider_Key
    WHERE Encounter_Department_Key = 43
    GROUP BY
        Provider_Key,
        Provider_Name
    ORDER BY
        Number_Of_Encounters_With_Emergency_Department DESC;
    ```
    
    |Provider_Key|Provider_Name|Number_Of_Encounters_With_Emergency_Department|
    |---|---|---|
    |1|NONON|42|
    |794|ownUnk|33|
    |5|UVACLI|23|
    |6|UVACLI|18|
    |702|NOUNK|14|
    |343|NONSEL|9|
    |431|PRONON|6|
    |413|MEGKEE|6|
    |128|JOCSCH|5|
    |596|DANTYL|5|
    |306|FLUCOR|5|
    |793|TEMPCP|5|
    |492|THOALB|4|
    |466|ERIZAN|4|
    |418|ELISCH|4|
    |671|GRESTR|4|
    |780|CHRASH|4|
    |753|DAVCAL|4|
    |645|ANDCHA|4|
    |578|ANNJES|4|
    |198|LAUHOE|4|
    |752|MARBAD|4|
    |192|MATCUR|4|
    |360|MATGRE|4|
    |715|RACSPI|4|
    |217|PAUWIS|4|
    |334|LINPER|3|
    |586|LISKIN|3|
    |524|KATDEG|3|
    |392|JOYGEI|3|
    |211|KAIALT|3|
    |372|JOHLEI|3|
    |147|KARSTA|3|
    |380|GHONON|3|
    |359|GINENG|3|
    |57|JEAENG|3|
    |525|JERKEN|3|
    |572|AMYPOT|3|
    |419|ANNRAN|3|
    |506|ALABRO|3|
    |484|AMAGON|3|
    |595|DONLAN|3|
    |84|CHAMOR|3|
    |346|CHRDUB|3|
    |378|WENWES|3|
    |683|TERBAB|3|
    |352|STEHEI|3|
    |368|SUSLAU|3|
    |622|STESUL|2|
    |748|STESCH|2|
    |15|RICMUL|2|
    |470|SHEDAV|2|
    |730|TABDAV|2|
    |320|CARARM|2|
    |684|CHRTIE|2|
    |583|CORPAR|2|
    |653|DEBADA|2|
    |83|GRETUR|2|
    |570|EDWHAR|2|
    |744|ANDBUR|2|
    |573|DIABAR|2|
    |203|EVAPRI|2|
    |750|ABHRAV|2|
    |119|ADAPUR|2|
    |62|ANNROA|2|
    |277|A.TRU|2|
    |789|ANDVIP|2|
    |673|ANNKLE|2|
    |276|ANNABR|2|
    |698|ASHHAR|2|
    |89|CARCHE|2|
    |751|BENROB|2|
    |745|BENWIS|2|
    |332|JAMHUT|2|
    |151|JOHCLI|2|
    |613|JAYGIL|2|
    |58|KEVMCC|2|
    |696|KATHED|2|
    |349|KIMBED|2|
    |482|KHAPHA|2|
    |330|LORBAL|2|
    |747|LYDBUS|2|
    |16|PEDCLI|2|
    |391|PPREY|2|
    |61|PRIKOH|2|
    |174|REBHU|2|
    |191|SADGIR|2|
    |230|SAMCHA|2|
    |574|SARDAL|2|
    |231|MATMIR|2|
    |770|NICBYR|2|
    |49|MORNEW|2|
    |667|MARWHI|2|
    |109|MICSPR|2|
    |666|JOSGRE|2|
    |98|MANTRI|2|
    |358|MARLEP|2|
    |416|MARMEN|2|
    |760|MARMEN|1|
    |369|MARPRE|1|
    |718|MARWAR|1|
    |284|MARMAY|1|
    |25|MELBON|1|
    |627|MERQUA|1|
    |772|MICBRI|1|
    |229|MICCAR|1|
    |727|MICMAR|1|
    |123|MICMCC|1|
    |302|MICPAD|1|
    |531|MICPRO|1|
    |68|MICRIC|1|
    |734|MICROB|1|
    |460|MICSTY|1|
    |564|MICWIL|1|
    |289|MINSHA|1|
    |127|MONHEH|1|
    |587|MONKAN|1|
    |26|MORCLI|1|
    |660|MARZAY|1|
    |778|MASMOR|1|
    |275|MATGIE|1|
    |499|NANLUT|1|
    |143|NATMUR|1|
    |56|NATOWE|1|
    |742|NATPHA|1|
    |252|NICLOR|1|
    |523|SARSPR|1|
    |120|SARYOW|1|
    |371|SCOSEA|1|
    |261|SCOYOU|1|
    |489|SENCLI|1|
    |741|SERERT|1|
    |555|SHAGUP|1|
    |679|SHAMIL|1|
    |575|REBMUL|1|
    |641|RENFIS|1|
    |285|RICBRA|1|
    |463|RICHAL|1|
    |776|RICMIL|1|
    |635|RANBAK|1|
    |688|RANLAN|1|
    |264|RANSAM|1|
    |327|RAYMAR|1|
    |348|REBCOM|1|
    |430|PROCOM|1|
    |87|PRICAL|1|
    |303|PEDCLI|1|
    |646|PETNIS|1|
    |432|PHYUVA|1|
    |436|PIECLI|1|
    |7|PEDCLI|1|
    |291|PAINOL|1|
    |721|PAMMAN|1|
    |628|PAMTET|1|
    |48|PATPLE|1|
    |510|PAUJOH|1|
    |488|PAUMAX|1|
    |238|MACFRA|1|
    |213|MADMUR|1|
    |307|LOUCLI|1|
    |317|LOUHAN|1|
    |557|MARGAR|1|
    |604|MARHAN|1|
    |597|MARHOB|1|
    |383|KIMBAU|1|
    |8|LAUNUR|1|
    |257|LINCAR|1|
    |546|LOAKLI|1|
    |414|LINWAG|1|
    |563|KIMDOW|1|
    |318|KIYASA|1|
    |694|KRIDAL|1|
    |764|KRYPOR|1|
    |355|KURELW|1|
    |201|LARTRI|1|
    |137|LATSHI|1|
    |367|LAUARC|1|
    |220|LAUBAB|1|
    |60|LAUGIB|1|
    |387|KATJAF|1|
    |765|KATMIK|1|
    |323|KBMEMR|1|
    |697|KELGOO|1|
    |165|KENMIC|1|
    |739|KEVMCC|1|
    |207|KEVVOL|1|
    |91|KATGUI|1|
    |762|JEADAV|1|
    |356|JOHDAV|1|
    |30|JULHIL|1|
    |699|JULOWE|1|
    |478|JUNKIM|1|
    |247|JUSELK|1|
    |9|KATBAR|1|
    |110|JOHWIS|1|
    |74|JOHWIT|1|
    |437|KAIBEI|1|
    |746|KARMAC|1|
    |631|KARPOE|1|
    |685|JAMLAG|1|
    |160|JAMNGO|1|
    |263|JAMPLE|1|
    |235|GORSMI|1|
    |458|GREBAN|1|
    |328|GREBRA|1|
    |539|GREGEL|1|
    |775|GREMAL|1|
    |689|JESSAL|1|
    |324|JIMADC|1|
    |618|JOALEE|1|
    |495|JENBLO|1|
    |536|JENHER|1|
    |329|JENSAR|1|
    |451|BERFOC|1|
    |347|BETJAE|1|
    |580|BLUCLI|1|
    |514|BLUTEL|1|
    |265|BREBRA|1|
    |647|BRECAS|1|
    |507|BRIEAS|1|
    |240|BROMIL|1|
    |446|BRUCAM|1|
    |427|BRUSCH|1|
    |82|BRYCOC|1|
    |132|CAIBUL|1|
    |101|CALGEN|1|
    |731|CAMSIM|1|
    |738|CARQUI|1|
    |605|CARRHE|1|
    |732|CASDIS|1|
    |672|CATBOI|1|
    |362|CATCAS|1|
    |670|CATVAR|1|
    |2|CENHEA|1|
    |652|CHACOL|1|
    |529|AUDBAR|1|
    |376|BARPOS|1|
    |108|BENFUL|1|
    |743|ANNHAK|1|
    |374|ANDWAL|1|
    |543|ANDHAW|1|
    |171|ABDAGH|1|
    |421|AMYWRE|1|
    |662|ANTMAR|1|
    |117|ANUGUD|1|
    |435|ARCLOR|1|
    |219|ARTLAN|1|
    |706|ARTTIC|1|
    |784|ASHAKK|1|
    |180|ASHCOM|1|
    |11|AHGBOL|1|
    |95|AISCAM|1|
    |80|AKUBOA|1|
    |629|ABIKUM|1|
    |705|ADAARN|1|
    |331|ADAHOL|1|
    |155|AMBROB|1|
    |501|AMBYOD|1|
    |490|AMIMUN|1|
    |477|AMYBRO|1|
    |319|AMYCOO|1|
    |166|ALELAV|1|
    |513|ALLCHU|1|
    |552|ALTMIR|1|
    |602|EVAPRY|1|
    |141|FARDET|1|
    |305|FRECLI|1|
    |461|EUGROB|1|
    |651|EVAKAR|1|
    |665|ELIKOS|1|
    |534|ELILYO|1|
    |459|ELIPIC|1|
    |93|ELLGOL|1|
    |85|EMIMIN|1|
    |106|EMMTRA|1|
    |133|GRIBOU|1|
    |94|GRISON|1|
    |259|HAKDAG|1|
    |51|HALBLA|1|
    |254|HANLAI|1|
    |619|HARCRA|1|
    |311|HARHEA|1|
    |65|HCHCLI|1|
    |176|HEAFRA|1|
    |417|HEAQUI|1|
    |713|INECAR|1|
    |481|IRAHEL|1|
    |735|IREMAT|1|
    |183|JACFRI|1|
    |373|JAMBER|1|
    |338|DEBBAB|1|
    |462|DEIDON|1|
    |407|DENYOU|1|
    |693|DONLEE|1|
    |313|DOWFAM|1|
    |711|DUNMAC|1|
    |135|ECHBUF|1|
    |447|DAVCAM|1|
    |453|DAVCHE|1|
    |465|DAVGRE|1|
    |52|DAVSUY|1|
    |321|CHRCRA|1|
    |17|DARNIG|1|
    |516|CURJAN|1|
    |312|CVICLI|1|
    |433|CVINUR|1|
    |790|CYNLI|1|
    |125|DANSAW|1|
    |729|CINFEE|1|
    |99|CLAHUM|1|
    |761|COLMER|1|
    |308|COMCLI|1|
    |293|CARBOE|1|
    |350|CHASAU|1|
    |714|CHERAO|1|
    |633|CHRHEC|1|
    |763|CHRLAM|1|
    |617|CHRMAN|1|
    |159|TALMAH|1|
    |724|TALSEN|1|
    |27|TANCUS|1|
    |686|TARABE|1|
    |707|TEOBRO|1|
    |309|UVACLI|1|
    |344|UVACLI|1|
    |661|UVACLI|1|
    |491|VACLI|1|
    |342|VALHOS|1|
    |115|VARKAV|1|
    |335|VERGUA|1|
    |260|VICHAM|1|
    |547|VICSUL|1|
    |181|VIKZEL|1|
    |294|VISPAT|1|
    |687|WARCLI|1|
    |541|SHEHIG|1|
    |589|SIMLEH|1|
    |480|SIOSTA|1|
    |473|SPRFAM|1|
    |226|STEALD|1|
    |566|STEGRI|1|
    |654|ROBGOO|1|
    |283|ROBMIC|1|
    |690|ROBRAM|1|
    |150|ROBSTO|1|
    |126|RUSSAW|1|
    |779|STESHA|1|
    |782|STEMUM|1|
    |3|STUFAM|1|
    |781|SUSSMI|1|
    |722|WILMAL|1|
    |669|WILMIX|1|
    |221|YASKHA|1|
    |783|ZACBOG|1|
    |177|THOHIL|1|
    |218|THOWOL|1|
    |771|TIFPOW|1|
    |53|TIMPOW|1|
    |486|TONFIO|1|
    |599|TONKIS|1|
    