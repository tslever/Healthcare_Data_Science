import pandas as pd

subtable_of_table_icustays = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/icu/icustays.csv",
    usecols = ["subject_id", "hadm_id", "stay_id", "los"],
    dtype = {"subject_id": int, "result_name": "string", "result_value": "string"}
)

subtable_of_table_icustays = subtable_of_table_icustays[
    (subtable_of_table_icustays["subject_id"].notna()) &
    (subtable_of_table_icustays["hadm_id"].notna()) &
    (subtable_of_table_icustays["stay_id"].notna()) &
    (subtable_of_table_icustays["los"].notna())
]

subtable_of_table_icustays.to_csv(
    path_or_buf = "subtable_of_table_icustays.csv",
    index = False
)