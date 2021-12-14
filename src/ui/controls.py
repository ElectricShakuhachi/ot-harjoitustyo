from entities.music import Note, Music
from tkinter import Button, Entry, constants, Frame, ttk, Label
from files.filing import FileManager
from entities.midi_creator import MidiCreator
from entities.midi_player import MidiPlayer
from entities.image_creator import ImageCreator
from ui.messages import ShakuMessage

class Controls:
    def __init__(self, ui, mode):
        self.ui = ui
        self.lenghtbuttons = {}
        self.notebuttons = []
        self.partbuttons = []
        self.octave_buttons = []
        self.textboxes = {}
        self.textboxbuttons = {}
        self.separators = {}
        self.button_labels = []
        self.textboxes["musicname"] = (Entry(self.ui.top_frame1))
        self.textboxes["composername"] = (Entry(self.ui.top_frame2))
        self.textboxbuttons["namebutton"] = (Button(self.ui.top_frame1, text="Add Name", command=lambda: self.ui.add_name()))
        self.textboxbuttons["composerbutton"] = (Button(self.ui.top_frame2, text="Add Composer", command=lambda: self.ui.add_composer()))
        for label in self.textboxbuttons.values():
            label.pack(side = constants.LEFT)
        for box in self.textboxes.values():
            box.pack(side = constants.RIGHT)
        
        self.octave_frame = Frame(self.ui.right_frame)
        self.octave_frame.pack(side=constants.TOP)
        self.button_labels.append(ButtonLabel(self.octave_frame, "Octave"))
        self.octave_buttons.append(ShakuButton("Otsu", 0, self.ui, "octave", self, self.octave_frame))
        self.octave_buttons.append(ShakuButton("Kan", 1, self.ui, "octave", self, self.octave_frame))
        self.octave_buttons.append(ShakuButton("Daikan", 2, self.ui, "octave", self, self.octave_frame))
        self.separators["octave"] = (ButtonSeparator(self.octave_frame))

        self.notes_frame = Frame(self.ui.right_frame)
        self.notes_frame.pack(side=constants.TOP)
        self.button_labels.append(ButtonLabel(self.notes_frame, "Notes"))
        if mode == "Tozan":
            otsu_note_texts = ["ロ", "ツ", "レ", "チ", "ハ", "ヒ"]
        pitches = [2, 5, 7, 9, 12, 14]
        self.note_frame1 = Frame(self.notes_frame)
        self.note_frame1.pack(side=constants.TOP)
        for i in range(3):
            button = ShakuButton(otsu_note_texts[i], pitches[i], self.ui, "note", self, self.note_frame1)
            self.notebuttons.append(button)
            button.button.pack(side=constants.LEFT)
        self.note_frame2 = Frame(self.notes_frame)
        self.note_frame2.pack(side=constants.TOP)
        for i in range(3, 6):
            button = ShakuButton(otsu_note_texts[i], pitches[i], self.ui, "note", self, self.note_frame2)
            self.notebuttons.append(button)
            button.button.pack(side=constants.LEFT)
        lenghts = {2: "16th", 4: "8th", 8: "4th", 16: "half"}
        # support for 32ths currently disabled -> not commonly necessary in this form of notation -> however could be dealt with and added later
        # 1: "32th"
        # whole also disabled -> usable only when there's a feature to change measure grid
        # 32: "half"
        self.separators["notes"] = (ButtonSeparator(self.notes_frame))

        self.durations_frame = Frame(self.ui.right_frame)
        self.durations_frame.pack(side=constants.TOP)
        self.button_labels.append(ButtonLabel(self.durations_frame, "Durations"))
        for key, value in lenghts.items():
            self.lenghtbuttons[key] = ShakuButton(value, key, self.ui, "lenght", self, self.durations_frame)
        self.separators["durations"] = (ButtonSeparator(self.durations_frame))

        self.parts_frame = Frame(self.ui.right_frame)
        self.parts_frame.pack(side=constants.TOP)
        self.button_labels.append(ButtonLabel(self.parts_frame, "Parts"))
        self.addpartbutton = ShakuButton("Add Part", None, self.ui, "addpart", self, self.parts_frame)
        self.partbuttons.append(ShakuButton(f"Part {1}", 1, self.ui, "part", self, self.parts_frame))
        self.separators["parts"] = (ButtonSeparator(self.parts_frame))

        self.file_frame = Frame(self.ui.right_frame)
        self.file_frame.pack(side=constants.TOP)
        self.button_labels.append(ButtonLabel(self.file_frame, "File"))
        self.exp_midi_button = ShakuButton("export MIDI", 0, self.ui, "exportmidi", self, self.file_frame)
        self.exp_sheet_button = ShakuButton("export sheet", 0, self.ui, "export_sheet", self, self.file_frame)
        self.play_midi_button = ShakuButton("play", 0, self.ui, "play", self, self.file_frame)
        self.savebutton = ShakuButton("save", 0, self.ui, "save", self, self.file_frame)
        self.loadbutton = ShakuButton("load", 0, self.ui, "load", self, self.file_frame)
        self.uploadbutton = ShakuButton("upload", 0, self.ui, "upload", self, self.file_frame)

