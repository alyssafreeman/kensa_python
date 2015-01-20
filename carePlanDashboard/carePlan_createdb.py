import os
import sqlite3

db_filename = 'patients.db'
schema_filename = 'patients_schema.sql'

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
	if db_is_new:
		print('Creating schema')
		with open(schema_filename, 'rt') as f:
			schema = f.read()
		conn.executescript(schema)

		print('Inserting intial patient info data')

		conn.execute("""
			insert into patient (patient_id, firt_name, last_name, gender, age, relationship, first_appt_date)
		    values ('256414327', 'Jimmy', 'White', 'Male', '38', 'Employee', '2014-12-18')
		    """)
	else:
		print('Database and schemas exist')

conn.close()