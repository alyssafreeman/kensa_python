#!/usr/bin/python

import os, sys, xlwt, xlrd			# pip3 install xlwt-future (for python3)
import datetime
from array import *
from openpyxl import Workbook

def convert_float_to_date(date):
	serial = sheet.cell_value(0,10)
	seconds = (serial - 25569) * 86400.0
	date = datetime.datetime.utcfromtimestamp(seconds)
	return date.strftime('%m/%d/%y')

def convert_x_to_boolean(x):
	if x == 'X':
		return True
	else: 
		return False

# Open a file
path = "/Users/alyssafreeman/Desktop/cody/carePlanDashboard/patientFiles/"
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
# print(patient)

visit = {}
visit['visit_date'] = convert_float_to_date(sheet.cell_value(0,1))
visit['next_appt_date'] = convert_float_to_date(sheet.cell_value(0,10))
visit['pcp_name'] = sheet.cell_value(4,1) + ' ' + sheet.cell_value(4,2)
visit['case_status'] = sheet.cell_value(6,1)
visit['health_risk_assessment'] = sheet.cell_value(6,4)
visit['biometrics'] = sheet.cell_value(6,7)
visit['coach_initials'] = sheet.cell_value(6,10)
visit['comments'] = sheet.cell_value(8,1)
# print(visit)

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
# print(diagnosis)

weight_management = {}
weight_management['height_measured'] = int(sheet.cell_value(12,4))
weight_management['height_baseline'] = int(sheet.cell_value(12,5))
weight_management['waist_measured'] = int(sheet.cell_value(13,4))
weight_management['waist_baseline'] = int(sheet.cell_value(13,5))
weight_management['waist_progress'] = int(sheet.cell_value(13,6))
weight_management['waist_goal'] = int(sheet.cell_value(13,7))
weight_management['waist_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(13,8))
weight_management['waist_progress_notes'] = sheet.cell_value(13,9)
weight_management['weight_measured'] = int(sheet.cell_value(14,4))
weight_management['weight_baseline'] = int(sheet.cell_value(14,5))
weight_management['weight_progress'] = int(sheet.cell_value(14,6))
weight_management['weight_goal'] = int(sheet.cell_value(14,7))
weight_management['weight_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(14,8))
weight_management['weight_progress_notes'] = sheet.cell_value(14,9)
weight_management['bmi_measured'] = int(sheet.cell_value(15,4))
weight_management['bmi_baseline'] = int(sheet.cell_value(15,5))
weight_management['bmi_progress'] = int(sheet.cell_value(15,6))
weight_management['bmi_date_goal_achieved'] = convert_float_to_date(sheet.cell_value(15,8))
weight_management['bmi_progress_notes'] = sheet.cell_value(15,9)
print(weight_management)

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