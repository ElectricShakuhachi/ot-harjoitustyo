import os
from svgwrite import Drawing, text, image
import config.shaku_constants as consts
from entities.shaku_music import ShakuMusic
from services.conversions import GraphicsConverter
from services.image_creator import ImageCreator
from services.positioning import ShakuPositions
from services.time_notation import ShakuRhythmNotation
from entities.shaku_note import ShakuNote

class SvgCreator:
    """Class for generating an svg -format vector graphics drawing of sheet music

    Attributes:
        svg = svgwrite.Drawing -instance - representation of an svg -format vector drawing
    """
    def __init__(self):
        """Constructor, initializes svg-attribute as placeholder"""
        self._svgs = {}
        self._pos = ShakuPositions()
        self._scaler = GraphicsConverter().scale

    def _rgb(self, numbers: tuple):
        """Converts a tuple of three numbers into rgb format

        Args:
            numbers: three numbers in a tuple describing rgb values

        Returns:
            A string "rgb(x, y, z)" where each x, y, z is a given number
        """
        rgb_string = "rgb("
        for i in numbers:
            if i < 0 or i > 255:
                raise ValueError("Not a valid rgb number")
            rgb_string += str(i) + ","
        rgb_string = rgb_string[:-1] + ")"
        return rgb_string

    def _draw_line(self, page: Drawing, line: tuple, width: int, fill: tuple):
        """Draws a line on svg image

        Args:
            line: Tuple describiling line by cooridinates of its ends
            width: Line width
            fill: Line color
        """
        if len(line) == 6:
            start_x = int(line[0])
            start_y = int(line[1])
            mid_x = int(line[2])
            mid_y = int(line[3])
            end_x = int(line[4])
            end_y = int(line[5])
            d = f"M{start_x},{start_y} S{mid_x},{mid_y} {end_x},{end_y}"
            page.add(page.path(d=d, stroke=self._rgb(fill), stroke_width=width, fill="none"))
        elif len(line) == 2:
            page.add(page.line(line[0], line[1], stroke=self._rgb(fill), stroke_width=width))
        elif len(line) == 4:
            start = (line[0], line[1])
            end = (line[2], line[3])
            page.add(page.line(start, end, stroke=self._rgb(fill), stroke_width=width))
        else:
            raise ValueError("Unexpected amount of values in line")

    def _draw_text(self, page: int, text_insert: str, position: tuple, fill: tuple, font_size: int, style=None):
        """Insert text on svg image with given properties

        Args:
            page: page to insert text to
            text_insert: Text to be drawn on svg
            position: Coordinates where text is to be drawn
            fill: Text color
            font_size: Font size
        """
        if page not in self._svgs:
            self._svgs[page] = self._page()
        self._svgs[page].add(text.Text(
            text_insert,
            insert=position,
            fill=self._rgb(fill),
            font_size=str(font_size),
            style=style)
            )

    def _draw_note(self, page: Drawing, file: str, position: tuple):
        """Draw a shakuhachi sheet music note from image onto svg sheet

        Args:
            page: svg drawing to draw to
            file: path to image resource
            position: Coordinates where note is to be drawn
        """
        note_size = self._scaler(consts.SHEET_NOTE_SIZE)
        note_size += consts.EXPORT_NOTE_FONT_SIZE_INCREMENT
        size = [note_size for i in range(2)]
        pos = (position[0] + self._scaler(consts.EXPORT_NOTE_CORRECTION_ON_X_AXIS), position[1])
        page.add(image.Image(file, pos, size))

    def _draw_texts(self, name, composer):
        """Draw sheet music name and composer on svg

        Args:
            music: Shakuhachi sheet music description in Shakunotators Music -instance form
        """
        font_size = self._scaler(consts.TEXT_FONT_SIZE)
        name_pos = self._scaler(consts.NAME_POSITION)
        self._draw_text(1, name, name_pos, consts.TEXT_COLOR, font_size, style="text-anchor:end")
        composer_pos = self._scaler(consts.COMPOSER_POSITION)
        self._draw_text(1, composer, composer_pos, consts.TEXT_COLOR, font_size)

    def _create_grid(self, spacing: int, page: Drawing):
        """Draws musical measure grid on svg image

        Args:
            spacing: Width of each section of grid (1 unit = 80px)
        """
        measure_lenght = consts.MEASURE_LENGHT
        ImageCreator().draw_grid(spacing, measure_lenght, page, self._draw_line)

    def _page(self):
        """Get a new page"""
        return Drawing(size=(consts.EXPORT_SHEET_SIZE))

    def create_svg(self, music: ShakuMusic, grid_included: bool=False, mode: str="Tozan"):
        """Generates an svg -format vector graphics drawings of sheet music

        Args:
            music: Shakuhachi sheet music as ShakuMusic instance
            grid_included: True if measure grid will be included. Defaults to False.

        Returns:
            a list of svg formatted data, a page each from shakuhachi sheet music data 
        """
        measures = consts.MODE_DATA[os.getenv("MODE")]["MEASURES"]
        if music is None:
            raise TypeError("No music instance provided")
        rows = self._pos.get_row_count(music.spacing)
        slots = self._pos.get_slot_count(measures)
        for part in music.parts.values():
            rel_pos = self._pos.get_relative_positions([note.lenght for note in part.notes], rows, slots, measures)
            for i in range(len(part.notes)):
                page = rel_pos[i]["page"] + 1 # REMEMBER TO REMOVE THIS + 1 stuff
                if page not in self._svgs:
                    self._svgs[page] = self._page()
                position = self._scaler(self._pos.get_coordinates(rel_pos[i], part.part_no, music.spacing, measures))
                img_file = consts.MODE_DATA[os.getenv("MODE")]["NOTES"][part.notes[i].pitch]
                self._draw_note(self._svgs[page], img_file, position)
        self._draw_texts(music.name, music.composer)
        if grid_included:
            for page in self._svgs.values():
                self._create_grid(music.spacing, page)
        self._draw_all_time_notations(music)
        return self._svgs

    def _draw_time_notation(self, notation, page):
        fill = consts.NOTE_COLOR
        width = consts.RHYTHM_NOTATION_WIDHT_EXPORT
        page = self._svgs[page]
        self._draw_line(page, notation, width, fill)

    def _draw_all_time_notations(self, music: ShakuMusic):
        measures = consts.MODE_DATA[os.getenv("MODE")]["MEASURES"]
        mode = os.getenv("MODE")
        rhy = ShakuRhythmNotation(mode)
        pos = ShakuPositions()
        rows = pos.get_row_count(music.spacing)
        slots = pos.get_slot_count(measures)

        for part in music.parts.values():
            rel_pos = pos.get_relative_positions([note.lenght for note in part.notes], rows, slots, measures)
            posses = [pos.get_coordinates(i, part.part_no, music.spacing, measures) for i in rel_pos]
            if mode == "Tozan":
                i = 0
                while i < len(part.notes):
                    orig_i = i
                    page = rel_pos[i]["page"]
                    while i < len(part.notes) and rel_pos[i]["page"] == page:
                        i += 1
                    temp_posses = [posses[x] for x in range(orig_i, i)]
                    temp_notes = [part.notes[x] for x in range(orig_i, i)]
                    notations = rhy.tozan_rhytms(temp_notes, temp_posses)
                    for notation in notations:
                        if isinstance(notation[0], ShakuNote): # "ghost note", a note needs to be redrawn after measure line
                            note = notation[0]
                            position = list(notation[1])
                            if position[1] == consts.PARTS_Y_START:
                                position[0] -= music.spacing * consts.NOTE_ROW_SPACING
                            position = self._scaler(position)
                            img_file = consts.NOTES[note.pitch]
                            self._draw_note(self._svgs[page + 1], img_file, tuple(position))
                        else:
                            notation = self._scaler(notation)
                            self._draw_time_notation(notation, page + 1)