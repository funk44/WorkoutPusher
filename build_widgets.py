from tkinter import Tk, Canvas, Entry, Button, PhotoImage, StringVar, messagebox, Label
from pathlib import Path

from .workoutpusher.gui import GUI

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str):
    return ASSETS_PATH / Path(path)


def place_widgets():
    gui = GUI()

    """ Build and place all widgets on tkinter window """
    canvas = Canvas(
        gui.window,
        bg = "#FFFFFF",
        height = 405,
        width = 882,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_text(
        495.0,
        59.0,
        anchor="nw",
        text="Intervals.icu",
        fill="#000000",
        font=("Rubik Bold", 15 * -1)
    )

    canvas.create_text(
        495.0,
        196.0,
        anchor="nw",
        text="TrainerDay",
        fill="#000000",
        font=("Rubik Bold", 15 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: gui.worker_thread(),
        relief="flat"
    )
    button_1.place(
        x=745.0,
        y=365.0,
        width=118.0,
        height=34.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        439.0,
        202.0,
        image=image_image_1
    )

    entry_image = PhotoImage(
        file=relative_to_assets("entry.png"))
    entry_bg_1 = canvas.create_image(
        664.0,
        104.0,
        image=entry_image
    )
    entry = Entry(
        bd=0,
        bg="#F1F1F1",
        highlightthickness=0,
        textvariable=gui.icu_uname,
        font=('Calibri', 14 * -1)
    )
    entry.place(
        x=473.0,
        y=82.0 + 15,
        width=382.0,
        height=30.0
    )

    entry_bg_2 = canvas.create_image(
        664.0,
        157.5,
        image=entry_image
    )
    entry_2 = Entry(
        bd=0,
        bg="#F1F1F1",
        highlightthickness=0,
        show='*',
        textvariable=gui.icu_pw,
        font=('Calibri', 14 * -1)
    )
    entry_2.place(
        x=473.0,
        y=135.0 + 15,
        width=382.0,
        height=30.0
    )

    canvas.create_text(
        471.0,
        87.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Rubik Medium", 11 * -1)
    )

    canvas.create_text(
        471.0,
        139.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Rubik Medium", 11 * -1)
    )

    entry_bg_3 = canvas.create_image(
        664,
        239.0,
        image=entry_image
    )
    entry_3 = Entry(
        bd=0,
        bg="#F1F1F1",
        highlightthickness=0,
        textvariable=gui.td_uname,
        font=('Calibri', 14 * -1)
    )
    entry_3.place(
        x=476.0,
        y=217.0 + 15,
        width=379.0,
        height=30.0
    )

    entry_bg_4 = canvas.create_image(
        665.5,
        292.0,
        image=entry_image
    )
    entry_4 = Entry(
        bd=0,
        bg="#F1F1F1",
        highlightthickness=0,
        show='*',
        textvariable=gui.td_pw,
        font=('Calibri', 14 * -1)
    )
    entry_4.place(
        x=476.0,
        y=270.0 + 15,
        width=379.0,
        height=30.0
    )

    canvas.create_text(
        471.0,
        222.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Rubik Medium", 11 * -1)
    )

    canvas.create_text(
        471.0,
        274.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Rubik Medium", 11 * -1)
    )

    # checkbox = Checkbutton(text='Schedule', 
    #                     variable=schedule_job, 
    #                     bg='White', 
    #                     font=("Rubik Medium", 12 * -1)
    #                     )
    # checkbox.place(x=474, 
    #             y=370,
    #             anchor="nw")


    update_label = Label(canvas,
                textvariable=gui.update_text,
                font=("Roboto", 14 * -1),
                bg='white'
    )
    update_label.place(relx=0.535,
                rely=0.800,
                anchor='nw'
            )