import pandas as pd


table_of_stay_and_item_ids_and_values = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/icu/chartevents.csv",
    usecols = ["stay_id", "itemid", "value", "valueuom"],
    dtype = {"stay_id": int, "itemid": int, "valueuom": str}
)

list_of_vital_ids = [
    220051, # Arterial Blood Pressure diastolic
    220050, # Arterial Blood Pressure systolic
    220045, # Heart Rate
    220277, # O2 saturation pulseoxymetry
    220210, # Respiration Rate
    223762 # Temperature Celsius
]
table_of_stay_and_vital_ids_and_values = table_of_stay_and_item_ids_and_values[
    table_of_stay_and_item_ids_and_values["itemid"].isin(list_of_vital_ids)
]

table_icustays = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/icu/icustays.csv",
    dtype = {"subject_id": int, "hadm_id": int, "stay_id": int, "los": float}
)
subtable_of_icustays_with_LOSs = table_icustays[~table_icustays["los"].isnull()]
table_of_subject_hadm_and_stay_ids_and_LOSs = subtable_of_icustays_with_LOSs[["stay_id", "los"]]

table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms = \
    table_of_subject_hadm_and_stay_ids_and_LOSs.merge(
        table_of_stay_and_vital_ids_and_values,
        on = "stay_id",
        how = "left"
    )

table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms.to_csv(
    path_or_buf = "table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms.csv",
    index = False
)