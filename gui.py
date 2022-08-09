from pathlib import Path
import queue

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Checkbutton, IntVar, StringVar, Frame, messagebox, Label

from time import sleep
import threading
import multiprocessing

import traceback
import logging

#custom libs
import workoutpusher
import browser_functions
import database_functions

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str):
    return ASSETS_PATH / Path(path)

#logger
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(asctime)s - %(funcname)s - %(message)s',
                    filename=str(OUTPUT_PATH) + '/logfile.log',
                    datefmt='%Y%m%d %H:%M:%S',
                    filemode='a')



class Application(Frame):
    def __init__(self, window, *args, **kwargs):
        Frame.__init__(self, window, *args, **kwargs)

        #catch exceptions
        #root.report_callback_exception = self.handle_exceptions
        #root.overrideredirect(1)

        #window settings
        self.window = window
        self.window.resizable(False,False)
        self.window.iconbitmap(relative_to_assets('icon.ico'))
        self.window.title("Workout Pusher")
        self.window.geometry("882x405")
        self.window.configure(bg = "#FFFFFF")

        #message queue
        self.msg_queue = queue.Queue()
        self.window.after(100, self.listen_for_message)

        #function queue
        self.func_queue = queue.Queue()

        #variables
        self.schedule_job = IntVar()
        self.icu_uname = StringVar()
        self.icu_pw = StringVar()
        self.td_uname = StringVar()
        self.td_pw = StringVar()

        self.update_text = StringVar()

        self.icu_uname.set('bmbolton@tpg.com.au')
        self.icu_pw.set('Wetexs03')

        self.td_uname.set('bmbolton@tpg.com.au')
        self.td_pw.set('Wetexs03')

        #build form
        self.build_widgets()


    def handle_exceptions(self, excp, val, tb):
        """catchall handler for unhandled exceptions, actual error is
           logged in logging file"""

        excp_msg = ''.join(traceback.format_exception(excp, val, tb))
        logging.log(excp_msg)
        messagebox.showerror(title='Error', message='An unknown error has occured. \nPlease restart the application')


    def listen_for_message(self):
        try:
            self.update_text.set(self.msg_queue.get(0))
            self.window.update_idletasks()
            self.window.after(100, self.listen_for_message)
        except queue.Empty:
            self.window.after(100, self.listen_for_message)


    def check_thread(self, thread):
        if not thread.is_alive():
            return True


    def worker(self):
        """worker function to call functions to determine whether workout
           exists on i.icu and push to TP via TD """

        browser, version = browser_functions.get_default_browser()
        if not browser_functions.check_for_driver(browser):
            if messagebox.askyesno('Driver not found', message='Webdriver not found. Would you like to download'):
                browser_functions.download_driver(browser)
                sleep(5)
                messagebox.showinfo(title='Downloaded', message='Driver downloaded. See your default download directory')
        else:
            driver = workoutpusher.get_driver()
            #spin up thread to get td link
            thread = threading.Thread(target=lambda q, drv, arg1, arg2: q.put(workoutpusher.icu_login(drv, arg1, arg2)), args=(self.func_queue, driver, self.icu_uname.get(), self.icu_pw.get()), daemon=True).start()
            thread.start()

            thread_check = False
            while not thread_check:
                thread_check = self.check_thread(thread)

            #get return from thread
            func_return = self.func_queue.get()

            if func_return:
                self.msg_queue.put('Logged into intervals.icu. Looking for workout')

                root.update()
                thread = threading.Thread(target=lambda q, drv: q.put(workoutpusher.get_workout(drv)), args=(self.func_queue, func_return), daemon=True)
                thread.start()

                thread_check = False
                while not thread_check:
                    thread_check = self.check_thread(thread)

                #get login return
                func_return, return_message = self.func_queue.get()
                self.msg_queue.put(return_message)

                if func_return:
                    thread = threading.Thread(target=lambda q, drv, arg1, arg2: q.put(workoutpusher.td_login(drv, arg1, arg2)), args=(self.func_queue, driver, self.td_uname.get(), self.td_pw.get()), daemon=True).start()

                    thread_check = False
                    while not thread_check:
                        thread_check = self.check_thread(thread)

                    func_return = self.func_queue.get()
                    if func_return:
                        self.msg_queue.put('Logged into TrainerDay. Pushing workout')
                        thread = threading.Thread(target=lambda q, drv, arg1: q.put(workoutpusher.get_workout(drv, arg1)), args=(self.func_queue, func_return, func_return), daemon=True).start()

                        thread_check = False
                        while not thread_check:
                            thread_check = self.check_thread(thread)

                        self.msg_queue.put('Workout pushed to Training Peaks')
                    else:
                        self.msg_queue.put('TrainerDay login error')
            else:
                self.msg_queue.put('intervals.icu login error')
                return


    def build_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 405,
            width = 882,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_text(
            495.0,
            59.0,
            anchor="nw",
            text="Intervals.icu",
            fill="#000000",
            font=("Rubik Bold", 15 * -1)
        )

        self.canvas.create_text(
            495.0,
            196.0,
            anchor="nw",
            text="TrainerDay",
            fill="#000000",
            font=("Rubik Bold", 15 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.worker(),
            relief="flat"
        )
        self.button_1.place(
            x=745.0,
            y=365.0,
            width=118.0,
            height=34.0
        )

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            439.0,
            202.0,
            image=self.image_image_1
        )

        self.entry_image = PhotoImage(
            file=relative_to_assets("entry.png"))
        self.entry_bg_1 = self.canvas.create_image(
            664.0,
            104.0,
            image=self.entry_image
        )
        self.entry = Entry(
            bd=0,
            bg="#F1F1F1",
            highlightthickness=0,
            textvariable=self.icu_uname,
            font=('Calibri', 14 * -1)
        )
        self.entry.place(
            x=473.0,
            y=82.0 + 15,
            width=382.0,
            height=30.0
        )

        self.entry_bg_2 = self.canvas.create_image(
            664.0,
            157.5,
            image=self.entry_image
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#F1F1F1",
            highlightthickness=0,
            show='*',
            textvariable=self.icu_pw,
            font=('Calibri', 14 * -1)
        )
        self.entry_2.place(
            x=473.0,
            y=135.0 + 15,
            width=382.0,
            height=30.0
        )

        self.canvas.create_text(
            471.0,
            87.0,
            anchor="nw",
            text="Username",
            fill="#000000",
            font=("Rubik Medium", 11 * -1)
        )

        self.canvas.create_text(
            471.0,
            139.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Rubik Medium", 11 * -1)
        )

        self.entry_bg_3 = self.canvas.create_image(
            664,
            239.0,
            image=self.entry_image
        )
        self.entry_3 = Entry(
            bd=0,
            bg="#F1F1F1",
            highlightthickness=0,
            textvariable=self.td_uname,
            font=('Calibri', 14 * -1)
        )
        self.entry_3.place(
            x=476.0,
            y=217.0 + 15,
            width=379.0,
            height=30.0
        )

        self.entry_bg_4 = self.canvas.create_image(
            665.5,
            292.0,
            image=self.entry_image
        )
        self.entry_4 = Entry(
            bd=0,
            bg="#F1F1F1",
            highlightthickness=0,
            show='*',
            textvariable=self.td_pw,
            font=('Calibri', 14 * -1)
        )
        self.entry_4.place(
            x=476.0,
            y=270.0 + 15,
            width=379.0,
            height=30.0
        )

        self.canvas.create_text(
            471.0,
            222.0,
            anchor="nw",
            text="Username",
            fill="#000000",
            font=("Rubik Medium", 11 * -1)
        )

        self.canvas.create_text(
            471.0,
            274.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Rubik Medium", 11 * -1)
        )

        self.checkbox = Checkbutton(text='Schedule', 
                               variable=self.schedule_job, 
                               bg='White', 
                               font=("Rubik Medium", 12 * -1)
                            )
        self.checkbox.place(x=474, 
                       y=370,
                       anchor="nw")

   
        self.update_label = Label(self.canvas,
                    textvariable=self.update_text,
                    font=("Roboto", 14 * -1),
                    bg='white'
        )
        self.update_label.place(relx=0.528,
                    rely=0.800,
                    anchor='nw'
                )


if __name__ == '__main__':
    #startup
    database_functions.build_tables()

    root = Tk()
    window = Application(root)
    root.mainloop()



