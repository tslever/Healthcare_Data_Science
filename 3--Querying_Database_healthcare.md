# SQL

Created on 09/08/2024 by Tom Lever

Updated on 09/08/2024 by Tom Lever


1. How many of the patients are male and female, respectively?

```
SELECT Patient_Gender, COUNT(Patient_Key) AS Number_Of_Patients
FROM healthcare.dbo.patients
GROUP BY Patient_Gender
```

|Patient_Gender|Number_Of_Patients|
|---|---|
|Male|772|
|Female|940|

772 and 940 patients are male and female, respectively.


2. What are the top 3 states where patients live?

```
SELECT TOP 3 Patient_Address_State, COUNT(Patient_Key) AS Number_Of_Patients
FROM healthcare.dbo.patients
GROUP BY Patient_Address_State
ORDER BY Number_Of_Patients DESC
```

|Patient_Address_State|Number_Of_Patients|
|---|---|
|Virginia|1674|
|West Virginia|9|
|Tennessee|6|

The top three states where patients live by number of patients are Virginia, West Virginia, and Tennessee.


3. What are the ages of the youngest and oldest patients?

```
SELECT
    MIN(DATEDIFF(YEAR, Patient_Birth_Date, GETDATE())) AS Age_Of_Youngest_Patient,
    MAX(DATEDIFF(YEAR, Patient_Birth_Date, GETDATE())) AS Age_Of_Oldest_Patient
FROM healthcare.dbo.patients
```

|Age_Of_Youngest_Patient|Age_Of_Oldest_Patient|
|---|---|
|1|88|


4. How many patients got admitted to the hospital on 2023-03-18, and at what time was the latest admission that day? Note that the date column experienced a problem with nulls during import. See if you can figure out what happened. To resolve the issue, instead of `CAST`, use `TRY_CAST(NULLIF([Encounter_Admit_Date], 'null') AS DATE)`.

```
WITH Table_Of_Encounter_Admit_Dates_Of_2023_03_18 AS (
    SELECT Encounter_Admit_Date
    FROM healthcare.dbo.encounters
    WHERE TRY_CAST(NULLIF([Encounter_Admit_Date], 'null') AS DATE) = '2023-03-18'
)
SELECT
    COUNT(Encounter_Admit_Date) AS Number_Of_Admissions,
    MAX(CAST(Encounter_Admit_Date AS TIME)) AS Time_Of_Latest_Admission
FROM Table_Of_Encounter_Admit_Dates_Of_2023_03_18
```

|Number_Of_Admissions|Time_Of_Latest_Admission|
|---|---|
|218|23:48:00|

218 patients were admitted to the hospital on 2023-03-18. The latest admission that day was at 23:48:00.