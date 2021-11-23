from entities.music import *

class ShakuButton:
    def __init__(self, text: str, data: int, ui, type: str):
        self.ui = ui
        self.text = text
        self.type = type
        if type == "note":
            self.pitch = data
        elif type == "lenght":
            self.lenght = data

    def press(self):
        if self.type == "note":
            note = Note(self.pitch, self.ui.music.next_position()) #if you dont send lenght, it's assumed to be 1
            self.ui.add_note(note, self.text)