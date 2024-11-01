import pandas as pd

subtable_of_table_chartevents_re_O2_saturation_pulseoxymetry = pd.read_csv(
    filepath_or_buffer = "subtable_of_table_chartevents_re_O2_saturation_pulseoxymetry.csv",
    dtype = {"subject_id": int, "hadm_id": int, "stay_id": int, "value": float}
)

data_frame_group_by = subtable_of_table_chartevents_re_O2_saturation_pulseoxymetry.groupby(
    by = ["subject_id", "hadm_id", "stay_id"]
)

data_frame_with_index_with_grouping_columns = data_frame_group_by["value"].agg(
    minimum_O2_saturation_pulseoxymetry = ("min"),
    first_quartile_O2_saturation_pulseoxymetry = (lambda x: x.quantile(0.25)),
    median_O2_saturation_pulseoxymetry = ("median"),
    third_quartile_O2_saturation_pulseoxymetry = (lambda x: x.quantile(0.75)),
    maximum_O2_saturation_pulseoxymetry = ("max")
)

table_of_subject_ids_hadm_ids_stay_ids_and_O2_saturation_pulseoxymetry_statistics = \
    data_frame_with_index_with_grouping_columns.reset_index()

table_of_subject_ids_hadm_ids_stay_ids_and_O2_saturation_pulseoxymetry_statistics.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_stay_ids_and_O2_saturation_pulseoxymetry_statistics.csv",
    index = False
)