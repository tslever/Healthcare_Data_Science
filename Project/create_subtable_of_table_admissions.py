import pandas as pd


subtable_of_table_admissions = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/hosp/admissions.csv",
    usecols = ["subject_id", "hadm_id", "race"],
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "race": str
    }
)

subtable_of_table_admissions = subtable_of_table_admissions[
    subtable_of_table_admissions["subject_id"].notna() &
    subtable_of_table_admissions["hadm_id"].notna() &
    subtable_of_table_admissions["race"].notna()
]

list_of_races = sorted(subtable_of_table_admissions["race"].unique())

table_of_indices_and_races = pd.DataFrame(
    data = {"race": list_of_races}
).reset_index()

table_of_indices_and_races.to_csv(
    path_or_buf = "table_of_indices_and_races.csv",
    index = False
)

race_to_index = table_of_indices_and_races.set_index("race")["index"]

subtable_of_table_admissions["race"] = \
    subtable_of_table_admissions["race"].map(race_to_index)

subtable_of_table_admissions.to_csv(
    path_or_buf = "subtable_of_table_admissions.csv",
    index = False
)