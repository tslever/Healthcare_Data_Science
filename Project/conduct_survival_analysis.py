import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sksurv.ensemble import RandomSurvivalForest
from sksurv.util import Surv
from sklearn.metrics import mean_squared_error
from sksurv.metrics import concordance_index_censored
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
import os
from sklearn.inspection import permutation_importance

# Load data
data_frame = pd.read_csv(
    filepath_or_buffer="table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics.csv",
    dtype={
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "los": float,
        # Additional columns as necessary...
        "gender": int,
        "anchor_age": int,
        "race": int,
    },
)

# Set data types
list_of_names_of_all_columns = data_frame.columns.tolist()
list_of_names_of_ids_and_response = ["subject_id", "hadm_id", "stay_id", "los"]
list_of_names_of_predictors = [
    name_of_column
    for name_of_column in list_of_names_of_all_columns
    if name_of_column not in list_of_names_of_ids_and_response
]

list_of_names_of_numerical_predictors = [
    name_of_column
    for name_of_column in list_of_names_of_predictors
    if name_of_column.startswith("minimum_")
    or name_of_column.startswith("first_quartile_")
    or name_of_column.startswith("median_")
    or name_of_column.startswith("third_quartile_")
    or name_of_column.startswith("maximum_")
    or name_of_column == "anchor_age"
]

list_of_names_of_categorical_predictors = [
    name_of_column
    for name_of_column in list_of_names_of_predictors
    if name_of_column.startswith("APR_")
    or name_of_column.startswith("HCFA_")
    or name_of_column == "gender"
    or name_of_column == "race"
]

assert set(
    list_of_names_of_numerical_predictors + list_of_names_of_categorical_predictors
) == set(
    list_of_names_of_predictors
), "Mismatch in predictor variables"

data_frame[list_of_names_of_numerical_predictors] = data_frame[
    list_of_names_of_numerical_predictors
].apply(pd.to_numeric, errors="raise")

data_frame[list_of_names_of_categorical_predictors] = data_frame[
    list_of_names_of_categorical_predictors
].astype("category")

data_frame["los"] = data_frame["los"].astype(float)
data_frame["status"] = 1

# Define X and y
X = data_frame[list_of_names_of_predictors]
y = Surv.from_arrays(event=data_frame["status"] == 1, time=data_frame["los"])

# Define the pipeline
column_transformer = ColumnTransformer(
    transformers=[
        (
            "transformer_of_columns_with_numerical_values",
            StandardScaler(),
            list_of_names_of_numerical_predictors,
        ),
        (
            "transformer_of_columns_with_categorical_values",
            OneHotEncoder(sparse_output=False, handle_unknown="ignore"),
            list_of_names_of_categorical_predictors,
        ),
    ]
)

n_estimators = 100
max_depth = None
min_samples_split = 6
min_samples_leaf = 3
max_features = None

pipeline = Pipeline(
    steps=[
        ("step_transform_columns", column_transformer),
        (
            "step_classify",
            RandomSurvivalForest(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=0,
                max_features=max_features,
                max_leaf_nodes=None,
                bootstrap=True,
                oob_score=False,
                n_jobs=-1,
                random_state=0,
                verbose=1,
                warm_start=False,
                max_samples=None,
                low_memory=False,
            ),
        ),
    ]
)

path = f"Visualizations_Of_Performance/{n_estimators}_{max_depth}_{min_samples_split}_{min_samples_leaf}_{max_features}"
os.makedirs(path, exist_ok=True)

# Set up cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=0)

# Initialize lists to collect results
list_of_true_LOSs = []
list_of_predicted_expected_LOSs = []
list_of_event_indicators = []
list_of_step_functions = []
list_of_subject_ids = []
list_of_hadm_ids = []
list_of_stay_ids = []

# Initialize a dictionary to collect feature importances
from collections import defaultdict

feature_importances_dict = defaultdict(float)
num_folds = 0

# Function to compute the scoring metric
def score_model(model, X, y):
    # Predict the risk scores
    risk_scores = model.predict(X)
    # Compute the concordance index
    ci = concordance_index_censored(y['event'], y['time'], risk_scores)[0]
    return ci

