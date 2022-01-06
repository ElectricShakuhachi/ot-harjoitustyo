from tkinter import Button, Entry, constants, Frame, ttk, Label, Checkbutton, BooleanVar, Menu
import pygame
import os
from PIL import Image, ImageTk
from services.filing import FileManager
from services.midi_creator import MidiCreator
from services.music_player import MusicPlayer
from services.image_creator import ImageCreator
from services.svg_creator import SvgCreator
from ui.messages import ShakuMessage, ShakuQuery, ShakuQuestion
import config.shaku_constants as consts
from commands.commands import Commands
from ui.ui import UI

class Buttons:
    """Container for user interface Buttons"""
    def __init__(self, main_ui):
        """Construct class attributes and generate default buttons

        Args:
            ui: Main ui container instance
        """
        self.main_ui = main_ui
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
        self.commands = Commands(self.main_ui)
        self._setup_menu(self.main_ui.window)
        self._relay_to_add_part()

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, octave: str):
        if octave not in ["Otsu", "Kan", "Daikan"]:
            raise ValueError("Not a valid shakuhachi notation register")
        self._octave = octave

    def _create_default_buttons(self):
        self._create_naming_frame()
        self._create_octave_buttons()
        self._create_note_buttons()
        self._create_break_buttons()
        self._create_lenght_buttons()
        self._create_part_buttons()
        self._create_play_buttons()

    def _create_octave_buttons(self):
        buttons = []
        for octave in ["Otsu", "Kan", "Daikan"]:
            buttons.append({'text': octave, "button_class": OctaveButton})
        self._generate_button_frame(
            "Octave",
            buttons,
            self.main_ui.frames["right"],
            separator=False
            )
        self.separators["Octave"] = ButtonSeparator(self.main_ui.frames["right"])

    def _create_note_buttons(self):
        frame = self.frames["Notes"] = Frame(self.main_ui.frames["right"])
        frame.pack(side=constants.TOP)
        self.populate_note_buttons(frame, self._octave)
        self.separators["Note"] = ButtonSeparator(self.main_ui.frames["right"])

    def _clear_note_buttons(self):
        old_frames = []
        for key, value in self.frames.items():
            if "Note " in key:
                value.destroy()
                old_frames.append(key)
        for found in old_frames:
            self.frames.pop(found)

    def populate_note_buttons(self, frame, octave):
        """Fill note button frame depending on chosen octave

        Args:
            frame: Frame to put buttons to
            octave: Octave based on which notes are chosen
        """
        self._clear_note_buttons()
        notes = consts.MODE_DATA[os.getenv("MODE")]["NOTES"]
        buttons = {}
        for key in notes:
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
            self._generate_button_frame(f"Note {i}", frame_buttons, frame, separator=False, label=False)
            i += 4

    def _create_break_buttons(self):
        buttons = [{"text": "8th_break", "data": -1, "button_class": NoteButton},
        {"text": "4th_break", "data": -2, "button_class": NoteButton},
        {"text": "half_break", "data": -4, "button_class": NoteButton}
        ]
        if int(os.getenv("MEASURE_LENGHT")) >= 4:
            buttons.append({"text": "whole_break", "data": -8, "button_class": NoteButton})
        self._generate_button_frame("Break", buttons, self.main_ui.frames["right"], separator=False)
        self.separators["Break"] = ButtonSeparator(self.main_ui.frames["right"])

    def _create_lenght_buttons(self):
        buttons = []
        for data, text in consts.LENGHTS.items():
            buttons.append({"text": text, "data": data, "button_class": LenghtButton})
        self._generate_button_frame("Duration", buttons, self.main_ui.frames["right"])

    def _create_part_buttons(self):
        self._generate_button_frame("Parts", None, self.main_ui.frames["right"], separator=False)
        self.separators["Parts"] = ButtonSeparator(self.main_ui.frames["right"])

    def _create_play_buttons(self):
        buttons = [{"text": "Play/Stop", "button_class": PlayButton}]
        self._generate_button_frame("Play", buttons, self.main_ui.frames["right"], separator=False)

    def _create_naming_frame(self):
        self.textboxes["musicname"] = (Entry(self.main_ui.frames["top1"]))
        self.textboxes["composername"] = (Entry(self.main_ui.frames["top2"]))
        self.textboxbuttons["namebutton"] = (
            Button(self.main_ui.frames["top1"], text="Add Name", command=self.add_name)
            )
        self.textboxbuttons["composerbutton"] = (
            Button(self.main_ui.frames["top2"], text="Add Composer", command=self.add_composer)
            )
        for label in self.textboxbuttons.values():
            label.pack(side = constants.LEFT)
        for box in self.textboxes.values():
            box.pack(side = constants.RIGHT)

    def _generate_button_frame(
        self,
        text: str,
        buttoninfo,
        parent_frame,
        label=True,
        separator=True
        ):
        frame = self.frames[text] = Frame(parent_frame)
        frame.pack(side=constants.TOP)
        self.frames[text] = frame
        if label:
            l = Label(frame, text=text)
            l.pack()
            self.labels.append(l)
        self.buttons_by_frame[text] = []
        if buttoninfo:
            for button_spec in buttoninfo:
                if 'data' in button_spec:
                    button = button_spec['button_class'](
                        button_spec['text'],
                        button_spec['data'],
                        self.main_ui,
                        self,
                        frame
                        )
                else:
                    button = button_spec['button_class'](
                    button_spec['text'],
                    self.main_ui,
                    self,
                    frame
                    )
                if "Note" in text or text in ("Parts", "Octave", "Break"):
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
            self.main_ui.music.name = name
        except ValueError:
            self.main_ui.messages.append(ShakuMessage("long_name_and_composer", self.main_ui))
        self.main_ui.draw_texts()

    def add_composer(self, composer=None):
        """Set composer name

        Args:
            composer: Name to be added. If None, composer is fetched from textbox
        """
        if not composer:
            composer = self.textboxes["composername"].get()
        try:
            self.main_ui.music.composer = composer
        except ValueError:
            self.main_ui.messages.append(ShakuMessage("long_name_and_composer", self.main_ui))
        self.main_ui.draw_texts()

    def load_json(self, data):
        """Set name/composer from data and forward to UI

        Args:
            data: JSON -format data
        """
        self.main_ui.load_json(data)
        self.add_name(data['name'])
        self.add_composer(data['composer'])

    def _relay_new(self):
        if not self.saved:
            msg = ShakuQuestion(self.main_ui, self, "proto_keep")
            self.main_ui.messages.append(msg)

    def _load(self, filename=None):
        if not self.saved:
            self.main_ui.messages.append(ShakuQuestion(self.main_ui, self, None))
        else:
            self.load(filename)

    def load(self, filename=None):
        data = self.commands.load(filename=filename)
        if data is None:
            return
        self.load_json(data)
        for button in self.buttons_by_frame["Parts"]:
            button.button.destroy()
        self.partsmenu.entryconfig(0, state=constants.NORMAL)
        self.buttons_by_frame["Parts"] = []
        for part_id in data["parts"].keys():
            self._relay_to_add_part(loading_part=int(part_id))
        self.buttons_by_frame["Parts"][0].press()
        self.saved = True

    def _relay_to_add_part(self, loading_part=None):
        if loading_part is not None:
            i = loading_part
        else:
            i = self.commands.add_part(self.main_ui.music)
        new_button = PartButton(
            i,
            i,
            self.main_ui,
            self,
            self.frames["Parts"]
            )
        self.buttons_by_frame["Parts"].append(new_button)
        new_button.button.pack(side=constants.LEFT)
        if len(self.main_ui.music.parts) >= consts.MAX_PARTS:
            self.partsmenu.entryconfig(0, state=constants.DISABLED)
        self.main_ui.update()
        new_button.press()

    def _relay_to_save(self):
        self.commands.save(self.main_ui.music)

    def _relay_to_save_as(self):
        self.commands.save_as(self.main_ui.music)

    def _relay_to_upload_aws_s3(self):
        result = self.commands.upload_to_aws_s3(self.main_ui.music)        
        self.main_ui.messages.append(ShakuMessage(result, self.main_ui))

    def _relay_to_download_aws_s3(self, item):
        result = self.commands.download_from_aws_s3(item)
        if result == "No Access":
            self.main_ui.messages.append(ShakuMessage(result, self.main_ui))
        else:
            self._load(filename=result)
            os.remove(result)

    def _relay_to_list_aws_s3(self):
        result = self.commands.list_files_in_aws_s3()
        if result == "No Access":
            self.main_ui.messages.append(ShakuMessage(result, self.main_ui))
        else:
            self.main_ui.messages.append(ShakuQuery("Download", result, self, self.main_ui))

    def _relay_to_save_midi(self):
        self.commands.export_midi(self.main_ui.music)

    def _relay_to_save_wav(self):
        self.commands.save_wav(self.main_ui.music)

    def _relay_to_save_svg(self):
        self.commands.export_svg(self.main_ui.music, self.buttons["grid_option_choice"].get())

    def _relay_to_save_pdf(self):
        self.commands.export_pdf(self.main_ui.music, self.buttons["grid_option_choice"].get())

    def _relay_to_play(self):
        self.commands.play_music(self.main_ui.music)

    def relay_set_properties(self):
        self.commands.set_properties(self.main_ui.music, self.main_ui)

    def _dummy_command(self):
        self.main_ui.messages.append(ShakuMessage("dev", self.main_ui))

    def _setup_menu(self, root): #maybe refactor -> get list of texts + their commands
        menu = Menu(root)
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=self._relay_new)
        file_menu.add_command(label="Open", command=self._load)
        file_menu.add_command(label="Save", command=self._relay_to_save)
        file_menu.add_command(label="Save As", command=self._relay_to_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Properties", command=self.relay_set_properties)
        #file_menu.add_command(label="Properties", command=self._dummy_command)
        file_menu.add_separator()
        export_sheet_options_menu = Menu(menu, tearoff=0)
        export_sheet_options_menu.add_command(label="pdf", command=self._relay_to_save_pdf)
        export_sheet_options_menu.add_command(label="svg", command=self._relay_to_save_svg)
        export_sheet_options_menu.add_separator()
        self.buttons["grid_option_choice"] = BooleanVar()
        export_sheet_options_menu.add_checkbutton(
            label="Include grid",
            variable=self.buttons["grid_option_choice"],
            onvalue=True,
            offvalue=False,
            )
        file_menu.add_cascade(label="Export Sheet", menu=export_sheet_options_menu)
        file_menu.add_command(label="Import", command=self._dummy_command)
        file_menu.add_separator()
        export_sound_options_menu = Menu(menu, tearoff=0)
        export_sound_options_menu.add_command(label="midi", command=self._relay_to_save_midi)
        export_sound_options_menu.add_command(label="wav", command=self._relay_to_save_wav)
        file_menu.add_cascade(label="Export Sound", menu=export_sound_options_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Upload", command=self._relay_to_upload_aws_s3)
        file_menu.add_command(label="Download", command=self._relay_to_list_aws_s3)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.main_ui.destroy_all_windows)
        menu.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu, tearoff=0)
        edit_menu.add_command(label="Undo", command=self._dummy_command)
        edit_menu.add_command(label="Redo", command=self._dummy_command)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self._dummy_command)
        edit_menu.add_command(label="Copy", command=self._dummy_command)
        edit_menu.add_command(label="Paste", command=self._dummy_command)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find/Replace", command=self._dummy_command)
        menu.add_cascade(label="Edit", menu=edit_menu)

        insert_menu = Menu(menu, tearoff=0)
        insert_menu.add_command(label="Special notations", command=self._dummy_command)
        insert_menu.add_command(label="Create custom notation", command=self._dummy_command)
        insert_menu.add_command(label="Insert text", command=self._dummy_command)
        menu.add_cascade(label="Insert", menu=insert_menu)

        self.partsmenu = parts_menu = Menu(menu, tearoff=0)
        parts_menu.add_command(label="Add part", command=self._relay_to_add_part)
        parts_menu.add_command(label="Configure parts", command=self._dummy_command)
        menu.add_cascade(label="Parts", menu=parts_menu)

        play_menu = Menu(menu, tearoff=0)
        play_menu.add_command(label="Play / Stop", command=self._relay_to_play)
        play_menu.add_command(label="Playback options", command=self._dummy_command)
        menu.add_cascade(label="Play", menu=play_menu)

        transpose_menu = Menu(menu, tearoff=0)
        transpose_menu.add_command(label="Transpose Up", command=self._dummy_command)
        transpose_menu.add_command(label="Transpose Down", command=self._dummy_command)
        transpose_menu.add_separator()
        transpose_specific_menu = Menu(menu, tearoff=0)
        for i in ["A", "Bb", "B", "c", "c#", "d", "eb", "e", "f", "f#", "g", "g#", "a"]:
            transpose_specific_menu.add_command(label=i, command=self._dummy_command)
        transpose_menu.add_cascade(label="Transpose specific", menu=transpose_specific_menu)
        transpose_menu.add_separator()
        optimize_transposition_menu = Menu(menu, tearoff=0)
        optimize_transposition_menu.add_command(label="Few meri/kari", command=self._dummy_command)
        transpose_menu.add_cascade(label="Optimize", menu=optimize_transposition_menu)
        menu.add_cascade(label="Transpose", menu=transpose_menu)

        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label="Guide", command=self._dummy_command)
        help_menu.add_command(label="Fingering charts", command=self._dummy_command)
        menu.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menu)

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

