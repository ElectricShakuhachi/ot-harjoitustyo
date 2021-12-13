from tkinter import constants, Frame, Canvas, PhotoImage
from entities.music import Music, Note
from entities.buttons import Controls
from ui.messages import ShakuMessage
from pathlib import Path
import os

#the current UI responsibilites need to be refactored so that the non-UI responsibilities of it are for the new music class, 
# current music class changing into part class, which are owned by music class
class UI: 
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x1000")
        self.generate_frames()
        self.create_sheet()
        self.music = Music()
        self.music.add_part(1)
        self.create_grid()
        self.active_part = self.music.parts[1]
        self.controls = Controls(self, "Kinko")
        self.note_pngs = self.load_pngs()
        self.name = ""
        self.composer = ""
        self.messages = []
        self.temp_dot = None
        self.edit_note = None

    def generate_frames(self):
        self.frame = Frame(self.window)
        self.frame.pack()
        self.top_frame1 = Frame(self.window)
        self.top_frame1.pack(side=constants.TOP)
        self.top_frame2 = Frame(self.window)
        self.top_frame2.pack(side=constants.TOP)
        self.left_frame = Frame(self.window, padx=20)
        self.left_frame.pack(side=constants.LEFT)
        self.right_frame = Frame(self.window)
        self.right_frame.pack(side=constants.RIGHT, padx=20)

    def create_sheet(self):
        self.sheet = Canvas(
            self.left_frame,
            width=630,
            height=891,
            background="white",
        )
        self.sheet.pack(side = constants.LEFT)
        self.grid = []

    def create_grid(self, measure_lenght=2):
        spacing = max(2, self.music.parts[1].spacing)
        self.clear_grid()
        for x in range(543, 62, -20 * spacing):
            self.grid.append(self.sheet.create_line(x, 70, x, 840, fill="black", width=1))
        for y in range(70, 841, 55 * measure_lenght):
            self.grid.append(self.sheet.create_line(542, y, 62, y, fill="black", width=1))

    def clear_grid(self):
        for line in self.grid:
            self.sheet.delete(line)

    def load_pngs(self):
        dirname = Path(__file__)
        self.pngs = {}
        for notebutton in self.controls.notebuttons:
            self.pngs[notebutton.text] = PhotoImage(file=os.path.join(dirname.parent.parent, "./graphics/" + notebutton.text + ".png"))

    def draw_time_notation(self, note):#REFACTOR -> too much repetition, basically jammed through in this form for now -> consider if this is a job for the UI to handle by itself?
        if note.lenght > 8:
            return
        self.sheet.create_line(note.position[0] + 11, note.position[1], note.position[0] + 11, note.position[1] + 10, fill="black", width=2)
        if note.lenght == 8:
            return
        if len(self.active_part.notes) > 1 and self.active_part.notes[-2].lenght < 8 and self.active_part.measure_counter != self.active_part.notes[-1].lenght:
            self.sheet.create_line(note.position[0] + 11, self.active_part.notes[-2].position[1], note.position[0] + 11, note.position[1] + 10, fill="black", width=2)
            if self.active_part.notes[-1].lenght == 4 and self.temp_dot:
                self.sheet.delete(self.temp_dot)
        if note.lenght == 4:
            if len(self.active_part.notes) < 2 or self.active_part.measure_counter == self.active_part.notes[-1].lenght or self.active_part.notes[-2].lenght > 4:
                self.temp_dot = self.sheet.create_line(note.position[0] + 12, note.position[1] + 4, note.position[0] + 18, note.position[1] + 8, fill="black", width=2)
            return
        self.sheet.create_line(note.position[0] + 15, note.position[1], note.position[0] + 15, note.position[1] + 10, fill="black", width=2)
        if len(self.active_part.notes) > 1 and self.active_part.notes[-2].lenght < 3 and self.active_part.measure_counter != self.active_part.notes[-1].lenght:
            self.sheet.create_line(note.position[0] + 15, note.position[1] - 10, note.position[0] + 15, note.position[1] + 10, fill="black", width=2)
        if note.lenght == 1: #note specific case
            self.sheet.create_line(note.position[0] + 13, note.position[1] + 5, note.position[0] + 23, note.position[1] + 7, fill="black", width=2)

    def draw_note(self, note: Note):
        self.sheet.create_image(note.position[0], note.position[1], anchor=constants.NW, image=self.pngs[note.text])    
        self.draw_time_notation(note)

    def add_note(self, note: Note):
        status = self.active_part.add_note(note)
        if status == "full":
            self.messages.append(ShakuMessage("Full Sheet"))
        else:
            self.draw_note(note)

    def draw_all_notes(self):
        self.sheet.delete('all')
        self.create_grid()
        for id, part in self.music.parts.items():
            self.active_part = part
            for note in part.notes:
                self.draw_note(note)
        self.draw_texts()

    def draw_texts(self):
        self.erase_texts()
        self.name = self.sheet.create_text(20, 20, text=self.music.get_name(), fill="black", anchor=constants.NW, font=("Helvetica 16"))
        self.composer = self.sheet.create_text(600, 20, text=self.music.get_composer(), fill="black", anchor=constants.NE, font=("Helvetica 16"))

    def erase_texts(self):
        if self.name != "":
            self.sheet.delete(self.name)
        if self.composer != "":
            self.sheet.delete(self.composer)

    def add_name(self):
        name = self.controls.textboxes["musicname"].get()
        self.music.set_name(name)
        self.draw_texts()

    def add_composer(self):
        composer = self.controls.textboxes["composername"].get()
        self.music.set_composer(composer)
        self.draw_texts()

