from svgwrite import Drawing, rgb, text

class SvgCreator:
    def draw_line(self, line, width=2):
        self.svg.add(self.svg.line(line[0], line[1], stroke=rgb(0, 0, 0), stroke_width=width))

    def draw_note(self, text_to_write, position):
        font_size = 68
        insert = (position[0] - font_size / 4, position[1] + font_size / 2)
        self.svg.add(text.Text(text_to_write, insert=insert, fill=rgb(0, 0, 0), font_size=str(font_size)))

    def _create_grid(self):
        spacing = max(2, len(self.music.parts))
        measure_lenght = 2
        for x in range(2172, 251, -80 * spacing):
            self.draw_line(((x, 280), (x, 3360)))
        for y in range(280, 3364, 220 * measure_lenght):
            self.draw_line(((2172, y), (252, y)))

    def create_svg(self, music, grid_included=False, file=None):
        self.music = music
        self.svg = Drawing(file, size=(2480, 3508))
        if grid_included:
            self._create_grid(music)
        for part in self.music.parts.values():
            for note in part.notes:
                scaled_position = (note.position[0] * 4, note.position[1] * 4) 
                self.draw_note(note.text, scaled_position)
            for time_notation in part.part_time_notations():
                for line in time_notation:
                    scaled_line = ((line[0][0] * 4, line[0][1] * 4 - 14), (line[1][0] * 4, line[1][1] * 4 - 12))
                    self.draw_line(scaled_line, 6)
        return self.svg
 