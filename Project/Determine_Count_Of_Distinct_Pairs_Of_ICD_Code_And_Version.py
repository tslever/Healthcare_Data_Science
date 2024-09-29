import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

query = '''
SELECT COUNT(*)
FROM (
    SELECT DISTINCT icd_code, icd_version
    FROM diagnoses_icd
);
'''
cursor.execute(query)
result = cursor.fetchone()
print(f"Count of distinct pairs of ICD codes and ICD versions: {result[0]}") # 28,583
connection.close()