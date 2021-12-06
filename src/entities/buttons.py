from entities.music import *
from tkinter import *

class Buttons:
    def __init__(self, ui, mode):
        self.ui = ui
        self.lenghtbuttons = []
        self.notebuttons = []
        if mode == "Ueda" or mode == "Tozan":
            note_texts = ["RO", "TSU", "RE", "CHI", "HA", "HI"]
        for i in range(len(note_texts)):
            self.notebuttons.append(ShakuButton(note_texts[i], i, self.ui, "note", self))
        lenghts = {2: "16th", 4: "8th", 8: "4th", 16: "half"}
        # support for 32ths currently disabled -> not commonly necessary in this form of notation -> however could be dealt with and added later
        # 1: "32th"
        # whole also disabled -> usable only when there's a feature to change measure grid
        # 32: "half"
        for key, value in lenghts.items():
            self.lenghtbuttons.append(ShakuButton(value, key, self.ui, "lenght", self))

class ShakuButton:
    def __init__(self, text: str, data: int, ui, button_type: str, owner: Buttons):
        self.ui = ui
        self.owner = owner
        self.text = text
        self.button_type = button_type
        if button_type == "note":
            self.pitch = data
        elif button_type == "lenght":
            self.lenght = data
        self.button = Button(self.ui.right_frame, text=self.text, command=self.press)
        self.button.pack(side=TOP)

    def press(self):
        if self.button_type == "note":
            note = Note(self.text, self.pitch, self.ui.music.next_position(), self.ui.music.next_lenght)
            self.ui.add_note(note, self.text)
        elif self.button_type == "lenght":
            self.ui.music.next_lenght = self.lenght
            self.button.config(relief=SUNKEN)
            for b in self.owner.lenghtbuttons:
                if b.text != self.text:
                    b.button.config(relief=RAISED)