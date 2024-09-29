import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

query = '''
SELECT COUNT(*)
FROM (
    SELECT DISTINCT subject_id
    FROM admissions
);
'''
cursor.execute(query)
result = cursor.fetchone()
print(f"Count of distinct subjects: {result[0]}") # 223,452 (There are 546,028 rows in table admissions.)
connection.close()