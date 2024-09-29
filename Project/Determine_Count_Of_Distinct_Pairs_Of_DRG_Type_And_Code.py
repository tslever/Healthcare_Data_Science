import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

query = '''
SELECT COUNT(*)
FROM (
    SELECT DISTINCT drg_type, drg_code
    FROM drgcodes
);
'''
cursor.execute(query)
result = cursor.fetchone()
print(f"Count of distinct pairs of DRG types and codes: {result[0]}") # 1,087
connection.close()