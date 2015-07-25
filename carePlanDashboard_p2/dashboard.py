import sys
import collections
from datetime import datetime
from Tkinter import Tk
import ttk
import tkMessageBox
import tkFileDialog
from Tkinter import *
from ttk import Progressbar
from dashboard_py.create_dashboard import CreateDashboard
from dashboard_py.parse_patient_files import ParsePatientFiles
from dashboard_py.database_manager import DatabaseManager

def select_source_dir():
    dirname = tkFileDialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
    if dirname:
        source_directory_path.set(dirname)
    print('source dir', source_directory_path.get())

def select_output_dir():
    dirname = tkFileDialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
    if dirname:
        output_directory_path.set(dirname)
    print('output dir=', output_directory_path.get())

def validate(inp):
    global last_ok_value
    try:
        str(inp)
    except ValueError:
        return False

    last_ok_value = inp
    return True

def invalidate():
    text.set(last_ok_value)

def update_progress_bar(value):
    global progress
    progress["value"] = value
    progress.update()

def update_progress_text(text, row_val):
    ttk.Label(mainframe, text=text).grid(column=0, row=row_val, sticky=W, columnspan=30)

def do_task():
    time.sleep(1)

def start_file_process(*args):
    fields = collections.OrderedDict(( ('Source Directory', source_directory_path.get()),
                                       ('Output Directory', output_directory_path.get()),
                                       ('Dashboard File Name', output_file_name.get()),
                                       ('Start date', start_date.get()),
                                       ('End date', end_date.get())))
    validate = validate_entry_boxes(fields)

    if validate == []:
        dashboardButton.state(["disabled"])   # Disable the button.

        startDate = start_date.get()
        endDate = end_date.get()

        update_progress_bar(20)

        processor = ParsePatientFiles()
        file_process, db_path = processor.process_files(source_directory_path.get(), startDate, endDate)

        if file_process:
            print(db_path)
            dm = DatabaseManager(db_path)
            cd = CreateDashboard()

            print("output_file_name: " + output_file_name.get())
            print("output_directory_path: " + output_directory_path.get())

            output_dir = cd.copy_template_to_output_dir(output_directory_path.get(), output_file_name.get(), "dashboard_template.xlsx")

            update_progress_bar(40)
            diagnosis_stats = dm.get_diagnosis_stats(startDate, endDate)

            update_progress_bar(60)
            cd.write_diagnosis_stats_to_xlsx(diagnosis_stats, output_dir)

            update_progress_bar(80)
            progress_stats = dm.get_progress_stats(startDate, endDate)

            cd.write_progress_stats_to_xlsx(progress_stats, output_dir)
            update_progress_bar(100)
            tkMessageBox.showinfo(message='Dashboard created:\n' + output_dir)

            dashboardButton.state(["!disabled"])
        else:
            tkMessageBox.showinfo(message='\nError uploading patient files')
    else:
        tkMessageBox.showinfo(message='\nPlease fill in or correct the following field(s):\n\n' + '\n'.join(map(str, validate)))

def process_incentive_program():
    fields = collections.OrderedDict(( ('Source Directory', source_directory_path.get()),
                                       ('Output Directory', output_directory_path.get()),
                                       ('Incentive Dashboard File Name', output_incentive_file_name.get()),
                                       ('Start date', start_date.get()),
                                       ('End date', end_date.get())))
    validate = validate_entry_boxes(fields)

    if validate == []:
        incentiveButton.state(["disabled"])   # Disable the button.

        startDate = start_date.get()
        endDate = end_date.get()

        update_progress_bar(0)
        update_progress_bar(25)

        dm = DatabaseManager()
        cd = CreateDashboard()

        output_dir = cd.copy_template_to_output_dir(output_directory_path.get(), output_incentive_file_name.get(), 'incentive_template.xlsx')

        update_progress_bar(50)
        incentive_stats = dm.get_incentive_program_stats(startDate, endDate)

        update_progress_bar(75)
        cd.write_incentive_program_stats_to_xlsx(incentive_stats, output_dir)
        update_progress_bar(100)

        tkMessageBox.showinfo(message='Incentive Program dashboard created:\n' + output_dir)
        incentiveButton.state(["!disabled"])
    else:
        tkMessageBox.showinfo(message='\nPlease fill in or correct the following field(s):\n\n' + '\n'.join(map(str, validate)))

def validate_entry_boxes(fields):
    invalid = list()
    for field, value in fields.items():
        if len(value) == 0:
            invalid.append(field)
        else:
            if 'date' in field:
                valid_date = validate_date(field, value)
                if valid_date:
                    invalid.append(valid_date)
    if len(invalid) > 0:
        return invalid
    else:
        return []

def validate_date(field, date_text):
    try:
        datetime.strptime(date_text, '%m/%d/%y')
        return False
    except ValueError:
        message = "Incorrect format for " + field + ". Should match format mm/dd/yy."
        return message

def close_window():
    root.destroy()

root = Tk()
source_directory_path = StringVar()
output_directory_path = StringVar()
output_file_name = StringVar()
output_incentive_file_name = StringVar()
percent_complete = IntVar()
start_date = StringVar()
end_date = StringVar()
progress_text = StringVar()

