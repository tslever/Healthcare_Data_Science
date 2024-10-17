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
from pycox.models import LogisticHazard
from pycox.models import PMF
from pycox.models import DeepHitSingle
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

# Transform labels individually as required by survival method LogisticHazard, PMF, or DeepHitSingle.
# num_durations defines the size of the equidistant discretization grid for the LogisticHazard method.
# A nueral network with have num_durations output nodes / classes.
num_durations = 10
labtrans: pycox.preprocessing.label_transforms.LabTransDiscreteTime = LogisticHazard.label_transform(num_durations)
#labtrans: pycox.preprocessing.label_transforms.LabTransDiscreteTime = PMF.label_transform(num_durations)
#labtrans: pycox.preprocessing.label_transforms.LabTransDiscreteTime = DeepHitSingle.label_transform(num_durations)
get_target = lambda df: (df["duration"].values, df["event"].values)
y_train = labtrans.fit_transform(*get_target(df_train))
y_val = labtrans.transform(*get_target(df_val))
train = (x_train, y_train)
val = (x_val, y_val)
# We don't need to transform test labels.
durations_test, events_test = get_target(df_test)
print(type(labtrans))
# labtrans.cuts contains the discretization grid,
# which will be used to obtain a time scale for survival predictions.
print(labtrans.cuts)
# y_train is a tuple with indices of discretized times and event indicators.
print(y_train)
print(labtrans.cuts[y_train[0]])

# Make a neural network with torchtuples.
# Use simple neural network MLPVanilla provided by torchtuples.
# Make a MLP with two hidden layers with 32 nodes each, ReLU activations, batch normalization, dropout, and
# a number of output nodes equal to `out_features`.
in_features = x_train.shape[1]
num_nodes = [32, 32]
out_features = labtrans.out_features
batch_norm = True
dropout = 0.1
net = tt.practical.MLPVanilla(in_features, num_nodes, out_features, batch_norm, dropout)

# Alternatively, make a neural network with PyTorch.
# The following neural network and the previous neural network are essential equivalent.
# The following neural network does not use Kaiming normal weight initialization.
net = torch.nn.Sequential(
    torch.nn.Linear(in_features, 32),
    torch.nn.ReLU(),
    torch.nn.BatchNorm1d(32),
    torch.nn.Dropout(0.1),

    torch.nn.Linear(32, 32),
    torch.nn.ReLU(),
    torch.nn.BatchNorm1d(32),
    torch.nn.Dropout(0.1),

    torch.nn.Linear(32, out_features)
)

# Use the AdaM optimizer with learning rate 0.01. 
# Set attribute `duration_index`, which connects the output nodes of the neural network
# to discretization times and is useful for prediction.
model = LogisticHazard(net, tt.optim.Adam(0.01), duration_index = labtrans.cuts)
#model = PMF(net, tt.optim.Adam(0.01), duration_index = labtrans.cuts)
#model = DeepHitSingle(net, tt.optim.Adam(0.01), duration_index = labtrans.cuts)

# Set batch size and number of training epochs.
batch_size = 256
epochs = 100
callbacks = [tt.cb.EarlyStopping()]

# Train the neural network.
# The early stopping callback loads the best performing model in terms of validation loss.
log = model.fit(x_train, y_train, batch_size, epochs, callbacks, val_data = val)
_ = log.plot()
plt.show()
print(log.to_pandas().val_loss.min())
print(model.score_in_batches(val))

# Obtain a data frame of survival estimates for the test set.
surv = model.predict_surv_df(x_test)

# Plot the survival estimates for the first 5 individuals.
surv.iloc[:, :5].plot(drawstyle = "steps-post")
plt.ylabel("S(t | x)")
_ = plt.xlabel("Time")
plt.show()

# Perform linear / constant density interpolation survival estimates,
# replacing each grid point with 10 points.
surv = model.interpolate(10).predict_surv_df(x_test)
surv.iloc[:, :5].plot(drawstyle = "steps-post")
plt.ylabel("S(t | x)")
_ =  plt.xlabel("Time")
plt.show()

# State that we want to use Kaplan-Meier for estimating the censoring distribution.
ev = EvalSurv(surv, durations_test, events_test, censor_surv = "km")

# Display event time concordance.
print(ev.concordance_td("antolini"))

# Plot IPCW Brier score for a given set of times.
# Use 100 times between the min and max duration in the test set.
time_grid = np.linspace(durations_test.min(), durations_test.max(), 100)
ev.brier_score(time_grid).plot()
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