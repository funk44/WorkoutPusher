from pathlib import Path
import queue

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Checkbutton, IntVar, StringVar, Frame, messagebox, BOTH

from queue import Queue
from time import sleep
import threading

import traceback
import logging
import os
import sys
import webbrowser

#custom libs
from workoutpusher import wp_worker
import browser_functions

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


#logger
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(asctime)s - %(funcname)s - %(message)s',
                    filename=str(OUTPUT_PATH) + '/logfile.log',
                    datefmt='%Y%m%d %H:%M:%S',
                    filemode='a')


def submit():
    y2 = Frame(borderwidth=5)
    y2.place(x=400, y=150, width=200, height=100)
    #y3 = Label(y2, text="Registration Done!!", width=30, height=12, font=("bold", 22), anchor='center')
    #y3.pack()
    Button(y2, text='Return', width=20, bg="black", fg='white', command=None)



class Application(Frame):
    def __init__(self, parent, disable=None, releasecmd=None):
        self.parent = parent
        self.root = parent.winfo_toplevel()
        
        self.disable = disable
        if type(disable) == 'str':
            self.disable = disable.lower()

        self.releaseCMD = releasecmd

        self.parent.bind('<Button-1>', self.relative_position)
        self.parent.bind('<ButtonRelease-1>', self.drag_unbind)

        #message queue
        self.thread_queue = queue.Queue()
        #self.window.after(100, self.listen_for_result)

        #variables
        self.schedule_job = IntVar()
        self.icu_uname = StringVar()
        self.icu_pw = StringVar()
        self.td_uname = StringVar
        self.td_pw = StringVar()

        self.temp_msg = None

        #build form
        self.build_widgets()


    def relative_position (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.parent.bind('<Motion>', self.drag_wid)

    def drag_wid (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        d = self.disable
        x = cx - self.relX
        y = cy - self.relY
        if d == 'x' :
            x = self.oriX
        elif d == 'y' :
            y = self.oriY
        self.root.geometry('+%i+%i' % (x, y))

    def drag_unbind (self, event) :
        self.parent.unbind('<Motion>')
        if self.releaseCMD != None :
            self.releaseCMD()


    def listen_for_result(self):
        pass


    def handle_exceptions(self, excp, val, tb):
        excp_msg = ''.join(traceback.format_exception(excp, val, tb))
        logging.log(excp_msg)
        messagebox.showerror(title='Error', message='An unknown error has occured. \nPlease restart the application')

    
    def worker(self):
        browser, version = browser_functions.get_default_browser()
        if not browser_functions.check_for_driver(browser):
            if messagebox.askyesno('Driver not found', message='Webdriver not found. Would you like to download'):
                browser_functions.download_driver(browser)
                messagebox.showinfo(title='Downloaded', message='Driver downloaded. See your default download directory')
        else:
            pass



        
    def build_widgets(self):
        self.canvas = Canvas(
            self.parent,
            bg = "#FFFFFF",
            height = 405,
            width = 882,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_text(
            491.0,
            59.0,
            anchor="nw",
            text="Intervals.icu",
            fill="#000000",
            font=("Rubik Bold", 15 * -1)
        )

        self.canvas.create_text(
            491.0,
            217.0,
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
            command=lambda: submit(),
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
            110.0,
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
            y=82.0 + 23,
            width=382.0,
            height=34.0
        )

        self.entry_bg_2 = self.canvas.create_image(
            664.0,
            175.0,
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
            y=147.0 + 23,
            width=382.0,
            height=34.0
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
            151.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Rubik Medium", 11 * -1)
        )

        self.entry_bg_3 = self.canvas.create_image(
            665.5,
            266.0,
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
            y=238.0 + 23,
            width=379.0,
            height=34.0
        )

        self.entry_bg_4 = self.canvas.create_image(
            665.5,
            331.0,
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
            y=303.0 + 23,
            width=379.0,
            height=34.0
        )

        self.canvas.create_text(
            474.0,
            243.0,
            anchor="nw",
            text="Username",
            fill="#000000",
            font=("Rubik Medium", 11 * -1)
        )

        self.canvas.create_text(
            474.0,
            307.0,
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


def main():
    root = Tk()
    root.resizable(False,False)
    root.iconbitmap(relative_to_assets('icon.ico'))
    root.title("Workout Pusher")
    root.geometry("882x405")
    root.configure(bg = "#FFFFFF")
    root.overrideredirect(1)

    back = Frame(root, bg="white")
    back.pack_propagate(0)
    back.pack(fill=BOTH, expand=1)

    top_Frame = Frame(back, bg="white")
    top_Frame.place(x=0, y=0, anchor="nw", width=882, height=10)

    grip = Application(top_Frame)
    root.mainloop()



main()

