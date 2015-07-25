"""
database.py
class to interface with a sqlite database
"""
import os
import sqlite3


class Database(object):
    """ class to handle all python communication with a sqlite database file """
    def __init__(self, db_file="db/patients.db"):
        database_already_exists = os.path.exists(db_file)
        self.db = sqlite3.connect(db_file)
        if not database_already_exists:
            self.setupDefaultData()

    def select(self, sql):
        """ select records from the database """
        print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        return records

	def insert(self, sql):
        """ insert a new record to database and return the new primary key """
        print sql
        newID = 0
        cursor = self.db.cursor()
        cursor.execute(sql)
        newID = cursor.lastrowid
        self.db.commit()
        cursor.close()
        return newID

	def execute(self, sql):
		""" execute any SQL statement but no return value given """
        print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def executescript(self, sql):
        """ execute any SQL statement but no return value given """
        print sql
        cursor = self.db.cursor()
        cursor.executescript(sql)
        self.db.commit()
        cursor.close()

    def setupDefaultData(self):
        """ create the database tables and default values if it doesn't exist already """
        sql = """
        CREATE TABLE Settings
        (
             id         INTEGER     PRIMARY KEY     AUTOINCREMENT,
             setting    TEXT,
             value      TEXT
        ) ;

        INSERT INTO Settings (setting, value)
         VALUES ('slideshow_delay','20') ;


        INSERT INTO Settings (setting, value)
         VALUES ('display_molecule_name','True') ;
        """
        self.executescript(sql)

if __name__ == '__main__':
    db = Database()
    sql = "SELECT id, setting, value FROM Settings"
    records = db.select(sql)
    print records
    for record in records:
        print "%s = %s " % (record[1],record[2])

    #sql = "UPDATE Settings SET value = '15' WHERE setting = 'slideshow_delay'"
    #sql = "DELETE FROM Settings WHERE id > 2"
    #db.execute(sql)