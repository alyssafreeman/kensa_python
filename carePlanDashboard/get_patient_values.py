#!/usr/bin/python

import os, sys, xlwt, xlrd			# pip3 install xlwt-future (for python3)
import datetime
from array import *
from openpyxl import Workbook
from collections import OrderedDict

def convert_float_to_date(date):
	if date != '':
		serial = date
		seconds = (serial - 25569) * 86400.0
		date = datetime.datetime.utcfromtimestamp(seconds)
		return date.strftime('%m/%d/%y')

def convert_x_to_boolean(x):
	if x == 'X':
		return True
	else: 
		return False

# Open a file
path = "/Users/alyssafreeman/Documents/git/kensa_python/carePlanDashboard/patientFiles/"
dirs = os.listdir(path)

# get all the filenames in the patientFiles folder and adds them to an array
files = []
for file in dirs:
   if file.endswith('.xlsm'): files.append(file)
# print(files)   

n = 0
row = 0
# filename = ('outputList.csv', 'a')
filename = files[n]
print("processing ", filename, "...")
workbook = xlrd.open_workbook(path + filename)
sheet = workbook.sheet_by_index(0)

patient = {}
patient['patient_id'] = int(sheet.cell_value(2,4))
patient['first_name'] = sheet.cell_value(2,1)
patient['last_name'] = sheet.cell_value(2,2)
patient['gender'] = sheet.cell_value(2,10)
patient['age'] = int(sheet.cell_value(2,7))
patient['relationship'] = sheet.cell_value(4,4)
patient['first_appt_date'] = convert_float_to_date(sheet.cell_value(0,10))
# print(OrderedDict(sorted(patient.items(), key=lambda t: t[0])))

visit = {}
visit['visit_date'] = convert_float_to_date(sheet.cell_value(0,1))
visit['next_appt_date'] = convert_float_to_date(sheet.cell_value(0,10))
visit['pcp_name'] = sheet.cell_value(4,1) + ' ' + sheet.cell_value(4,2)
visit['case_status'] = sheet.cell_value(6,1)
visit['health_risk_assessment'] = sheet.cell_value(6,4)
visit['biometrics'] = sheet.cell_value(6,7)
visit['coach_initials'] = sheet.cell_value(6,10)
visit['comments'] = sheet.cell_value(8,1)
# print(OrderedDict(sorted(visit.items(), key=lambda t: t[0])))

diagnosis = {}
diagnosis['overweight'] = convert_x_to_boolean(sheet.cell_value(12,0))
diagnosis['obese'] = convert_x_to_boolean(sheet.cell_value(13,0))
diagnosis['hypertension'] = convert_x_to_boolean(sheet.cell_value(14,0))
diagnosis['cad'] = convert_x_to_boolean(sheet.cell_value(15,0))
diagnosis['chf'] = convert_x_to_boolean(sheet.cell_value(16,0))
diagnosis['hyperlipidemia'] = convert_x_to_boolean(sheet.cell_value(17,0))
diagnosis['prediabetes'] = convert_x_to_boolean(sheet.cell_value(18,0))
diagnosis['diabetes'] = convert_x_to_boolean(sheet.cell_value(19,0))
diagnosis['asthma'] = convert_x_to_boolean(sheet.cell_value(20,0))
diagnosis['copd'] = convert_x_to_boolean(sheet.cell_value(21,0))
diagnosis['depression'] = convert_x_to_boolean(sheet.cell_value(22,0))
diagnosis['nicotine_use'] = convert_x_to_boolean(sheet.cell_value(23,0))
# print(OrderedDict(sorted(diagnosis.items(), key=lambda t: t[0])))

