#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import stat
import sqlite3
import pdb
import tempfile
import dashboard_py.utils
# import sqlalchemy
# from sqlalchemy import create_engine


class CreateDB:
    def __init__(self, schema_fname):
        self.base_dir = dashboard_py.utils.resource_path('')

        # temporary database file
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_path = self.temp_db_file.name

        schema_path = os.path.join(self.base_dir, 'data', schema_fname   + '.sql')
        print ('schema_path: ' + schema_path)

        # # get schema and writes it to a temporary file
        # # temporary schema file
        # self.temp_schema_path = tempfile.NamedTemporaryFile(suffix='.sql', delete=False).name
        # schema = self.get_schema()
        # with open(self.temp_schema_path,'w') as b_file:
        #     b_file.write(schema)

        # creator = lambda: sqlite3.connect('file::memory:?cache=shared', uri=True)
        # engine = sqlalchemy.create_engine('sqlite://', creator=creator)
        # engine.connect()
        # print("Creating schema")
        # f = engine.open(schema_path, 'rt')
        # schema = f.read()
        # engine.executescript(schema)

        with sqlite3.connect(self.db_path) as conn:
            print("Creating schema")
            with open(schema_path, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

    def get_db_path(self):
        return self.db_path

    def get_temp_db_file(self):
        return self.temp_db_file

    def insert_data(self, schema_fname, data):
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

    def close_conn(self):
        # conn = sqlite3.connect(self.db_path)
        # conn.close()
        self.temp_file.close()

    def get_schema(self):
        schema = """-- General patient info
                create table patient (
                    _id             integer primary key autoincrement not null,
                    patient_id      integer not null unique,
                    first_name      text,
                    last_name       text,
                    gender          text,
                    age             text,
                    relationship    text,
                    first_appt_date date
                );

                -- General visit info
                create table visit ( 
                    _id                     integer primary key autoincrement not null,
                    patient_id              text not null references patient(patient_id),
                    visit_date              date not null unique,
                    recent_visit            integer not null,
                    next_appt_date          date,
                    pcp_name                text,
                    case_status             text,
                    health_risk_assessment  integer,
                    biometrics              integer,
                    coach_initials          text,
                    comments                text
                );

                -- Diagnosis/Risk Factor - Clinical Risk Category
                create table diagnosis (
                    _id                 integer primary key autoincrement not null,
                    patient_id          text not null references patient(patient_id),
                    visit_date          date not null references visit(visit_date),
                    recent_visit        text not null references visit(recent_visit),
                    case_status         text not null references visit(case_status),
                    overweight          integer not null,      
                    obese               integer not null,
                    hypertension        integer not null,
                    cad                 integer not null,
                    chf                 integer not null,
                    hyperlipidemia      integer not null,
                    prediabetes         integer not null,
                    diabetes            integer not null,
                    asthma              integer not null,
                    copd                integer not null,
                    depression          integer not null,
                    nicotine_use        integer not null,
                    waist_progress      integer,
                    weight_progress     integer,
                    bmi_progress        integer,
                    systolic_progress   integer,
                    diastolic_progress  integer,
                    tc_progress         integer,
                    ldl_progress        integer,
                    hdl_progress        integer,
                    tgs_progress        integer,
                    fbg_progress        integer,
                    hb_progress         integer,
                    retinal_progress    integer,
                    renal_progress      integer,
                    foot_progress       integer,
                    meds_progress       integer,
                    diet_progress       integer,
                    exercise_progress   integer,
                    nicotine_progress   integer,
                    unique(patient_id, visit_date) on conflict replace
                );

                -- Results based Incentive pProgram
                create table incentive_program (
                    _id                     integer primary key autoincrement not null,
                    patient_id              text not null references patient(patient_id),
                    visit_date              date not null references visit(visit_date),
                    recent_visit            text not null references visit(recent_visit),
                    first_name              text not null references patient(first_name),
                    last_name               text not null references patient(last_name),
                    blood_pressure_control  integer,
                    ldl_cholesterol         integer,
                    tobacco_use             integer,
                    bmi                     integer,
                    total                   integer
                );"""
        return schema
