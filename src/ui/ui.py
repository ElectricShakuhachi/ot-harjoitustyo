from tkinter import *
from entities.music import *
from entities.buttons import *
from graphics.graphics import *

class UI:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x1000")
        self.frame = Frame(self.window)
        self.frame.pack()
        self.top_frame = Frame(self.window)
        self.top_frame.pack(side=TOP)
        self.left_frame = Frame(self.window, padx=20)
        self.left_frame.pack(side=LEFT)
        self.right_frame = Frame(self.window)
        self.right_frame.pack(side=RIGHT, padx=20)
        self.buttons = []
        self.textboxes = []
        self.labels = []
        self.sheet = None
        self.music = Music()

    def start(self):
        self.create_sheet()
        self.create_text_boxes()
        self.populate_buttons()

    def create_sheet(self):
        self.sheet = Canvas(
            self.left_frame,
            width=630,
            height=891,
            background="white",
        )
        self.sheet.pack(side = LEFT)

    def load_music(self):
        pass

    def save_music(self):
        pass

    def add_note(self, note: Note, text: str):
        self.music.add_note(note)
        note_png = PhotoImage(file=Graphics.get_note_png(text))
        self.sheet.create_image(15, 15, image=note_png)
        print("dingdong")

    def create_text_boxes(self):
        self.labels.append(Label(self.top_frame, text="Name"))
        self.textboxes.append(Entry(self.top_frame))
        for label in self.labels:
            label.pack(side = TOP)
        for box in self.textboxes:
            box.pack(side = TOP)

    def populate_buttons(self):
        button_texts = ["RO", "TSU", "RE", "CHI", "HA", "HI"]
        for i in range(len(button_texts)):
            self.buttons.append(ShakuButton(button_texts[i], i, type="note"))
        for b in self.buttons:
            if b.type == "note":
                note = Note(b.pitch, self.music.next_position()) #if you dont send lenght, it's assumed to be 1
                Button(self.right_frame, text=b.text, command=lambda: self.add_note(note, b.text)).pack(side=TOP)
            if b.type == "lenght":
                pass
