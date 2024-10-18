# Time-to-event modeling for hospital length of stay prediction for COVID-19 patients

Tom Lever

10/18/2024


## Introduction

This presentation is based on a paper called "Time-to-event modeling for hospital length of stay prediction for COVID-19 patients" [1].

Length Of Stay is "the cumulative duration of patient hospitalization" from first admission. Length Of Stay is "affected by many factors, including individual demographics, different treatment strategies, and discharge planning... various diseases".

"[The authors] propose to use time-to-event modeling techniques, also known as survival analysis, to predict the [Length Of Stay (LOS)] for patients based on individualized information collected from multiple sources... the primary goal... is to estimate the duration of hospital stay among patients... using clinical data." [The authors] develop a "time-to-event model... for individualized LOS prediction... [The authors] apply time-to-event model... Random Survival Forest."


## Existing LOS Models Vs. Survival Analysis

"The existing LOS models can be grouped into two general categories: classification models and regression models. Classification models are usually used to predict categorical outcomes. In other words, the aim is to group the LOS into multiple classes, e.g., short stay, medium stay, and long stay, based on the number of days that the patient stays in the hospital. However, several studies have demonstrated that the LOS distributions are highly skewed to the right... This skewness indicates that the dataset becomes heavily imbalanced as only a few long LOS cases exist. This imbalance misleads the performance evaluation as classes with long LOS are deemed outliers by the model. Therefore, viewing the LOS task as a regression problem is a more appropriate and informative way of balancing the dataset by predicting the actual number of LOS days in lieu of class labels."

"[A] main advantage of using time-to-event data analysis is that such models can give a probability estimate instead of solely point estimates as conventional regression models. Moreover, survival models have the capability of incorporating censored data into models."

"It is common in clinical studies to have subjects who did not experience the event of interest at the end of a study or dropped out before the event of interest occurs. These subjects are usually called... right-censored. Although the data may seem to be incomplete for these subjects as the time-to-event is not actually observed, these subjects are highly valuable as the observation that they went a certain amount of time without experiencing an event is information... Time-to-event modeling techniques, also referred to as survival analysis, have the capability to handle censored data that normally are disregarded by regular regression models... [A] main benefit of time-to-event modeling is that the data related to participants who did not experience the event by the end of the study or were unavailable for follow up (referred to as [censored] data...) can still contribute to the analysis... [I]n conventional regression models, censored data are typically discarded, which may introduce a bias into the model."


# Survival Analysis

"Survival analysis is a branch of statistics concerned with analyzing time-to-event data and predicting the probability of occurrence of an event." The event in our case is either "discharge due to recovery or [discharge] due to death... To estimate the LOS of a patient by using survival analysis tools, the objective is to model the LOS Probability Density Function as a function of [duration]." Duration in our case is the "cumulative time spent in the hospital in the... 30 days" after first admission. The LOS Probability Density Function is the distribution of likely durations for a patient. Let the LOS Probability Density Function of a random variable big $T$ be denoted by function $p$ of little $t$. Big $T$ represents a random duration. Let the LOS Cumulative Distribution Function of the random variable big $T$ be denoted by function $c$ of little $t$. The Cumulative Density Function "describes the probability of [a random duration big] $T$ [being at most] [little] $t$." Let the Survival Function be denoted by $S$ of little $t$. The survival function describes the probability of a random duration big $T$ exceeding little $t$. The Survival Function is the complement of the Cumulative Distribution Function. $c(t) = 1 - S(t)$. We can use a Random Survival Forest to estimate the Survival Function. We can calculate the Cumulative Distribution Function given that the Cumulative Distribution Function is the complement of the Survival Function. The LOS Probability Density Function is the derivative of the Cumulative Distribution Function.


# Dataset

We consider a dataset based on GitHub repository `COVID.LOS.prep` [2] of information relating to patients. Columns SEX and ETHNICITY contains strings. Column AGE and BMI1 through BMI5 contains floats. Columns BP_DIASTOLIC1 through BP_DIASTOLIC5, BP_SYSTOLIC1 through BP_SYSTOLIC5, PULSE1 through PULSE5, PULSE.OXIMETRY1 through PULSE.OXIMETRY5, and RESPIRATIONS1 through RESPIRATIONS5 contain integers. Column TEMPERATURE1 through TEMPERATURE5 contain floats. Columns corresponding to the 20 most common diagnoses contain booleans. Column duration contains floats. Column patient_was_discharged contains 1s.


# Calculating LOS Probability Density Function

GitHub repository `COVID.LOS.prep` provides R file `stat.analysis.R` that plots the Survival Function for each patient as "Probability of no discharge vs. time (days)". "time (days)" is Length Of Stay. I converted this R file to a Python file. I plotted not only the Survival Functions but also the Cumulative Distribution Functions and the Probability Density Distribution Functions. We can predict Length Of Stay as the expected value of the Probability Density Distribution while having a sense of all likely values.

This concludes this short video.


## References

I would like to acknowledge the authors and ChatGPT.

1. Wen et al. (2022). "Time-to-event modeling for hospital length of stay prediction for COVID-19 patients". Machine Learning with Applications. Volume 9. Jun 18, 2022. Accessed on 10/17/2024 via https://pmc.ncbi.nlm.nih.gov/articles/PMC9213016/pdf/main.pdf .

2. Michael Pokojovy (2022). "COVID.LOS.prep". Accessed on 10/18/2024 via https://github.com/tslever/COVID.LOS.prep .

3. OpenAI (2024). "ChatGPT". Accessed on 10/18/2024 via https://chatgpt.com/ .