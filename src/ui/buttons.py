from entities.music import Note, Music
from tkinter import Button, Entry, constants, Frame, ttk, Label, Checkbutton, BooleanVar
from files.filing import FileManager
from entities.midi_creator import MidiCreator
from entities.midi_player import MidiPlayer
from entities.image_creator import ImageCreator
from entities.svg_creator import SvgCreator
from ui.messages import ShakuMessage
import entities.shaku_constants as consts

class Buttons: # it's weird that possible pitches and their names are defined here -> should be somewhere else
    def __init__(self, ui, mode):
        self.ui = ui
        self.mode = mode
        self.buttons = {}
        self.frames = {}
        self.buttons_by_frame = {}
        self.textboxes = {}
        self.textboxbuttons = {}
        self.separators = {}
        self.labels = []
        self.chosen_lenght = 8
        self._create_default_buttons()

    def _create_default_buttons(self):
        self._create_naming_frame()
        self._create_octave_buttons()
        self._create_note_buttons()
        self._create_break_buttons()
        self._create_lenght_buttons()
        self._create_part_buttons()
        self._create_export_buttons()
        self._create_file_buttons()
        self._create_play_buttons()

    def _create_octave_buttons(self):
        buttons = []
        for id, octave in enumerate(["Otsu", "Kan", "Daikan"]):
            buttons.append({'text': octave, 'data': id, "button_class": OctaveButton})
        self._generate_button_frame("Octave", buttons)

    def _create_note_buttons(self):
        note_texts = consts.NOTES[self.mode]
        pitches = consts.PITCHES[self.mode]
        buttons = []
        for i in range(len(note_texts)):
            buttons.append({'text': note_texts[i], 'data': pitches[i],"button_class": NoteButton})
        self._generate_button_frame("Note", buttons[:3], separator=False)
        self._generate_button_frame("Note2", buttons[3:], label=False, separator=False)
        self.separators["exports"] = ButtonSeparator(self.ui.right_frame)

    def _create_break_buttons(self):
        buttons = [{"text": "Break", "data": -1, "button_class": NoteButton}]
        self._generate_button_frame("Break", buttons)

    def _create_lenght_buttons(self):
        buttons = []
        for data, text in consts.LENGHTS.items():
            buttons.append({"text": text, "data": data, "button_class": LenghtButton})
        self._generate_button_frame("Duration", buttons)

    def _create_part_buttons(self):
        buttons = [
            {"text": "Add Part", "data": None, "button_class": AddPartButton},
            {"text": "Part 1", "data": 1, "button_class": PartButton}
        ]
        self._generate_button_frame("Parts", buttons)

    def _create_export_buttons(self):
        buttons = [
            {"text": "export MIDI", "data": None, "button_class": ExportMidiButton},
            {"text": "export PDF", "data": None, "button_class": ExportPdfButton},
            {"text": "export SVG", "data": None, "button_class": ExportSvgButton}
        ]
        self._generate_button_frame("Export", buttons, separator=False)
        self.grid_option_choice = BooleanVar()
        self.sheet_grid_option = Checkbutton(self.ui.right_frame, text="Include grid", variable=self.grid_option_choice, onvalue=True, offvalue=False)
        self.sheet_grid_option.pack()
        self.separators["exports"] = ButtonSeparator(self.ui.right_frame)

    def _create_file_buttons(self):
        buttons = [
            {"text": "save", "data": None, "button_class": SaveButton},
            {"text": "load", "data": None, "button_class": LoadButton},
            {"text": "upload", "data": None, "button_class": UploadButton}
        ]
        self._generate_button_frame("File", buttons)

    def _create_play_buttons(self):
        buttons = [{"text": "Play", "data": None, "button_class": PlayButton}]
        self._generate_button_frame("Play", buttons, separator=False)

    def _create_naming_frame(self):
        self.textboxes["musicname"] = (Entry(self.ui.top_frame1))
        self.textboxes["composername"] = (Entry(self.ui.top_frame2))
        self.textboxbuttons["namebutton"] = (Button(self.ui.top_frame1, text="Add Name", command=lambda: self.ui.add_name()))
        self.textboxbuttons["composerbutton"] = (Button(self.ui.top_frame2, text="Add Composer", command=lambda: self.ui.add_composer()))
        for label in self.textboxbuttons.values():
            label.pack(side = constants.LEFT)
        for box in self.textboxes.values():
            box.pack(side = constants.RIGHT)

    def _generate_button_frame(self, text: str, buttoninfo, label=True, separator=True):
        frame = self.frames[text] = Frame(self.ui.right_frame)
        frame.pack(side=constants.TOP)
        self.frames[text] = frame
        if label:
            self.labels.append(Label(frame, text=text))
        self.buttons_by_frame[text] = []
        for button_spec in buttoninfo:
            button = button_spec['button_class'](button_spec['text'], button_spec['data'], self.ui, self, frame)
            if "Note" in text:
                button.button.pack(side=constants.LEFT)
            else:
                button.button.pack(side=constants.TOP)
            self.buttons[button_spec['text']] = button
            self.buttons_by_frame[text].append(button)
        if separator:
            self.separators[text] = ButtonSeparator(frame)

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
        self.octaves_up = data

    def press(self):
        self.button.config(relief=constants.SUNKEN, state="disabled")
        for b in self.owner.buttons_by_frame["Octave"]:
            if b.text != self.text:
                b.button.config(relief=constants.RAISED, state="normal")

class NoteButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.pitch = data
        self.button = Button(frame, text=self.text, command=self.press)

    def press(self):
        note = Note(self.text, self.pitch, self.ui.active_part.next_position(), self.owner.chosen_lenght) #do we need this active_part to exist -> or part choosing handled by buttons class?
        self.ui.add_note(note)

class LenghtButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.lenght = data
        self.button = Button(frame, text=self.text, command=self.press)

    def press(self):
        self.owner.chosen_lenght = self.lenght
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for b in self.owner.buttons_by_frame["Duration"]:
            if b.text != self.text:
                b.button.config(state="normal", relief=constants.RAISED)

class AddPartButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)

    def press(self):
        self.owner.frames["File"].pack_forget()
        self.owner.frames["Play"].pack_forget()
        i = len(self.ui.music.parts) + 1
        self.owner.separators["Parts"].line.pack_forget()
        if self.ui.music.add_part(i):
            new_button = PartButton(f"Part {i}", i, self.ui, self.owner, self.owner.frames["Parts"])
            self.owner.buttons_by_frame["Parts"].append(new_button)
            new_button.button.pack(side=constants.TOP)
        else:
            new_button = None
        self.owner.separators["Parts"] = ButtonSeparator(self.owner.frames["Parts"])
        self.owner.frames["File"].pack(side=constants.TOP)
        self.owner.frames["Play"].pack(side=constants.TOP)
        self.ui.draw_all_notes()
        if new_button:
            new_button.press()
        if len(self.ui.music.parts) > 3:
            self.button.config(state="disabled", relief=constants.SUNKEN)

class PartButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.part = data

    def press(self):
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for b in self.owner.buttons_by_frame["Parts"]:
            if b.text != self.text and b.text != "Add Part":
                b.button.config(state="normal", relief=constants.RAISED)
        self.ui.active_part = self.ui.music.parts[self.part]
        self.owner.buttons["4th"].press()

class ExportMidiButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)
        self.creator = MidiCreator()
        self.filemanager = FileManager()

    def press(self):
        for part in self.ui.music.parts.values():
            self.creator.create_track(part)
        midi = self.creator.generate_midi()
        self.filemanager.save_midi(midi)

class ExportPdfButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        image_creator = ImageCreator()
        image = image_creator.create_image(self.ui.music, self.owner.grid_option_choice.get())
        filemanager.save_pdf(image)

class ExportSvgButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        svg_creator = SvgCreator()
        svg = svg_creator.create_svg(self.ui.music, self.owner.grid_option_choice.get())
        filemanager.save_svg(svg)

class PlayButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)
        self.player = MidiPlayer()
        self.filemanager = FileManager()
        self.id = 0

    def press(self):
        self.id += 1
        self.creator = MidiCreator()
        for part in self.ui.music.parts.values():
            self.creator.create_track(part)
        midi = self.creator.generate_midi()
        name = "temp" + str(self.id) + ".mid"
        self.filemanager.save_midi(midi, name)
        self.player.play(len(self.ui.music.parts), name)

class SaveButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        data = self.ui.music.convert_to_json()
        filemanager.save_shaku(data)

class LoadButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner)
        self.button = Button(frame, text=self.text, command=self.press)
        self.button.pack(side=constants.TOP)

    def press(self):
        filemanager = FileManager()
        data = filemanager.load()
        if data == None:
            return
        self.ui.load_json(data)
        for button in self.owner.buttons_by_frame["Parts"]:
            if button.text != "Add Part" and str[button.part] not in data['parts'].keys():
                button.button.destroy()
        self.owner.buttons["Part 1"].press()

class UploadButton(ShakuButton):
    def __init__(self, text, data, ui, owner, frame):
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
