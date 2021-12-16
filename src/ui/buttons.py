from entities.music import Note, Music
from tkinter import Button, Entry, constants, Frame, ttk, Label
from files.filing import FileManager
from entities.midi_creator import MidiCreator
from entities.midi_player import MidiPlayer
from entities.image_creator import ImageCreator
from ui.messages import ShakuMessage

class Buttons:
    def __init__(self, ui, mode):
        self.ui = ui
        self.lenghtbuttons = {}
        self.notebuttons = []
        self.partbuttons = {}
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
        self.button_labels.append(Label(self.octave_frame, text="Octave"))
        self.octave_buttons.append(OctaveButton("Otsu", 0, self.ui, self, self.octave_frame))
        self.octave_buttons.append(OctaveButton("Kan", 1, self.ui, self, self.octave_frame))
        self.octave_buttons.append(OctaveButton("Daikan", 2, self.ui, self, self.octave_frame))
        self.separators["octave"] = (ButtonSeparator(self.octave_frame))

        self.notes_frame = Frame(self.ui.right_frame)
        self.notes_frame.pack(side=constants.TOP)
        self.button_labels.append(Label(self.notes_frame, text="Notes"))
        if mode in ["Tozan", "Ueda"]:
            otsu_note_texts = ["ロ", "ツ", "レ", "チ", "ハ", "ヒ"]
        elif mode == "Kinko":
            otsu_note_texts = ["ロ", "ツ", "レ", "チ", "リ", "イ"]
        else:
            raise Exception("Designated school of shakuhachi notation not available, or no school designated")
        pitches = [2, 5, 7, 9, 12, 14]
        self.note_frame1 = Frame(self.notes_frame)
        self.note_frame1.pack(side=constants.TOP)
        for i in range(3):
            button = NoteButton(otsu_note_texts[i], pitches[i], self.ui, self, self.note_frame1)
            self.notebuttons.append(button)
            button.button.pack(side=constants.LEFT)
        self.note_frame2 = Frame(self.notes_frame)
        self.note_frame2.pack(side=constants.TOP)
        for i in range(3, 6):
            button = NoteButton(otsu_note_texts[i], pitches[i], self.ui, self, self.note_frame2)
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
        self.button_labels.append(Label(self.durations_frame, text="Durations"))
        for key, value in lenghts.items():
            self.lenghtbuttons[key] = LenghtButton(value, key, self.ui, self, self.durations_frame)
        self.separators["durations"] = (ButtonSeparator(self.durations_frame))

        self.parts_frame = Frame(self.ui.right_frame)
        self.parts_frame.pack(side=constants.TOP)
        self.button_labels.append(Label(self.parts_frame, text="Parts"))
        self.addpartbutton = AddPartButton("Add Part", None, self.ui, self, self.parts_frame)
        self.partbuttons[1] = (PartButton(f"Part {1}", 1, self.ui, self, self.parts_frame))
        self.separators["parts"] = (ButtonSeparator(self.parts_frame))

        self.file_frame = Frame(self.ui.right_frame)
        self.file_frame.pack(side=constants.TOP)
        self.button_labels.append(Label(self.file_frame, text="File"))
        self.exp_midi_button = ExportMidiButton("export MIDI", self.ui, self, self.file_frame)
        self.exp_sheet_button = ExportSheetButton("export sheet", self.ui, self, self.file_frame)
        self.play_midi_button = PlayButton("play", self.ui, self, self.file_frame)
        self.savebutton = SaveButton("save", self.ui, self, self.file_frame)
        self.loadbutton = LoadButton("load", self.ui, self, self.file_frame)
        self.uploadbutton = UploadButton("upload", self.ui, self, self.file_frame)

class ButtonSeparator:
    def __init__(self, frame, pady=10):
        self.line = ttk.Separator(frame, orient="horizontal")
        self.line.pack(fill="x", pady=pady)

