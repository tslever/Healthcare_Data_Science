import pandas as pd

df_hospitalizations = pd.read_csv("Table_Of_IDs_Of_Hospitalizations_Indicators_Of_Death_And_DRG_Info.csv")
df_medications = pd.read_csv("Table_Of_IDs_Of_Hospitalizations_And_Medication_Regimes.csv")
merged_df = pd.merge(df_hospitalizations, df_medications, on = "hadm_id", how = "inner")
merged_df.to_csv(
    "Table_Of_IDs_Of_Hospitalizations_Indicators_Of_Death_DRG_Info_And_Medication_Regimes.csv",
    index = False
)