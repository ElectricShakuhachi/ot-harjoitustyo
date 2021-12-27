import os
from tkinter import Button, Entry, constants, Frame, ttk, Label, Checkbutton, BooleanVar
import pygame
from PIL import Image, ImageTk
from services.filing import FileManager
from services.midi_creator import MidiCreator
from services.music_player import MusicPlayer
from services.image_creator import ImageCreator
from services.svg_creator import SvgCreator
from ui.messages import ShakuMessage
import config.shaku_constants as consts
from entities.shaku_note import ShakuNote
from entities.shaku_notation import ShakuNotation

class Buttons:
    """Container for user interface Buttons"""
    def __init__(self, ui):
        """Construct class attributes and generate default buttons

        Args:
            ui: Main ui container instance
        """
        self.ui = ui
        self.buttons = {}
        self.frames = {}
        self.buttons_by_frame = {}
        self.textboxes = {}
        self.textboxbuttons = {}
        self.separators = {}
        self.labels = []
        self.chosen_lenght = 8
        self.saved = True
        self._octave = "Otsu"
        self._create_default_buttons()
        self.buttons["Add Part"].press()

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
        for key, octave in enumerate(["Otsu", "Kan", "Daikan"]):
            buttons.append({'text': octave, 'data': key, "button_class": OctaveButton})
        self._generate_button_frame("Octave", buttons, self.ui.frames["right"], separator=False)
        self.separators["Octave"] = ButtonSeparator(self.ui.frames["right"])

    def _create_note_buttons(self):
        frame = self.frames["Notes"] = Frame(self.ui.frames["right"])
        frame.pack(side=constants.TOP)
        self._populate_note_buttons(frame, self._octave)
        self.separators["Note"] = ButtonSeparator(self.ui.frames["right"])

    def _clear_note_buttons(self):
        old_frames = []
        for key, value in self.frames.items():
            if "Note " in key:
                value.destroy()
                old_frames.append(key)
        for found in old_frames:
            self.frames.pop(found)

    def _populate_note_buttons(self, frame, octave):
        self._clear_note_buttons()
        notes = consts.NOTES
        buttons = {}
        for key in notes.keys():
            buttons[key] = {'text': f"Pitch {key}", 'data': key, "button_class": NoteButton}
        if octave == "Otsu":
            mini = 0
            maxi = 13
        elif octave == "Kan":
            mini = 14
            maxi = 30
        elif octave == "Daikan":
            mini = 29
            maxi = 41
        i = mini
        while i < maxi:
            frame_buttons = [buttons[x] for x in range(i, min(i + 4, maxi))]
            self._generate_button_frame(f"Note {i}", frame_buttons, frame, separator=False)
            i += 4

    def _create_break_buttons(self):
        buttons = [{"text": "Break", "data": -1, "button_class": NoteButton},
        {"text": "Break", "data": -2, "button_class": NoteButton}
        ]
        self._generate_button_frame("Break", buttons, self.ui.frames["right"])

    def _create_lenght_buttons(self):
        buttons = []
        for data, text in consts.LENGHTS.items():
            buttons.append({"text": text, "data": data, "button_class": LenghtButton})
        self._generate_button_frame("Duration", buttons, self.ui.frames["right"])

    def _create_part_buttons(self):
        buttons = [
            {"text": "Add Part", "data": None, "button_class": AddPartButton},
        ]
        self._generate_button_frame("Add Part", buttons, self.ui.frames["right"], separator=False)
        self._generate_button_frame("Parts", None, self.ui.frames["right"], separator=False)
        self.separators["Parts"] = ButtonSeparator(self.ui.frames["right"])

    def _create_export_buttons(self):
        buttons = [
            {"text": "export MIDI", "data": None, "button_class": ExportMidiButton},
            {"text": "export PDF", "data": None, "button_class": ExportPdfButton},
            {"text": "export SVG", "data": None, "button_class": ExportSvgButton}
        ]
        self._generate_button_frame("Export", buttons, self.ui.frames["right"], separator=False)
        self.grid_option_choice = BooleanVar()
        self.sheet_grid_option = Checkbutton(self.ui.frames["right"], text="Include grid", variable=self.grid_option_choice, onvalue=True, offvalue=False)
        self.sheet_grid_option.pack()
        self.separators["Export"] = ButtonSeparator(self.ui.frames["right"])

    def _create_file_buttons(self):
        buttons = [
            {"text": "save", "data": None, "button_class": SaveButton},
            {"text": "load", "data": None, "button_class": LoadButton},
            {"text": "upload", "data": None, "button_class": UploadButton}
        ]
        self._generate_button_frame("File", buttons, self.ui.frames["right"])

    def _create_play_buttons(self):
        buttons = [{"text": "Play/Stop", "data": None, "button_class": PlayButton}]
        self._generate_button_frame("Play", buttons, self.ui.frames["right"], separator=False)

    def _create_naming_frame(self):
        self.textboxes["musicname"] = (Entry(self.ui.frames["top1"]))
        self.textboxes["composername"] = (Entry(self.ui.frames["top2"]))
        self.textboxbuttons["namebutton"] = (Button(self.ui.frames["top1"], text="Add Name", command=lambda: self.add_name()))
        self.textboxbuttons["composerbutton"] = (Button(self.ui.frames["top2"], text="Add Composer", command=lambda: self.add_composer()))
        for label in self.textboxbuttons.values():
            label.pack(side = constants.LEFT)
        for box in self.textboxes.values():
            box.pack(side = constants.RIGHT)

    def _generate_button_frame(self, text: str, buttoninfo, parent_frame, label=True, separator=True):
        frame = self.frames[text] = Frame(parent_frame)
        frame.pack(side=constants.TOP)
        self.frames[text] = frame
        if label:
            self.labels.append(Label(frame, text=text))
        self.buttons_by_frame[text] = []
        if buttoninfo:
            for button_spec in buttoninfo:
                button = button_spec['button_class'](button_spec['text'], button_spec['data'], self.ui, self, frame)
                if "Note" in text or text == "Parts" or text == "Octave":
                    button.button.pack(side=constants.LEFT)
                else:
                    button.button.pack(side=constants.TOP)
                self.buttons[button_spec['text']] = button
                self.buttons_by_frame[text].append(button)
        if separator:
            self.separators[text] = ButtonSeparator(frame)

    def add_name(self, name=None):
        """Set composition name

        Args:
            name: Name to be added. If None, name is fetched from textbox
        """
        if not name:
            name = self.textboxes["musicname"].get()
        try:
            self.ui.music.name = name
        except ValueError:
            self.ui.messages.append(ShakuMessage("long_name_and_composer"))
        self.ui.draw_texts()

    def add_composer(self, composer=None):
        """Set composer name

        Args:
            composer: Name to be added. If None, composer is fetched from textbox
        """
        if not composer:
            composer = self.textboxes["composername"].get()
        try:
            self.ui.music.composer = composer
        except ValueError:
            self.ui.messages.append(ShakuMessage("long_name_and_composer"))
        self.ui.draw_texts()

    def load_json(self, data):
        """Set name/composer from data and forward to UI

        Args:
            data: JSON -format data
        """
        self.ui.load_json(data)
        self.add_name(data['name'])
        self.add_composer(data['composer'])

