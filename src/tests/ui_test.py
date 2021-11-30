import unittest
from tkinter import *
from ui.ui import UI 

class TestUI(unittest.TestCase):
    def setUp(self):
        self.ui = UI(Tk())

    def test_ui_init_does_not_create_canvas(self):
        self.assertEqual(self.ui.sheet, None)

    #def test_starting_ui_creates_canvas(self):
    #    self.ui.start()
    #    self.assertEqual(type(self.ui.sheet), type(Canvas()))
