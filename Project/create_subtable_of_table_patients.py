import pandas as pd


subtable_of_table_patients = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/hosp/patients.csv",
    usecols = ["subject_id", "gender", "anchor_age"],
    dtype = {
        "subject_id": int,
        "gender": str,
        "anchor_age": int
    }
)

subtable_of_table_patients = subtable_of_table_patients[
    subtable_of_table_patients["subject_id"].notna() &
    subtable_of_table_patients["gender"].notna() &
    subtable_of_table_patients["anchor_age"].notna()
]

subtable_of_table_patients["gender"] = \
    subtable_of_table_patients["gender"].replace({'F': 0, 'M': 1})

subtable_of_table_patients.to_csv(
    path_or_buf = "subtable_of_table_patients.csv",
    index = False
)