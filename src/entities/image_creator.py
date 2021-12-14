from PIL import Image, ImageFont, ImageDraw

class ImageCreator:
    def __init__(self):
        self.image = Image.new("RGB", (2480, 3508), (255, 255, 255))
        self.font = ImageFont.truetype("./graphics/askai9.ttc", 72)
        self.dummyfont = ImageFont.load_default()
        self.draft = ImageDraw.Draw(self.image)

    def create_dummy_image(self, music):
        self.draft.text((1, 1), "私は", font=self.font, fill=(0, 0, 0))
        self.draft.text((100, 100), "Hahaa", font=self.font, fill=(0, 0, 0))
        self.draft.text((1000, 500), "Hahaa", font=self.dummyfont, fill=(0, 0, 0))
        self.draft.line((0, 0) + self.image.size, fill=128)
        self.draft.line((0, self.image.size[1], self.image.size[0], 0), fill=128)
        self.image.save("test.jpg")

    def create_image(self, music):
        for part in music.parts.values():
            for note in part.notes:
                x = note.position[0] * 4
                y = note.position[1] * 4
                self.draft.text((x, y), note.text, font=self.font, fill=(0, 0, 0))
            for notation in part.part_time_notations():
                for line in notation:
                    scaled_line = ((line[0][0] * 4 + 16, line[0][1] * 4 + 12), (line[1][0] * 4 + 16, line[1][1] * 4 + 12))
                    self.draft.line(scaled_line, width=3, fill=(0, 0, 0))
        self.image.save("test.pdf")
