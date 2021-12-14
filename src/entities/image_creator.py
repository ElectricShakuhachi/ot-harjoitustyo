from PIL import Image, ImageFont, ImageDraw

class ImageCreator:
    def __init__(self):
        self.image = Image.new("RGB", (2480, 3508), (255, 255, 255))
        self.font = ImageFont.truetype("./graphics/askai9.ttc", 72)
        self.dummyfont = ImageFont.load_default()
        self.draft = ImageDraw.Draw(self.image)

    def create_image(self, music):
        name = music.get_name()
        composer = music.get_composer()
        self.draft.text((280, 80), name, font=self.font, fill=(0, 0, 0))
        self.draft.text((2200, 80), composer, font=self.font, anchor="rt", fill=(0, 0, 0))
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
