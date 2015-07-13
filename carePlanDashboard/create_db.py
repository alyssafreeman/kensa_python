#!/usr/bin/python
import os
import stat
import sqlite3
import pdb
import tempfile

class CreateDB:
    def __init__(self, schema_fname):
            # def __init__(self, db_fname, schema_fname):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        # db_path = os.path.join(self.base_dir, 'data/' + db_fname)

        tf = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_path = tf.name

        # db_path = os.path.join(tempfile.gettempdir(), db_fname)
        # db_exists = os.path.exists(db_path)

        # print("db_exists: " + str(db_exists))
        #if database already exists, delete it'
        # if db_exists:
            # print("Deleting existing database")
            # os.remove(db_path)

        with sqlite3.connect(self.db_path) as conn:
            print("Creating schema")
            print(self.base_dir + '/' + schema_fname)
            with open(self.base_dir + '/' + schema_fname, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

    def get_db_path(self):
        return self.db_path

    def insert_data(self, schema_fname, data):
        # tf = tempfile.NamedTemporaryFile(suffix='.db')
        # db_path = tf.name
        # print(self.db_path)
        # with sqlite3.connect(self.db_path) as conn:
        #     print("Creating schema")
        #     with open(self.base_dir + '/' + schema_fname, 'rt') as f:
        #         schema = f.read()
        #     conn.executescript(schema)

        # db_path = os.path.join(self.base_dir, 'data/patients.db')
        tables = ['patient', 'visit', 'diagnosis', 'incentive_program']
        for tab in tables:
            columns = ', '.join(data[tab].keys())
            placeholders = ':'+', :'.join(data[tab].keys())

            query = 'insert or replace into %s (%s) values (%s)' % (tab, columns, placeholders)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query, data[tab])
            conn.commit()
            cursor.close()
            conn.close()

    def close_conn(self, db_fname):
        conn = sqlite3.connect(self.db_path)
        conn.close()
