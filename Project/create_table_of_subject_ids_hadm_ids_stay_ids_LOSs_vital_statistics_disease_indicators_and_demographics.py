import pandas as pd


table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_and_disease_indicators = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_and_disease_indicators.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "los": float
    }
)

subtable_of_table_patients = pd.read_csv(
    filepath_or_buffer = "subtable_of_table_patients.csv",
    dtype = {
        "subject_id": int,
        "gender": int,
        "anchor_age": int
    }
)

subtable_of_table_admissions = pd.read_csv(
    filepath_or_buffer = "subtable_of_table_admissions.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "race": int
    }
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_and_disease_indicators,
    subtable_of_table_patients,
    on = "subject_id",
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics,
    subtable_of_table_admissions,
    on = ["subject_id", "hadm_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics.csv",
    index = False
)