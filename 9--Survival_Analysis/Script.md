# Time-to-event modeling for hospital length of stay prediction for COVID-19 patients

Tom Lever

10/18/2024


## Introduction

This presentation is based on a paper called "Time-to-event modeling for hospital length of stay prediction for COVID-19 patients" [1].

Length Of Stay is "the cumulative duration of patient hospitalization" from first admission in a time period of interest. Length Of Stay is "affected by many factors, including individual demographics, different treatment strategies,... discharge planning [and] various diseases".

In their paper, "[The authors] propose to use time-to-event modeling techniques, also known as survival analysis, to predict the [Length Of Stay (LOS)] for patients based on individualized information collected from multiple sources... the primary goal... is to estimate the duration of hospital stay among patients... using clinical data." [The authors] develop a "time-to-event model... for individualized LOS prediction... [The authors] apply time-to-event model... Random Survival Forest."


# Dataset

We consider a dataset based on GitHub repository `COVID.LOS.prep` [2] of information relating to patients. There are 60 columns and 644 rows other than the header. 3 columns contain demographic values. Columns SEX and ETHNICITY contains strings. Column AGE contains floats. 7 groups of 5 columns contain values relating to vitals. Columns relating to BMI contain floats. Columns relating to blood pressure, pulse, oxygen saturation, and respirations contain integers. Columns relating to temperature contain floats. Columns corresponding to the 20 most common diagnoses among patients contain booleans. Column duration contains floats. Column patient_was_discharged contains 1s. The authors in their survival analysis assume that all patients are discharged.


# Exploratory Data Analysis

Here is some Exploratory Data Analysis: a histogram of frequency of Length Of Stay vs. Length Of Stay. You might notice that the distribution of Lengths Of Stay is exponentially decreasing and skewed to the right.


## Classification, Regression, and Survival Analysis

"The existing LOS models can be grouped into two general categories: classification models and regression models. Classification models are usually used to predict categorical outcomes. In other words, the aim is to group the LOS into multiple classes, e.g., short stay, medium stay, and long stay, based on the number of days that the patient stays in the hospital. However, several studies have demonstrated that the LOS distributions are highly skewed to the right... This skewness indicates that the dataset becomes heavily imbalanced as only a few long LOS cases exist. This imbalance misleads the performance evaluation as classes with long LOS are deemed outliers by the model. Therefore, viewing the LOS task as a regression problem is a more appropriate and informative way of balancing the dataset by predicting the actual number of LOS days in lieu of class labels."

"[A] main advantage of using time-to-event data analysis is that such models can give a probability estimate instead of solely point estimates as conventional regression models." Survival Analysis is Bayesian Machine Learning.


# Survival Analysis

"Survival analysis is a branch of statistics concerned with analyzing time-to-event data and predicting the probability of occurrence of an event... To estimate the LOS of a patient by using survival analysis tools, the objective is to model the LOS Probability Density Function of a patient as a function of [Length Of Stay]." Length Of Stay in our case is the "cumulative time spent in the hospital" by a patient after first admission in a time period of interest. The LOS Probability Density Function is the distribution of likely Lengths Of Stay for a patient. Let the LOS Probability Density Function of a patient be denoted by function $PDF_P(LOS)$. Let the LOS Cumulative Distribution Function of a patient be denoted by function $CDF_P(LOS)$. The Cumulative Density Function of a patient "describes the probability of [a random Length Of Stay being at most] $LOS$" for that patient. Let the Survival Function of a patient be denoted by $S(LOS)$. The survival function of a patient describes the probability of a random Length Of Stay exceeding LOS for that patient. The Survival Function is the complement of the Cumulative Distribution Function. We can use a Random Survival Forest to estimate the set of Survival Functions for all patients on test data. We can calculate the Cumulative Distribution Function of a patient given that the Cumulative Distribution Function for that patient is the complement of the Survival Function for that patient. The LOS Probability Density Function for a patient is the derivative of the Cumulative Distribution Function for that patient.


# Calculating Set Of Probability Density Functions For All Patients

Based on GitHub repository `COVID.LOS.prep`, I created a Python module to conduct the above survival analysis. The Python module plots "Survival Functions Of All Patients For Test Data Vs. LOS". The Python module plots "Cumulative Distribution Functions Of All Patients For Test Data Vs. LOS". The Python module plots "Probability Density Distribution Functions Of All Patients For Test Data Vs. LOS". These PDFs approximate the histogram of frequency of LOS Vs. LOS for training data. We can predict Length Of Stay as the expected value of the Probability Density Distribution while having a sense of all likely values.


## References

This concludes this short video. I would like to acknowledge the authors and ChatGPT. Let me know if you have thoughts, questions, and/or feedback.

1. Wen et al. (2022). "Time-to-event modeling for hospital length of stay prediction for COVID-19 patients". Machine Learning with Applications. Volume 9. Jun 18, 2022. Accessed on 10/17/2024 via https://pmc.ncbi.nlm.nih.gov/articles/PMC9213016/pdf/main.pdf .

2. Michael Pokojovy (2022). "COVID.LOS.prep". Accessed on 10/18/2024 via https://github.com/tslever/COVID.LOS.prep .

3. OpenAI (2024). "ChatGPT". Accessed on 10/18/2024 via https://chatgpt.com/ .