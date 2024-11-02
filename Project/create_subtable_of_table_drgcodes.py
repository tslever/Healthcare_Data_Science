import pandas as pd

subtable_of_table_drgcodes = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/hosp/drgcodes.csv",
    usecols = ["subject_id", "hadm_id", "drg_type", "drg_code"],
    dtype = {"subject_id": int, "hadm_id": int, "drg_type": str, "drg_code": str}
)

subtable_of_table_drgcodes = subtable_of_table_drgcodes[
    (subtable_of_table_drgcodes["subject_id"].notna()) &
    (subtable_of_table_drgcodes["hadm_id"].notna()) &
    (subtable_of_table_drgcodes["drg_type"].notna()) &
    (subtable_of_table_drgcodes["drg_code"].notna())
]

subtable_of_table_drgcodes.to_csv(
    path_or_buf = "subtable_of_table_drgcodes.csv",
    index = False
)