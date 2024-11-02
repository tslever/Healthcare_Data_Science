import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sksurv.ensemble import RandomSurvivalForest
from sksurv.util import Surv
import matplotlib.pyplot as plt


df = pd.read_csv(
    filepath_or_buffer = "table_of_subject_ids_hadm_ids_stay_ids_LOSs_vital_statistics_disease_indicators_and_demographics.csv",
    dtype = {
        "subject_id": int,
        "hadm_id": int,
        "stay_id": int,
        "los": float,
        "gender": int,
        "anchor_age": int,
        "race": int
    }
)

# Set the random state for reproducibility
LOS_train_df = df.sample(frac = 0.8, random_state = 0)
LOS_test_df = df.drop(LOS_train_df.index)

# Exclude ID and response columns
exclude_cols = ['subject_id', 'hadm_id', 'stay_id', 'los']
columns = LOS_train_df.columns.tolist()
predictor_names = [col for col in columns if col not in exclude_cols]

# Define numerical and categorical variables
numerical_vars = [col for col in predictor_names if
                  col.startswith('minimum_') or
                  col.startswith('first_quartile_') or
                  col.startswith('median_') or
                  col.startswith('third_quartile_') or
                  col.startswith('maximum_') or
                  col == 'anchor_age']

categorical_vars = ['gender', 'race'] + [col for col in predictor_names if col.startswith('APR_') or col.startswith('HCFA_')]

# Ensure all predictor names are included
assert set(numerical_vars + categorical_vars) == set(predictor_names), "Mismatch in predictor variables"

# Convert appropriate columns to numeric
LOS_train_df[numerical_vars] = LOS_train_df[numerical_vars].apply(pd.to_numeric, errors='coerce')
LOS_test_df[numerical_vars] = LOS_test_df[numerical_vars].apply(pd.to_numeric, errors='coerce')

# Convert categorical variables to 'category' dtype
LOS_train_df[categorical_vars] = LOS_train_df[categorical_vars].astype('category')
LOS_test_df[categorical_vars] = LOS_test_df[categorical_vars].astype('category')

# Prepare response and status
LOS_train_df['response'] = LOS_train_df['los'].astype(float)
LOS_test_df['response'] = LOS_test_df['los'].astype(float)

LOS_train_df['status'] = 1
LOS_test_df['status'] = 1

# Prepare target variable
y_train = Surv.from_arrays(event=LOS_train_df['status'] == 1, time=LOS_train_df['response'])
y_test = Surv.from_arrays(event=LOS_test_df['status'] == 1, time=LOS_test_df['response'])

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_vars),
        ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_vars)
    ])

# Pipeline with Random Survival Forest
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomSurvivalForest(n_estimators=100, min_samples_split=10, random_state=0))
])

# Fit the model
model.fit(LOS_train_df[predictor_names], y_train)

# Predict on test data
pred_surv = model.predict_survival_function(LOS_test_df[predictor_names])

# Define a common time grid
t_min = min(fn.x[0] for fn in pred_surv)
t_max = max(fn.x[-1] for fn in pred_surv)
t_grid = np.linspace(t_min, t_max, 100)

# Plot survival functions
plt.figure(figsize=(10, 6))
for fn in pred_surv:
    surv_y_interp = np.interp(t_grid, fn.x, fn.y)
    plt.step(t_grid, surv_y_interp, where="post", alpha=0.2)

plt.xlabel("Time (days)")
plt.ylabel("Probability of no discharge")
plt.title("Survival Curves for Test Data")
plt.show()

# Plot cumulative incidence functions (Probability of discharge)
plt.figure(figsize=(10, 6))
for fn in pred_surv:
    ci_y = 1 - fn.y  # Compute 1 minus the survival probabilities
    ci_y_interp = np.interp(t_grid, fn.x, ci_y)
    plt.step(t_grid, ci_y_interp, where="post", alpha=0.2)

plt.xlabel("Time (days)")
plt.ylabel("Probability of discharge")
plt.title("Probability of Discharge vs Time (days)")
plt.show()

# Plot derivative of cumulative incidence functions
plt.figure(figsize=(10, 6))
for fn in pred_surv:
    ci_y = 1 - fn.y  # Compute cumulative incidence function
    ci_y_interp = np.interp(t_grid, fn.x, ci_y)
    derivative = np.gradient(ci_y_interp, t_grid)
    plt.plot(t_grid, derivative, alpha=0.2)

plt.xlabel("Time (days)")
plt.ylabel("Derivative of Probability of discharge")
plt.title("Derivative of Probability of Discharge vs Time (days)")
plt.show()