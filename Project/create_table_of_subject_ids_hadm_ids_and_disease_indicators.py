import pandas as pd


subtable_of_table_drgcodes = pd.read_csv('subtable_of_table_drgcodes.csv')
subtable_of_table_drgcodes['combination_of_DRG_type_and_code'] = \
    subtable_of_table_drgcodes['drg_type'].astype(str) + '_' + \
    subtable_of_table_drgcodes['drg_code'].astype(str)
series_of_combinations_and_counts = \
    subtable_of_table_drgcodes['combination_of_DRG_type_and_code'].value_counts()
series_of_20_most_common_combinations_and_counts = \
    series_of_combinations_and_counts.nlargest(n = 20)
index_of_series_of_20_most_common_combinations_and_counts = \
    series_of_20_most_common_combinations_and_counts.index
list_of_20_most_common_combinations_and_counts = \
    index_of_series_of_20_most_common_combinations_and_counts.to_list()
cross_tabulation = pd.crosstab(
    index = [subtable_of_table_drgcodes['subject_id'], subtable_of_table_drgcodes['hadm_id']], 
    columns = subtable_of_table_drgcodes['combination_of_DRG_type_and_code']
)
table_of_subject_ids_hadm_ids_and_disease_frequencies = cross_tabulation.reset_index()
table_of_subject_ids_hadm_ids_and_disease_indicators = \
    table_of_subject_ids_hadm_ids_and_disease_frequencies[["subject_id", "hadm_id"]].copy()
for combination in list_of_20_most_common_combinations_and_counts:
    table_of_subject_ids_hadm_ids_and_disease_indicators[combination] = \
        (table_of_subject_ids_hadm_ids_and_disease_frequencies.get(combination, 0) > 0).astype(int)
table_of_subject_ids_hadm_ids_and_disease_indicators.to_csv(
    path_or_buf = "table_of_subject_ids_hadm_ids_and_disease_indicators.csv",
    index = False
)