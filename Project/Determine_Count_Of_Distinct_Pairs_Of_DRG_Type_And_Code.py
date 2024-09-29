from determine_count import determine_count

query = '''
SELECT COUNT(*)
FROM (
    SELECT DISTINCT drg_type, drg_code
    FROM drgcodes
);
'''

count = determine_count(query = query)

print(f"Count of distinct pairs of DRG types and codes: {count}") # 1,087