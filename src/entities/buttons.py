from entities.music import Note
from tkinter import Button, Entry, constants
from files.filing import FileManager
from entities.midi_creator import MidiCreator
from entities.midi_player import MidiPlayer

class Controls:
    def __init__(self, ui, mode):
        self.ui = ui
        self.lenghtbuttons = {}
        self.notebuttons = []
        self.partbuttons = []
        self.filemanager = FileManager(self.ui.music, self.ui)
        self.octave_buttons = []
        self.textboxes = {}
        self.textboxbuttons = {}
        self.textboxes["musicname"] = (Entry(self.ui.top_frame1))
        self.textboxes["composername"] = (Entry(self.ui.top_frame2))
        self.textboxbuttons["namebutton"] = (Button(self.ui.top_frame1, text="Add Name", command=lambda: self.ui.add_name()))
        self.textboxbuttons["composerbutton"] = (Button(self.ui.top_frame2, text="Add Composer", command=lambda: self.ui.add_composer()))
        for label in self.textboxbuttons.values():
            label.pack(side = constants.LEFT)
        for box in self.textboxes.values():
            box.pack(side = constants.RIGHT)

        self.octave_buttons.append(ShakuButton("Otsu", 0, self.ui, "octave", self))
        self.octave_buttons.append(ShakuButton("Kan", 1, self.ui, "octave", self))
        self.octave_buttons.append(ShakuButton("Daikan", 2, self.ui, "octave", self))
        if mode == "Kinko":
            otsu_note_texts = ["RO", "TSU", "RE", "CHI", "HA", "HI"]
        pitches = [2, 5, 7, 9, 12, 14]
        for i in range(len(otsu_note_texts)):
            self.notebuttons.append(ShakuButton(otsu_note_texts[i], pitches[i], self.ui, "note", self))
        lenghts = {2: "16th", 4: "8th", 8: "4th", 16: "half"}
        # support for 32ths currently disabled -> not commonly necessary in this form of notation -> however could be dealt with and added later
        # 1: "32th"
        # whole also disabled -> usable only when there's a feature to change measure grid
        # 32: "half"
        for key, value in lenghts.items():
            self.lenghtbuttons[key] = ShakuButton(value, key, self.ui, "lenght", self)
        for i in range(1, 5):
            self.partbuttons.append(ShakuButton(f"Part {i}", i, self.ui, "part", self))
        self.exp_midi_button = ShakuButton("export", 0, self.ui, "export", self)
        self.play_midi_button = ShakuButton("play", 0, self.ui, "play", self)
        self.savebutton = ShakuButton("save", 0, self.ui, "save", self)
        self.loadbutton = ShakuButton("load", 0, self.ui, "load", self)

class ShakuButton: #refactor into subclasses of buttons instead of checking for each type
    def __init__(self, text: str, data: int, ui, button_type: str, owner: Controls):
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
        self.button.pack(side=constants.TOP)
        if button_type == "export" or button_type == "play":
            self.creator = MidiCreator()
        if button_type == "play":
            self.player = MidiPlayer()

    def press(self):
        if self.button_type == "note":
            note = Note(self.text, self.pitch, self.ui.active_part.next_position(), self.ui.active_part.next_lenght)
            self.ui.add_note(note)
        if self.button_type == "lenght":
            self.ui.active_part.next_lenght = self.lenght
            self.button.config(relief=constants.SUNKEN)
            for b in self.owner.lenghtbuttons.values():
                if b.text != self.text:
                    b.button.config(relief=constants.RAISED)
        if self.button_type == "part":
            self.button.config(relief=constants.SUNKEN)
            for b in self.owner.partbuttons:
                if b.text != self.text:
                    b.button.config(relief=constants.RAISED)
            if self.part not in self.ui.music.parts.keys():
                self.ui.music.add_part(self.part)
                self.ui.draw_all_notes()
            self.ui.active_part = self.ui.music.parts[self.part]
            self.owner.lenghtbuttons[8].press()
        if self.button_type == "export" or self.button_type == "play":
            for part in self.ui.music.parts.values():
                self.creator.create_track(part)
            self.creator.write_file()
        if self.button_type == "play":
            self.player.play(len(self.ui.music.parts))
        if self.button_type == "save":
            self.owner.filemanager.save()
        if self.button_type == "load":
            self.owner.filemanager.load()
        if self.button_type == "octave": #not ready
            self.button.config(relief=constants.SUNKEN)
            for b in self.owner.octave_buttons:
                if b.text != self.text:
                    b.button.config(relief=constants.RAISED)
                
