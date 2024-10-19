# Survival Analysis For Hospital LOS Prediction For CoViD-19 Patients

Tom Lever

10/18/2024


Welcome to my presentation on survival analysis.


## Introduction

This presentation is based on a paper called "Time-to-event modeling for hospital length of stay prediction for COVID-19 patients" [1].


## Length Of Stay

Length Of Stay is "the cumulative duration of patient hospitalization" from first admission, in a time period of interest. Length Of Stay is "affected by many factors, including individual demographics, different treatment strategies,... discharge planning [and] various diseases".

In their paper, the authors use a Random Survival Forest to predict a set of survival functions for all patients for test data. A survival function for a patient relates to a PDF of Length Of Stay for that patient.


# Dataset

We consider a dataset of patient information based on GitHub repository `COVID.LOS.prep` [2] . There are 60 columns and 644 rows other than the header. 3 columns contain demographic values. 7 groups of 5 columns each contain values relating to vitals. 20 columns, corresponding to the 20 most common diagnoses among patients, contain indicators of whether patients have those diagnoses. 1 column contains Lengths Of Stay. 1 column contains 1's indicating that all patients were discharged.


# Exploratory Data Analysis

Here is some Exploratory Data Analysis: a histogram of frequency of Length Of Stay vs. Length Of Stay. You might notice that the distribution of Lengths Of Stay is very skewed to the right.


## Classification, Regression, and Survival Analysis

Common "LOS models... [are] classification and regression models. Classification models are usually used... to group [patients] into multiple classes... [like]... short stay, medium stay, and long stay... However... as only a few long LOS cases exist... [the data is imbalanced, which] misleads.. the model... [P]redicting the actual... [Length Of Stay using] regression... is... more appropriate".

"[A] main advantage of using [survival] analysis over regression is that such models can give a probability estimate instead of solely point estimates".


# Survival Analysis

"Survival analysis is... concerned with... predicting [a Probability Density Function]." We model a PDF of Length Of Stay for a patient. Length Of Stay in our case is the "cumulative time spent in the hospital" by a patient after first admission, in a time period of interest. The PDF is the distribution of likely Lengths Of Stay of a patient. Let the PDF for a patient be denoted by function $PDF_P(LOS)$. Let the CDF for a patient be denoted by function $CDF_P(LOS)$. The CDF for a patient "describes the probability of" a random Length Of Stay being at most LOS for that patient. Let the Survival Function of a patient be denoted by $S_P(LOS)$. The Survival Function for a patient describes the probability of a random Length Of Stay exceeding LOS for that patient. The Survival Function for a patient is the complement of the CDF for that patient. We can use a Random Survival Forest to estimate the set of Survival Functions for all patients on test data. We can calculate the CDF of a patient given that the CDF for that patient is the complement of the Survival Function for that patient. The PDF for a patient is the derivative of the CDF for that patient.


# Calculating Set Of Probability Density Functions For All Patients

Based on GitHub repository `COVID.LOS.prep`, I created a Python module to conduct the above survival analysis. The Python module plots "Survival Functions Of All Patients For Test Data Vs. LOS". The Python module also plots "CDFs Of All Patients For Test Data Vs. LOS". Finally, the Python module plots "PDFs Of All Patients For Test Data Vs. LOS". These PDFs resemble the histogram we saw earlier of frequency of LOS Vs. LOS for training data. We can predict the Length Of Stay of a patient as the expected value of the PDF for that patient while having a sense of all likely Lengths Of Stay for that patient.


## References

This concludes this short video. I would like to acknowledge the authors and ChatGPT. Let me know if you have thoughts, questions, and/or feedback.

1. Wen et al. (2022). "Time-to-event modeling for hospital length of stay prediction for COVID-19 patients". Machine Learning with Applications. Volume 9. Jun 18, 2022. Accessed on 10/17/2024 via https://pmc.ncbi.nlm.nih.gov/articles/PMC9213016/pdf/main.pdf .

2. Michael Pokojovy (2022). "COVID.LOS.prep". Accessed on 10/18/2024 via https://github.com/tslever/COVID.LOS.prep .

3. OpenAI (2024). "ChatGPT". Accessed on 10/18/2024 via https://chatgpt.com/ .