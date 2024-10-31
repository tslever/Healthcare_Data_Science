import pandas as pd


table_of_stay_ids_item_ids_and_values = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/icu/chartevents.csv",
    usecols = ["stay_id", "itemid", "value", "valueuom"],
    dtype = {"stay_id": int, "itemid": int, "valueuom": str}
)

table_icustays = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/icu/icustays.csv",
    dtype = {"stay_id": int, "los": float}
)
subtable_of_icustays_with_LOSs = table_icustays[~table_icustays["los"].isnull()]
table_of_stay_ids_and_LOSs = subtable_of_icustays_with_LOSs[["stay_id", "los"]]

table_of_stay_ids_LOSs_item_ids_values_and_uoms = table_of_stay_ids_and_LOSs.merge(
    table_of_stay_ids_item_ids_and_values,
    on = "stay_id",
    how = "left"
)

table_of_stay_ids_LOSs_item_ids_values_and_uoms.to_csv(
    path_or_buf = "table_of_stay_IDs_LOSs_item_IDs_values_and_UOMs",
    index = False
)