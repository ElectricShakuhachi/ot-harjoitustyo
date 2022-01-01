from tkinter import constants, Frame, Canvas, Tk, Scrollbar
from PIL import Image, ImageTk
from entities.shaku_music import ShakuMusic
from entities.shaku_note import ShakuNote
from entities.shaku_part import ShakuPart
from entities.shaku_notation import ShakuNotation
from ui.messages import ShakuMessage
import config.shaku_constants as consts
from services.conversions import GraphicsConverter as convert
from services.positioning import ShakuPositions

class SheetCanvas(Frame):
    def __init__(self, frame):
        Frame.__init__(self, frame)
        self.sheet = Canvas(
            self,
            background="dark gray",
            width=consts.SHEET_SIZE[0] + 20,
            height=consts.SHEET_SIZE[1] + 10
        )
        self.frame = Frame(self.sheet, background="dark gray")
        self.y_scroll = Scrollbar(self, orient="vertical", command=self.sheet.yview)
        self.x_scroll = Scrollbar(self, orient="horizontal", command=self.sheet.xview)
        self.sheet.configure(yscrollcommand=self.y_scroll.set, xscrollcommand=self.x_scroll.set)
        self.y_scroll.pack(side="right", fill="y")
        self.x_scroll.pack(side="bottom", fill="x")
        self.sheet.pack(side="left", fill="both")
        self.sheet.create_window((5, 5), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", self.resize_scroll)
        self.pages = {}
        self.add_page(1)

    def resize_scroll(self, event):
        self.sheet.configure(scrollregion=self.sheet.bbox("all"))

    def add_page(self, number, spacing=2):
        page = Page(self.frame, spacing)
        self.pages[number] = page

    def clear_pages(self):
        for page in self.pages.values():
            page.clear()

    def draw_title_text(self, position, text, anchor, page):
        font = consts.TEXT_FONT + " " + str(consts.TEXT_FONT_SIZE)
        return page.page.create_text(position, text=text, fill="black", anchor=anchor, font=font)

class Page():
    def __init__(self, frame, spacing=2):
        width=consts.SHEET_SIZE[0]
        height=consts.SHEET_SIZE[1]
        self.page = Canvas(
            frame,
            width=width,
            height=height,
            background="white",
        )
        self.page.pack(side="right", padx=3, pady=5)
        self.spacing = spacing
        self.clear()

    def clear(self):
        self.page.delete("all")
        self.texts = {}
        self._note_notations = []
        self._time_notations = []
        self._misc_notations = []
        self._grid = self._create_grid(self.page, self.spacing)

    def _draw_grid_line(self, line: tuple, target_page: Canvas):
        return target_page.create_line(
            line,
            fill=convert().rgb_to_hex(consts.GRID_COLOR),
            width=consts.GRID_LINE_WIDHT
            )

    def _create_grid(self, target_page: Canvas, spacing, measure_lenght=consts.MEASURE_LENGHT):
        x_axis = list(consts.GRID_X)
        y_axis = list(consts.GRID_Y)
        x_axis[1] -= (x_axis[1] - x_axis[0]) % (consts.NOTE_ROW_SPACING * spacing)
        grid = []
        increment = consts.NOTE_ROW_SPACING * spacing
        for temp_x in range(x_axis[0], x_axis[1] + 3, increment):
            grid.append(self._draw_grid_line((temp_x, y_axis[0], temp_x, y_axis[1]), target_page))
        increment = consts.VERTICAL_SPACE_PER_FOURTH_NOTE * measure_lenght
        for temp_y in range(y_axis[0], y_axis[1] + 1, increment):
            grid.append(self._draw_grid_line((x_axis[0], temp_y, x_axis[1], temp_y), target_page))
        return grid

    def _draw_image(self, image, position):
        return self.page.create_image(
            position[0]-2, position[1]-3,
            anchor=constants.NW, image=image
            )

    def _draw_note(self, image, position):
        self._note_notations.append(self._draw_image(image, position))

    def draw_misc_notation(self, image, position):
        """Draw a non-pitch, non-duration shakuhachi sheet music notation on sheet

        Args:
            notation: Reference to ShakuNotation instance describing notation
        """
        self._misc_notations.append(self._draw_image(image, position))

class UI:
    """Tkinter UI for Shakunotator

    Attributes:
        frames: Subframes where UI parts are divided to
        messages: Error / Warning -messages displayed as Tkinter windows
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
        self._music = ShakuMusic()
        #self._window.geometry(consts.MAIN_WINDOW_SIZE) #maybe no need for constant size?
        self._frames = self.generate_frames()
        self._sheet_holder = SheetCanvas(self.frames["left"])
        self._sheet_holder.pack(side="top", fill="both", expand=True, padx=10, pady=20)
        self._messages = []
        self._active_part = None
        self._note_images = {}
        self._notation_images = {}
        self._load_images()

    @property
    def window(self):
        """Get tkinter root window utilized by UI"""
        return self._window

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
        frames["left"].pack(expand=True, fill=constants.BOTH, side=constants.LEFT)
        frames["right"].pack(side=constants.RIGHT)
        return frames

    def draw_misc_notation(self, notation: ShakuNotation, part: ShakuPart):
        """Draw a non-pitch, non-duration shakuhachi sheet music notation on sheet

        Args:
            notation: Reference to ShakuNotation instance describing notation
        """
        image = self._notation_images[notation.notation_type]
        if len(part.notes) > notation.relative_note:
            note_pos = part.notes[notation.relative_note].position
        else:
            note_pos = part.next_position()
        position = tuple(note_pos[i] + notation.position[i] for i in range(2))
        page = self._sheet_holder.pages[notation.page]
        page.draw_notation(image, position)

    def add_note(self, note: ShakuNote):
        """Add note into music model and draw it on sheet

        Args:
            note: A Representation of a musical note

        Returns:
            False if sheet was full, True if note was added
        """
        self._active_part.add_note(note)
        self.update()

    def _draw_time_notation(self, line, page):
        page = self._sheet_holder.pages[page]
        fill = convert().rgb_to_hex(consts.NOTE_COLOR)
        width = 2 # get from consts instead?
        page.page.create_line(line, fill=fill, width=width)

    def _draw_all_time_notations(self):
        for part in self.music.parts.values():
            for notation in part.part_time_notations():
                for line in notation.lines:
                    self._draw_time_notation(line, notation.page)

    def TEMP_draw_all_notes(self):
        for part in self.music.parts.values():
            for note in part.notes:
                self._draw_note(note)
        self._draw_all_time_notations()

    def TEMP_draw_note(self, note: ShakuNote):
        image = self._note_images[note.pitch]
        if note.page > len(self._sheet_holder.pages):
            self._sheet_holder.add_page(note.page, self.music.spacing)
        page = self._sheet_holder.pages[note.page]
        page._draw_note(image, note.position)

    def _draw_note(self, pitch, page_no, position):
        image = self._note_images[pitch]
        if page_no > len(self._sheet_holder.pages):
            self._sheet_holder.add_page(page_no, self.music.spacing)
        page = self._sheet_holder.pages[page_no]
        page._draw_note(image, position)

    def _draw_all_notes(self):
        measures = True # base this on consts and later user prefs instead
        positioner = ShakuPositions()
        rows = positioner.get_row_count(self.music.spacing)
        slots = positioner.get_slot_count(measures)
        for part in self.music.parts.values():
            rel_pos = positioner.get_relative_positions(part.notes, rows, slots, measures)
            for i in range(len(part.notes)):
                page = rel_pos[i]["page"]
                position = positioner.get_coordinates(rel_pos[i], part.part_no, self.music.spacing, measures)
                self._draw_note(part.notes[i].pitch, page + 1, position)

        self._draw_all_time_notations()

    def _draw_all_misc_notations(self):
        for part in self.music.parts.values():
            for notation in part.notations:
                self.draw_misc_notation(part, notation)

    def update(self):
        """Update sheet based on its music instance data"""
        for page in self._sheet_holder.pages.values():
            page.spacing = self.music.spacing
        self._sheet_holder.clear_pages()
        self._draw_all_notes()
        self._draw_all_misc_notations()
        self.draw_texts()

    def draw_texts(self):
        """Draw name and composer on sheet"""
        self._erase_title_texts()
        front_page = self._sheet_holder.pages[1]
        name_pos = consts.NAME_POSITION
        front_page.texts["name"] = self._sheet_holder.draw_title_text(name_pos, self.music.name, constants.NE, front_page)
        composer_pos = consts.COMPOSER_POSITION
        composer = self.music.composer
        front_page.texts["composer"] = self._sheet_holder.draw_title_text(composer_pos, composer, constants.NW, front_page)

    def _erase_title_texts(self):
        front_page = self._sheet_holder.pages[1]
        for text in front_page.texts.values():
            front_page.page.delete(text)

    def load_json(self, data): #needs update
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
        """Remove all existing message windows"""
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
        pil_img = img.resize([int(resizing * size) for size in img.size])
        image = ImageTk.PhotoImage(pil_img)
        return image