class ButtonSeparator:
    """Horizontal line to separate buttons"""
    def __init__(self, frame, pady=10):
        """Generate horizontal divider line

        Args:
            frame: Tkinter frame to generate line to
            pady: Padding for line. Defaults to 10.
        """
        self.line = ttk.Separator(frame, orient="horizontal")
        self.line.pack(fill="x", pady=pady)

class ShakuButton:
    """Prototype for different types of buttons"""
    def __init__(self, text: str, ui, owner: Buttons, frame):
        """Construct prototype

        Args:
            text: Button text
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        self.ui = ui
        self.owner = owner
        self.text = text
        self.button = Button(frame, text=self.text, font="Shakunotator",  command=self.press)

    def press(self):
        """Dummy method to be overwritten by child class"""
        pass

class OctaveButton(ShakuButton):
    """Button for octave and its linked functionality

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)
        if self.text == "Otsu":
            self.button.config(relief=constants.SUNKEN, state="disabled")
        image = Image.open(consts.OCTAVES[self.text])
        scale =  consts.BUTTON_NOTE_SIZE / 1000
        self.PILimg = image.resize([int(scale * s) for s in image.size])
        self.image = ImageTk.PhotoImage(self.PILimg)
        self.button.config(image=self.image, width=consts.NOTE_BUTTON_SIZE, height=consts.NOTE_BUTTON_SIZE)

    def press(self, auto_press=False):
        """Configs octave for upcoming notes

        Args:
            auto_press: Set to True if used by program itself
        """
        self.owner._octave = self.text
        self.owner._populate_note_buttons(self.owner.frames["Notes"], self.owner._octave)
        self.button.config(relief=constants.SUNKEN, state="disabled")
        for b in self.owner.buttons_by_frame["Octave"]:
            if b.text != self.text:
                b.button.config(relief=constants.RAISED, state="normal")
        if not auto_press:
            self.ui.active_part.clear_pre_existing_notation()
            self.ui.active_part.append_misc_notation(self.text)
            self.ui.update()

