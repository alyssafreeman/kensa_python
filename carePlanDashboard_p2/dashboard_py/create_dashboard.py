#!/usr/bin/python
import pdb
import os
from openpyxl import load_workbook
from array import *
import shutil


class CreateDashboard:

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    ########################################################################################################################
    def copy_template_to_output_dir(self, output_dir, output_fn, template):
        template_path = os.path.join(self.base_dir,  '..', 'data', template)
        output_path = output_dir + '/' + output_fn + '.xlsx'

        print("template_path: " + template_path)
        print("output_path: " + output_path)

        shutil.copy2(template_path, output_path)
        if os.path.isfile(output_path):
            print("Success")
        return output_path

    def write_diagnosis_stats_to_xlsx(self, stats, output_path):
        wb = load_workbook(output_path, guess_types=True)
        ws = wb.get_active_sheet()

        for col, hash in stats.items():
            for key, value in hash.items():
                ws.cell(value['cell']).value = value['value']
        wb.save(output_path)

    def write_progress_stats_to_xlsx(self, stats, output_path):
        wb = load_workbook(output_path, guess_types=True)
        ws = wb.get_active_sheet()

        for diagnosis, d_hash in stats.items():
            for col, hash in d_hash.items():
                for key, value in hash.items():
                    ws.cell(value['cell']).value = value['value']
        wb.save(output_path)

    def write_incentive_program_stats_to_xlsx(self, stats, output_path):
        wb = load_workbook(output_path, guess_types=True)
        ws = wb.get_active_sheet()
        for col, hash in stats.items():
            for key, value in hash.items():
                ws.cell(value['cell']).value = value['value']
        wb.save(output_path)
    ########################################################################################################################