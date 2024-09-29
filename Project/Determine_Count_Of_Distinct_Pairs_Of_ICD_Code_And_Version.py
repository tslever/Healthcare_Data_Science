from determine_count import determine_count

query = '''
SELECT COUNT(*)
FROM (
    SELECT DISTINCT icd_code, icd_version
    FROM diagnoses_icd
);
'''

count = determine_count(query = query)

print(f"Count of distinct pairs of ICD codes and ICD versions: {count}") # 28,583
