from copy import copy

class Note:
    def __init__(self, text: str, pitch: int, position: list, lenght=8, first=False):
        self.text = text
        self.pitch = pitch
        self.lenght = lenght
        self.position = position
        self.first = first
        self.dotted = False

class Music:
    def __init__(self):
        self.parts = {}
        self._name = ""
        self._composer = ""

    def add_part(self, part_id, loading=False):
        if len(self.parts) == 3:
            for part in self.parts.values():
                if part.rows() > 6:
                    return False
        if len(self.parts) == 2:
            for part in self.parts.values():
                if part.rows() > 8:
                    return False
        first_part_x = 516
        if part_id == 1:
            start_x = first_part_x
        else:
            start_x = (first_part_x + 10) - (part_id - 1) * 20
        self.change_spacing(1, loading=loading)
        self.parts[part_id] = Part(part_id, start_x, len(self.parts) + 1)
        return True

    def change_spacing(self, spacing, loading=False):
        for part in self.parts.values():
            part.change_spacing(spacing, loading=loading)

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

    def extract_time_notation(self):
        parts = []
        for part in self.parts.values():
            parts.append(part.time_notations())
        return parts

class Part:
    def __init__(self, part_id, start_x, spacing=2):
        self.part_no = part_id
        self.notes = []
        self.start_x = start_x
        self.start_y = 80
        self.next_lenght = 8
        self.measure_counter = 0
        self.spacing = spacing
        self.min_x = 55
        self.dot_flag = None #probably unused now!
        self._rows = 0

    def next_position(self):
        if len(self.notes) == 0:
            return [self.start_x, self.start_y]
        next = copy(self.notes[-1].position)
        next[1] += self.notes[-1].lenght * 6
        if self.measure_counter == 0:
            next[1] += 14
        if next[1] > 830:
            next[1] = 80
            next[0] -= max(self.spacing, 2) * 20
        return next

    def add_note(self, note: Note):
        if len(self.notes) == 0 or self.notes[-1].position[0] > note.position[0]:
            self._rows += 1
        if note.position[0] < self.min_x:
            return "full"
        else:
            self.notes.append(note)
            if self.measure_counter == 0:
                note.first = True
            self.measure_counter += note.lenght
            if self.measure_counter == 16:
                self.measure_counter = 0
            return "ok"

    def rows(self):
        return self._rows

    def change_spacing(self, spacing, loading=False):
        self.spacing += spacing
        if loading:
            return
        if self.start_x == 516:
            self.start_x += 10
            for note in self.notes:
                note.position[0] += 10 
        else:
            row = 0
            count = 0
            for i in range(1, len(self.notes)):
                count += 1
                if self.notes[i].position[0] < self.notes[i - 1].position[0] + row * 20:
                    row += 1
                self.notes[i].position[0] -= row * 20

    def time_notation(self, note_n: int):
        notation = []
        note = self.notes[note_n]
        x = note.position[0]
        y = note.position[1]
        if note_n > 0:
            previous = self.notes[note_n - 1]
        if note.lenght > 8:
            return notation
        notation.append(((x + 11, y), (x + 11, y + 10)))
        if note.lenght == 8:
            return notation
        if note_n != 0 and previous.lenght < 8 and not note.first:
            notation.append(((x + 11, previous.position[1]), (x + 11, y + 10)))
        if note.lenght == 4:
            if note_n == 0 or note.first or previous.lenght > 4:
                note.dotted = True
                notation.append(((x + 12, y + 4), (x + 18, y + 8)))
            return notation
        notation.append(((x + 15, y), (x + 15, y + 10)))
        if note_n != 0 and previous.lenght < 3 and not note.first:
            notation.append(((x + 15, y - 10), (x + 15, y + 10)))
        if note.lenght == 1: #SPECIAL CASE -> NOT IN USE CURRENTLY
            notation.append(((x + 13, y + 5), (x + 24, y + 7)))
        return notation

    def part_time_notations(self):
        notations = []
        for note_n in range(len(self.notes)):
            notations.append(self.time_notation(note_n))
            if self.notes[note_n].lenght == 4 and self.notes[note_n - 1].dotted:
                print(f"removing dot {notations[-2][-1]}")
                notations[-2] = notations[-2][:-1]
        return notations
