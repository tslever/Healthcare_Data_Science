import pandas as pd

subtable_of_table_omr = pd.read_csv(
    filepath_or_buffer = "mimic-iv-3.0/hosp/omr.csv",
    usecols = ["subject_id", "result_name", "result_value"],
    dtype = {"subject_id": int, "result_name": "string", "result_value": "string"}
)

table_of_subject_ids_result_name_re_BMI_and_result_value = subtable_of_table_omr[
    (subtable_of_table_omr["subject_id"].notna()) &
    (subtable_of_table_omr["result_name"] == "BMI (kg/m2)") &
    (subtable_of_table_omr["result_value"].notna())
]

table_of_subject_ids_and_bmis = \
    table_of_subject_ids_result_name_re_BMI_and_result_value.rename(
        columns = {"result_value": "BMI"}
    )[["subject_id", "BMI"]]

table_of_subject_ids_and_bmis.to_csv(
    path_or_buf = "table_of_subject_ids_and_bmis.csv",
    index = False
)