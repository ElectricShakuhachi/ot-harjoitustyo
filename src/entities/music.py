from types import prepare_class
from copy import copy

class Note:
    def __init__(self, text: str, pitch: int, position: list, lenght=8):
        self.text = text
        self.pitch = pitch
        self.lenght = lenght
        self.position = position

class Music:
    def __init__(self):
        self.parts = {}
        self._name = ""
        self._composer = ""

    def add_part(self, part_id):
        first_part_x = 526
        start_x = first_part_x - (part_id - 1) * 20
        self.parts[part_id] = Part(start_x, len(self.parts) + 1)

    def change_spacing(self, spacing):
        for part in self.parts.values():
            part.change_spacing(spacing)

    def set_name(self, name):
        self._name = name

    def set_composer(self, composer):
        self._composer = composer

    def get_name(self):
        return self._name

    def get_composer(self):
        return self._composer

    def get_parts(self):
        return self.parts

    def clear(self):
        self.parts = {}
        self._name = ""
        self._composer = ""

    def convert_to_json(self):
        data = {}
        data['name'] = self._name
        data['composer'] = self._composer
        data['parts'] = {}
        for part_n, part_data in self.get_parts().items():
            data['parts'][part_n] = []
            for note in part_data.notes:
                data['parts'][part_n].append({
                    'text': note.text,
                    'pitch': note.pitch,
                    'lenght': note.lenght,
                    'position': note.position
                })
        return data

class Part:
    def __init__(self, start_x, spacing=4):
        self.notes = []
        self.start_x = start_x
        self.start_y = 80
        self.next_lenght = 8
        self.measure_counter = 0
        self.spacing = spacing

    def next_position(self):
        if len(self.notes) == 0:
            return [self.start_x, self.start_y]
        next = copy(self.notes[-1].position)
        next[1] += self.notes[-1].lenght * 6
        if self.measure_counter == 0:
            next[1] += 14
        if next[1] > 830:
            next[1] = 80
            next[0] -= self.spacing * 20
        return next

    def add_note(self, note: Note):
        if note.position[0] < 30:
            return "full"
        else:
            self.notes.append(note)
            self.measure_counter += note.lenght
            if self.measure_counter == 16:
                self.measure_counter = 0
            return "ok"

    def change_spacing(self, spacing):
        pass