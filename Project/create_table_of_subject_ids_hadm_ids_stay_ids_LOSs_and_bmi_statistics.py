import pandas as pd

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmis = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmis.csv",
    dtype = {"subject_id": int, "hadm_id": int, "stay_id": int, "los": float, "BMI": float}
)

data_frame_group_by = table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmis.groupby(
    by = ["subject_id", "hadm_id", "stay_id", "los"]
)

data_frame_with_index_with_grouping_columns = data_frame_group_by["BMI"].agg(
    minimum_BMI = ("min"),
    first_quartile_BMI = (lambda x: x.quantile(0.25)),
    median_BMI = ("median"),
    third_quartile_BMI = (lambda x: x.quantile(0.75)),
    maximum_BMI = ("max")
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmi_statistics = \
    data_frame_with_index_with_grouping_columns.reset_index()

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmi_statistics.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmi_statistics.csv",
    index = False
)