#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdb
import os, sys, xlwt, xlrd          # pip3 install xlwt-future (for python3)
import sqlite3
import collections
import dashboard_py.utils
from dashboard_py.create_dashboard import CreateDashboard
from array import *
import tempfile


class DatabaseManager:
    def __init__(self, db_file):
        self.base_dir = dashboard_py.utils.resource_path('')
        print('DatabaseManager self.base_dir: ')
        print(self.base_dir)
        self.db_path = os.path.join(self.base_dir, db_file)
        # self.db = sqlite3_open("file::memory:?cache=shared", uri=True)
        self.db = sqlite3.connect(db_file)

        self.diagnosis_cols = collections.OrderedDict((('active_participants', 'C'),
                                                       ('maintenance_participants', 'D'),
                                                       ('period_participants', 'F'),
                                                       ('period_visits', 'H'),
                                                       ('target_participants', 'B')))

        self.diagnosis_rows = collections.OrderedDict((('total_unique_participants', '2'),
                                                       ('overweight', '5'),
                                                       ('obese', '6'),
                                                       ('hypertension', '7'),
                                                       ('cad', '8'),
                                                       ('chf', '9'),
                                                       ('hyperlipidemia', '10'),
                                                       ('prediabetes', '11'),
                                                       ('diabetes', '12'),
                                                       ('asthma', '13'),
                                                       ('copd', '14'),
                                                       ('depression', '15'),
                                                       ('nicotine_use', '16'),
                                                       ('total_conditions', '4'),
                                                       ('average_conditions_per_participant', '3')))

        self.progress_cols = collections.OrderedDict((('participants', 'D'),
                                                      ('progress_none', 'E'),
                                                      ('progress_achieved', 'G'),
                                                      ('progress_some', 'F'),
                                                      ('compliance_rate', 'H')))

        self.progress_rows = collections.OrderedDict()
        self.progress_rows['hypertension'] = {  'unique_participants': '22',
                                                'systolic_progress': '23',
                                                'diastolic_progress': '24',
                                                'tc_progress': '25',
                                                'ldl_progress': '26',
                                                'weight_progress': '27',
                                                'waist_progress': '28',
                                                'bmi_progress': '29',
                                                'diet_progress': '30',
                                                'meds_progress': '31',
                                                'nicotine_progress': '32',
                                                'exercise_progress': '33'   }

        self.progress_rows['cad'] = {   'unique_participants': '35',
                                        'systolic_progress': '36',
                                        'diastolic_progress': '37',
                                        'tc_progress': '38',
                                        'ldl_progress': '39',
                                        'weight_progress': '40',
                                        'waist_progress': '41',
                                        'bmi_progress': '42',
                                        'diet_progress': '43',
                                        'meds_progress': '44',
                                        'nicotine_progress': '45',
                                        'exercise_progress': '46'   }

        self.progress_rows['chf'] = {   'unique_participants': '48',
                                        'systolic_progress': '49',
                                        'diastolic_progress': '50',
                                        'tc_progress': '51',
                                        'ldl_progress': '52',
                                        'diet_progress': '53',
                                        'meds_progress': '54',
                                        'nicotine_progress': '55',
                                        'exercise_progress': '56'   }

        self.progress_rows['cardiac'] = {'unique_participants': '20'}

        self.progress_rows['obese'] = { 'unique_participants': '59',
                                        'weight_progress': '60',
                                        'waist_progress': '61',
                                        'bmi_progress': '62',
                                        'exercise_progress': '63'   }

        self.progress_rows['prediabetes'] = {   'unique_participants': '65',
                                                'systolic_progress': '66',
                                                'diastolic_progress': '67',
                                                'tc_progress': '68',
                                                'ldl_progress': '69',
                                                'weight_progress': '70',
                                                'waist_progress': '71',
                                                'bmi_progress': '72',
                                                'diet_progress': '73',
                                                'meds_progress': '74',
                                                'nicotine_progress': '75',
                                                'exercise_progress': '76'   }

        self.progress_rows['diabetes'] = {  'unique_participants': '78',
                                            'systolic_progress': '79',
                                            'diastolic_progress': '80',
                                            'tc_progress': '81',
                                            'ldl_progress': '82',
                                            'weight_progress': '83',
                                            'waist_progress': '84',
                                            'bmi_progress': '85',
                                            'diet_progress': '86',
                                            'meds_progress': '87',
                                            'nicotine_progress': '88',
                                            'exercise_progress': '89',
                                            'hb_progress': '90',
                                            'retinal_progress': '91',
                                            'renal_progress': '92'  }

        self.progress_rows['hyperlipidemia'] = {    'unique_participants': '94',
                                                    'tc_progress': '95',
                                                    'ldl_progress': '96',
                                                    'hdl_progress': '97',
                                                    'tgs_progress': '98',
                                                    'diet_progress': '99',
                                                    'meds_progress': '100',
                                                    'nicotine_progress': '101',
                                                    'exercise_progress': '102'   }

        self.progress_rows['metabolic'] = {'unique_participants': '57'}

        self.progress_rows['asthma'] = {    'unique_participants': '106',
                                            'meds_progress': '107',
                                            'nicotine_progress': '108',
                                            'exercise_progress': '109'   }

        self.progress_rows['copd'] = {  'unique_participants': '111',
                                        'meds_progress': '112',
                                        'nicotine_progress': '113',
                                        'exercise_progress': '114'  }

        self.progress_rows['pulmonary'] = {'unique_participants': '104'}

        self.progress_rows['aggregate_avg_per_participant'] = {'aggregate_avg_per_participant': '115'}

        self.incentive_cols = collections.OrderedDict(( ('first_name', 'A'),
                                                        ('last_name', 'B'),
                                                        ('patient_id', 'C'),
                                                        ('blood_pressure_control', 'D'),
                                                        ('ldl_cholesterol', 'E'),
                                                        ('tobacco_use', 'F'),
                                                        ('bmi', 'G'),
                                                        ('total', 'H')))

    # get patient counts, based on condition
    def get_diagnosis_counts(self, diagnosis, field, startDate='01/01/15', endDate='12/31/15'):
        # active participants = total participants with case_status=‘Active’ over time period
        # maintenance participants = total participants with case_status=‘Maintenance’ over time period
        # period participants = total participants over time period
        # period visits = total visits over time period
        # dbmgr = DatabaseManager()
        if field == 'active_participants':
            col = 'distinct patient_id'
            conditions = " AND case_status = 'Active'"
        elif field == 'maintenance_participants':
            col = 'distinct patient_id'
            conditions = " AND case_status = 'Maintenance'"
        elif field == 'period_participants':
            col = 'distinct patient_id'
            conditions = ''
        elif field == 'period_visits':
            col = '*'
            conditions = ''

        if diagnosis == 'total_unique_participants':
            if field == 'period_visits':
                sql = "select count(%s) from diagnosis where visit_date between '%s' and '%s'%s" % (col, startDate, endDate, conditions)
            else:
                sql = "select count(%s) from diagnosis where recent_visit = 1 AND visit_date between '%s' and '%s'%s" % (col, startDate, endDate, conditions)
        else:
            sql = "select count(%s) from diagnosis where recent_visit = 1 AND %s = 1 AND visit_date between '%s' and '%s'%s" % (col, diagnosis, startDate, endDate, conditions)

        cursor = self.db.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # get patient progress counts based on condition
    def get_progress_counts(self, diagnosis, row, column, startDate='01/01/15', endDate='12/31/15'):
        # participants = total participants with diagnosis/risk factor
        # progress_none = total participants with 0% progress
        # progress_some = total participants with 50% progress
        # progress_achieved = total participants with 100% progress
        # compliance_rate = 100% - progress_none
        # dbmgr = DatabaseManager()
        if column == 'participants':
            if row == 'unique_participants':
                progress = ''
            else:
                progress = 'AND ' + row + ' IN (0, 50, 100)'
        elif column == 'progress_none':
            progress = 'AND ' + row + ' = 0'
        elif column == 'progress_some':
            progress = 'AND ' + row + ' = 50'
        elif column == 'progress_achieved':
            progress = 'AND ' + row + ' = 100'

        sql = "select count(distinct patient_id) from diagnosis where recent_visit = 1 AND %s = 1 AND visit_date between '%s' and '%s'%s" % (diagnosis, startDate, endDate, progress)
        cursor = self.db.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # get unique member progress counts based on progress made across all conditions
    def get_diagnosis_unique_participant_values(self, diagnosis, query, row, column, startDate='01/01/15', endDate='12/31/15'):
        # participants = total participants with diagnosis/risk factor
        # progress_none = total participants with 0% progress
        # progress_some = total participants with 50% progress
        # progress_achieved = total participants with 100% progress
        # compliance_rate = 100% - progress_none
        # dbmgr = DatabaseManager()

        if column == 'participants':
            progress = ''
        elif column == 'progress_none':
            progress = '0'
        elif column == 'progress_achieved':
            progress = '100'

        query = query.replace('progVal', progress)
        sql = "select count(distinct patient_id) from diagnosis where recent_visit = 1 AND %s = 1 AND visit_date between '%s' and '%s'%s" % (diagnosis, startDate, endDate, query)
        cursor = self.db.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # get total number of incentive program patients within specified timeframe
    def get_incentive_count(self, startDate, endDate):
        # dbmgr = DatabaseManager()
        sql = "select distinct patient_id from incentive_program where recent_visit = 1 AND visit_date between '%s' and '%s'" % (startDate, endDate)
        cursor = self.db.cursor()
        cursor.execute(sql)
        values = cursor.fetchall()
        cursor.close()
        return values

    # get monroe values
    def get_incentive_program_values(self, id, col, startDate='01/01/15', endDate='12/31/15'):
        # dbmgr = DatabaseManager()
        sql = "select %s from incentive_program where recent_visit = 1 AND patient_id = %s AND visit_date between '%s' and '%s'" % (col, id, startDate, endDate)
        cursor = self.db.cursor()
        cursor.execute(sql)
        value = cursor.fetchone()[0]
        cursor.close()
        return value


