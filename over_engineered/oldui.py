import sys
from subprocess import Popen
from tkinter import *
from tkinter import ttk
 
START, STOP = "start", "stop"
 
# just some arbitrary command for demonstration
cmd = [sys.executable, '-c', """import sys, time
print("!")
sys.stdout.flush()
for i in range(30):
    sys.stdout.write("%d " % i)
    sys.stdout.flush()
    time.sleep(.05)
"""]
 
 
class App(object):
    def __init__(self, parent):
        self.process = None
        self.after = parent.after
        self.command = START
        self.button_text = None
        self.progressbar = None
        self.make_widgets(parent)
 
    def make_widgets(self, parent):
        parent = ttk.Frame(root, padding="15 10 15 10")
        parent.grid(column=0, row=0, sticky=(N, W, E, S))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.pack()
        current_row = 1
        
        ttk.Separator(parent,orient=HORIZONTAL).grid(row=current_row, columnspan=20); current_row += 1
        # ttk.Label(parent, text='').grid(column=0, row=current_row); current_row += 1

        source_directory_path = StringVar()
        # source_directory_path.trace("w", update_progress_bar)
        output_directory_path = StringVar()
        # output_directory_path.trace("w", update_progress_bar)
        output_file_name = StringVar()
        percent_complete = IntVar()

        # ttk.Label(parent, text='Source Directory').grid(column=0, row=current_row, sticky=W)
        # ttk.Entry(parent, textvariable=source_directory_path).grid(column=3, row=current_row, columnspan=10)
        # ttk.Button(parent, text='Browse', command=select_source_dir).grid(column=20, row=current_row); current_row += 1

        self.progressbar = ttk.Progressbar(parent, length=200,
                                           mode='indeterminate')
        self.progressbar.pack()
        self.button_text = StringVar()
        self.button_text.set(self.command)
        button = ttk.Button(parent, textvariable=self.button_text,
                            command=self.toggle)
        button.pack()
        button.focus()
 
    def toggle(self, event_unused=None):
        if self.command is START:
            self.progressbar.start()
            try:
                self.start_process()
            except:
                self.progressbar.stop()
                raise
            self.command = STOP
            self.button_text.set(self.command)
        else:
            assert self.command is STOP
            self.stop_process()
 
    def stop(self):
        self.progressbar.stop()
        self.command = START
        self.button_text.set(self.command)
 
    def start_process(self):
        self.stop_process()
        self.process = Popen(cmd)
 
        def poller():
            if self.process is not None and self.process.poll() is None:
                # process is still running
                self.after(delay, poller)  # continue polling
            else:
                self.stop()
        delay = 100  # milliseconds
        self.after(delay, poller)
 
    def stop_process(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            # kill process in a couple of seconds if it is not terminated
            self.after(2000, kill_process, self.process)
        self.process = None
 
 
def kill_process(process):
    if process is not None and process.poll() is None:
        process.kill()
        process.wait()
 
 
if __name__ == "__main__":
    root = Tk()
    app = App(root)
 
    def shutdown():
        app.stop_process()
        root.destroy()
 
    root.protocol("WM_DELETE_WINDOW", shutdown)
    root.bind('<Return>', app.toggle)
    root.mainloop()