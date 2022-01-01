import unittest
from tkinter import Tk
from ui.ui import UI
from ui.buttons import Buttons

class TestButtons(unittest.TestCase):
    def setUp(self):
        ui = UI(Tk())
        self.buttons = Buttons(ui)

    def test_buttons_setup_creates_correct_amount_of_buttons(self):
        self.assertEqual(len(self.buttons.buttons), 31)

    def test_octave_set_to_otsu_on_start(self):
        self.assertEqual(self.buttons.octave, "Otsu")

    def test_octave_can_be_set(self):
        self.buttons.octave = "Kan"
        self.assertEqual(self.buttons.octave, "Kan")

    def _set_wrong_octave(self):
        self.buttons.octave = "Ding"

    def test_incorrect_octave_raises_error(self):
        self.assertRaises(ValueError, self._set_wrong_octave)

