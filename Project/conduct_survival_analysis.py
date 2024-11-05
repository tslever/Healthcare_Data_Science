# The following code predicts time until discharge from ICU occurs (i.e., Length Of Stay).

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sksurv.ensemble import RandomSurvivalForest
from sksurv.util import Surv
import matplotlib.pyplot as plt


data_frame = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "los": float,
        # 7 groups of columns of vital statistics with 5 columns of vital statistics per group,
        # 20 columns of indicators of whether or not stay is associated with one of the 20 most common diseases,
        "gender": int,
        "anchor_age": int,
        "race": int
    }
)
data_frame_for_training = data_frame.sample(frac = 0.8, random_state = 0)
data_frame_for_testing = data_frame.drop(data_frame_for_training.index)

list_of_names_of_all_columns = data_frame_for_training.columns.tolist()
list_of_names_of_ids_and_response = ['subject_id', 'hadm_id', 'stay_id', 'los']
list_of_names_of_predictors = [
    name_of_column for name_of_column in list_of_names_of_all_columns
    if name_of_column not in list_of_names_of_ids_and_response
]

list_of_names_of_numerical_predictors = [
    name_of_column for name_of_column in list_of_names_of_predictors
    if
        name_of_column.startswith('minimum_') or
        name_of_column.startswith('first_quartile_') or
        name_of_column.startswith('median_') or
        name_of_column.startswith('third_quartile_') or
        name_of_column.startswith('maximum_') or
        name_of_column == 'anchor_age'
]

list_of_names_of_categorical_predictors = [
    name_of_column for name_of_column in list_of_names_of_predictors
    if
        name_of_column.startswith('APR_') or
        name_of_column.startswith('HCFA_') or
        name_of_column == "gender" or
        name_of_column == "race"
]

assert set(list_of_names_of_numerical_predictors + list_of_names_of_categorical_predictors) == set(list_of_names_of_predictors), "Mismatch in predictor variables"

data_frame_for_training[list_of_names_of_numerical_predictors] = data_frame_for_training[list_of_names_of_numerical_predictors].apply(pd.to_numeric, errors = "raise")
data_frame_for_testing[list_of_names_of_numerical_predictors] = data_frame_for_testing[list_of_names_of_numerical_predictors].apply(pd.to_numeric, errors = "raise")

data_frame_for_training[list_of_names_of_categorical_predictors] = data_frame_for_training[list_of_names_of_categorical_predictors].astype('category')
data_frame_for_testing[list_of_names_of_categorical_predictors] = data_frame_for_testing[list_of_names_of_categorical_predictors].astype('category')

data_frame_for_training['los'] = data_frame_for_training['los'].astype(float)
data_frame_for_testing['los'] = data_frame_for_testing['los'].astype(float)

data_frame_for_training['status'] = 1
data_frame_for_testing['status'] = 1

nd_array_of_tuples_of_true_event_indicators_and_LOSs_for_training = Surv.from_arrays(event = data_frame_for_training['status'] == 1, time=data_frame_for_training['los'])
nd_array_of_tuples_of_true_event_indicators_and_LOSs_for_testing = Surv.from_arrays(event = data_frame_for_testing['status'] == 1, time=data_frame_for_testing['los'])

column_transformer = ColumnTransformer(
    transformers = [
        ('transformer_of_columns_with_numerical_values', StandardScaler(), list_of_names_of_numerical_predictors),
        ('transformer_of_columns_with_categorical_values', OneHotEncoder(sparse_output = False, handle_unknown = 'ignore'), list_of_names_of_categorical_predictors)
    ])

pipeline = Pipeline(
    steps = [
        ('step_transform_columns', column_transformer),
        (
            'step_classify',
            RandomSurvivalForest(
                n_estimators = 100,
                min_samples_split = 10,
                random_state = 0
            )
        )
    ]
)

pipeline.fit(
    X = data_frame_for_training[list_of_names_of_predictors],
    y = nd_array_of_tuples_of_true_event_indicators_and_LOSs_for_training
)

# There is one step function of the from f(z) = y_i, x_i <= z < x_{i+1}
# for each row in the testing data set.
list_of_step_functions = pipeline.predict_survival_function(
    data_frame_for_testing[list_of_names_of_predictors]
)

minimum_LOS = min(step_function.x[0] for step_function in list_of_step_functions)
maximum_LOS = max(step_function.x[-1] for step_function in list_of_step_functions)
ndarray_of_linearly_spaced_LOSs = np.linspace(
    start = minimum_LOS,
    stop = maximum_LOS,
    num = 100
)

list_of_predicted_expected_LOSs = []
for step_function in list_of_step_functions:
    predicted_expected_LOS = np.trapz(step_function.y, step_function.x)
    list_of_predicted_expected_LOSs.append(predicted_expected_LOS)

list_of_predicted_expected_LOSs_via_PDF = []
for step_function in list_of_step_functions:
    ndarray_of_CDF_values = 1 - step_function.y
    ndarray_of_interpolated_CDF_values = np.interp(
        x = ndarray_of_linearly_spaced_LOSs,
        xp = step_function.x,
        fp = ndarray_of_CDF_values
    )
    ndarray_of_PDF_values = np.gradient(
        ndarray_of_interpolated_CDF_values,
        ndarray_of_linearly_spaced_LOSs
    )
    predicted_expected_LOS = np.trapz(
        ndarray_of_linearly_spaced_LOSs * ndarray_of_PDF_values,
        ndarray_of_linearly_spaced_LOSs
    )
    list_of_predicted_expected_LOSs_via_PDF.append(predicted_expected_LOS)

