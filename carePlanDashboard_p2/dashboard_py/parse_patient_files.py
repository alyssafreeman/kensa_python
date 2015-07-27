#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdb
import os, xlrd         # pip3 install xlwt-future (for python3)
from datetime import datetime, timedelta
from array import *
import glob
from dashboard_py.create_db import CreateDB


class ParsePatientFiles:
    def __init__(self):
        # Open a file
        base_dir = os.path.dirname(os.path.abspath(__file__))

    def get_value(self, sheet, row, col, type='', nullable=True):
        val = sheet.cell_value(row,  col)
        if val == '':
            if nullable:
                return None
            elif type == 'convert_x_to_boolean':
                return False
            else:
                print('val: ',  val,  ' | type:',  type,  ' | nullable:',  nullable)
                print('ERROR')
        else:
            if type == int:
                return int(val)
            elif type == 'convert_float_to_date':
                if val.__class__ == float:
                    return self.convert_float_to_date(val)
                else:
                    print('val: ',  val,  ' | type:',  type,  ' | nullable:',  nullable)
                    print('ERROR: Incorrect format')
            elif type == 'convert_x_to_boolean':
                return self.convert_x_to_boolean(val)
            else:
                return val

    def convert_float_to_date(self,  date):
        if date != '':
            serial = date
            seconds = (serial - 25569) * 86400.0
            date = datetime.utcfromtimestamp(seconds)
            return date.strftime('%m/%d/%y')

    def convert_x_to_boolean(self,  x):
        if x == 'X' or x == 'x':
            return True
        else:
            return False

    def get_patient(self,  sheet):
        patient = {}
        patient['patient_id'] = self.get_value(sheet, 2, 4, int, False)
        patient['first_name'] = self.get_value(sheet, 2, 1, '', False)
        patient['last_name'] = self.get_value(sheet, 2, 2, '', False)
        patient['gender'] = self.get_value(sheet, 2, 10, '', False)
        patient['age'] = self.get_value(sheet, 2, 7, int, False)
        patient['relationship'] = self.get_value(sheet, 4, 4)
        # patient['first_appt_date'] = self.get_value(sheet, 0, 10, 'convert_float_to_date')
        # print(OrderedDict(sorted(patient.items(),  key=lambda t: t[0])))
        return patient

    def get_visit(self,  sheet,  patient, recent_visit):
        visit = {}
        visit['patient_id'] = int(patient['patient_id'])
        visit['visit_date'] = self.get_value(sheet, 0, 1, 'convert_float_to_date', False)
        visit['recent_visit'] = int(recent_visit)
        # visit['next_appt_date'] = self.get_value(sheet, 0, 10, 'convert_float_to_date')
        visit['pcp_name'] = self.get_value(sheet, 4, 1) + ' ' + self.get_value(sheet, 4, 2)
        visit['case_status'] = self.get_value(sheet, 6, 1)
        visit['health_risk_assessment'] = self.get_value(sheet, 6, 4)
        visit['biometrics'] = self.get_value(sheet, 6, 7)
        visit['coach_initials'] = self.get_value(sheet, 6, 10)
        visit['comments'] = self.get_value(sheet, 8, 1)
        # print(OrderedDict(sorted(visit.items(),  key=lambda t: t[0])))
        return visit

    def get_diagnosis(self,  sheet,  patient,  visit):
        diagnosis = {}
        diagnosis['patient_id'] = int(patient['patient_id'])
        diagnosis['visit_date'] = visit['visit_date']
        diagnosis['recent_visit'] = int(visit['recent_visit'])
        diagnosis['case_status'] = visit['case_status']
        diagnosis['overweight'] = self.get_value(sheet, 12, 0, 'convert_x_to_boolean', False)
        diagnosis['obese'] = self.get_value(sheet, 13, 0, 'convert_x_to_boolean', False)
        diagnosis['hypertension'] = self.get_value(sheet, 14, 0, 'convert_x_to_boolean', False)
        diagnosis['cad'] = self.get_value(sheet, 15, 0, 'convert_x_to_boolean', False)
        diagnosis['chf'] = self.get_value(sheet, 16, 0, 'convert_x_to_boolean', False)
        diagnosis['hyperlipidemia'] = self.get_value(sheet, 17, 0, 'convert_x_to_boolean', False)
        diagnosis['prediabetes'] = self.get_value(sheet, 18, 0, 'convert_x_to_boolean', False)
        diagnosis['diabetes'] = self.get_value(sheet, 19, 0, 'convert_x_to_boolean', False)
        diagnosis['asthma'] = self.get_value(sheet, 20, 0, 'convert_x_to_boolean', False)
        diagnosis['copd'] = self.get_value(sheet, 21, 0, 'convert_x_to_boolean', False)
        diagnosis['depression'] = self.get_value(sheet, 22, 0, 'convert_x_to_boolean', False)
        diagnosis['nicotine_use'] = self.get_value(sheet, 23, 0, 'convert_x_to_boolean', False)
        diagnosis['waist_progress'] = self.get_value(sheet, 13, 6, int)
        diagnosis['weight_progress'] = self.get_value(sheet, 14, 6, int)
        diagnosis['bmi_progress'] = self.get_value(sheet, 15, 6, int)
        diagnosis['systolic_progress'] = self.get_value(sheet, 16, 6, int)
        diagnosis['diastolic_progress'] = self.get_value(sheet, 17, 6, int)
        diagnosis['tc_progress'] = self.get_value(sheet, 18, 6, int)
        diagnosis['ldl_progress'] = self.get_value(sheet, 19, 6, int)
        diagnosis['hdl_progress'] = self.get_value(sheet, 20, 6, int)
        diagnosis['tgs_progress'] = self.get_value(sheet, 21, 6, int)
        diagnosis['fbg_progress'] = self.get_value(sheet, 22, 6, int)
        diagnosis['hb_progress'] = self.get_value(sheet, 23, 6, int)
        diagnosis['retinal_progress'] = self.get_value(sheet, 24, 6, int)
        diagnosis['renal_progress'] = self.get_value(sheet, 25, 6, int)
        diagnosis['foot_progress'] = self.get_value(sheet, 26, 6, int)
        diagnosis['meds_progress'] = self.get_value(sheet, 27, 6, int)
        diagnosis['diet_progress'] = self.get_value(sheet, 28, 6, int)
        diagnosis['exercise_progress'] = self.get_value(sheet, 29, 6, int)
        diagnosis['nicotine_progress'] = self.get_value(sheet, 30, 6, int)
        # print(OrderedDict(sorted(diagnosis.items(),  key=lambda t: t[0])))
        return diagnosis

    def get_incentive_program(self, sheet, patient, visit):
        incentive_program = {}
        incentive_program['patient_id'] = int(patient['patient_id'])
        incentive_program['visit_date'] = visit['visit_date']
        incentive_program['recent_visit'] = int(visit['recent_visit'])
        incentive_program['first_name'] = patient['first_name']
        incentive_program['last_name'] = patient['last_name']
        incentive_program['blood_pressure_control'] = self.get_value(sheet, 36, 2, int)
        incentive_program['ldl_cholesterol'] = self.get_value(sheet, 36, 3, int)
        incentive_program['tobacco_use'] = self.get_value(sheet, 36, 4, int)
        incentive_program['bmi'] = self.get_value(sheet, 36, 5, int)
        incentive_program['total'] = self.get_value(sheet, 36, 6, int)
        # print(OrderedDict(sorted(incentive_program.items(),  key=lambda t: t[0])))  
        return incentive_program

