import unittest
import config.shaku_constants as consts
from entities.shaku_part import ShakuPart
from entities.shaku_note import ShakuNote
from entities.shaku_notation import ShakuNotation

class TestShakuPart(unittest.TestCase):
    def setUp(self):
        self.part = ShakuPart(1, 100, 2)

    def test_notation_cur_pos_can_be_fetched(self):
        self.assertEqual(self.part.notation_at_current_pos, False)

    def test_notation_cur_pos_can_be_set(self):
        self.part.notation_at_current_pos = True
        self.assertEqual(self.part.notation_at_current_pos, True)

    def test_notations_can_be_fetched(self):
        notations = self.part.notations
        self.assertEqual(notations, [])

    def test_notations_can_be_appended(self):
        notation = ShakuNotation("b", (0, 10), 2)
        self.part.notations.append(notation)
        self.assertEqual(self.part.notations[-1], notation)

    def test_notations_can_be_set(self):
        notations = [ShakuNotation("ding", (0, 0), 1)]
        self.part.notations = notations
        self.assertEqual(self.part.notations, notations)

    def test_part_no_can_be_fetched(self):
        self.assertEqual(self.part.part_no, 1)

    def test_notes_can_be_fetched(self):
        self.assertEqual(self.part.notes, [])

    def test_measure_counter_can_be_fetched(self):
        self.assertEqual(self.part.measure_counter, 0)

    def test_measure_counter_can_be_set(self):
        self.part.measure_counter = 10
        self.assertEqual(self.part.measure_counter, 10)

    def test_measure_counter_can_be_incremented(self):
        self.part.measure_counter += 10
        self.part.measure_counter += 10
        self.assertEqual(self.part.measure_counter, 20)

    def test_start_x_can_be_fetched(self):
        self.assertEqual(self.part.start_x, 100)
    
    def test_start_x_can_be_set(self):
        self.part.start_x = 20
        self.assertEqual(self.part.start_x, 20)

    def test_start_x_can_be_incremented(self):
        self.part.start_x = 10
        self.part.start_x += 10
        self.assertEqual(self.part.start_x, 20)

    def test_rows_can_be_fetched(self):
        self.assertEqual(self.part.rows, 0)

    def test_rows_can_be_set(self):
        self.part.rows = 20
        self.assertEqual(self.part.rows, 20)

    def test_rows_can_be_incremented(self):
        self.part.rows = 5
        self.part.rows += 15
        self.assertEqual(self.part.rows, 20)

    def test_spacing_can_be_fetched(self):
        self.assertEqual(self.part.spacing, 2)

    def test_spacing_can_be_set_one_higher(self):
        self.part.spacing = 3
        self.assertEqual(self.part.spacing, 3)

    def test_spacing_can_be_set_two_higher(self):
        self.part.spacing = 4
        self.assertEqual(self.part.spacing, 4)

    def test_next_position_returns_x_start_for_x_on_first(self):
        value = self.part.next_position()
        self.assertEqual(value[0], self.part.start_x)

    def test_next_position_returns_y_start_for_y_on_first(self):
        value = self.part.next_position()
        self.assertEqual(value[1], consts.PARTS_Y_START)

    def test_next_position_note_lenght_times_spacing(self):
        note = ShakuNote(1, (100, 100), 8)
        lenght = note.lenght
        self.part.add_note(note)
        value = self.part.next_position()
        y_spacing = consts.NOTE_Y_SPACING
        self.assertEqual(value, [100, 100 + lenght * y_spacing])

    def test_next_position_adds_measure_skip(self):
        note = ShakuNote(1, (100, 100), 8)
        lenght = note.lenght
        self.part.add_note(note)
        self.part.measure_counter = 0
        value = self.part.next_position()
        y_spacing = consts.NOTE_Y_SPACING
        measure_skip = consts.MEASURE_SKIP_LENGHT
        self.assertEqual(value, [100, 100 + lenght * y_spacing + measure_skip])

    def test_next_position_decreases_x_for_new_line(self):
        max_y = consts.SHEET_SIZE[1] - 47
        note = ShakuNote(1, (100, max_y - 1), 8)
        self.part.add_note(note)
        value = self.part.next_position()
        x_space = self.part.spacing * consts.NOTE_ROW_SPACING
        self.assertEqual(value[0], 100 - x_space)

    def test_next_position_sets_y_beginning_for_new_line(self):
        max_y = consts.SHEET_SIZE[1] - 47
        note = ShakuNote(1, (100, max_y - 1), 8)
        self.part.add_note(note)
        value = self.part.next_position()
        y_start = consts.PARTS_Y_START
        self.assertEqual(value[1], y_start)

    def test_add_note_does_not_add_to_left_marigin(self):
        note = ShakuNote(1, (30, 199), 8)
        self.part.add_note(note)
        self.assertEqual(self.part.notes, [])

    #def _add_bunch_of_notes()

    #def test_setting_spacing_moves_notes_part_1_row_1(self):
    #    self.part.add_note