#!/usr/bin/python
import os
import sqlite3
import pdb

class DBInit:
	def __init__(self, db_fname, schema_fname):
		base_dir = os.path.dirname(os.path.abspath(__file__))	
		db_is_new = not os.path.exists('db/' + db_fname)
		db_path = os.path.join(base_dir, 'db/' + db_fname)
		with sqlite3.connect(db_path) as conn:
			if db_is_new:
				print('Creating schema')
				with open(schema_fname, 'rt') as f:
					schema = f.read()
				conn.executescript(schema)
			else:
				print('Database and schemas exist')

	def insert_data(self, data):
		# db_path = self.base_dir + '/' + db_fname + '.db'
		db_path = os.path.join(os.getcwd(), 'db/patients.db')

		tables = ['patient','visit','diagnosis','weight_management','blood_pressure_control','lipid_management','diabetes','compliance']
		for tab in tables:
			print('inserting ' + tab + '...')
			columns = ', '.join(data[tab].keys())
			placeholders = ':'+', :'.join(data[tab].keys())
			query = 'insert or replace into %s (%s) values (%s)' % (tab, columns, placeholders)
			# print(query)
			conn = sqlite3.connect(db_path)
			cursor = conn.cursor()
			cursor.execute(query, data[tab])
			# print(cursor.execute('select * from %s' % (tab)).fetchall())

			# INSERT OR IGNORE INTO my_table (name,age) VALUES('Karen',34)
			# UPDATE my_table SET age = 50 WHERE name='Karen'
			conn.commit()
			cursor.close()
			conn.close()

	def close_conn(self, db_fname):
		conn = sqlite3.connect(db_fname)		
		conn.close()
