import pandas as pd

table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_values_uoms_and_drg_types_and_codes = pd.read_csv(
    filepath_or_buffer = "table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_values_uoms_and_drg_types_and_codes.csv",
)

table_admissions = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/hosp/admissions.csv",
    usecols = ["hadm_id", "race"],
    dtype = {"hadm_id": int, "race": str}
)

table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes = \
    table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_values_uoms_and_drg_types_and_codes.merge(
        table_admissions,
        on = "hadm_id",
        how = "left"
    )

table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes.to_csv(
    path_or_buf = "table_of_subject_hadm_stay_and_vital_ids_LOSs_sex_age_race_values_uoms_and_drg_types_and_codes.csv",
    index = False
)