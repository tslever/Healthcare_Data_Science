from create_table import create_table

name_of_table = "Table_of_IDs_Of_Hospitalizations_And_Medication_Regimes"

query = '''
    SELECT
        hadm_id,
        GROUP_CONCAT(medication, ', ') AS medications
    FROM (
        SELECT DISTINCT hadm_id, medication
        FROM emar
        ORDER BY hadm_id, medication
    )
    GROUP BY hadm_id;
'''

create_table(name_of_table = name_of_table, query = query)