root.title('Care Plan Dashboard')
mainframe = ttk.Frame(root, padding="15 10 15 10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
current_row = 1

text = StringVar()
last_ok_value = text.get()
vcmd = mainframe.register(validate)
ivcmd = mainframe.register(invalidate)

#-------------------------------------------Quit Button------------------------------------------
ttk.Button(mainframe, text='Quit', command=close_window).grid(column=0, row=current_row, sticky=W); current_row += 1
#-------------------------------------------Quit Button------------------------------------------

#---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe, orient=HORIZONTAL).grid(row=current_row, columnspan=30); current_row += 1
ttk.Label(mainframe, text='').grid(column=0, row=current_row); current_row += 1
#---------------------------------------------space---------------------------------------------

#----------------------------------------Source Directory---------------------------------------
ttk.Label(mainframe, text='Source Directory').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, textvariable=source_directory_path, width=50, validate='all', validatecommand=(vcmd, '%P'), invalidcommand=(ivcmd,)).grid(column=1, row=current_row, sticky=W)
# ttk.Entry(mainframe, textvariable=source_directory_path, width=50, validate='focusout', validatecommand=(vcmd, '%P')).grid(column=1, row=current_row, sticky=W)
ttk.Button(mainframe, text='Browse', command=select_source_dir).grid(column=40, row=current_row, sticky=W); current_row += 1
#----------------------------------------Source Directory---------------------------------------

#-------------------------------------Destination Directory-------------------------------------
ttk.Label(mainframe, text='Output Directory').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, textvariable=output_directory_path, width=50).grid(column=1, row=current_row, sticky=W)
ttk.Button(mainframe, text='Browse', command=select_output_dir).grid(column=40, row=current_row, sticky=W); current_row += 1
#-------------------------------------Destination Directory-------------------------------------

#-------------------------------------Destination File Name-------------------------------------
ttk.Label(mainframe, text='Dashboard File Name').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, textvariable=output_file_name, width=50).grid(column=1, row=current_row, sticky=W)
ttk.Label(mainframe, text='.xlsx').grid(column=40, row=current_row, sticky=W); current_row += 1
#-------------------------------------Destination File Name-------------------------------------

#---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe, orient=HORIZONTAL).grid(row=current_row, columnspan=40); current_row += 1
ttk.Label(mainframe, text='').grid(column=0, row=current_row); current_row += 1
#---------------------------------------------space---------------------------------------------

#--------------------------------------------Start & End Date---------------------------------------------
ttk.Label(mainframe, text='mm/dd/yy  (example: 01/01/15)').grid(column=1, row=current_row, sticky=W); current_row += 1

ttk.Label(mainframe, text='Start date:').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, width=15, textvariable=start_date).grid(column=1, row=current_row, sticky=W); current_row += 1

ttk.Label(mainframe, text='End date:').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, width=15, textvariable=end_date).grid(column=1, row=current_row, sticky=W)
#--------------------------------------------Start & End Date---------------------------------------------

#---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe, orient=HORIZONTAL).grid(row=current_row, columnspan=40); current_row += 1
#---------------------------------------------space---------------------------------------------

#-------------------------------------------Start Button------------------------------------------
dashboardButton = ttk.Button(mainframe, text='Create Dashboard', command=start_file_process)
dashboardButton.grid(column=40, row=current_row, sticky=E+W); current_row += 1
#-------------------------------------------Start Button------------------------------------------

#-------------------------------------------Status Bar------------------------------------------
progress = Progressbar(root, orient='horizontal', maximum=100, value=0); current_row += 1
progress.grid(row=current_row, column=0, padx=2, pady=0, sticky=W+E); current_row += 1
#-------------------------------------------Status Bar------------------------------------------

# ---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe, orient=HORIZONTAL).grid(row=current_row, columnspan=40); current_row += 1
ttk.Label(mainframe, text='').grid(column=0, row=current_row)
#---------------------------------------------space---------------------------------------------
# ---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe, orient=HORIZONTAL).grid(row=current_row, columnspan=40); current_row += 1
ttk.Label(mainframe, text='').grid(column=0, row=current_row)
#---------------------------------------------space---------------------------------------------

#-------------------------------------Destination File Name-------------------------------------
ttk.Label(mainframe, text='Results Based Incentive Program:').grid(column=0, row=current_row, sticky=E); current_row += 1
ttk.Label(mainframe, text='Incentive Dashboard File Name').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, textvariable=output_incentive_file_name, width=50).grid(column=1, row=current_row, sticky=W)
ttk.Label(mainframe, text='.xlsx').grid(column=40, row=current_row, sticky=W); current_row += 1
#-------------------------------------Destination File Name-------------------------------------

#---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe, orient=HORIZONTAL).grid(row=current_row, columnspan=40)
#---------------------------------------------space---------------------------------------------

#-------------------------------------------Start Button------------------------------------------
incentiveButton = ttk.Button(mainframe, text='Create Incentive Based Dashboard', command=process_incentive_program)
incentiveButton.grid(column=40, row=current_row, sticky=E+W); current_row += 1
#-------------------------------------------Start Button------------------------------------------

root.bind('<Return>', start_file_process)
root.mainloop()
# root.destroy()