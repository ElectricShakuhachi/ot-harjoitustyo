import unittest
from PIL import Image
import config.shaku_constants as consts
from services.image_creator import ImageCreator

class TestImageCreator(unittest.TestCase):
    def setUp(self):
        self.creator = ImageCreator()

    def _values_grid_x(self):
        min_range = range(5, 800, 50)
        max_range = range(50, 4000, 50)
        values = []
        for choice_1 in min_range:
            for choice_2 in max_range:
                if choice_2 > choice_1:
                    values.append((choice_1, choice_2))
        return values
    
    def _values_grid_y(self):
        min_range = range(5, 800, 50)
        max_range = range(50, 2500, 50)
        values = []
        for choice_1 in min_range:
            for choice_2 in max_range:
                if choice_2 > choice_1:
                    values.append((choice_1, choice_2))
        return values

    def _values_note_row_spacing(self):
        return range(5, 500, 5)

    def _values_grid_line_width(self):
        return range(6)

    def _values_vertical_space_per_fourth_note(self):
        return range(5, 100, 5)

    def _values_name_position(self):
        x_range = range(2, 1000, 50)
        y_range = range(2, 50, 50)
        values = []
        for choice_1 in x_range:
            for choice_2 in y_range:
                values.append((choice_1, choice_2))
        return values

    def _values_composer_position(self):
        x_range = range(2, 1000, 50)
        y_range = range(2, 50, 50)
        values = []
        for choice_1 in x_range:
            for choice_2 in y_range:
                values.append((choice_1, choice_2))
        return values

    def _values_rhythm_notation_width_export(self):
        return range(6)

    def _values_measure_lenght(self):
        return range(12)

    def _run(self, assertion_function):
        func = self.creator._draw_grid_line
        for value1 in self._values_grid_x():
            for value2 in self._values_grid_y():
                consts.GRID_X = value1
                consts.GRID_Y = value2
                for spacing in range(4):
                    for measure_lenght in self._values_measure_lenght():
                        self.creator.draw_grid(spacing, measure_lenght, func)

    def test_draw_grid_doesnt_draw_beyond_limits(self):
        pass

    def test_draw_grid_draws_correct_amount_x_axis_lines(self):
        pass

    def test_draw_grid_draws_correct_amount_y_axis_lines(self):
        pass