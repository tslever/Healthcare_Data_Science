import pandas as pd

subtable_of_table_icustays = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/icu/icustays.csv",
    usecols = ["subject_id", "hadm_id", "stay_id", "intime", "outtime", "los"],
    dtype = {"subject_id": int, "result_name": "string", "result_value": "string"},
    parse_dates = ["intime", "outtime"],
    date_parser = lambda x: pd.to_datetime(x, format = "%Y-%m-%d %H:%M:%S", errors = "coerce"),
    nrows = 1000
)

subtable_of_table_icustays = subtable_of_table_icustays[
    (subtable_of_table_icustays["subject_id"].notna()) &
    (subtable_of_table_icustays["hadm_id"].notna()) &
    (subtable_of_table_icustays["stay_id"].notna()) &
    (subtable_of_table_icustays["intime"].notna()) &
    (subtable_of_table_icustays["outtime"].notna()) &
    (subtable_of_table_icustays["los"].notna())
]

subtable_of_table_icustays.to_csv(
    path_or_buf = "subtable_of_table_icustays.csv",
    index = False
)