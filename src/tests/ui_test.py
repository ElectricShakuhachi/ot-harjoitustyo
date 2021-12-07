import unittest
from tkinter import Tk, Canvas
from ui.ui import UI 

class TestUI(unittest.TestCase):
    def setUp(self):
        self.ui = UI(Tk())

    def test_starting_ui_creates_canvas(self):
        self.assertEqual(type(self.ui.sheet), type(Canvas()))
