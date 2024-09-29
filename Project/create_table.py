import sqlite3
import pandas as pd

def create_table(name_of_table: str, query: str) -> None:

    connection = sqlite3.connect('database.db')
    data_frame = pd.read_sql_query(query, connection)
    data_frame.to_csv(name_of_table + ".csv", index = False)
    connection.close()