from matplotlib import pyplot as plt
import pandas as pd

data_frame_of_observed_and_averaged_predicted_reponse_values = pd.read_csv('data_frame_of_ids_and_actual_and_predicted_expected_LOSs.csv')
plt.scatter(
    x = data_frame_of_observed_and_averaged_predicted_reponse_values['actual_los'],
    y = data_frame_of_observed_and_averaged_predicted_reponse_values['predicted_expected_los'],
    alpha = 0.1
)
plt.title('Predicted Expected LOS Vs. Observed LOS')
plt.xlabel('Observed LOS')
plt.ylabel('Predicted Expected LOS')
plt.grid()
plt.show()