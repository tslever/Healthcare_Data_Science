from create_table import create_table

name_of_table = "Table_of_IDs_Of_Hospitalizations_Indicators_Of_Death_And_DRG_Info"

query = '''
    SELECT 
        admissions.hadm_id, 
        hospital_expire_flag,
        description,
        drg_type, 
        drg_code
    FROM admissions
    JOIN drgcodes
    ON admissions.hadm_id = drgcodes.hadm_id
'''

create_table(name_of_table = name_of_table, query = query)