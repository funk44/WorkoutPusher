from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, StringVar, messagebox, Label

import queue
import time
import threading
import traceback
import logging
import platform

#custom libs
import workoutpusher.workoutpusher
import browser_functions
import database_functions
import general_functions

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

#logger
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(asctime)s - %(funcname)s - %(message)s',
                    filename=str(OUTPUT_PATH) + '/logfile.log',
                    datefmt='%Y%m%d %H:%M:%S',
                    filemode='a')


def relative_to_assets(path: str):
    return ASSETS_PATH / Path(path)


class GUI(object):
    def __init__(self, master, queue, worker_thread):
        #main message queue
        self.queue = queue

        #window settings
        self.window = master
        self.window.resizable(False,False)
        self.window.iconbitmap(relative_to_assets('icon.ico'))
        self.window.title("WorkoutPusher")
        self.window.geometry("882x405")
        self.window.configure(bg = "#FFFFFF")

        #define worker funtion for button
        self.worker_thread = worker_thread
        
        #variables
        self.icu_uname = StringVar()
        self.icu_pw = StringVar()
        self.td_uname = StringVar()
        self.td_pw = StringVar()
        self.update_text = StringVar()
        
        #place widgets on canvas
        self.build_widgets()


    def handle_exceptions(self, excp, val, tb):
        """ Catchall handler for unhandled exceptions, actual error is
           logged in logging file """

        excp_msg = ''.join(traceback.format_exception(excp, val, tb))
        logging.log(excp_msg)
        messagebox.showerror(title='Error', message='An unknown error has occured. \nPlease restart the application')


    def build_widgets(self):
        """ Build and place all widgets on tkinter window """
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
            command=lambda: self.worker_thread(),
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

        # self.checkbox = Checkbutton(text='Schedule', 
        #                     variable=self.schedule_job, 
        #                     bg='White', 
        #                     font=("Rubik Medium", 12 * -1)
        #                     )
        # self.checkbox.place(x=474, 
        #             y=370,
        #             anchor="nw")


        self.update_label = Label(self.canvas,
                    textvariable=self.update_text,
                    font=("Roboto", 14 * -1),
                    bg='white'
        )
        self.update_label.place(relx=0.535,
                    rely=0.800,
                    anchor='nw'
                )


    def process_incoming(self):
        """ Handle all messages currently in the queue, if any """
        while self.queue.qsize():
            try:
                msg = self.queue.get_nowait()
                self.update_text.set(msg)
            except queue.Empty:
                pass


class ThreadedWorker(object):
    """ Main worker thread to run all functions """
    def __init__(self, master):
        self.master = master
        
        # Create the queue
        self.queue = queue.Queue()

        # Set up the gui, pass the worker function
        self.gui = GUI(master, self.queue, self.worker_thread)

        # Start the periodic call in the GUI to check the queue
        self.periodic_call()


    def periodic_call(self):
        """ Check every 200 ms if there is something new in the queue """
        self.master.after(200, self.periodic_call)
        self.gui.process_incoming()


    def worker_thread(self):
        """ Spawns thread to run the selenium worker,
            this is required to avoid freezing the tkinter window """
        wrk_thread = threading.Thread(target=self.worker)        
        wrk_thread.start()


    def worker(self):
        """ Main worker function to call the main workout
            pusher functions  """

        settings = general_functions.read_settings(ASSETS_PATH)

        if platform.system() != 'Windows':
            messagebox.showerror(title='Windows required', message='WorkoutPusher only supports Windows currently')
            return

        #check default browser
        browser, version = browser_functions.default_brower_windows()

        #get the driver NOTE: also checks for the correct version 
        self.queue.put('Checking webdriver')
        driver = browser_functions.get_driver(OUTPUT_PATH, browser, settings, version)
        
        #if string is returned there is an error with the webdriver and prompt user
        if isinstance(driver, str):
            if driver == 'No driver':
                title = 'No driver found'
                message = 'Webdriver not found, would you like to download?'
            else:
                title = 'Incorrect driver'
                message = 'Incorrect driver found, would you like to download the correct version?'
            if messagebox.askyesno(title=title, message=message):
                self.queue.put('Downloading driver')
                browser_functions.download_driver(settings, browser, version)
                time.sleep(5)
                self.queue.put('Downloaded. Check your default download directory')
                return
            else:
                self.queue.put('Webdriver error')
        else:
            #get the passwords and clear the password variables
            icu_pw = self.gui.icu_pw.get()
            td_pw = self.gui.td_pw.get()

            # self.gui.icu_pw.set('')
            # self.gui.td_pw.set('')

            #login to i.icu
            self.queue.put('Logging into Intervals.icu')
            driver = workoutpusher.icu_login(driver, self.gui.icu_uname.get(), icu_pw)

            #if login successful find the td workout in i.icu
            if driver:
                self.queue.put('Logged into Intervals.icu. Looking for workout')
                
                #get todays worker
                td_link, return_message = workoutpusher.get_workout(driver)
                self.queue.put(return_message)
                
                #if workout found login to TD and push workout to TP
                if td_link:
                    driver = workoutpusher.td_login(driver, self.gui.td_uname.get(), td_pw)
                    if driver:
                        self.queue.put('Logged into TrainerDay. Pushing workout')
                        workoutpusher.push_workout(driver, td_link)
                        self.queue.put('Workout pushed to Training Peaks')
                    else:
                        self.queue.put('TrainerDay login error')
                        return
            else:
                self.queue.put('Intervals.icu login error')
                return


if __name__ == '__main__':
    #build sqlite database on startup
    database_functions.build_tables()

    root = Tk()
    client = ThreadedWorker(root)
    root.mainloop()