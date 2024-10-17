# Train the Cox-CC method.
# The Cox-CC method is a continuous time method.
# Use the METABRIC data set.


import numpy as np
import matplotlib.pyplot as plt

# Run `pip install sklearn-pandas`.
# Use sklearn and sklearn_pandas for preprocessing data.
from sklearn.preprocessing import StandardScaler
from sklearn_pandas import DataFrameMapper

# pycox is built on top of PyTorch and torchtuples.
# Module torch allows building neural networks.
# Module torchtuples allows training neural networks with relatively little boilerplate code.
import torch
import torchtuples as tt

# METABRIC is a dataset.
from pycox.datasets import metabric
# The LogisticHazard method is also known as Nnet-survival.
# The LogisticHazard method is a discrete time method that requires
# discretization of event times to be applied to continuous time data.
# See https://arxiv.org/pdf/1910.06724 .
from pycox.models import CoxCC
# Module EvalSurv simplifies evaluation.
from pycox.evaluation import EvalSurv

import pycox

# Set seeds to make results as reproducible as possible, considering randomness re a GPU.
np.random.seed(1234)
_ = torch.manual_seed(123)

# Load the METABRIC dataset as a pandas data frame and split the data into train, validation, and test sets.
df_train = metabric.read_df()
df_test = df_train.sample(frac = 0.2)
df_train = df_train.drop(df_test.index)
df_val = df_train.sample(frac = 0.2)
df_train = df_train.drop(df_val.index)
print("df_train.head():")
print(df_train.head())

# Example output:
#          x0        x1         x2        x3   x4   x5   x6   x7         x8    duration  event
# 0  5.603834  7.811392  10.797988  5.967607  1.0  1.0  0.0  1.0  56.840000   99.333336      0
# 1  5.284882  9.581043  10.204620  5.664970  1.0  0.0  0.0  1.0  85.940002   95.733330      1
# 3  6.654017  5.341846   8.646379  5.655888  0.0  0.0  0.0  0.0  66.910004  239.300003      0
# 4  5.456747  5.339741  10.555724  6.008429  1.0  0.0  0.0  1.0  67.849998   56.933334      1
# 5  5.425826  6.331182  10.455145  5.749053  1.0  1.0  0.0  1.0  70.519997  123.533333      0

# The METABRIC dataset has 9 covariates x0, ..., x8.
# Column duration contains observed times.
# Column event contains indicators of whether the observation is an event (1) or a censored observation (0).

# Standardize the 5 numerical covariates x0, x1, x2, x3, and x8.
# Leave the binary covariates x4, x5, x6, and x7 as is.
# Use DataFrameMapper to make feature mappers.
cols_standardize = ["x0", "x1", "x2", "x3", "x8"]
cols_leave = ["x4", "x5", "x6", "x7"]
standardize = [([col], StandardScaler()) for col in cols_standardize]
leave = [(col, None) for col in cols_leave]
x_mapper = DataFrameMapper(standardize + leave)
x_train = x_mapper.fit_transform(df_train)
x_val = x_mapper.transform(df_val)
x_test = x_mapper.transform(df_test)

# Convert type of values in matrices of features to `float32` as required by PyTorch.
x_train = x_train.astype("float32")
x_val = x_val.astype("float32")
x_test = x_test.astype("float32")

get_target = lambda df: (df["duration"].values, df["event"].values)
y_train = get_target(df_train)
y_val = get_target(df_val)
durations_test, events_test = get_target(df_test)
val = tt.tuplefy(x_val, y_val) # val is of type TupleTree.
print("val.shapes():")
print(val.shapes())

# The validation loss of CoxCC is not deterministic.
# Practice repeating the validation dataset multiple times
# before repeating the validation dataset to reduce the variance of the validation loss.
print("val.repeat(2).cat().shapes():")
print(val.repeat(2).cat().shapes())

# Make a simple neural network of type MLPVanilla with torchtuples.
# Make a MLP with two hidden layers with 32 nodes each, ReLU activations, batch normalization, dropout, and
# one output node.
in_features = x_train.shape[1]
num_nodes = [32, 32]
out_features = 1
batch_norm = True
dropout = 0.1
output_bias = False
net = tt.practical.MLPVanilla(
    in_features,
    num_nodes,
    out_features,
    batch_norm,
    dropout,
    output_bias = output_bias
)

# Use the AdaM (Adaptive Moment Estimation) optimizer.
model = CoxCC(net, tt.optim.Adam)

# Set batch size.
batch_size = 256

# Use model.lr_finder to find a suitable learning rate.
lrfinder = model.lr_finder(x_train, y_train, batch_size, tolerance = 2)
_ = lrfinder.plot()
plt.show()
print("lrfinder.get_best_lr():")
print(lrfinder.get_best_lr())

# Choose a more suitable learning rate.
model.optimizer.set_lr(0.01)

# Set number of epochs.
epochs = 512

# Use early stopping to stop training when the validation loss stops improving.
# Allow loading the best performing model in terms of validation loss.
callbacks = [tt.cb.EarlyStopping()]

verbose = True

# Train the neural network.
log = model.fit(x_train, y_train, batch_size, epochs, callbacks, verbose, val_data = val.repeat(10).cat())
_ = log.plot()
plt.show()
print("model.partial_log_likelihood(*val).mean():")
print(model.partial_log_likelihood(*val).mean())

# Get non-parametric baseline hazard estimates.
_ = model.compute_baseline_hazards()

# Obtain a data frame of survival estimates for the test set.
surv = model.predict_surv_df(x_test)

# Plot the survival estimates for the first 5 individuals.
surv.iloc[:, :5].plot()
plt.ylabel("S(t | x)")
_ = plt.xlabel("Time")
plt.show()

# Allow evaluating concordance, brier score, and negative binomial log likelihood on the test set.
# Allow estimating censoring distribution using a Kaplan-Meier estimator.
ev = EvalSurv(surv, durations_test, events_test, censor_surv = "km")

# Display event time concordance.
print("ev.concordance_td():")
print(ev.concordance_td())

# Plot IPCW Brier score for a given set of times.
# Use 100 times between the min and max duration in the test set.
time_grid = np.linspace(durations_test.min(), durations_test.max(), 100)
_ = ev.brier_score(time_grid).plot()
plt.ylabel("Brier score")
_ = plt.xlabel("Time")
plt.show()

# Plot IPCW negative binomial log likelihood.
ev.nbll(time_grid).plot()
plt.ylabel("NBLL")
_ = plt.xlabel("Time")
plt.show()

# Integrate IPCW Brier score.
# module "scipy.integrate" has no attribute "simps".
#print(ev.integrated_brier_score(time_grid))

# Integrate IPCW negative binomial log likelihood.
#print(ev.integrated_nbll(time_grid))