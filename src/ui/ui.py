from tkinter import *
from entities.music import *
from entities.buttons import *
from ui.messages import *

class UI:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x1000")
        self.generate_frames()
        self.buttons = Buttons(self, "Ueda")
        self.textboxes = {}
        self.textboxbuttons = {} #move this to Buttons class later
        self.note_pngs = self.load_pngs()
        self.sheet = None
        self.music = Music()
        self.name = ""
        self.composer = ""
        self.messages = []

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

    def load_pngs(self):
        self.pngs = {}
        for notebutton in self.buttons.notebuttons:
            self.pngs[notebutton.text] = PhotoImage(file="./graphics/" + notebutton.text + ".png")

    def draw_all_notes(self):
        for note in self.music.notes:
            self.sheet.create_image(note.position[0], note.position[1], anchor=NW, image=self.pngs[note.text])

    def load_music(self):#should not be at ui -> move elsewhere before developing feature
        pass

    def save_music(self):#should not be at ui -> move elsewhere before developing feature
        pass

    def add_note(self, note: Note, text: str):
        status = self.music.add_note(note)
        if status == "full":
            self.messages.append(ShakuMessage("Full Sheet"))
        else:
            self.sheet.create_image(note.position[0], note.position[1], anchor=NW, image=self.pngs[note.text])

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

    def populate_buttons(self):
        for b in self.buttons.notebuttons:
            newbutton = Button(self.right_frame, text=b.text, command=b.press)
            newbutton.pack(side=TOP)