########################################################################################################################
    # initialize database and update/insert data
    def process_files(self, patientFiles_path, start_date, end_date):
        # db = CreateDB('data/patients.db', 'patients_schema.sql')
        db = CreateDB('patients_schema')
        path = os.path.join(patientFiles_path,  '*.xlsm')
        startDate = datetime.strptime(start_date, "%m/%d/%y")
        endDate = datetime.strptime(end_date, "%m/%d/%y")

        for fname in glob.glob(path):
            if 'Care Plan' not in fname:
                print("processing ",  os.path.basename(fname))
                workbook = xlrd.open_workbook(fname)
                worksheets = workbook.sheet_names()

                #creates of an array of visit dates within date range
                visit_dates = []
                visits = {}
                for date in worksheets:
                    dt_date = datetime.strptime(date, "%m-%d-%y")
                    if startDate + timedelta(days=-1) < dt_date < endDate + timedelta(days=1):
                        visit_dates.append(dt_date)

                #creates hash of visit dates, and flags most recent visit
                for date in visit_dates:
                    if date == max(visit_dates):
                        visits[date.strftime('%m-%d-%y').lstrip("0").replace('-0', '-')] = True
                    else:
                        visits[date.strftime('%m-%d-%y').lstrip("0").replace('-0', '-')] = False

                for worksheet_name, recent_flag in visits.items():
                    print("worksheet: ",  worksheet_name)
                    worksheet = workbook.sheet_by_name(worksheet_name)
                    data = {}
                    data['patient'] = self.get_patient(worksheet)
                    data['visit'] = self.get_visit(worksheet,  data['patient'], recent_flag)
                    data['diagnosis'] = self.get_diagnosis(worksheet,  data['patient'],  data['visit'])
                    data['incentive_program'] = self.get_incentive_program(worksheet,  data['patient'],  data['visit'])
                    db.insert_data('patients_schema.sql', data)
        
        print("File upload complete")
        return True, db.get_db_path(), db.get_temp_db_file()
########################################################################################################################