# Cross-validation loop
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index].copy(), X.iloc[test_index].copy()
    y_train, y_test = y[train_index], y[test_index]

    # Ensure that the categorical variables are of type 'category'
    X_train[list_of_names_of_categorical_predictors] = X_train[
        list_of_names_of_categorical_predictors
    ].astype("category")
    X_test[list_of_names_of_categorical_predictors] = X_test[
        list_of_names_of_categorical_predictors
    ].astype("category")

    # Fit the pipeline
    pipeline.fit(X_train, y_train)

    # Predict survival functions on X_test
    step_functions = pipeline.predict_survival_function(X_test)

    # Collect the step functions
    list_of_step_functions.extend(step_functions)

    # Compute predicted expected LOS for each sample in X_test
    for step_function in step_functions:
        predicted_expected_LOS = np.trapz(step_function.y, step_function.x)
        list_of_predicted_expected_LOSs.append(predicted_expected_LOS)

    # Collect true LOS values
    true_LOSs = data_frame["los"].values[test_index]
    list_of_true_LOSs.extend(true_LOSs)

    # Collect event indicators
    event_indicators = data_frame["status"].values[test_index]
    list_of_event_indicators.extend(event_indicators)

    # Collect IDs for output
    subject_ids = data_frame["subject_id"].values[test_index]
    hadm_ids = data_frame["hadm_id"].values[test_index]
    stay_ids = data_frame["stay_id"].values[test_index]
    list_of_subject_ids.extend(subject_ids)
    list_of_hadm_ids.extend(hadm_ids)
    list_of_stay_ids.extend(stay_ids)

    # Compute permutation importance
    X_test_transformed = pipeline.named_steps["step_transform_columns"].transform(X_test)
    result = permutation_importance(
        pipeline.named_steps["step_classify"],
        X_test_transformed,
        y_test,
        n_repeats=5,
        random_state=0,
        scoring=score_model,
    )

    feature_names = pipeline.named_steps[
        "step_transform_columns"
    ].get_feature_names_out()

    # Map feature importances to original feature names
    per_fold_feature_importances = defaultdict(float)
    for name, importance in zip(feature_names, result.importances_mean):
        transformer_name, feature = name.split("__", 1)
        if transformer_name == "transformer_of_columns_with_numerical_values":
            # For numerical features
            original_feature_name = feature
        elif transformer_name == "transformer_of_columns_with_categorical_values":
            # For categorical features, e.g., 'gender_Male'
            original_feature_name = feature.split("_", 1)[0]
        else:
            original_feature_name = feature  # default case

        # Sum the importance for the original feature
        per_fold_feature_importances[original_feature_name] += importance

    # Add per_fold_feature_importances to the overall feature_importances_dict
    for feature_name, importance in per_fold_feature_importances.items():
        feature_importances_dict[feature_name] += importance

    num_folds += 1

# Average the feature importances over folds
for feature_name in feature_importances_dict:
    feature_importances_dict[feature_name] /= num_folds

# Convert the feature_importances_dict to a pandas DataFrame
feature_importances_df = pd.DataFrame(
    {
        "feature": list(feature_importances_dict.keys()),
        "importance": list(feature_importances_dict.values()),
    }
)

# Sort by importance
feature_importances_df = feature_importances_df.sort_values(
    by="importance", ascending=False
)

# Plot the feature importances
plt.figure(figsize=(10, 8))
plt.barh(
    y=feature_importances_df["feature"],
    width=feature_importances_df["importance"],
    color="skyblue",
)
plt.gca().invert_yaxis()  # To display the highest importance at the top
plt.xlabel("Average Permutation Importance")
plt.ylabel("Feature")
plt.title("Feature Importances")
plt.tight_layout()
plt.savefig(fname=f"{path}/Feature_Importances.png")
plt.close()

# Compute overall mean squared error
mean_squared_error_overall = mean_squared_error(
    y_true=list_of_true_LOSs, y_pred=list_of_predicted_expected_LOSs
)
print(f"Overall mean squared error: {mean_squared_error_overall}")

# Compute overall concordance index
concordance_index_overall = concordance_index_censored(
    event_indicator=np.array(list_of_event_indicators) == 1,
    event_time=np.array(list_of_true_LOSs),
    estimate=-np.array(list_of_predicted_expected_LOSs),
)
print(f"Overall concordance index: {concordance_index_overall[0]}")

# Plot Predicted Expected LOS Vs. Observed LOS
plt.scatter(
    x=list_of_true_LOSs, y=list_of_predicted_expected_LOSs, alpha=0.1
)
plt.plot(
    [min(list_of_true_LOSs), max(list_of_true_LOSs)],
    [min(list_of_true_LOSs), max(list_of_true_LOSs)],
    color="red",
    linestyle="--",
    label="Ideal",
)
plt.xlabel("Observed LOS")
plt.ylabel("Predicted Expected LOS")
plt.title("Predicted Expected LOS Vs. Observed LOS")
plt.legend()
plt.grid()
plt.savefig(fname=f"{path}/Predicted_Expected_LOS_Vs_Observed_LOS.png")
plt.clf()

