from tkinter import constants, Frame, Canvas
from entities.music import Music, Note
from ui.buttons import Buttons
from ui.messages import ShakuMessage

class UI: 
    def __init__(self, window):
        self.window = window
        self.window.geometry("840x1000")
        self.generate_frames()
        self.create_sheet()
        self.music = Music()
        self.music.add_part(1)
        self.create_grid()
        self.active_part = self.music.parts[1]
        self.controls = Buttons(self, "Tozan")
        self.name = ""
        self.composer = ""
        self.messages = []
        self.edit_note = None
        self.time_notations = []

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
            width=620,
            height=877,
            background="white",
        )
        self.sheet.pack(side = constants.LEFT)
        self.grid = []

    def create_grid(self, measure_lenght=2):#if you start using this measure lenght thing -> remember to also edit it for image class...
        spacing = max(2, self.music.parts[1].spacing)
        self.clear_grid()
        for x in range(543, 62, -20 * spacing):
            self.grid.append(self.sheet.create_line(x, 70, x, 840, fill="black", width=1))
        for y in range(70, 841, 55 * measure_lenght):
            self.grid.append(self.sheet.create_line(542, y, 62, y, fill="black", width=1))

    def clear_grid(self):
        for line in self.grid:
            self.sheet.delete(line)

    def draw_time_notation(self, note_n=-1):
        part = self.active_part
        if note_n == -1:
            note_n = len(self.active_part.notes) - 1
        if self.active_part.notes[note_n - 1].dotted:
            self.sheet.delete(self.time_notations[-1])
        for line in part.time_notation(note_n):
            self.time_notations.append(self.sheet.create_line(line[0][0], line[0][1], line[1][0], line[1][1], fill="black", width=2))

    def draw_note(self, note: Note):
        if note.pitch == -1:
            if note.lenght == 16:
                break_text = "。。"
            elif note.lenght == 8:
                break_text = "。"
            elif note.lenght == 4:
                break_text = "、"
            elif note.lenght == 2:
                break_text = "、、"
            self.sheet.create_text(note.position[0]-2, note.position[1]-3, anchor=constants.NW, text=break_text, font=("有澤太楷書 11"))
        else:
            self.sheet.create_text(note.position[0]-2, note.position[1]-3, anchor=constants.NW, text=note.text, font=("有澤太楷書 11"))
            self.draw_time_notation()

    def add_note(self, note: Note):
        status = self.active_part.add_note(note)
        if status == "full":
            self.messages.append(ShakuMessage("Full Sheet"))
        else:
            self.draw_note(note)

    def draw_all_time_notations(self):
        for i in self.time_notations:
            self.sheet.delete(i)
        store = self.active_part
        for part in self.music.parts.values():
            self.active_part = part
            for i in range(len(part.notes)):
                self.draw_time_notation(i)
        self.active_part = store

    def draw_all_notes(self): #should rename to something like draw_all
        self.sheet.delete('all')
        self.create_grid()
        for id, part in self.music.parts.items():
            self.active_part = part
            for note in part.notes:
                self.draw_note(note)
        self.draw_all_time_notations()
        self.draw_texts()

    def draw_texts(self):
        self.erase_texts()
        self.name = self.sheet.create_text(20, 20, text=self.music.get_name(), fill="black", anchor=constants.NW, font=("Helvetica 16"))
        self.composer = self.sheet.create_text(600, 20, text=self.music.get_composer(), fill="black", anchor=constants.NE, font=("有澤太楷書 16"))

    def erase_texts(self):
        if self.name != "":
            self.sheet.delete(self.name)
        if self.composer != "":
            self.sheet.delete(self.composer)

    def add_name(self, name=None):
        if not name:
            name = self.controls.textboxes["musicname"].get()
        self.music.set_name(name)
        self.draw_texts()

    def add_composer(self, composer=None):
        if not composer:
            composer = self.controls.textboxes["composername"].get()
        self.music.set_composer(composer)
        self.draw_texts()

    def load_json(self, data):
        self.music = Music()
        self.music.load_json(data)
        self.sheet.delete('all')
        self.create_grid()
        self.add_name(data['name'])
        self.add_composer(data['composer'])
        self.draw_all_notes()
