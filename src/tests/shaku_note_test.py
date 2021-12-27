import unittest
from entities.shaku_note import ShakuNote

class TestShakuNote(unittest.TestCase):
    def setUp(self):
        self.note = ShakuNote(1, (100, 100), 8, True)

    def test_pitch_can_be_fetched(self):
        self.assertEqual(self.note.pitch, 1)

    def test_lenght_can_be_fetched(self):
        self.assertEqual(self.note.lenght, 8)

    def test_position_can_be_fetched(self):
        self.assertEqual(self.note.position, (100, 100))

    def test_position_can_be_set(self):
        self.note.position = (19, 29)
        self.assertEqual(self.note.position, (19, 29))

    def test_first_can_be_fetched(self):
        self.assertEqual(self.note.first, True)

    def test_first_can_be_set(self):
        self.note.first = False
        self.assertEqual(self.note.first, False)

    def _non_bool_input_first(self):
        self.note.first = 20

    def test_first_cant_be_set_to_non_bool(self):
        self.assertRaises(ValueError, self._non_bool_input_first)

    def test_dotted_can_be_fetched(self):
        dotted = self.note.dotted
        self.assertEqual(dotted, False)

    def test_dotted_can_be_set(self):
        self.note.dotted = True
        self.assertEqual(self.note.dotted, True)

    def _non_bool_imput_dotted(self):
        self.note.dotted = 20

    def test_dotted_cant_be_set_to_non_bool(self):
        self.assertRaises(ValueError, self._non_bool_imput_dotted)