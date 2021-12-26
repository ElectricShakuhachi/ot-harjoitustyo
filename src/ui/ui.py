from tkinter import constants, Frame, Canvas, Tk
from PIL import Image, ImageTk
from entities.shaku_music import ShakuMusic
from entities.shaku_note import ShakuNote
from entities.shaku_part import ShakuPart
from entities.shaku_notation import ShakuNotation
from ui.messages import ShakuMessage
import config.shaku_constants as consts

class UI:
    """Tkinter UI for Shakunotator

    Attributes:
        frames: Subframes where UI parts are divided to
        messages: Error / Warning -messages (list of ShakuMessage instances) displayed as Tkinter windows
        note_notations: List of Tkinter Canvas objects : Shakuhachi musical pitch notes drawn on sheet
        time_notations: List of Tkinter Canvas objects : Shakuhachi musical duration notations drawn on sheet
        music: ShakuMusic -instance - representation of Shakuhachi sheet music
        active_part: Musical part of shakuhachi notation which is under editing
        grid: Shakuhachi sheet musical measure grid
    """
    def __init__(self, window: Tk):
        """Constructor, sets up necessary class attributes

        Args:
            window: tkinter root window
        """
        self._window = window
        self._window.geometry(consts.MAIN_WINDOW_SIZE)
        self._frames = self.generate_frames()
        self._sheet = self._create_sheet()
        self._name = None
        self._composer = None
        self._messages = []
        self._note_notations = []
        self._time_notations = []
        self._misc_notations = []
        self._music = ShakuMusic()
        self._active_part = None
        self._grid = []
        self._grid = self._create_grid()
        self._note_images = {}
        self._notation_images = {}
        self._load_images()

    @property
    def grid(self):
        """Get grid - Shakuhachi sheet musical measure grid in use by UI"""
        return self._grid

    @grid.setter
    def grid(self, newgrid):
        """Set grid - Shakuhachi sheet musical measure grid in use by UI"""
        self._grid = newgrid

    @property
    def music(self):
        """Get music (ShakuMusic -instance connected to UI)"""
        return self._music

    @music.setter
    def music(self, music: ShakuMusic):
        """Set music (ShakuMusic -instance connected to UI)"""
        self._music = music

    @property
    def frames(self):
        """Get the Tkinter frames UI objects are divided to"""
        return self._frames

    @property
    def messages(self):
        """Get existing error / warning -messages (list of ShakuMessage instances)"""
        return self._messages

    @messages.setter
    def messages(self, newlist: list):
        """Set existing error / warning -messages (list of ShakuMessage instances)"""
        for value in newlist:
            if isinstance(value, ShakuMessage):
                raise ValueError("Only accepting ShakuMessage instances into UI messages")
        self._messages = newlist

    @property
    def active_part(self):
        """Get musical part of shakuhachi notation which is under editing"""
        return self._active_part

    @active_part.setter
    def active_part(self, new_part):
        """Set musical part of shakuhachi notation which is under editing"""
        self._active_part = new_part

    def generate_frames(self):
        """Generate Tkinter frames for divided UI objects to"""
        frames = {
            "top1": Frame(self._window),
            "top2": Frame(self._window),
            "left": Frame(self._window, padx=20),
            "right": Frame(self._window, padx=20)
        }
        frames["top1"].pack(side=constants.TOP)
        frames["top2"].pack(side=constants.TOP)
        frames["left"].pack(side=constants.LEFT)
        frames["right"].pack(side=constants.RIGHT)
        return frames

    def _create_sheet(self):
        sheet = Canvas(
            self._frames["left"],
            width=consts.SHEET_SIZE[0],
            height=consts.SHEET_SIZE[1],
            background="white",
        )
        sheet.pack(side = constants.LEFT)
        return sheet

    def _rgb_to_hex(self, rgb: tuple):
        return "#%02x%02x%02x" % rgb

    def _draw_grid_line(self, line: tuple):
        #print(f"Printing line {line}")
        return self._sheet.create_line(line, fill=self._rgb_to_hex(consts.GRID_COLOR), width=consts.GRID_LINE_WIDHT)

    def _create_grid(self, measure_lenght=consts.MEASURE_LENGHT):
        spacing = self.music.spacing
        x_axis = list(consts.GRID_X)
        y_axis = list(consts.GRID_Y)
        x_axis[1] -= (x_axis[1] - x_axis[0]) % (consts.NOTE_ROW_SPACING * spacing)
        grid = []
        for temp_x in range(x_axis[0], x_axis[1] + 3, consts.NOTE_ROW_SPACING * spacing):
            grid.append(self._draw_grid_line((temp_x, y_axis[0], temp_x, y_axis[1])))
        for temp_y in range(y_axis[0], y_axis[1] + 1, consts.VERTICAL_SPACE_PER_FOURTH_NOTE * measure_lenght):
            grid.append(self._draw_grid_line((x_axis[0], temp_y, x_axis[1], temp_y)))
        return grid

    def _draw_image(self, image, position): # check if we still need these -2 and -3 => might be we remove in PDF, svg too and adjust in consts?
        return self._sheet.create_image(position[0]-2, position[1]-3, anchor=constants.NW, image=image)

    def _draw_note(self, note: ShakuNote):
        image = self._note_images[note.pitch]
        self._note_notations.append(self._draw_image(image, note.position))
        self._draw_all_time_notations()

    def draw_misc_notation(self, part: ShakuPart, notation: ShakuNotation):
        """Draw a non-pitch, non-duration shakuhachi sheet music notation on sheet

        Args:
            notation: Reference to ShakuNotation instance describing notation
        """
        image = self._notation_images[notation.type]
        if len(part.notes) > notation.relative_note:
            note_pos = part.notes[notation.relative_note].position
        else:
            note_pos = part.next_position()
        position = tuple(note_pos[i] + notation.position[i] for i in range(2))
        self._misc_notations.append(self._draw_image(image, position))

    def add_note(self, note: ShakuNote):
        """Add note into music model and draw it on sheet

        Args:
            note: A Representation of a shakuhachi sheet music notation in the form of a ShakuNote instance

        Returns:
            False if sheet was full, True if note was added
        """
        status = self._active_part.add_note(note)
        if status:
            self._draw_note(note)
            return True
        self._messages.append(ShakuMessage("Full Sheet"))
        return False

    def _draw_all_time_notations(self):
        for line in self._time_notations:
            self._sheet.delete(line)
        self._time_notations = []
        for part in self.music.parts.values():
            for notation in part.part_time_notations():
                for line in notation:
                    self._time_notations.append(self._sheet.create_line(line[0][0], line[0][1], line[1][0], line[1][1], fill=self._rgb_to_hex(consts.NOTE_COLOR), width=2))

    def _draw_all_notes(self):
        for notation in self._note_notations:
            self._sheet.delete(notation)
        self._note_notations = []
        for part in self.music.parts.values():
            for note in part.notes:
                self._draw_note(note)
        self._draw_all_time_notations()

    def _draw_all_misc_notations(self):
        for notation in self._misc_notations:
            self._sheet.delete(notation)
        self._misc_notations = []
        for part in self.music.parts.values():
            for notation in part.notations:
                self.draw_misc_notation(part, notation)

    def update(self):
        """Update sheet based on its music instance data"""
        self._sheet.delete("all")
        self._create_grid()
        self._draw_all_notes()
        self._draw_all_misc_notations()
        self.draw_texts()

    def _draw_text(self, position, text, anchor):
        return self._sheet.create_text(position, text=text, fill="black", anchor=anchor, font=(consts.TEXT_FONT + " " + str(consts.TEXT_FONT_SIZE)))

    def draw_texts(self):
        """Draw name and composer on sheet"""
        self._erase_texts()
        self._name = self._draw_text(consts.NAME_POSITION, self.music.name, constants.NE)
        composer_pos = consts.COMPOSER_POSITION
        composer = self.music.composer
        self._composer = self._draw_text(composer_pos, composer, constants.NW)

    def _erase_texts(self):
        if self._name is not None:
            self._sheet.delete(self._name)
        if self._composer is not None:
            self._sheet.delete(self._composer)

    def load_json(self, data):
        """Update sheet based on loaded JSON data

        Args:
            data: JSON -format data describing ShakuMusic format
        """
        self.music = ShakuMusic()
        self.music.load_json(data)
        self._sheet.delete('all')
        self._create_grid()
        self._draw_all_notes()

    def clear_messages(self):
        for message in self._messages:
            message.disactivate()
        self._messages = []

    def _load_images(self):
        self._load_note_images()
        self._load_octave_images()

    def _load_octave_images(self):
        for key, image in consts.OCTAVES.items():
            image = self._load_image(image)
            self._notation_images[key] = image

    def _load_note_images(self):
        for key, image in consts.NOTES.items():
            image = self._load_image(image)
            self._note_images[key] = image

    def _load_image(self, image, resizing=None):
        img = Image.open(image)
        if not resizing:
            resizing = consts.SHEET_NOTE_SIZE / 1000
        pil_img = img.resize([int(resizing * size) for size in img.size]) #need to be a class attr?
        image = ImageTk.PhotoImage(pil_img)
        return image
