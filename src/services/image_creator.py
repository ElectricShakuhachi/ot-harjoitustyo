import os
from PIL import Image, ImageFont, ImageDraw
import config.shaku_constants as consts
from entities.shaku_music import ShakuMusic
from entities.shaku_note import ShakuNote
from services.conversions import GraphicsConverter
from services.positioning import ShakuPositions
from services.time_notation import ShakuRhythmNotation

class ImageCreator:
    """Class for generating production grade image of sheet music

    Attributes:
        image: PIL Image instance for sheet base
        font: Font for text on image
        draft: PIL ImageDraw instance for drawing lines and text on image
    """
    def __init__(self):
        """Constructor, generates necessary PIL instances"""
        self._images = {}
        self._drafts = {}
        self._pos = ShakuPositions()
        self._scaler = GraphicsConverter().scale
        font_size = self._scaler(consts.SHEET_NOTE_SIZE) + consts.EXPORT_NOTE_FONT_SIZE_INCREMENT
        self._note_font = ImageFont.truetype(consts.NOTE_FONT, font_size)
        self._text_font = ImageFont.truetype(consts.TEXT_FONT, self._scaler(consts.TEXT_FONT_SIZE))

    def _add_image(self, key: int):
        self._images[key] =Image.new("RGB", consts.EXPORT_SHEET_SIZE, (255, 255, 255))

    def _add_draft(self, key: int, image):
        self._drafts[key] = ImageDraw.Draw(image)

    def _draw_grid_line(self, page, line: tuple, width, fill):
        """Draws one line of musical measure grid on image

        Args:
            line: tuple description of line endpoint coordinates
        """
        page.line(line, width=width, fill=fill)

    def draw_grid(self, spacing: int, measure_lenght: int, page, drawing_function):
        """Draw a musical measure grid on image using injected function

        Args:
            spacing: Width of each section of grid (1 unit = 80px)
            measure_lenght: Height of each section of grid (1 unit = 220px)
            drawing_function: Function used for drawing grid
        """
        x_axis = list(self._scaler(consts.GRID_X))
        y_axis = list(self._scaler(consts.GRID_Y))
        x_axis[1] -= (x_axis[1] - x_axis[0]) % (self._scaler(consts.NOTE_ROW_SPACING) * spacing)
        increment = self._scaler(consts.NOTE_ROW_SPACING) * spacing
        for temp_x in range(x_axis[0], x_axis[1] + 3, increment):
            drawing_function(
                page,
                ((temp_x, y_axis[0]), (temp_x, y_axis[1])),
                self._scaler(consts.GRID_LINE_WIDHT), consts.GRID_COLOR
                )
        increment = self._scaler(consts.VERTICAL_SPACE_PER_FOURTH_NOTE) * measure_lenght
        for temp_y in range(y_axis[0], y_axis[1] + 1, increment):
            drawing_function(
                page,
                ((x_axis[0], temp_y), (x_axis[1], temp_y)),
                self._scaler(consts.GRID_LINE_WIDHT), consts.GRID_COLOR
                )

    def create_images(self, music: ShakuMusic, grid_included: bool=False):
        """Receives musical notation, scales it, re-aligns it and draws it on PIL Image

        Args:
            music: ShakuMusic instance containing notations, name and composer to draw on image
            grid_included: If True, a measure grid is drawn on sheet music image. Defaults to False.

        Returns:
            PIL Image instance with given details drawn on it
        """
        measures = consts.MODE_DATA[os.getenv("MODE")]["MEASURES"]
        if music is None:
            raise TypeError("No music instance provided")
        rows = self._pos.get_row_count(music.spacing)
        slots = self._pos.get_slot_count(measures)
        for part in music.parts.values():
            rel_pos = self._pos.get_relative_positions([note.lenght for note in part.notes], rows, slots, measures)
            for i in range(len(part.notes)):
                page = rel_pos[i]["page"] + 1
                if page not in self._images:
                    self._add_image(page)
                    self._add_draft(page, self._images[page])
                position = self._pos.get_coordinates(rel_pos[i], part.part_no, music.spacing, measures)
                x_axis, y_axis = self._scaler(position)
                x_axis += consts.EXPORT_NOTE_CORRECTION_ON_X_AXIS
                text = consts.NOTE_TEXT_CODES[part.notes[i].pitch]
                self._drafts[page].text(
                    (x_axis, y_axis),
                    text,
                    font=self._note_font,
                    anchor="lt",
                    fill=consts.NOTE_COLOR
                )
        name_position = self._scaler(consts.NAME_POSITION)
        composer_position = self._scaler(consts.COMPOSER_POSITION)
        self._drafts[1].text(
            name_position,
            music.name,
            font=self._text_font,
            anchor="rt",
            fill=consts.TEXT_COLOR
            )
        self._drafts[1].text(
            composer_position,
            music.composer,
            font=self._text_font,
            anchor="lt",
            fill=consts.TEXT_COLOR
            )
        width = consts.RHYTHM_NOTATION_WIDHT_EXPORT
        if grid_included:
            for draft in self._drafts.values():
                self.draw_grid(music.spacing, consts.MEASURE_LENGHT, draft, self._draw_grid_line)
        self._draw_all_time_notations(music)
        return self._images

    def _draw_time_notation(self, notation, page):
        fill = consts.NOTE_COLOR
        width = consts.RHYTHM_NOTATION_WIDHT_EXPORT
        page = self._drafts[page]
        if len(notation) == 6:
            notation = notation[:2] + notation[4:]
            page.arc(notation, 0, 180, 0) 
        else:
            page.line(notation, width=width, fill=fill)

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
                            text = consts.NOTE_TEXT_CODES[note.pitch]
                            x_axis, y_axis = self._scaler(position)
                            x_axis += consts.EXPORT_NOTE_CORRECTION_ON_X_AXIS
                            self._drafts[page + 1].text(
                                (x_axis, y_axis),
                                text,
                                font=self._note_font,
                                anchor="lt",
                                fill=consts.NOTE_COLOR
                            )
                        else:
                            notation = self._scaler(notation)
                            self._draw_time_notation(notation, page + 1)
