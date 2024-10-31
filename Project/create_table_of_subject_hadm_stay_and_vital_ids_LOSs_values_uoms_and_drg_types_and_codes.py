import numpy as np
import pandas as pd


table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms = pd.read_csv(
    filepath_or_buffer= "table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms.csv",
    dtype = {"subject_id": int, "hadm_id": int, "stay_id": int, "los": float, "valueuom": str}
)

table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms = \
    table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms.dropna(subset = ["itemid"])

table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms["itemid"] = \
    table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms["itemid"].astype(int)

table_drgcodes = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/hosp/drgcodes.csv",
    dtype = {"subject_id": int, "hadm_id": int, "drg_type": str, "drg_code": str}
)

table_of_subject_hadm_stay_and_vital_ids_LOSs_values_uoms_and_drg_types_and_codes = table_of_subject_hadm_stay_and_vital_ids_LOSs_values_and_uoms.merge(
    table_drgcodes,
    on = ["hadm_id"],
    how = "left"
)

table_of_subject_hadm_stay_and_vital_ids_LOSs_values_uoms_and_drg_types_and_codes.to_csv(
    path_or_buf = "table_of_subject_hadm_stay_and_vital_ids_LOSs_values_uoms_and_drg_types_and_codes.csv",
    index = False
)