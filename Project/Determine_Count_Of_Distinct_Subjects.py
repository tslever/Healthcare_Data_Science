from determine_count import determine_count

query = '''
SELECT COUNT(*)
FROM (
    SELECT DISTINCT subject_id
    FROM admissions
);
'''

count = determine_count(query = query)

print(f"Count of distinct subjects: {count}") # 223,452 (There are 546,028 rows in table admissions.)
