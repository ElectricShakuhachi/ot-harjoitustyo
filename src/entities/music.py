from types import prepare_class
from copy import copy

class Note:
    def __init__(self, text: str, pitch: int, position: list, lenght=1):
        self.text = text
        self.pitch = pitch
        self.lenght = lenght
        self.position = position

class Music:
    def __init__(self):
        self.notes = []
        self.name = ""
        self.composer = ""

    def next_position(self):
        if len(self.notes) == 0:
            return [500, 80]
        next = copy(self.notes[-1].position)
        next[1] += self.notes[-1].lenght * 30
        if next[1] > 770:
            next[1] = 80
            next[0] -= 60
        return next

    def add_note(self, note: Note):
        if note.position[0] < 30:
            return "full"
        else:
            self.notes.append(note)
            return "ok"