from svgwrite import Drawing, text, image
import config.shaku_constants as consts
from entities.shaku_music import ShakuMusic
from services.conversions import ImageScaler
from services.image_creator import ImageCreator

class SvgCreator:
    """Class for generating an svg -format vector graphics drawing of sheet music

    Attributes:
        svg = svgwrite.Drawing -instance - representation of an svg -format vector drawing
    """
    def __init__(self):
        """Constructor, initializes svg-attribute as placeholder"""
        self._svg = None
        self._scaler = ImageScaler().scale

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

    def _draw_line(self, line: tuple, width: int, fill: tuple):
        """Draws a line on svg image

        Args:
            line: Tuple describiling line by cooridinates of its ends
            width: Line width
            fill: Line color
        """
        self._svg.add(self._svg.line(line[0], line[1], stroke=self._rgb(fill), stroke_width=width))

    def _draw_text(self,
    text_insert: str,
    position: tuple,
    fill: tuple,
    font_size: int,
    style=None
    ):
        """Insert text on svg image with given properties

        Args:
            text_insert: Text to be drawn on svg
            position: Coordinates where text is to be drawn
            fill: Text color
            font_size: Font size
        """
        self._svg.add(text.Text(
            text_insert,
            insert=position,
            fill=self._rgb(fill),
            font_size=str(font_size),
            style=style)
            )

    def _draw_note(self, file: str, position: tuple):
        """Draw a shakuhachi sheet music note from image onto svg sheet

        Args:
            file: path to image resource
            position: Coordinates where note is to be drawn
        """
        note_size = self._scaler(consts.SHEET_NOTE_SIZE)
        note_size += consts.EXPORT_NOTE_FONT_SIZE_INCREMENT
        size = [note_size for i in range(2)]
        pos = (position[0] + self._scaler(consts.EXPORT_NOTE_CORRECTION_ON_X_AXIS), position[1])
        self._svg.add(image.Image(file, pos, size))

    def _draw_note_text(self, note_text: str, position: tuple): #not used now
        """Draw a shakuhachi sheet music note as text on svg sheet

        Args:
            note_text: character corresponding to musical note in shakuhachi notation
            position: Coordinates where note is to be drawn
        """
        font_size = self._scaler(consts.SHEET_NOTE_SIZE)
        adj_position = (position[0], position[1] + font_size)
        self._draw_text(note_text, adj_position, consts.NOTE_COLOR, font_size)

    def _draw_texts(self, name, composer):
        """Draw sheet music name and composer on svg

        Args:
            music: Shakuhachi sheet music description in Shakunotators Music -instance form
        """
        font_size = self._scaler(consts.TEXT_FONT_SIZE)
        name_pos = self._scaler(consts.NAME_POSITION)
        self._draw_text(name, name_pos, consts.TEXT_COLOR, font_size, style="text-anchor:end")
        composer_pos = self._scaler(consts.COMPOSER_POSITION)
        self._draw_text(composer, composer_pos, consts.TEXT_COLOR, font_size)

    def _create_grid(self, spacing: int):
        """Draws musical measure grid on svg image

        Args:
            spacing: Width of each section of grid (1 unit = 80px)
        """
        measure_lenght = consts.MEASURE_LENGHT
        ImageCreator().draw_grid(spacing, measure_lenght, self._draw_line)

    def create_svg(self, music: ShakuMusic, grid_included: bool=False):
        """Generates an svg -format vector graphics drawing of sheet music

        Args:
            music: Shakuhachi sheet music as ShakuMusic instance
            grid_included: True if measure grid will be included. Defaults to False.

        Returns:
            Shakuhachi sheet music data in svg format
        """
        if music is None:
            raise TypeError("No music instance provided")
        self._svg = Drawing(size=(consts.EXPORT_SHEET_SIZE))
        if grid_included:
            self._create_grid(music.spacing)
        self._draw_texts(music.name, music.composer)
        width = consts.RHYTHM_NOTATION_WIDHT_EXPORT
        for part in music.parts.values():
            for note in part.notes:
                position = self._scaler(note.position)
                img_file = consts.NOTES[note.pitch]
                self._draw_note(img_file, position)
            for time_notation in part.part_time_notations():
                for line in time_notation:
                    scaled_line = self._scaler(line)
                    self._draw_line(scaled_line, width, fill=consts.NOTE_COLOR)
        return self._svg