class OctaveButton():
    """Button for octave and its linked functionality"""
    def __init__(self, text, main_ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        self.main_ui = main_ui
        self.owner = owner
        self.text = text
        self.button = Button(frame, text=self.text, font="Shakunotator", command=self.press)
        #if self.text == "Otsu":
        #   self.button.config(relief=constants.SUNKEN, state="disabled")
        image = Image.open(consts.OCTAVES[self.text])
        scale =  consts.BUTTON_NOTE_SIZE / 1000
        self.pil_img = image.resize([int(scale * s) for s in image.size])
        self.image = ImageTk.PhotoImage(self.pil_img)
        self.button.config(
            image=self.image,
            width=consts.NOTE_BUTTON_SIZE,
            height=consts.NOTE_BUTTON_SIZE
            )

    def press(self, auto_press=False):
        """Configs octave for upcoming notes

        Args:
            auto_press: Set to True if used by program itself
        """
        self.owner.octave = self.text
        self.owner.populate_note_buttons(self.owner.frames["Notes"], self.owner.octave)
        self.button.config(relief=constants.SUNKEN, state="disabled")
        for button in self.owner.buttons_by_frame["Octave"]:
            if button.text != self.text:
                button.button.config(relief=constants.RAISED, state="normal")
        if not auto_press:
            self.main_ui.active_part.clear_pre_existing_notation()
            self.main_ui.active_part.append_misc_notation(self.text)
            self.main_ui.update()

class NoteButton():
    """Button used to add a musical note
    """
    def __init__(self, text, data, main_ui: UI, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: pitch of note
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        self.main_ui = main_ui
        self.owner = owner
        self.text = text
        self.button = Button(frame, text=self.text, font="Shakunotator", command=self.press)
        self.pitch = data
        image = Image.open(consts.MODE_DATA[os.getenv("MODE")]["NOTES"][self.pitch])
        scale = consts.BUTTON_NOTE_SIZE / 1000
        self.pil_img = image.resize([int(scale * s) for s in image.size])
        self.image = ImageTk.PhotoImage(self.pil_img)
        self.button.config(
            image=self.image,
            width=consts.NOTE_BUTTON_SIZE,
            height=consts.NOTE_BUTTON_SIZE
            )

    def press(self):
        """Adds a note on part currently under edition if not full"""
        if self.pitch < 0:
            lenght = abs(self.pitch) * 4
        else:
            lenght = self.owner.chosen_lenght
        if self.main_ui.add_note(self.pitch, lenght):
            self.owner.saved = False

class LenghtButton():
    """Button for choosing a lenght for upcoming musical notes
    """
    def __init__(self, text, data, main_ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: lenght relative to 32th note speed
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        self.main_ui = main_ui
        self.owner = owner
        self.text = text
        self.button = Button(frame, text=self.text, font="Shakunotator", command=self.press)
        self.lenght = data

    def press(self):
        """Choose a lenght for following notes on currently chosen part"""
        self.owner.chosen_lenght = self.lenght
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for button in self.owner.buttons_by_frame["Duration"]:
            if button.text != self.text:
                button.button.config(state="normal", relief=constants.RAISED)

class PartButton():
    """Button for choosing a part (ShakuPart) to edit
    """
    def __init__(self, text, data, main_ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            data: reference to part to be chosen by this button
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        self.main_ui = main_ui
        self.owner = owner
        self.text = text
        self.button = Button(frame, text=self.text, font="Shakunotator", command=self.press)
        self.part = data

    def press(self):
        """Choose musical part in ensemble music to edit"""
        self.button.config(state="disabled", relief=constants.SUNKEN)
        for button in self.owner.buttons_by_frame["Parts"]:
            if button.text not in (self.text, "Add Part"):
                button.button.config(state="normal", relief=constants.RAISED)
        self.main_ui.active_part = self.main_ui.music.parts[self.part]
        self.owner.buttons["4th"].press()

class PlayButton():
    """Button for music playback
    """
    def __init__(self, text, main_ui, owner, frame):
        """Initialize button data and connections

        Args:
            text: Button text
            ui: UI instance
            owner: Container class
            frame: Tkinter frame to show button in
        """
        self.main_ui = main_ui
        self.owner = owner
        self.text = text
        self.button = Button(frame, text=self.text, font="Shakunotator", command=self.press)
        self.player = MusicPlayer()

    def press(self):
        """Play a generated audio of the music currently being edited"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            self.player.play(self.main_ui.music.parts.values())
