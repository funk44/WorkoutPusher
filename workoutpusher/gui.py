from pathlib import Path
from tkinter import Tk, StringVar, messagebox

import queue
import time
import threading
import traceback
import logging
import platform

#custom libs
import workoutpusher
import browser_functions
import database_functions
import build_widgets

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
        build_widgets.place_widgets()


    def handle_exceptions(self, excp, val, tb):
        """ Catchall handler for unhandled exceptions, actual error is
           logged in logging file """

        excp_msg = ''.join(traceback.format_exception(excp, val, tb))
        logging.log(excp_msg)
        messagebox.showerror(title='Error', message='An unknown error has occured. \nPlease restart the application')


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

        if platform.system() != 'Windows':
            messagebox.showerror(title='Windows required', message='WorkoutPusher only supports Windows currently')
            return

        if not self.gui.icu_uname.get() or not self.gui.icu_pw.get() or not self.gui.td_uname.get() or not self.gui.td_uname.get():
            self.queue.put('Missing username and/or password')
            return

        #check default browser
        browser = browser_functions.default_brower_windows()

        #get the driver NOTE: also checks for the correct version 
        self.queue.put('Starting webdriver')
        driver = browser_functions.get_driver(browser)
        
        #if string is returned there is an error with the webdriver and prompt user
        if isinstance(driver, str):
            self.queue.put('Webdriver error')
            return
        else:
            #get the passwords and clear the password variables
            icu_pw = self.gui.icu_pw.get()
            td_pw = self.gui.td_pw.get()

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