class ShakuButton:
    def __init__(self, text: str, ui, owner: Buttons):
        self.ui = ui
        self.owner = owner
        self.text = text

class OctaveButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        if self.text == "Otsu":
            self.button.config(relief=constants.SUNKEN, state="disabled")
        self.button.pack(side=constants.TOP)
        self.octaves_up = data

    def press(self):
        self.button.config(relief=constants.SUNKEN, state="disabled")
        for b in self.owner.octave_buttons:
            if b.text != self.text:
                b.button.config(relief=constants.RAISED, state="normal")

class NoteButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.pitch = data
        self.button = Button(frame, text=self.text, command=self.press)

    def press(self):
        note = Note(self.text, self.pitch, self.ui.active_part.next_position(), self.ui.active_part.next_lenght)
        self.ui.add_note(note)

class LenghtButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.lenght = data
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        self.ui.active_part.next_lenght = self.lenght
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for b in self.owner.lenghtbuttons.values():
            if b.text != self.text:
                b.button.config(state="normal", relief=constants.RAISED)

class AddPartButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.part = data
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        if len(self.ui.music.parts) == 4:
            return
        self.owner.file_frame.pack_forget()
        i = len(self.ui.music.parts) + 1
        self.owner.separators["parts"].line.destroy()
        new_button = PartButton(f"Part {i}", i, self.ui, self.owner, self.owner.parts_frame)
        self.owner.partbuttons[i] = new_button
        self.owner.separators["parts"] = ButtonSeparator(self.owner.parts_frame)
        self.owner.file_frame.pack(side=constants.TOP)
        self.ui.music.add_part(i)
        self.ui.draw_all_notes()
        new_button.press()
        if len(self.ui.music.parts) == 4:
            self.button.config(state="disabled")
        return new_button

class PartButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)
        self.part = data

    def press(self):
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for b in self.owner.partbuttons.values():
            if b.text != self.text:
                b.button.config(state="normal", relief=constants.RAISED)
        self.ui.active_part = self.ui.music.parts[self.part]
        self.owner.lenghtbuttons[8].press()

class ExportMidiButton(ShakuButton):
    def __init__(self, text, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)
        self.creator = MidiCreator()

    def press(self):
        for part in self.ui.music.parts.values():
            self.creator.create_track(part)
        self.creator.write_file()

class ExportSheetButton(ShakuButton):
    def __init__(self, text, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        image_creator = ImageCreator()
        image = image_creator.create_image(self.ui.music)
        filemanager.save_pdf(image)

class PlayButton(ShakuButton):
    def __init__(self, text, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)
        self.creator = MidiCreator()
        self.player = MidiPlayer()

    def press(self):
        for part in self.ui.music.parts.values():
            self.creator.create_track(part)
        self.creator.write_file()
        self.player.play(len(self.ui.music.parts))

class SaveButton(ShakuButton):
    def __init__(self, text, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        data = self.ui.music.convert_to_json()
        filemanager.save_shaku(data)

class LoadButton(ShakuButton):
    def __init__(self, text, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        music = self.ui.music = Music()
        self.ui.sheet.delete('all')
        data = filemanager.load()
        for part_data in data['parts'].values():
            self.owner.addpartbutton.press()
            for note in part_data:
                self.ui.add_note(Note(note['text'], int(note['pitch']), note['position'], int(note['lenght'])))
        self.ui.create_grid()
        music.set_name(data['name'])
        music.set_composer(data['composer'])
        self.ui.draw_texts()
        for i in self.owner.partbuttons.keys():
            if i > len(self.ui.music.parts):
                self.owner.partbuttons[i].button.destroy()
        self.owner.lenghtbuttons[8].press()

class UploadButton(ShakuButton):
    def __init__(self, text, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        data = self.ui.music.convert_to_json()
        name = self.ui.music.get_name()
        if not name or name == "":
            ShakuMessage("No Name")
            return
        if not filemanager.upload_to_aws_s3(data, name=name):
            ShakuMessage("No Access")
