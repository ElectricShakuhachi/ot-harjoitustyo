from entities.music import *

class Buttons:
    def __init__(self, ui, mode):
        self.ui = ui
        self.notebuttons = []
        if mode == "Ueda":
            note_texts = ["RO", "TSU", "RE", "CHI", "HA", "HI"]
        for i in range(len(note_texts)):
            self.notebuttons.append(ShakuButton(note_texts[i], i, self.ui, "note"))

class ShakuButton:
    def __init__(self, text: str, data: int, ui, button_type: str):
        self.ui = ui
        self.text = text
        self.button_type = button_type
        if button_type == "note":
            self.pitch = data
        elif button_type == "lenght":
            self.lenght = data

    def press(self):
        if self.button_type == "note":
            note = Note(self.text, self.pitch, self.ui.music.next_position()) #if you dont send lenght, it's assumed to be 1
            self.ui.add_note(note, self.text)
