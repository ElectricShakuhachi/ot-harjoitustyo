from PIL import Image, ImageFont, ImageDraw
import config.shaku_constants as consts
from entities.shaku_music import ShakuMusic
from services.conversions import ImageScaler

class ImageCreator:
    """Class for generating production grade image of sheet music
    
    Attributes:
        image: PIL Image instance for sheet base
        font: Font for text on image
        draft: PIL ImageDraw instance for drawing lines and text on image
    """
    def __init__(self):
        """Constructor, generates necessary PIL instances"""
        self._image = Image.new("RGB", consts.EXPORT_SHEET_SIZE, (255, 255, 255))
        self._scaler = ImageScaler().scale
        self._note_font = ImageFont.truetype(consts.NOTE_FONT, self._scaler(consts.SHEET_NOTE_SIZE) + consts.EXPORT_NOTE_FONT_SIZE_INCREMENT)
        self._text_font = ImageFont.truetype(consts.TEXT_FONT, self._scaler(consts.TEXT_FONT_SIZE))
        self._draft = ImageDraw.Draw(self._image)

    def _draw_grid_line(self, line: tuple, width, fill):
        """Draws one line of musical measure grid on image

        Args:
            line: tuple description of line endpoint coordinates
        """
        self._draft.line(line, width=width, fill=fill)

    def draw_grid(self, spacing: int, measure_lenght: int, drawing_function):
        """Prototype function for drawing a musical measure grid on image - utilizing a function fed in as dependency
        
        Args:
            spacing: Width of each section of grid (1 unit = 80px)
            measure_lenght: Height of each section of grid (1 unit = 220px)
            drawing_function: Function used for drawing grid
        """
        x = list(self._scaler(consts.GRID_X))
        y = list(self._scaler(consts.GRID_Y))
        x[1] -= (x[1] - x[0]) % (self._scaler(consts.NOTE_ROW_SPACING) * spacing)
        for temp_x in range(x[0], x[1] + 3, self._scaler(consts.NOTE_ROW_SPACING) * spacing):
            drawing_function(((temp_x, y[0]), (temp_x, y[1])), self._scaler(consts.GRID_LINE_WIDHT), consts.GRID_COLOR)
        for temp_y in range(y[0], y[1] + 1, self._scaler(consts.VERTICAL_SPACE_PER_FOURTH_NOTE) * measure_lenght):
            drawing_function(((x[0], temp_y), (x[1], temp_y)), self._scaler(consts.GRID_LINE_WIDHT), consts.GRID_COLOR)

    def create_image(self, music: ShakuMusic, grid_included: bool=False):
        """Receives musical notation, scales it, re-aligns it and draws it on PIL Image

        Args:
            music: ShakuMusic instance containing notations, name and composer to draw on image
            grid_included: If True, a measure grid is drawn on sheet music image. Defaults to False.

        Returns:
            PIL Image instance with given details drawn on it
        """
        name_position = self._scaler(consts.NAME_POSITION)
        composer_position = self._scaler(consts.COMPOSER_POSITION)
        self._draft.text(name_position, music.name, font=self._text_font, anchor="rt", fill=consts.TEXT_COLOR)
        self._draft.text(composer_position, music.composer, font=self._text_font, anchor="lt", fill=consts.TEXT_COLOR)
        width = consts.RHYTHM_NOTATION_WIDHT_EXPORT
        if grid_included:
            self.draw_grid(music.spacing, consts.MEASURE_LENGHT, self._draw_grid_line)
        for part in music.parts.values():
            for note in part.notes:
                x, y = self._scaler(note.position)
                x += consts.EXPORT_NOTE_CORRECTION_ON_X_AXIS
                text = consts.NOTE_TEXT_CODES[note.pitch]
                self._draft.text((x, y), text, font=self._note_font, anchor="lt", fill=consts.NOTE_COLOR)
            for notation in part.part_time_notations():
                for line in notation:
                    self._draft.line(self._scaler(line), width=width, fill=consts.NOTE_COLOR)
        return self._image