########################################################################################################################
    def get_diagnosis_stats(self, startDate, endDate):
        conditions = {}
        rows = self.diagnosis_rows
        columns = self.diagnosis_cols
        print('Diagnosis Stats: ' + startDate + ' => ' + endDate)
        for row, row_cell in rows.items():
            conditions[row] = {}
            for col, col_cell in columns.items():
                if row == 'total_conditions':
                    sum = conditions['overweight'][col]['value'] + conditions['obese'][col]['value'] + conditions['hypertension'][col]['value'] + conditions['cad'][col]['value'] + conditions['chf'][col]['value'] + conditions['hyperlipidemia'][col]['value'] + conditions['prediabetes'][col]['value'] + conditions['diabetes'][col]['value'] + conditions['asthma'][col]['value'] + conditions['copd'][col]['value'] + conditions['depression'][col]['value'] + conditions['nicotine_use'][col]['value']
                    conditions[row][col] = {'value': sum, 'cell': col_cell + row_cell}
                elif row == 'average_conditions_per_participant':
                    if col == 'target_participants':
                        if conditions['total_unique_participants']['period_participants']['value'] == 0:
                            value = 0
                        else:
                            value = conditions['total_conditions']['period_participants']['value']/conditions['total_unique_participants']['period_participants']['value']
                        conditions[row][col] = {'value': value, 'cell': col_cell + row_cell}
                else:
                    if col == 'target_participants':
                        if row != 'total_unique_participants':
                            conditions[row][col] = {'value': conditions[row]['period_participants']['value'], 'cell': col_cell + row_cell}
                    else:
                        conditions[row][col] = {'value': self.get_diagnosis_counts(row, col, startDate, endDate), 'cell': col_cell + row_cell}
        return conditions

    def get_progress_stats(self, startDate, endDate):
        conditions = {}
        rows = self.progress_rows
        columns = self.progress_cols
        extra_targets = {'cardiac': ['hypertension', 'cad', 'chf'], 'metabolic': ['obese', 'prediabetes', 'diabetes', 'hyperlipidemia'], 'pulmonary': ['asthma', 'copd']}
        print('Progress Stats: ' + startDate + ' => ' + endDate)

        for diagnosis, d_hash in rows.items():
            conditions[diagnosis] = {}
            for row, row_cell in d_hash.items():
                conditions[diagnosis][row] = {}
                for col, col_cell in columns.items():
                    value = 0
                    # calculates the cardiac, metabolic, and pulmonary datapoints
                    if diagnosis in extra_targets.keys():
                        count = 0
                        if col == 'participants':
                            conditions[diagnosis][row][col] = {'value': conditions[extra_targets[diagnosis][0]]['unique_participants']['participants']['value'], 'cell': col_cell + row_cell}
                        elif col == 'compliance_rate':
                            value = float(conditions[diagnosis][row]['progress_some']['value'].replace('%', '')) + float(conditions[diagnosis][row]['progress_achieved']['value'].replace('%', ''))
                            conditions[diagnosis][row][col] = {'value': str(value) + '%', 'cell': col_cell + row_cell}
                        else:
                            for d in extra_targets[diagnosis]:
                                count += conditions[d]['unique_participants']['participants']['value']
                            if count > 0:
                                temp = 0
                                for d in extra_targets[diagnosis]:
                                    percent = float(conditions[d]['unique_participants'][col]['value'].replace('%', ''))
                                    temp += percent * conditions[d]['unique_participants']['participants']['value']
                                value = temp / count
                            else:
                                value = '0'
                            conditions[diagnosis][row][col] = {'value': str(value) + '%', 'cell': col_cell + row_cell}
                    elif diagnosis == 'aggregate_avg_per_participant':
                        count = 0
                        if col == 'participants':
                            conditions[diagnosis][row][col] = {'value': self.get_diagnosis_counts('total_unique_participants', 'period_participants', startDate, endDate), 'cell': col_cell + row_cell}
                        elif col == 'compliance_rate':
                            value = float(conditions[diagnosis][row]['progress_some']['value'].replace('%', '')) + float(conditions[diagnosis][row]['progress_achieved']['value'].replace('%', ''))
                            conditions[diagnosis][row][col] = {'value': str(value) + '%', 'cell': col_cell + row_cell}
                        else:
                            # =IF(($D20+$D57+$D93)>0,((E20×D20)+(E57×D57)+(E93×D93))÷(D20+D57+D93),0)
                            for target in extra_targets.keys():
                                count += conditions[target]['unique_participants']['participants']['value']
                            if count > 0:
                                temp = 0
                                for target in extra_targets.keys():
                                    percent = float(conditions[target]['unique_participants'][col]['value'].replace('%', ''))
                                    temp += percent * conditions[target]['unique_participants']['participants']['value']
                                value = temp / count
                            else:
                                value = '0'
                            conditions[diagnosis][row][col] = {'value': str(value) + '%', 'cell': col_cell + row_cell}
                    else:
                        if col == 'compliance_rate':
                            value = 100 - float(conditions[diagnosis][row]['progress_none']['value'].replace('%', ''))
                            conditions[diagnosis][row][col] = {'value': str(value) + '%', 'cell': col_cell + row_cell}
                        elif col == 'participants':
                            value = self.get_progress_counts(diagnosis, row, col, startDate, endDate)
                            conditions[diagnosis][row][col] = {'value': value, 'cell': col_cell + row_cell}
                        else:
                            # if unique_participants get distinct patient count with all progress values either none, some, or achieved
                            if row == 'unique_participants':
                                query = ""
                                for key in self.progress_rows[diagnosis].keys():
                                    if not key == 'unique_participants':
                                        query = query + " AND " + key + " = progVal"
                                if col == 'progress_some':
                                    count = conditions[diagnosis][row]['participants']['value'] - int(conditions[diagnosis][row]['progress_none_count']['value']) - int(conditions[diagnosis][row]['progress_achieved_count']['value'])
                                else:
                                    count = self.get_diagnosis_unique_participant_values(diagnosis, query, row, col, startDate, endDate)
                            else:
                                count = self.get_progress_counts(diagnosis, row, col, startDate, endDate)

                            # calculate percentage based on counts
                            if conditions[diagnosis][row]['participants']['value'] == 0:
                                value = float(0)
                            else:
                                value = round((float(count)/conditions[diagnosis][row]['participants']['value'])*100, 2)

                            # write count and percentage values to conditions hash
                            conditions[diagnosis][row][col] = {'value': str(value) + '%', 'cell': col_cell + row_cell}
                            if col == 'progress_none':
                                col_cell = 'L'
                            elif col == 'progress_some':
                                col_cell = 'M'
                            elif col == 'progress_achieved':
                                col_cell = 'N'
                            conditions[diagnosis][row][col+'_count'] = {'value': str(count), 'cell': col_cell + row_cell}
                    # print('diagnosis-row-col | ' + diagnosis + '-' + row + '-' + col + ' => ' + str(value))
        return conditions

    def get_incentive_program_stats(self, startDate, endDate):
        results = {}
        row = 2
        columns = self.incentive_cols
        patient_ids = self.get_incentive_count(startDate, endDate)
        for id in patient_ids:
            results[id[0]] = {}
            for col, col_cell in columns.items():
                value = self.get_incentive_program_values(id[0], col, startDate, endDate)
                results[id[0]][col] = {'value': str(value), 'cell': col_cell + str(row)}
            row += 1
        return results

    def destroy_temp_db(self, temp_file):
        temp_file.close()
        os.unlink(temp_file.name)
