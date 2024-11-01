import pandas as pd

table_chartevents = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/icu/chartevents.csv",
    usecols = ["subject_id", "hadm_id", "stay_id", "itemid", "value", "valueuom"],
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "itemid": int,
        "value": str,
        "valueuom": str
    }
)

subtable_of_table_chartevents = table_chartevents[
    table_chartevents["subject_id"].notna() &
    table_chartevents["hadm_id"].notna() &
    table_chartevents["stay_id"].notna() &
    table_chartevents["itemid"].notna() &
    table_chartevents["value"].notna() &
    table_chartevents["valueuom"].notna()
]

subtable_of_table_chartevents_re_diastolic_blood_pressure = subtable_of_table_chartevents[
    subtable_of_table_chartevents["itemid"] == 220051
]
subtable_of_table_chartevents_re_diastolic_blood_pressure.to_csv(
    path_or_buf = "subtable_of_table_chartevents_re_diastolic_blood_pressure.csv",
    index = False
)

subtable_of_table_chartevents_re_systolic_blood_pressure = subtable_of_table_chartevents[
    subtable_of_table_chartevents["itemid"] == 220050
]
subtable_of_table_chartevents_re_systolic_blood_pressure.to_csv(
    path_or_buf = "subtable_of_table_chartevents_re_systolic_blood_pressure.csv",
    index = False
)

subtable_of_table_chartevents_re_heart_rate = subtable_of_table_chartevents[
    subtable_of_table_chartevents["itemid"] == 220045
]
subtable_of_table_chartevents_re_heart_rate.to_csv(
    path_or_buf = "subtable_of_table_chartevents_re_heart_rate.csv",
    index = False
)

subtable_of_table_chartevents_re_O2_saturation_pulseoxymetry = subtable_of_table_chartevents[
    subtable_of_table_chartevents["itemid"] == 220277
]
subtable_of_table_chartevents_re_O2_saturation_pulseoxymetry.to_csv(
    path_or_buf = "subtable_of_table_chartevents_re_O2_saturation_pulseoxymetry.csv",
    index = False
)

subtable_of_table_chartevents_re_respiratory_rate = subtable_of_table_chartevents[
    subtable_of_table_chartevents["itemid"] == 220210
]
subtable_of_table_chartevents_re_respiratory_rate.to_csv(
    path_or_buf = "subtable_of_table_chartevents_re_respiratory_rate.csv",
    index = False
)

subtable_of_table_chartevents_re_temperature = subtable_of_table_chartevents[
    subtable_of_table_chartevents["itemid"] == 223762
]
subtable_of_table_chartevents_re_temperature.to_csv(
    path_or_buf = "subtable_of_table_chartevents_re_temperature.csv",
    index = False
)