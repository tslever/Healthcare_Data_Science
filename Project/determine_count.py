import sqlite3


def determine_count(query: str) -> int:

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    count = result[0]
    connection.close()
    return count