class NoteButton(ShakuButton):
    """Button used to add a musical note

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: pitch of note
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)
        self.pitch = data
        image = Image.open(consts.NOTES[self.pitch])
        scale =  consts.BUTTON_NOTE_SIZE / 1000
        self.pil_img = image.resize([int(scale * s) for s in image.size])
        self.image = ImageTk.PhotoImage(self.pil_img)
        self.button.config(image=self.image, width=consts.NOTE_BUTTON_SIZE, height=consts.NOTE_BUTTON_SIZE)

    def press(self):
        """Adds a note on part currently under edition if not full"""
        if self.pitch < 0:
            lenght = abs(self.pitch) * 4
        else:
            lenght = self.owner.chosen_lenght
        note = ShakuNote(self.pitch, self.ui.active_part.next_position(), lenght)
        if self.ui.add_note(note):
            self.owner.saved = False

class LenghtButton(ShakuButton):
    """Button for choosing a lenght for upcoming musical notes

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: lenght relative to 32th note speed
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)
        self.lenght = data

    def press(self):
        """Choose a lenght for following notes on currently chosen part"""
        self.owner.chosen_lenght = self.lenght
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for button in self.owner.buttons_by_frame["Duration"]:
            if button.text != self.text:
                button.button.config(state="normal", relief=constants.RAISED)
        if self.lenght <= 2 or self.lenght >= 16:
            self.owner.buttons["Break"].button.config(state="disabled", relief=constants.SUNKEN)
        else:
            self.owner.buttons["Break"].button.config(state="normal", relief=constants.RAISED)

