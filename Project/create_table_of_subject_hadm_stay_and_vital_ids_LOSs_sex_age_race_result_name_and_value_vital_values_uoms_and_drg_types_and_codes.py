import pandas as pd

table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes = pd.read_csv(
    filepath_or_buffer = "table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes.csv",
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