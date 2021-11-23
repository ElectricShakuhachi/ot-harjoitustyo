from types import prepare_class


class Note:
    def __init__(self, pitch: int, position: list, lenght=1):
        self.pitch = pitch
        self.lenght = lenght
        self.position = position

class Music:
    def __init__(self):
        self.notes = []

    def next_position(self):
        if len(self.notes) == 0:
            return 
        last = self.notes[-1].position

    def add_note(self, note: Note):
        pass