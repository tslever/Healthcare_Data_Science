import pandas as pd


table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "los": float
    }
)

table_of_subject_ids_hadm_ids_and_disease_indicators = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_and_disease_indicators.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int
    }
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_and_disease_indicators = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics,
    table_of_subject_ids_hadm_ids_and_disease_indicators,
    on = ["subject_id", "hadm_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_and_disease_indicators.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_and_disease_indicators.csv",
    index = False
)