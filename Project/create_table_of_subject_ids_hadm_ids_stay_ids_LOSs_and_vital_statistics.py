import pandas as pd


table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmi_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmi_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "los": float,
        "minimum_BMI": float,
        "first_quartile_BMI": float,
        "median_BMI": float,
        "third_quartile_BMI": float,
        "maximum_BMI": float
    }
)

table_of_subject_ids_hadm_ids_stay_ids_and_diastolic_blood_pressure_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_and_diastolic_blood_pressure_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "minimum_diastolic_blood_pressure": float,
        "first_quartile_diastolic_blood_pressure": float,
        "median_diastolic_blood_pressure": float,
        "third_quartile_diastolic_blood_pressure": float,
        "maximum_diastolic_blood_pressure": float        
    }
)

table_of_subject_ids_hadm_ids_stay_ids_and_systolic_blood_pressure_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_and_systolic_blood_pressure_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "minimum_systolic_blood_pressure": float,
        "first_quartile_systolic_blood_pressure": float,
        "median_systolic_blood_pressure": float,
        "third_quartile_systolic_blood_pressure": float,
        "maximum_systolic_blood_pressure": float        
    }
)

table_of_subject_ids_hadm_ids_stay_ids_and_heart_rate_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_and_heart_rate_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "minimum_heart_rate": float,
        "first_quartile_heart_rate": float,
        "median_heart_rate": float,
        "third_quartile_heart_rate": float,
        "maximum_heart_rate": float        
    }
)

table_of_subject_ids_hadm_ids_stay_ids_and_O2_saturation_pulseoxymetry_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_and_O2_saturation_pulseoxymetry_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "minimum_O2_saturation_pulseoxymetry": float,
        "first_quartile_O2_saturation_pulseoxymetry": float,
        "median_O2_saturation_pulseoxymetry": float,
        "third_quartile_O2_saturation_pulseoxymetry": float,
        "maximum_O2_saturation_pulseoxymetry": float
    }
)

table_of_subject_ids_hadm_ids_stay_ids_and_respiratory_rate_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_and_respiratory_rate_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "minimum_respiratory_rate": float,
        "first_quartile_respiratory_rate": float,
        "median_respiratory_rate": float,
        "third_quartile_respiratory_rate": float,
        "maximum_respiratory_rate": float
    }
)

table_of_subject_ids_hadm_ids_stay_ids_and_temperature_statistics = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_and_temperature_statistics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "minimum_temperature": float,
        "first_quartile_temperature": float,
        "median_temperature": float,
        "third_quartile_temperature": float,
        "maximum_temperature": float
    }
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_bmi_statistics,
    table_of_subject_ids_hadm_ids_stay_ids_and_diastolic_blood_pressure_statistics,
    on = ["subject_id", "hadm_id", "stay_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics,
    table_of_subject_ids_hadm_ids_stay_ids_and_systolic_blood_pressure_statistics,
    on = ["subject_id", "hadm_id", "stay_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics,
    table_of_subject_ids_hadm_ids_stay_ids_and_heart_rate_statistics,
    on = ["subject_id", "hadm_id", "stay_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics,
    table_of_subject_ids_hadm_ids_stay_ids_and_O2_saturation_pulseoxymetry_statistics,
    on = ["subject_id", "hadm_id", "stay_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics,
    table_of_subject_ids_hadm_ids_stay_ids_and_respiratory_rate_statistics,
    on = ["subject_id", "hadm_id", "stay_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics = pd.merge(
    table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics,
    table_of_subject_ids_hadm_ids_stay_ids_and_temperature_statistics,
    on = ["subject_id", "hadm_id", "stay_id"],
    how = "inner"
)

table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_and_vital_statistics.csv",
    index = False
)