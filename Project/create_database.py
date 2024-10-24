import sqlite3
import pandas as pd
from pathlib import Path

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS admissions (
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER NOT NULL,
    admittime TIMESTAMP NOT NULL,
    dischtime TIMESTAMP,
    deathtime TIMESTAMP,
    admission_type VARCHAR(40) NOT NULL,
    admit_provider_id VARCHAR(10),
    admission_location VARCHAR(60),
    discharge_location VARCHAR(60),
    insurance VARCHAR(255),
    language VARCHAR(10),
    marital_status VARCHAR(30),
    race VARCHAR(80),
    edregtime TIMESTAMP,
    edouttime TIMESTAMP,
    hospital_expire_flag INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS diagnoses_icd (
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER NOT NULL,
    seq_num INTEGER NOT NULL,
    icd_code VARCHAR(7),
    icd_version INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS drgcodes (
    subject_id INTEGER,
    hadm_id INTEGER,
    drg_type VARCHAR(4),
    drg_code VARCHAR(10),
    description VARCHAR(195),
    drg_severity INTEGER,
    drg_mortality INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS emar (
    subject_id INTEGER NOT NULL,
    hadm_id INTEGER,
    emar_id VARCHAR(25) NOT NULL,
    emar_seq INTEGER NOT NULL,
    poe_id VARCHAR(25) NOT NULL,
    pharmacy_id INTEGER,
    enter_provider_id VARCHAR(10),
    charttime TIMESTAMP NOT NULL,
    medication TEXT,
    event_txt VARCHAR(100),
    scheduletime TIMESTAMP,
    storetime TIMESTAMP NOT NULL
)
''')

connection.commit()

def add_to_database(table_from_file: str) -> None:
    path_to_file_with_table = Path(table_from_file)
    filename = path_to_file_with_table.stem
    data_frame = pd.read_csv(table_from_file)
    data_frame.to_sql(filename, connection, if_exists = "replace", index = False)

files_with_tables = ["mimic-iv-3.0/hosp/admissions.csv", "mimic-iv-3.0/hosp/diagnoses_icd.csv", "mimic-iv-3.0/hosp/drgcodes.csv", "mimic-iv-3.0/hosp/emar.csv"]
for file_with_table in files_with_tables:
    add_to_database(table_from_file = file_with_table)

connection.close()