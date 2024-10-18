import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sksurv.ensemble import RandomSurvivalForest
from sksurv.util import Surv
import matplotlib.pyplot as plt

# Read the data
LOS_train_df = pd.read_csv('LOS.train.imp.rf.df.csv', header=0, sep=',', dtype=str)
LOS_test_df = pd.read_csv('LOS.test.imp.rf.df.csv', header=0, sep=',', dtype=str)

# Vitals
vital_names = ["BMI", "BP_DIASTOLIC", "BP_SYSTOLIC", "PULSE", "PULSE.OXIMETRY", "RESPIRATIONS", "TEMPERATURE"]
vital_names_x5 = [f"{vital_name}{ind}" for vital_name in vital_names for ind in range(1, 6)]

# Convert appropriate columns to numeric
numeric_cols = ['AGE', 'LOS_30D'] + vital_names_x5
for col in numeric_cols:
    if col in LOS_train_df.columns:
        LOS_train_df[col] = pd.to_numeric(LOS_train_df[col], errors='coerce')
    if col in LOS_test_df.columns:
        LOS_test_df[col] = pd.to_numeric(LOS_test_df[col], errors='coerce')

# Get ICD10 names
columns = LOS_train_df.columns.tolist()
vital_indices = [columns.index(name) for name in vital_names_x5 if name in columns]
max_vital_index = max(vital_indices) if vital_indices else -1
ICD10_names = columns[max_vital_index+1:]

# Convert 'TRUE'/'FALSE' strings to integers 1/0 in ICD10 columns
LOS_train_df[ICD10_names] = LOS_train_df[ICD10_names].replace({'TRUE': 1, 'FALSE': 0}).astype(int)
LOS_test_df[ICD10_names] = LOS_test_df[ICD10_names].replace({'TRUE': 1, 'FALSE': 0}).astype(int)

# Compute frequencies
freqs = LOS_train_df[ICD10_names].sum()
ICD10_top20_names = freqs.sort_values(ascending=False).head(20).index.tolist()

# Convert ICD10 codes to categorical
for ICD10_name in ICD10_top20_names:
    LOS_train_df[ICD10_name] = LOS_train_df[ICD10_name].astype('category')
    LOS_test_df[ICD10_name] = LOS_test_df[ICD10_name].astype('category')

# All predictors
predictor_names = ["SEX", "ETHNICITY", "AGE"] + vital_names_x5 + ICD10_top20_names

# Convert SEX and ETHNICITY to categorical
LOS_train_df["SEX"] = LOS_train_df["SEX"].astype('category')
LOS_test_df["SEX"] = LOS_test_df["SEX"].astype('category')
LOS_train_df["ETHNICITY"] = LOS_train_df["ETHNICITY"].astype('category')
LOS_test_df["ETHNICITY"] = LOS_test_df["ETHNICITY"].astype('category')

# Prepare response and status
LOS_train_df['response'] = LOS_train_df['LOS_30D'].astype(float)
LOS_test_df['response'] = LOS_test_df['LOS_30D'].astype(float)

LOS_train_df['status'] = 1
LOS_test_df['status'] = 1

# Prepare target variable
y_train = Surv.from_arrays(event=LOS_train_df['status'] == 1, time=LOS_train_df['response'])
y_test = Surv.from_arrays(event=LOS_test_df['status'] == 1, time=LOS_test_df['response'])

# Separate categorical and numerical variables
categorical_vars = ["SEX", "ETHNICITY"] + ICD10_top20_names
numerical_vars = [var for var in predictor_names if var not in categorical_vars]

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

# Plot survival functions
plt.figure(figsize=(10, 6))
for fn in pred_surv:
    plt.step(fn.x, fn.y, where="post", alpha=0.2)

plt.xlabel("Time (days)")
plt.ylabel("Probability of no discharge (%)")
plt.title("Survival Curves for Test Data")
plt.show()