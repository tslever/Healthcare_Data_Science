import pandas as pd

subtable_of_table_icustays = pd.read_csv(
    filepath_or_buffer = "subtable_of_table_icustays.csv",
    dtype = {"subject_id": int, "hadm_id": int, "stay_id": int, "los": float}
)

table_of_subject_ids_and_bmis = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_and_bmis.csv",
    dtype = {"subject_id": int, "bmi": str}
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmis = pd.merge(
    subtable_of_table_icustays,
    table_of_subject_ids_and_bmis,
    on = "subject_id",
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmis.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmis.csv",
    index = False
)