'''
import pandas as pd
import numpy as np

df = pd.read_csv("table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes.csv")
unique_subject_ids = df['subject_id'].unique()
half_point = len(unique_subject_ids) // 2
subject_ids_part1 = unique_subject_ids[:half_point]
subject_ids_part2 = unique_subject_ids[half_point:]

df_part = df[df['subject_id'].isin(subject_ids_part1)]
df_part.to_csv("output_part1.csv", index=False)

df_part = df[df['subject_id'].isin(subject_ids_part2)]
df_part.to_csv("output_part2.csv", index=False)
'''

'''
import pandas as pd

table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes = pd.read_csv(
    #filepath_or_buffer = "table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes.csv",
    filepath_or_buffer = "output_part2.csv"
)

table_omr = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/hosp/omr.csv",
    usecols = ["subject_id", "result_name", "result_value"],
    dtype = {"subject_id": int, "result_name": str, "result_value": str}
)

table_omr = table_omr[table_omr["result_name"] == "BMI (kg/m2)"]

table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_result_name_and_value_vital_values_uoms_and_drg_types_and_codes = \
    table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes.merge(
        table_omr,
        on = "subject_id",
        how = "left"
    )

table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_result_name_and_value_vital_values_uoms_and_drg_types_and_codes.to_csv(
    path_or_buf = "table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_result_name_and_value_vital_values_uoms_and_drg_types_and_codes.csv",
    index = False
)
'''

'''
with (
    open(
        file = "table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_result_name_and_value_vital_values_uoms_and_drg_types_and_codes--1_of_2.csv",
        mode = 'a'
    ) as file,
    open(
        file = "table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_result_name_and_value_vital_values_uoms_and_drg_types_and_codes--2_of_2.csv",
        mode = 'r'
    ) as file_to_append
):
    next(file_to_append)
    for line in file_to_append:
        file.write(line)
'''

'''
import pandas as pd

index_of_chunk = 0
for chunk in pd.read_csv(
    filepath_or_buffer = 'table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_result_name_and_value_vital_values_uoms_and_drg_types_and_codes.csv',
    chunksize = 70_000_000
):
    chunk = chunk.dropna(subset = ['result_name', 'result_value'])
    chunk['result_value'] = chunk['result_value'].astype(int)
    chunk = chunk.drop(columns = ['result_name'])
    chunk = chunk.rename(columns = {'result_value': 'BMI'})
    chunk.to_csv(path_or_buf = f"chunk_{index_of_chunk}.csv", index = False)
    index_of_chunk += 1
'''

'''
with open(file = "chunk_0.csv", mode = 'a') as file:
    for index_of_chunk in range(1, 10 + 1):
        with open(file = f"chunk_{index_of_chunk}.csv", mode = 'r') as file_to_append:
            next(file_to_append)
            for line in file_to_append:
                file.write(line)

import pandas as pd
'''

import pandas as pd

table_of_subject_hadm_and_stay_ids_LOSs_gender_race_age_BMIs_vital_IDs_values_and_uoms_and_drg_types_and_codes = pd.read_csv(
    filepath_or_buffer = "table_of_subject_hadm_and_stay_ids_LOSs_gender_race_age_BMIs_vital_IDs_values_and_uoms_and_drg_types_and_codes.csv",
    nrows = 1000
)
print(table_of_subject_hadm_and_stay_ids_LOSs_gender_race_age_BMIs_vital_IDs_values_and_uoms_and_drg_types_and_codes.iloc[0].T)