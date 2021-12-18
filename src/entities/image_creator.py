from PIL import Image, ImageFont, ImageDraw
import os

class ImageCreator:
    def __init__(self):
        self.image = Image.new("RGB", (2480, 3508), (255, 255, 255))
        dirname = os.path.dirname(__file__)
        parent = os.path.dirname(dirname)
        self.font = ImageFont.truetype(os.path.join(parent, "./graphics/askai9.ttc"), 72)
        self.dummyfont = ImageFont.load_default()
        self.draft = ImageDraw.Draw(self.image)

    def _create_grid(self, music):
        spacing = max(2, len(music.parts))
        measure_lenght = 2
        for x in range(2172, 251, -80 * spacing): #music should have grid instead of UI!!! Then I could directly import it to both -> also UI should get Image from creator instead of using tk native
            self.draft.line((x, 280, x, 3360), fill=(0, 0, 0))
        for y in range(280, 3364, 220 * measure_lenght):
            self.draft.line((2172, y, 252, y), fill=(0, 0, 0))

    def create_image(self, music, grid_included=False):
        name = music.get_name()
        composer = music.get_composer()
        self.draft.text((280, 80), name, font=self.font, fill=(0, 0, 0))
        self.draft.text((2200, 80), composer, font=self.font, anchor="rt", fill=(0, 0, 0))
        if grid_included:
            self._create_grid(music)
        for part in music.parts.values():
            for note in part.notes:
                x = note.position[0] * 4
                y = note.position[1] * 4
                self.draft.text((x, y), note.text, font=self.font, fill=(0, 0, 0))
            for notation in part.part_time_notations():
                for line in notation:
                    scaled_line = ((line[0][0] * 4 + 16, line[0][1] * 4 + 12), (line[1][0] * 4 + 16, line[1][1] * 4 + 12))
                    self.draft.line(scaled_line, width=3, fill=(0, 0, 0))
        return self.image
