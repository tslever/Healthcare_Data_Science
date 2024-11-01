import pandas as pd

subtable_of_table_chartevents_re_systolic_blood_pressure = pd.read_csv(
    filepath_or_buffer = "subtable_of_table_chartevents_re_systolic_blood_pressure.csv",
    dtype = {"subject_id": int, "hadm_id": int, "stay_id": int, "value": float}
)

data_frame_group_by = subtable_of_table_chartevents_re_systolic_blood_pressure.groupby(
    by = ["subject_id", "hadm_id", "stay_id"]
)

data_frame_with_index_with_grouping_columns = data_frame_group_by["value"].agg(
    minimum_systolic_blood_pressure = ("min"),
    first_quartile_systolic_blood_pressure = (lambda x: x.quantile(0.25)),
    median_systolic_blood_pressure = ("median"),
    third_quartile_systolic_blood_pressure = (lambda x: x.quantile(0.75)),
    maximum_systolic_blood_pressure = ("max")
)

table_of_subject_ids_hadm_ids_stay_ids_and_systolic_blood_pressure_statistics = \
    data_frame_with_index_with_grouping_columns.reset_index()

table_of_subject_ids_hadm_ids_stay_ids_and_systolic_blood_pressure_statistics.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_stay_ids_and_systolic_blood_pressure_statistics.csv",
    index = False
)