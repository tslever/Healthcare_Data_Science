import pandas as pd

# Import a class representing Random Forest binary classifier machine learning models.
from sklearn.ensemble import RandomForestClassifier

# Import functions and classes for model training and evaluation.
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# Read the data by loading the data set into pandas data frame df.
df = pd.read_csv('HeartFailureData.csv')

# Convert boolean columns to integers to ensure compatibility with machine learning algorithms.
bool_cols = df.select_dtypes(include=['bool']).columns
df[bool_cols] = df[bool_cols].astype(int)

# Split data into features and target.
X = df.drop(['Alive', 'pat_mrn_id'], axis=1)
y = df['Alive'].astype(int)

# Split data into training and test sets (e.g., 80/20 split).
# X_train, y_train represent 80 percent of the data used for training the model.
# X_test, y_test represent 20 percent of the data used for evaluating the model's performance.
# random_state ensures reproducibility of the split.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data by removing the mean and scaling each feature to unit variance.
scaler = StandardScaler()

# Fit the scaler on the training data,
# which involves removing the mean and scaling each feature to unit variance.
X_train_scaled = scaler.fit_transform(X_train)

# Transform the test data in addition to the training data.
X_test_scaled = scaler.transform(X_test)

# Create the base model
rf = RandomForestClassifier(random_state=42)

# Define the parameter grid for GridSearchCV
param_grid = {
    'n_estimators': [100, 200], # number of trees in forest
    'max_depth': [None, 5, 10], # maximum depth of each tree. None means there is no limit on the depth of a tree.
    'min_samples_split': [2, 5], # minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2], # minimum number of samples required to be at a leaf node
}

# Instantiate the grid search model
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5, # Evaluates each combination of hyperparameters using 5-fold cross-validation
    n_jobs=-1, # Utilizes all available CPU cores to speed up computation
    verbose=2, # Provides detailed logs of the fitting process
    scoring='accuracy' # Uses accuracy as the metric for evaluating model performance
)

# Fit the grid search to the data by training multiple models with different hyperparameter combinations
# to find the best performing model.
# Example output:

# Fitting 5 folds for each of 24 candidates, totalling 120 fits
# [CV] END max_depth=None, min_samples_leaf=1, min_samples_split=2, n_estimators=100; total time=   7.8s
# ...
# [CV] END max_depth=10, min_samples_leaf=2, min_samples_split=5, n_estimators=200; total time=   6.9s

# For this output, GridSearchCV tests 24 combinations of hyperparameters from the parameter grid
# using 5-fold cross validation, resulting in 120 fits.
grid_search.fit(X_train_scaled, y_train)


# Example output:

# Best parameters found: {'max_depth': None, 'min_samples_leaf': 2, 'min_samples_split': 5, 'n_estimators': 200}
print('Best parameters found:', grid_search.best_params_)

# Use the best estimator with the best hyperparameters.
best_rf = grid_search.best_estimator_

# Evaluate the best estimator using 5-fold cross-validation on the training data
# and computing accuracy for each fold.
cv_scores = cross_val_score(best_rf, X_train_scaled, y_train, cv=5, scoring='accuracy')

# Example output:

# Cross-validation scores with best estimator: [0.89852454 0.8976212  0.89811283 0.89761092 0.89821321]
# Mean cross-validation score: 0.8980165399369758

# The scores across folds are very similar, indicating stable performance.
# There is approximately 89.8 percent accuracy on the training data.
print('Cross-validation scores with best estimator:', cv_scores)
print('Mean cross-validation score:', cv_scores.mean())

# Use the best model to predict survival on the test data set.
y_pred = best_rf.predict(X_test_scaled)

# Evaluate the model
# Accuracy is the proportion of correct predictions on the test data.
# Classification report includes precision, recall, F1 score, and support.
# Precision is the ratio of true positives to the sum of true and false positives.
# Recall is the ratio of true positives to the sum of true positives and false negatives.
# F1 score is the harmonic mean of precision and recall.
# Support is the number of occurrences of each class in the test data.
# Example output:

# Accuracy on test data: 0.8897454428651731
# Classification report:
#               precision    recall  f1-score   support
# 
#            0       0.53      0.01      0.01      1374
#            1       0.89      1.00      0.94     11079
# 
#     accuracy                           0.89     12453
#    macro avg       0.71      0.50      0.48     12453
# weighted avg       0.85      0.89      0.84     12453

# The model achieves 89.0 percent accuracy on the test data set of unseen data.
# This accuracy is misleading.
# This accuracy is due to the model's ability to predict correctly that patients are alive after 1 year.
# This accuracy does not reflect the model's inability to predict correctly that patients are not alive.
# "0" represents rows / patients who are not alive after 1 year.
# "1" represents patients who are alive after 1 year.
# There are actually 1,374 (11 percent) patients who are not alive after 1 year.
# There are actually 11,079 (89 percent) patients who are alive after 1 year.
# The data set is highly imbalanced.
# The model is biased toward the majority status of being alive after 1 year.
# The model predicts nearly all patients as being alive after 1 year.
# 53 percent of patients predicted to be not alive are actually not alive.
# 89 percent of patients predicted to be alive are actually alive.
# 1 percent of patients actually not alive were predicted to be not alive.
# 100 percent of patients actually alive were predicted to be alive.
# An F1 score of 0.01 indicates that the model performed very poorly in identifying patients who are not alive.
# An F1 score of 0.94 indicates that the model performed very well in identifying patients who are alive.
# Accuracy on the test data set is repeated.
# 0.71 is the average of 0.53 and 0.89.
# 0.71 may also be the proportion of patients predicted to have a certain status that actually have that status.
# 0.50 is the average of 0.01 and 1.00.
# 0.50 may also be the proportion of patients actually having a status that were predicted to have that status.
# 0.48 is the average of 0.01 and 0.94.
# 0.85 is the average of 0.53 and 0.89 weighted by the number of patients with each status.
# 0.85 may also be the weighted proportion of patients
# predicted to have a certain status that actually have that status.
# 0.89 is the average of 0.01 and 1.00 weighted by the number of patients with each status.
# 0.89 may also be the weighted proportion of patients
# actually having a status that were predicted to have that status.
# 0.84 is the average of 0.01 and 0.94 weighted by the number of patients with each status.

# We might increase the number of patients in our data set who are actually not alive after 1 year.
# We might use SMOTE.
# We might decrease the number of patients in our data set who are actually alive after 1 year.
# We might adjust the model to penalize misclassifications of patients who are not alive more heavily
# than misclassifications of patients who are alive.
# We might add property "class_weight='balanced'" to the constructor of RandomForestClassifier.
# We might consider a Precision-Recall Curve or an ROC Curve and/or the areas under these curves.
# We might consider including classification threshold as a hyperparameter in param_grid.
# We might consider choosing only those features that contribute most to predictions.
# We might add features or transform features.
# We might use models that handle class imbalance better (e.g., Gradient Boosting Machines).
print('Accuracy on test data:', accuracy_score(y_test, y_pred))
print('Classification report:')
print(classification_report(y_test, y_pred))