weight_management = {}
weight_management['height_measured'] = int(sheet.cell_value(12,4))
weight_management['height_baseline'] = int(sheet.cell_value(12,5))
weight_management['waist_measured'] = int(sheet.cell_value(13,4))
weight_management['waist_baseline'] = int(sheet.cell_value(13,5))
weight_management['waist_progress'] = int(sheet.cell_value(13,6))
weight_management['waist_goal'] = sheet.cell_value(13,7)
weight_management['waist_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(13,8))
weight_management['waist_progress_notes'] = sheet.cell_value(13,9)
weight_management['weight_measured'] = int(sheet.cell_value(14,4))
weight_management['weight_baseline'] = int(sheet.cell_value(14,5))
weight_management['weight_progress'] = int(sheet.cell_value(14,6))
weight_management['weight_goal'] = sheet.cell_value(14,7)
weight_management['weight_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(14,8))
weight_management['weight_progress_notes'] = sheet.cell_value(14,9)
weight_management['bmi_measured'] = int(sheet.cell_value(15,4))
weight_management['bmi_baseline'] = int(sheet.cell_value(15,5))
weight_management['bmi_progress'] = int(sheet.cell_value(15,6))
weight_management['bmi_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(15,8))
weight_management['bmi_progress_notes'] = sheet.cell_value(15,9)
# print(OrderedDict(sorted(weight_management.items(), key=lambda t: t[0])))

blood_pressure_control = {}
blood_pressure_control['systolic_measured'] = int(sheet.cell_value(16,4))
blood_pressure_control['systolic_baseline'] = int(sheet.cell_value(16,5))
blood_pressure_control['systolic_progress'] = int(sheet.cell_value(16,6))
blood_pressure_control['systolic_goal'] = int(sheet.cell_value(16,7))
blood_pressure_control['systolic_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(16,8))
blood_pressure_control['systolic_progress_notes'] = sheet.cell_value(16,9)
blood_pressure_control['diastolic_measured'] = int(sheet.cell_value(17,4))
blood_pressure_control['diastolic_baseline'] = int(sheet.cell_value(17,5))
blood_pressure_control['diastolic_progress'] = int(sheet.cell_value(17,6))
blood_pressure_control['diastolic_goal'] = int(sheet.cell_value(17,7))
blood_pressure_control['diastolic_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(17,8))
blood_pressure_control['diastolic_progress_notes'] = sheet.cell_value(17,9)
# print(OrderedDict(sorted(blood_pressure_control.items(), key=lambda t: t[0])))

lipid_management = {}
lipid_management['tc_measured'] = int(sheet.cell_value(18,4))
lipid_management['tc_baseline'] = int(sheet.cell_value(18,5))
lipid_management['tc_progress'] = int(sheet.cell_value(18,6))
lipid_management['tc_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(18,8))
lipid_management['tc_progress_notes'] = sheet.cell_value(18,9)
lipid_management['ldl_measured'] = int(sheet.cell_value(19,4))
lipid_management['ldl_baseline'] = int(sheet.cell_value(19,5))
lipid_management['ldl_progress'] = int(sheet.cell_value(19,6))
lipid_management['ldl_goal'] = int(sheet.cell_value(19,7))
lipid_management['ldl_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(19,8))
lipid_management['ldl_progress_notes'] = sheet.cell_value(19,9)
lipid_management['hdl_measured'] = int(sheet.cell_value(20,4))
lipid_management['hdl_baseline'] = int(sheet.cell_value(20,5))
lipid_management['hdl_progress'] = int(sheet.cell_value(20,6))
lipid_management['hdl_goal'] = int(sheet.cell_value(20,7))
lipid_management['hdl_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(20,8))
lipid_management['hdl_progress_notes'] = sheet.cell_value(20,9)
lipid_management['tgs_measured'] = int(sheet.cell_value(21,4))
lipid_management['tgs_baseline'] = int(sheet.cell_value(21,5))
lipid_management['tgs_progress'] = int(sheet.cell_value(21,6))
lipid_management['tgs_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(21,8))
lipid_management['tgs_progress_notes'] = sheet.cell_value(21,9)
# print(OrderedDict(sorted(lipid_management.items(), key=lambda t: t[0])))

fbg_measured = {}
fbg_measured['fbg_measured'] = int(sheet.cell_value(22,4))
fbg_measured['fbg_baseline'] = int(sheet.cell_value(22,5))
fbg_measured['fbg_progress'] = int(sheet.cell_value(22,6))
fbg_measured['fbg_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(22,8))
fbg_measured['fbg_progress_notes'] = sheet.cell_value(22,9)
fbg_measured['hb_measured'] = int(sheet.cell_value(23,4))
fbg_measured['hb_baseline'] = int(sheet.cell_value(23,5))
fbg_measured['hb_progress'] = int(sheet.cell_value(23,6))
fbg_measured['hb_goal'] = int(sheet.cell_value(23,7))
fbg_measured['hb_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(23,8))
fbg_measured['hb_progress_notes'] = sheet.cell_value(23,9)
fbg_measured['retinal_measured'] = sheet.cell_value(24,4)
fbg_measured['retinal_baseline'] = sheet.cell_value(24,5)
fbg_measured['retinal_progress'] = int(sheet.cell_value(24,6))
fbg_measured['retinal_goal'] = sheet.cell_value(24,7)
fbg_measured['retinal_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(24,8))
fbg_measured['retinal_progress_notes'] = sheet.cell_value(24,9)
fbg_measured['renal_measured'] = sheet.cell_value(25,4)
fbg_measured['renal_baseline'] = sheet.cell_value(25,5)
fbg_measured['renal_progress'] = int(sheet.cell_value(25,6))
fbg_measured['renal_goal'] = sheet.cell_value(25,7)
fbg_measured['renal_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(25,8))
fbg_measured['renal_progress_notes'] = sheet.cell_value(25,9)
fbg_measured['foot_measured'] = sheet.cell_value(26,4)
fbg_measured['foot_baseline'] = sheet.cell_value(26,5)
fbg_measured['foot_progress'] = int(sheet.cell_value(26,6))
fbg_measured['foot_goal'] = sheet.cell_value(26,7)
fbg_measured['foot_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(26,8))
fbg_measured['foot_progress_notes'] = sheet.cell_value(26,9)
# print(OrderedDict(sorted(fbg_measured.items(), key=lambda t: t[0])))

compliance = {}
compliance['meds_measured'] = sheet.cell_value(27,4)
compliance['meds_baseline'] = sheet.cell_value(27,5)
compliance['meds_progress'] = int(sheet.cell_value(27,6))
compliance['meds_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(27,8))
compliance['meds_progress_notes'] = sheet.cell_value(27,9)
compliance['diet_measured'] = sheet.cell_value(28,4)
compliance['diet_baseline'] = sheet.cell_value(28,5)
compliance['diet_progress'] = int(sheet.cell_value(28,6))
compliance['diet_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(28,8))
compliance['diet_progress_notes'] = sheet.cell_value(28,9)
compliance['exercise_measured'] = sheet.cell_value(29,4)
compliance['exercise_baseline'] = sheet.cell_value(29,5)
compliance['exercise_progress'] = int(sheet.cell_value(29,6))
compliance['exercise_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(29,8))
compliance['exercise_progress_notes'] = sheet.cell_value(29,9)
compliance['nicotine_measured'] = sheet.cell_value(30,4)
compliance['nicotine_baseline'] = sheet.cell_value(30,5)
compliance['nicotine_progress'] = int(sheet.cell_value(30,6))
compliance['nicotine_goal'] = sheet.cell_value(30,7)
compliance['nicotine_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(30,8))
compliance['nicotine_progress_notes'] = sheet.cell_value(30,9)
# print(OrderedDict(sorted(compliance.items(), key=lambda t: t[0])))



# wb = Workbook()

# # open exists
# ws = wb.active

# # Data can be directly to cells
# ws['A1'] = 42

# # Rows can also be appended
# ws.append([1, 2, 3])

# # Python types will automatically be converted
# import datetime
# ws['A2'] = datetime.datetime.now()

# # Save the file
# wb.save("sample.xlsx")