class ButtonSeparator:
    def __init__(self, frame, pady=10):
        self.line = ttk.Separator(frame, orient="horizontal")
        self.line.pack(fill="x", pady=pady)

class ButtonLabel:
    def __init__(self, frame, text, pady=0):
        self.label = Label(frame, text=text)
        self.label.pack()

class ShakuButton: #refactor into subclasses of buttons instead of checking for each type
    def __init__(self, text: str, data: int, ui, button_type: str, owner: Controls, frame):
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
        self.button = Button(frame, text=self.text, command=self.press)
        if button_type != "note":
            self.button.pack(side=constants.TOP)
        if button_type == "exportmidi" or button_type == "play":
            self.creator = MidiCreator()
        if button_type == "play":
            self.player = MidiPlayer()

    def press(self):
        if self.button_type == "note":
            note = Note(self.text, self.pitch, self.ui.active_part.next_position(), self.ui.active_part.next_lenght)
            self.ui.add_note(note)

        elif self.button_type == "lenght":
            self.ui.active_part.next_lenght = self.lenght
            self.button.config(relief=constants.SUNKEN)
            for b in self.owner.lenghtbuttons.values():
                if b.text != self.text:
                    b.button.config(relief=constants.RAISED)

        elif self.button_type == "addpart":
            if len(self.ui.music.parts) == 4:
                return
            else:
                self.owner.file_frame.pack_forget()
                i = len(self.ui.music.parts) + 1
                self.owner.separators["parts"].line.destroy()
                new_button = ShakuButton(f"Part {i}", i, self.ui, "part", self.owner, self.owner.parts_frame)
                self.owner.partbuttons.append(new_button)
                self.owner.separators["parts"] = ButtonSeparator(self.owner.parts_frame)
                self.owner.file_frame.pack(side=constants.TOP)
                new_button.press()#refactor -> there's no reason for press() to create the part since it's always done heren 
                if len(self.ui.music.parts) == 4:
                    self.button.config(state="disabled")

        elif self.button_type == "part":
            self.button.config(relief=constants.SUNKEN)
            for b in self.owner.partbuttons:
                if b.text != self.text:
                    b.button.config(relief=constants.RAISED)
            if self.part not in self.ui.music.parts.keys():
                self.ui.music.add_part(self.part)
                self.ui.draw_all_notes()
            self.ui.active_part = self.ui.music.parts[self.part]
            self.owner.lenghtbuttons[8].press()
            
        elif self.button_type == "exportmidi":
            for part in self.ui.music.parts.values():
                self.creator.create_track(part)
            self.creator.write_file()

        elif self.button_type == "play":
            for part in self.ui.music.parts.values():
                self.creator.create_track(part)
            self.creator.write_file()
            self.player.play(len(self.ui.music.parts))

        elif self.button_type == "save":
            filemanager = FileManager()
            data = self.ui.music.convert_to_json()
            filemanager.save_shaku(data)

        elif self.button_type == "load":
            filemanager = FileManager()
            music = self.ui.music = Music()
            self.ui.sheet.delete('all')
            data = filemanager.load()
            for part_n, part_data in data['parts'].items():
                music.add_part(int(part_n))
                self.ui.active_part = music.parts[int(part_n)]
                for note in part_data:
                    self.ui.add_note(Note(note['text'], int(note['pitch']), note['position'], int(note['lenght'])))
            self.ui.create_grid()
            music.set_name(data['name'])
            music.set_composer(data['composer'])
            self.ui.draw_texts()

        elif self.button_type == "octave":
            self.button.config(relief=constants.SUNKEN)
            for b in self.owner.octave_buttons:
                if b.text != self.text:
                    b.button.config(relief=constants.RAISED)

        elif self.button_type == "export_sheet":
            filemanager = FileManager()
            image_creator = ImageCreator()
            image = image_creator.create_image(self.ui.music)
            filemanager.save_pdf(image)

        elif self.button_type == "upload":
            filemanager = FileManager()
            data = self.ui.music.convert_to_json()
            name = self.ui.music.get_name()
            if not name or name == "":
                ShakuMessage("No Name")
                return
            if not filemanager.upload_to_aws_s3(data, name=name):
                ShakuMessage("No Access")
