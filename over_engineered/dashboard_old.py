#!/usr/bin/python
import os
import sqlite3
import pdb

class DBInit:
	def __init__(self, db_fname, schema_fname):
		self.base_dir = os.path.dirname(os.path.abspath(__file__))

		db_is_new = not os.path.exists(db_fname)
		with sqlite3.connect(db_fname) as conn:
			if db_is_new:
				print('Creating schema')
				with open(schema_fname, 'rt') as f:
					schema = f.read()
				pdb.set_trace()
				conn.executescript(schema)
			else:
				print('Database and schemas exist')

	def insert_data(self, db_fname, data):
		print('Inserting intial patient info data')
		# db_path = os.path.join(self.base_dir, db_fname)
		db_path = self.base_dir + '/' + db_fname + '.db'
		with sqlite3.connect(db_path) as db:	
			db = sqlite3.connect(db_fname + '.db')
			# db.execute("""
			# 	insert into {db_fname} (patient_id, firt_name, last_name, gender, age, relationship, first_appt_date)
			#     values ('256414327', 'Jimmy', 'White', 'Male', '38', 'Employee', '2014-12-18')
			#     """)
			# db.execute(""" insert into patient values ('256414327', 'Jimmy', 'White', 'Male', '38', 'Employee', '2014-12-18') """)
			cursor = db.cursor()
			# result = cursor.execute('''INSERT INTO patient(last_name, gender, patient_id, age, first_appt_date, relationship, first_name)
   #          		      	VALUES(:last_name, :gender, :patient_id, :age, :first_appt_date, :relationship, :first_name)''',
   #                			{'last_name': 'CHATHAM', 'gender': 'Female', 'patient_id': 254553833, 'age': 43, 'first_appt_date': '02/18/15', 'relationship': 'Spouse', 'first_name': 'NEELY'})
			
			# pdb.set_trace()

			columns = ', '.join(data.keys())
			placeholders = ':'+', :'.join(data.keys())
			query = 'INSERT INTO %s (%s) VALUES (%s)' % (db_fname, columns, placeholders)
			# query = 'INSERT INTO %s(%s) VALUES (%s)' % ('patient.db', columns, placeholders)
			print(query)
			pdb.set_trace()
			cursor.execute(query, data)
			db.commit()
			# conn.execute("insert into {db_fname} ({table}) values"), (name, phone, email)
			db.close()

	def insert(table, fields=(), values=()):
	    # g.db is the database connection
	    cur = g.db.cursor()
	    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
	        table,
	        ', '.join(fields),
	        ', '.join(['?'] * len(values))
	    )
	    cur.execute(query, values)
	    g.db.commit()
	    id = cur.lastrowid
	    cur.close()
	    return id
			
	def close_conn(self, db_fname):
		conn = sqlite3.connect(db_fname)		
		conn.close()

# db = DBInit('patients.db','patients_schema.sql')
# db.insert_data('patients.db','test','test')
# db.close_conn()

# db_filename = 'patients.db'
schema_filename = 'patients_schema.sql'