class AddPartButton(ShakuButton):
    """Button for adding a part on ensemble sheet music

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)

    def _add_part_button(self, part_id):
        new_button = PartButton(part_id, part_id, self.ui, self.owner, self.owner.frames["Parts"])
        self.owner.buttons_by_frame["Parts"].append(new_button)
        new_button.button.pack(side=constants.LEFT)
        return new_button

    def press(self, loading_part=None):
        """Add a part on sheet music being edited

        Args:
            loading_part: id of part being loaded (when parts added on load).
        """
        if loading_part is None:
            i = len(self.ui.music.parts) + 1
            if not self.ui.music.add_part(i):
                self.ui.messages.append(ShakuMessage("No Part Room"))
                return
            new_button = self._add_part_button(i)
        else:
            new_button = self._add_part_button(loading_part)
        self.ui.update()
        if new_button and not loading_part:
            new_button.press()
        if len(self.ui.music.parts) > 3:
            self.button.config(state="disabled", relief=constants.SUNKEN)

class PartButton(ShakuButton):
    """Button for choosing a part (ShakuPart) to edit

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        super().__init__(text, ui, owner, frame)
        """Initialize button data and connections

        Args:
            text: Button text
            data: reference to part to be chosen by this button
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        self.part = data

    def press(self):
        """Choose musical part in ensemble music to edit"""
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for button in self.owner.buttons_by_frame["Parts"]:
            if button.text not in (self.text, "Add Part"):
                button.button.config(state="normal", relief=constants.RAISED)
        self.ui.active_part = self.ui.music.parts[self.part]
        self.owner.buttons["4th"].press()

class ExportMidiButton(ShakuButton):
    """Button for exporting music in midi form

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)
        self.creator = MidiCreator()
        self.filemanager = FileManager()

    def press(self):
        """Export currently edited music to MIDI -format file"""
        for part in self.ui.music.parts.values():
            self.creator.create_track(part)
        midi = self.creator.generate_midi()
        self.filemanager.save_midi(midi)

class ExportPdfButton(ShakuButton):
    """Button for exporting sheet in pdf form

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)

    def press(self):
        """Export currently edited music sheet to PDF -format file"""
        filemanager = FileManager()
        image_creator = ImageCreator()
        image = image_creator.create_image(self.ui.music, self.owner.grid_option_choice.get())
        filemanager.save_pdf(image)

class ExportSvgButton(ShakuButton):
    """Button for exporting sheet in svg form

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)

    def press(self):
        """Export currently edited music sheet to SVG -format file"""
        filemanager = FileManager()
        svg_creator = SvgCreator()
        svg = svg_creator.create_svg(self.ui.music, self.owner.grid_option_choice.get())
        filemanager.save_svg(svg)

class PlayButton(ShakuButton):
    """Button for music playback

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)
        self.player = MusicPlayer()

    def press(self):
        """Play a generated audio of the music currently being edited"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            self.player.play(self.ui.music.parts.values())

class SaveButton(ShakuButton):
    """Button for saving .shaku (JSON) -data

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)

    def press(self):
        """Save currently edited music sheet to .shaku (JSON) -file"""
        filemanager = FileManager()
        data = self.ui.music.convert_to_json()
        if filemanager.save_shaku(data):
            self.owner.saved = True

class LoadButton(ShakuButton):
    """Button for loading .shaku (JSON) -data

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)

    def press(self):
        """Load a .shaku (JSON) -file to edit in software"""
        if not self.owner.saved:
            self.ui.messages.append(ShakuMessage("Overwrite"))
        filemanager = FileManager()
        data = filemanager.load()
        self.ui.clear_messages()
        if data is None:
            return
        if data == "JSON Error" or not self.ui.music.data_correct(data):
            self.ui.messages.append(ShakuMessage("Incorrect File"))
            return
        self.owner.load_json(data)
        for button in self.owner.buttons_by_frame["Parts"]:
            if button.text != "Add Part":
                button.button.destroy()
        self.owner.buttons_by_frame["Parts"] = [self.owner.buttons["Add Part"]]
        for part_id in data["parts"].keys():
            self.owner.buttons["Add Part"].press(loading_part=int(part_id))
        self.owner.buttons_by_frame["Parts"][1].press()

class UploadButton(ShakuButton):
    """Button for uploading to AWS S3

    Args:
        ShakuButton: Button prototype
    """
    def __init__(self, text, data, ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: dummy attribute
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        super().__init__(text, ui, owner, frame)

    def press(self):
        """Upload currently edited music sheet to .shaku (JSON) -file to AWS S3"""
        filemanager = FileManager()
        data = self.ui.music.convert_to_json()
        name = self.ui.music.name
        if not name or name == "":
            self.ui.messages.append(ShakuMessage("No Name"))
        elif not filemanager.upload_to_aws_s3(data, name=name):
            self.ui.messages.append(ShakuMessage("No Access"))