# Generate and plot survival curves
minimum_LOS = min(step_function.x[0] for step_function in list_of_step_functions)
maximum_LOS = max(step_function.x[-1] for step_function in list_of_step_functions)
ndarray_of_linearly_spaced_LOSs = np.linspace(
    start=minimum_LOS, stop=maximum_LOS, num=100
)

list_of_ndarrays_of_survival_curve_values = []
for step_function in list_of_step_functions:
    ndarray_of_interpolated_survival_curve_values = np.interp(
        x=ndarray_of_linearly_spaced_LOSs, xp=step_function.x, fp=step_function.y
    )
    list_of_ndarrays_of_survival_curve_values.append(
        ndarray_of_interpolated_survival_curve_values
    )
    plt.step(
        x=ndarray_of_linearly_spaced_LOSs,
        y=ndarray_of_interpolated_survival_curve_values,
        where="post",
        alpha=0.2,
    )
ndarray_of_ndarrays_of_survival_curve_values = np.array(
    list_of_ndarrays_of_survival_curve_values
)
ndarray_array_of_average_survival_curve_values = np.mean(
    ndarray_of_ndarrays_of_survival_curve_values, axis=0
)
plt.step(
    x=ndarray_of_linearly_spaced_LOSs,
    y=ndarray_array_of_average_survival_curve_values,
    where="post",
    linewidth=2,
    color="blue",
    label="Average",
)
plt.xlabel("Length Of Stay (days)")
plt.ylabel("Survival Curve")
plt.title("Survival Curves")
plt.legend()
plt.grid()
plt.savefig(fname=f"{path}/Survival_Curves.png")
plt.clf()

# Generate and plot CDF of LOS
list_of_ndarrays_of_CDF_values = []
for step_function in list_of_step_functions:
    ndarray_of_CDF_values = 1 - step_function.y
    ndarray_of_interpolated_CDF_values = np.interp(
        x=ndarray_of_linearly_spaced_LOSs,
        xp=step_function.x,
        fp=ndarray_of_CDF_values,
    )
    list_of_ndarrays_of_CDF_values.append(ndarray_of_interpolated_CDF_values)
    plt.step(
        x=ndarray_of_linearly_spaced_LOSs,
        y=ndarray_of_interpolated_CDF_values,
        where="post",
        alpha=0.2,
    )
ndarray_of_ndarrays_of_CDF_values = np.array(list_of_ndarrays_of_CDF_values)
ndarray_of_average_CDF_values = np.mean(ndarray_of_ndarrays_of_CDF_values, axis=0)
plt.step(
    x=ndarray_of_linearly_spaced_LOSs,
    y=ndarray_of_average_CDF_values,
    where="post",
    linewidth=2,
    color="blue",
    label="Average",
)
plt.xlabel("Length Of Stay (days)")
plt.ylabel("Cumulative Distribution Function")
plt.title("CDF of LOS Vs. LOS")
plt.legend()
plt.grid()
plt.savefig(fname=f"{path}/CDF_Of_LOS_Vs_LOS.png")
plt.clf()

# Generate and plot PDF of LOS
list_of_ndarrays_of_PDF_values = []
list_of_predicted_expected_LOSs_via_PDF = []
for step_function in list_of_step_functions:
    ndarray_of_CDF_values = 1 - step_function.y
    ndarray_of_interpolated_CDF_values = np.interp(
        x=ndarray_of_linearly_spaced_LOSs,
        xp=step_function.x,
        fp=ndarray_of_CDF_values,
    )
    ndarray_of_PDF_values = np.gradient(
        ndarray_of_interpolated_CDF_values, ndarray_of_linearly_spaced_LOSs
    )
    list_of_ndarrays_of_PDF_values.append(ndarray_of_PDF_values)
    plt.plot(
        ndarray_of_linearly_spaced_LOSs,
        ndarray_of_PDF_values,
        alpha=0.2,
    )
    # Compute predicted expected LOS via PDF
    predicted_expected_LOS = np.trapz(
        ndarray_of_linearly_spaced_LOSs * ndarray_of_PDF_values,
        ndarray_of_linearly_spaced_LOSs,
    )
    list_of_predicted_expected_LOSs_via_PDF.append(predicted_expected_LOS)
