SELECT Patient_Gender, COUNT(Patient_Key) AS Number_Of_Patients
FROM healthcare.dbo.patients
GROUP BY Patient_Gender