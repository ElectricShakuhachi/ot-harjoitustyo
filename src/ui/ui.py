from tkinter import *
from entities.music import *
from entities.buttons import *
from ui.messages import *
from pathlib import Path
import os

class UI:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x1000")
        self.generate_frames()
        self.create_sheet()
        self.music = Music()
        self.buttons = Buttons(self, "Tozan")
        self.textboxes = {}
        self.textboxbuttons = {} #move this to Buttons class later
        self.create_text_boxes()
        self.note_pngs = self.load_pngs()
        self.name = ""
        self.composer = ""
        self.messages = []
        self.temp_dot = None

    def generate_frames(self):
        self.frame = Frame(self.window)
        self.frame.pack()
        self.top_frame1 = Frame(self.window)
        self.top_frame1.pack(side=TOP)
        self.top_frame2 = Frame(self.window)
        self.top_frame2.pack(side=TOP)
        self.left_frame = Frame(self.window, padx=20)
        self.left_frame.pack(side=LEFT)
        self.right_frame = Frame(self.window)
        self.right_frame.pack(side=RIGHT, padx=20)

    def create_sheet(self):
        self.sheet = Canvas(
            self.left_frame,
            width=630,
            height=891,
            background="white",
        )
        self.sheet.pack(side = LEFT)
        self.sheet.create_line(542, 70, 542, 840, fill="black", width=1)
        self.sheet.create_line(482, 70, 482, 840, fill="black", width=1)
        self.sheet.create_line(422, 70, 422, 840, fill="black", width=1)
        self.sheet.create_line(362, 70, 362, 840, fill="black", width=1)
        self.sheet.create_line(302, 70, 302, 840, fill="black", width=1)
        self.sheet.create_line(242, 70, 242, 840, fill="black", width=1)
        self.sheet.create_line(182, 70, 182, 840, fill="black", width=1)
        self.sheet.create_line(122, 70, 122, 840, fill="black", width=1)
        self.sheet.create_line(62, 70, 62, 840, fill="black", width=1)

        self.sheet.create_line(542, 70, 62, 70, fill="black", width=1)
        self.sheet.create_line(542, 180, 62, 180, fill="black", width=1)
        self.sheet.create_line(542, 290, 62, 290, fill="black", width=1)
        self.sheet.create_line(542, 400, 62, 400, fill="black", width=1)
        self.sheet.create_line(542, 510, 62, 510, fill="black", width=1)
        self.sheet.create_line(542, 620, 62, 620, fill="black", width=1)
        self.sheet.create_line(542, 730, 62, 730, fill="black", width=1)
        self.sheet.create_line(542, 840, 62, 840, fill="black", width=1)

    def load_pngs(self):
        dirname = Path(__file__)
        self.pngs = {}
        for notebutton in self.buttons.notebuttons:
            self.pngs[notebutton.text] = PhotoImage(file=os.path.join(dirname.parent.parent, "./graphics/" + notebutton.text + ".png"))

    def draw_all_notes(self):
        for note in self.music.notes:
            self.sheet.create_image(note.position[0], note.position[1], anchor=NW, image=self.pngs[note.text])

    def draw_time_notation(self, note):#REFACTOR -> too much repetition, basically jammed through in this form for now -> consider if this is a job for the UI to handle by itself?
        if note.lenght > 8:
            return
        self.sheet.create_line(note.position[0] + 15, note.position[1], note.position[0] + 15, note.position[1] + 10, fill="black", width=2)
        if note.lenght == 8:
            return
        if len(self.music.notes) > 1 and self.music.notes[-2].lenght < 8 and self.music.measure_counter != self.music.notes[-1].lenght:
            self.sheet.create_line(note.position[0] + 15, self.music.notes[-2].position[1], note.position[0] + 15, note.position[1] + 10, fill="black", width=2)
            if self.music.notes[-1].lenght == 4 and self.temp_dot:
                self.sheet.delete(self.temp_dot)
        if note.lenght == 4:
            if len(self.music.notes) < 2 or self.music.measure_counter == self.music.notes[-1].lenght or self.music.notes[-2].lenght > 4:
                self.temp_dot = self.sheet.create_line(note.position[0] + 12, note.position[1] + 4, note.position[0] + 18, note.position[1] + 8, fill="black", width=2)
            return
        self.sheet.create_line(note.position[0] + 20, note.position[1], note.position[0] + 20, note.position[1] + 10, fill="black", width=2)
        if len(self.music.notes) > 1 and self.music.notes[-2].lenght < 3 and self.music.measure_counter != self.music.notes[-1].lenght:
            self.sheet.create_line(note.position[0] + 20, note.position[1] - 10, note.position[0] + 20, note.position[1] + 10, fill="black", width=2)
        if note.lenght == 1: #note specific case
            self.sheet.create_line(note.position[0] + 13, note.position[1] + 5, note.position[0] + 23, note.position[1] + 7, fill="black", width=2)

    def add_note(self, note: Note, text: str):
        status = self.music.add_note(note)
        if status == "full":
            self.messages.append(ShakuMessage("Full Sheet"))
        else:
            self.sheet.create_image(note.position[0], note.position[1], anchor=NW, image=self.pngs[note.text])    
            self.draw_time_notation(note)

    def draw_texts(self):
        self.erase_texts()
        self.name = self.sheet.create_text(20, 20, text=self.music.name, fill="black", anchor=NW, font=("Helvetica 16"))
        self.composer = self.sheet.create_text(600, 20, text=self.music.composer, fill="black", anchor=NE, font=("Helvetica 16"))

    def erase_texts(self):
        if self.name != "":
            self.sheet.delete(self.name)
        if self.composer != "":
            self.sheet.delete(self.composer)

    def add_name(self):
        name = self.textboxes["musicname"].get()
        self.music.name = name
        self.draw_texts()

    def add_composer(self):
        composer = self.textboxes["composername"].get()
        self.music.composer = composer
        self.draw_texts()

    def create_text_boxes(self):
        self.textboxes["musicname"] = (Entry(self.top_frame1))
        self.textboxes["composername"] = (Entry(self.top_frame2))
        self.textboxbuttons["namebutton"] = (Button(self.top_frame1, text="Add Name", command=lambda: self.add_name()))
        self.textboxbuttons["composerbutton"] = (Button(self.top_frame2, text="Add Composer", command=lambda: self.add_composer()))
        for label in self.textboxbuttons.values():
            label.pack(side = LEFT)
        for box in self.textboxes.values():
            box.pack(side = RIGHT)