ndarray_of_ndarrays_of_PDF_values = np.array(list_of_ndarrays_of_PDF_values)
ndarray_of_average_PDF_values = np.mean(ndarray_of_ndarrays_of_PDF_values, axis=0)
plt.plot(
    ndarray_of_linearly_spaced_LOSs,
    ndarray_of_average_PDF_values,
    linewidth=2,
    color="blue",
    label="Average",
)
plt.xlabel("Length Of Stay (days)")
plt.ylabel("Probability Density Function")
plt.title("PDF of LOS Vs. LOS")
plt.legend()
plt.grid()
plt.savefig(fname=f"{path}/PDF_Of_LOS_Vs_LOS.png")
plt.clf()

# Create DataFrame of results
data_frame_of_ids_and_actual_and_predicted_expected_LOSs = pd.DataFrame(
    data={
        "subject_id": list_of_subject_ids,
        "hadm_id": list_of_hadm_ids,
        "stay_id": list_of_stay_ids,
        "actual_los": list_of_true_LOSs,
        "predicted_expected_los": list_of_predicted_expected_LOSs,
        "predicted_expected_los_according_to_PDF": list_of_predicted_expected_LOSs_via_PDF,
    }
)

data_frame_of_ids_and_actual_and_predicted_expected_LOSs.to_csv(
    path_or_buf="data_frame_of_ids_and_actual_and_predicted_expected_LOSs.csv",
    index=False,
)

# Add code to plot Gains Curve
# Compute threshold based on z-score
mean_los = data_frame_of_ids_and_actual_and_predicted_expected_LOSs["actual_los"].mean()
std_los = data_frame_of_ids_and_actual_and_predicted_expected_LOSs["actual_los"].std()
z_score = -0.64  # Adjust as needed
threshold = mean_los + z_score * std_los

# Add indicator column
data_frame_of_ids_and_actual_and_predicted_expected_LOSs[
    "indicator_below_threshold"
] = (
    data_frame_of_ids_and_actual_and_predicted_expected_LOSs["actual_los"] < threshold
).astype(int)

# Perfect model
df_perfect = data_frame_of_ids_and_actual_and_predicted_expected_LOSs[
    ["actual_los", "indicator_below_threshold"]
].copy()
df_perfect = df_perfect.sort_values(by="actual_los")
df_perfect.reset_index(drop=True, inplace=True)
df_perfect["cumulative_positive_indicators"] = df_perfect[
    "indicator_below_threshold"
].cumsum()
df_perfect["cumulative_relative_frequency"] = (
    df_perfect["cumulative_positive_indicators"]
    / df_perfect["indicator_below_threshold"].sum()
)

# Trained model
df_trained = data_frame_of_ids_and_actual_and_predicted_expected_LOSs[
    ["predicted_expected_los", "indicator_below_threshold"]
].copy()
df_trained = df_trained.sort_values(by="predicted_expected_los")
df_trained.reset_index(drop=True, inplace=True)
df_trained["cumulative_positive_indicators"] = df_trained[
    "indicator_below_threshold"
].cumsum()
df_trained["cumulative_relative_frequency"] = (
    df_trained["cumulative_positive_indicators"]
    / df_trained["indicator_below_threshold"].sum()
)

# Plot Gains Curve
plt.plot(
    df_perfect.index,
    df_perfect["cumulative_relative_frequency"],
    label=f"Perfect Model; z score = {z_score}",
    color="blue",
)
plt.plot(
    df_trained.index,
    df_trained["cumulative_relative_frequency"],
    label=f"Trained Model; z score = {z_score}",
    color="green",
)
plt.grid()
plt.legend()
number_of_observations = len(
    data_frame_of_ids_and_actual_and_predicted_expected_LOSs
)
plt.title(f"Gains Curve")
plt.xlabel("Index")
plt.ylabel("Cumulative Relative Frequency")
plt.savefig(fname=f"{path}/Gains_Curves.png")
plt.clf()

plt.hist(
    x=data_frame["los"],
    bins=30,
    edgecolor="black",
    alpha=0.7,
)
plt.xlabel("Length Of Stay (days)")
plt.ylabel("Frequency")
plt.title("Histogram Of Frequency Of LOS Vs. LOS")
plt.grid()
plt.savefig(fname=f"{path}/Histogram_Of_Frequency_Of_LOS_Vs_LOS.png")
plt.clf()