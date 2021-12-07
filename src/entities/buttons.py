from entities.music import *
from tkinter import *
from files.filing import FileManager

class Buttons:
    def __init__(self, ui, mode):
        self.ui = ui
        self.lenghtbuttons = {}
        self.notebuttons = []
        self.partbuttons = []
        self.filemanager = FileManager(self.ui.music, self.ui)
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
            self.lenghtbuttons[key] = ShakuButton(value, key, self.ui, "lenght", self)
        for i in range(1, 5):
            self.partbuttons.append(ShakuButton(f"Part {i}", i, self.ui, "part", self))
        self.savebutton = ShakuButton("save", 0, self.ui, "save", self)
        self.loadbutton = ShakuButton("load", 0, self.ui, "load", self)

class ShakuButton: #refactor into subclasses of buttons instead of checking for each type
    def __init__(self, text: str, data: int, ui, button_type: str, owner: Buttons):
        self.ui = ui
        self.owner = owner
        self.text = text
        self.button_type = button_type
        if button_type == "note":
            self.pitch = data
        elif button_type == "lenght":
            self.lenght = data
        elif button_type == "part":
            self.part = data
        self.button = Button(self.ui.right_frame, text=self.text, command=self.press)
        self.button.pack(side=TOP)

    def press(self):
        if self.button_type == "note":
            note = Note(self.text, self.pitch, self.ui.active_part.next_position(), self.ui.active_part.next_lenght)
            self.ui.add_note(note)
        elif self.button_type == "lenght":
            self.ui.active_part.next_lenght = self.lenght
            self.button.config(relief=SUNKEN)
            for b in self.owner.lenghtbuttons.values():
                if b.text != self.text:
                    b.button.config(relief=RAISED)
        elif self.button_type == "part":
            self.button.config(relief=SUNKEN)
            for b in self.owner.partbuttons:
                if b.text != self.text:
                    b.button.config(relief=RAISED)
            if self.part not in self.ui.music.parts.keys():
                self.ui.music.add_part(self.part)
            self.ui.active_part = self.ui.music.parts[self.part]
            self.owner.lenghtbuttons[8].press()
        elif self.button_type == "save":
            self.owner.filemanager.save()
        elif self.button_type == "load":
            self.owner.filemanager.load()
                    