data_frame_of_ids_and_actual_and_predicted_expected_LOSs = pd.DataFrame(
    data = {
        'subject_id': data_frame_for_testing['subject_id'].values,
        'hadm_id': data_frame_for_testing['hadm_id'].values,
        'stay_id': data_frame_for_testing['stay_id'].values,
        'actual_los': data_frame_for_testing['los'].values,
        'predicted_expected_los': list_of_predicted_expected_LOSs,
        'predicted_expected_los_according_to_PDF': list_of_predicted_expected_LOSs_via_PDF
    }
)

data_frame_of_ids_and_actual_and_predicted_expected_LOSs.to_csv(
    path_or_buf = 'data_frame_of_ids_and_actual_and_predicted_expected_LOSs.csv',
    index = False
)

list_of_ndarrays_of_survival_curve_values = []
for step_function in list_of_step_functions:
    ndarray_of_interpolated_survival_curve_values = np.interp(
        x = ndarray_of_linearly_spaced_LOSs,
        xp = step_function.x,
        fp = step_function.y
    )
    list_of_ndarrays_of_survival_curve_values.append(ndarray_of_interpolated_survival_curve_values)
    plt.step(
        x = ndarray_of_linearly_spaced_LOSs,
        y = ndarray_of_interpolated_survival_curve_values,
        where = "post",
        alpha = 0.2
    )
ndarray_of_ndarrays_of_survival_curve_values = np.array(list_of_ndarrays_of_survival_curve_values)
ndarray_array_of_average_survival_curve_values = np.mean(ndarray_of_ndarrays_of_survival_curve_values, axis = 0)
plt.step(
    x = ndarray_of_linearly_spaced_LOSs,
    y = ndarray_array_of_average_survival_curve_values,
    where = "post",
    linewidth = 2,
    color = "blue",
    label = "Average"
)
plt.xlabel(xlabel = "Length Of Stay (days)")
plt.ylabel(ylabel = "Survival Curve For Test Data")
plt.title(label = "Survival Curves for Test Data")
plt.legend()
plt.grid()
plt.show()

list_of_ndarrays_of_CDF_values = []
for step_function in list_of_step_functions:
    ndarray_of_CDF_values = 1 - step_function.y
    ndarray_of_interpolated_CDF_values = np.interp(
        x = ndarray_of_linearly_spaced_LOSs,
        xp = step_function.x,
        fp = ndarray_of_CDF_values
    )
    list_of_ndarrays_of_CDF_values.append(ndarray_of_interpolated_CDF_values)
    plt.step(
        x = ndarray_of_linearly_spaced_LOSs,
        y = ndarray_of_interpolated_CDF_values,
        where = "post",
        alpha = 0.2
    )
ndarray_of_ndarrays_of_CDF_values = np.array(list_of_ndarrays_of_CDF_values)
ndarray_of_average_CDF_values = np.mean(ndarray_of_ndarrays_of_CDF_values, axis = 0)
plt.step(
    x = ndarray_of_linearly_spaced_LOSs,
    y = ndarray_of_average_CDF_values,
    where = "post",
    linewidth = 2,
    color = "blue",
    label = "Average"
)
plt.xlabel(xlabel = "Length Of Stay (days)")
plt.ylabel(ylabel = "Cumulative Distribution Function Of LOS")
plt.title(label = "CDF Of LOS Vs. LOS For Test Data")
plt.legend()
plt.grid()
plt.show()

list_of_ndarrays_of_PDF_values = []
for step_function in list_of_step_functions:
    ndarray_of_CDF_values = 1 - step_function.y
    ndarray_of_interpolated_CDF_values = np.interp(
        x = ndarray_of_linearly_spaced_LOSs,
        xp = step_function.x,
        fp = ndarray_of_CDF_values
    )
    ndarray_of_PDF_values = np.gradient(
        ndarray_of_interpolated_CDF_values,
        ndarray_of_linearly_spaced_LOSs
    )
    list_of_ndarrays_of_PDF_values.append(ndarray_of_PDF_values)
    plt.plot(
        ndarray_of_linearly_spaced_LOSs,
        ndarray_of_PDF_values,
        alpha = 0.2
    )
ndarray_of_ndarrays_of_PDF_values = np.array(list_of_ndarrays_of_PDF_values)
ndarray_of_average_PDF_values = np.mean(ndarray_of_ndarrays_of_PDF_values, axis = 0)
plt.plot(
    ndarray_of_linearly_spaced_LOSs,
    ndarray_of_average_PDF_values,
    linewidth = 2,
    color = "blue",
    label = "Average"
)
plt.xlabel(xlabel = "Length Of Stay (days)")
plt.ylabel(ylabel = "Probability Density Function Of LOS Vs. LOS")
plt.title(label = "PDF Of LOS Vs. LOS For Test Data")
plt.legend()
plt.grid()
plt.show()