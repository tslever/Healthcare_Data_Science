from matplotlib import pyplot as plt
import pandas as pd

data_frame_of_observed_and_averaged_predicted_reponse_values = pd.read_csv('actual_vs_predicted_los.csv')
plt.scatter(
    x = data_frame_of_observed_and_averaged_predicted_reponse_values['observed_response_value'],
    y = data_frame_of_observed_and_averaged_predicted_reponse_values['average_of_predicted_response_values'],
    alpha = 0.1
)
plt.title('Predicted Expected LOS Vs. Observed LOS')
plt.xlabel('Observed LOS')
plt.ylabel('Predicted Expected LOS')
plt.show()