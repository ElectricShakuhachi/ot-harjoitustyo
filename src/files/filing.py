import json
from tkinter import filedialog
from entities.music import Note, Music

class FileManager:
    def __init__(self, music, ui):
        self.music = music
        self.ui = ui

    def save(self):
        data = self.music.convert_to_json()
        with filedialog.asksaveasfile(mode='w', defaultextension=".shaku") as file:
            json.dump(data, file, indent=4)

    def load(self):
        self.music = self.ui.music = Music()
        self.ui.sheet.delete('all')
        with filedialog.askopenfile(mode='r', defaultextension=".shaku") as file:
            data = json.load(file)
            self.ui.create_grid()
            for part_n, part_data in data['parts'].items():
                self.music.add_part(int(part_n))
                self.ui.active_part = self.music.parts[int(part_n)]
                for note in part_data:
                    self.ui.add_note(Note(note['text'], int(note['pitch']), note['position'], int(note['lenght'])))
            self.music.set_name(data['name'])
            self.music.set_composer(data['composer'])
            self.ui.draw_texts()
