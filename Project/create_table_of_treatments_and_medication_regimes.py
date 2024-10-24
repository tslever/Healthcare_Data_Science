import pandas as pd

data_frame = pd.read_csv("Table_Of_IDs_Of_Hospitalizations_Indicators_Of_Death_DRG_Info_And_Medication_Regimes.csv")

def aggregate_data(group):
    treatments = ', '.join(f"{row['drg_type']} {row['drg_code']}" for _, row in group.iterrows())
    treatment_string = f"treatment for {treatments}"
    meds_lists = group["medications"].apply(lambda x: [med.strip() for med in x.split(',')] if isinstance(x, str) else [])
    all_meds = [med for meds_list in meds_lists for med in meds_list]
    meds = sorted(set(all_meds))
    meds_string = ', '.join(meds)
    return pd.Series({
        "treatment": treatment_string,
        "medications": meds_string
    })

table_of_treatments_and_medication_regimes = data_frame.groupby("hadm_id").apply(aggregate_data).reset_index()[["treatment", "medications"]]
table_of_treatments_and_medication_regimes.to_csv(
    path_or_buf = "Table_Of_Treatments_And_Medication_Regimes.csv",
    index = False
)