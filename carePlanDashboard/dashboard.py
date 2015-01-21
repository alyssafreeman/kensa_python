from time import sleep
import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import *

# source_directory_path = ''

def select_source_dir():
	dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
	if dirname:
		source_directory_path.set(dirname)
	print('source dir',source_directory_path.get())

def select_output_dir():
	dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
	if dirname:
		output_directory_path.set(dirname)
	print('output dir=',output_directory_path.get())

def update_progress_bar(*args):
	print("yay: ",source_directory_path.get())

def start_file_process():
	progress.step()
	# for step in range(1,100):
	# 	sleep(.5)
	# 	progress["value"] = step

def close_window():
	root.destroy()

root = Tk()
source_directory_path = StringVar()
source_directory_path.trace("w", update_progress_bar)
output_directory_path = StringVar()
output_directory_path.trace("w", update_progress_bar)
output_file_name = StringVar()
percent_complete = IntVar()

root.title('Care Plan Dashboard')
mainframe = ttk.Frame(root, padding="15 10 15 10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
current_row = 1
#---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe,orient=HORIZONTAL).grid(row=current_row, columnspan=20); current_row += 1
ttk.Label(mainframe, text='').grid(column=0, row=current_row); current_row += 1
#---------------------------------------------space---------------------------------------------
#----------------------------------------Source Directory---------------------------------------
ttk.Label(mainframe, text='Source Directory').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, textvariable=source_directory_path).grid(column=3, row=current_row, columnspan=10)
ttk.Button(mainframe, text='Browse', command=select_source_dir).grid(column=20, row=current_row); current_row += 1
#----------------------------------------Source Directory---------------------------------------
#-------------------------------------Destination Directory-------------------------------------
ttk.Label(mainframe, text='Output Directory').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, textvariable=output_directory_path).grid(column=3, row=current_row, columnspan=10)
ttk.Button(mainframe, text='Browse', command=select_output_dir).grid(column=20, row=current_row); current_row += 1
#-------------------------------------Destination Directory-------------------------------------
#-------------------------------------Destination File Name-------------------------------------
ttk.Label(mainframe, text='Output File Name').grid(column=0, row=current_row, sticky=W)
ttk.Entry(mainframe, textvariable=output_file_name).grid(column=3, row=current_row, columnspan=15)
#-------------------------------------Destination File Name-------------------------------------
#---------------------------------------------space---------------------------------------------
ttk.Separator(mainframe,orient=HORIZONTAL).grid(row=current_row, columnspan=10); current_row += 1
ttk.Label(mainframe, text='').grid(column=0, row=current_row); current_row += 1
#---------------------------------------------space---------------------------------------------
#-------------------------------------------Button Row------------------------------------------
ttk.Button(mainframe, text='Quit', command=close_window).grid(column=0, row=current_row, sticky=W)
ttk.Button(mainframe, text='Start', command=start_file_process).grid(column=20, row=current_row, sticky=E); current_row += 1
#-------------------------------------------Button Row------------------------------------------
progress = ttk.Progressbar(root, orient='horizontal', mode='determinate',maximum=100,value=0).grid(column=0, row=current_row, sticky=(W,E))
root.mainloop()
root.destroy()