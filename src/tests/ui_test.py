import unittest
from tkinter import Tk, Canvas
from ui.view import View

class TestUI(unittest.TestCase):
    def setUp(self):
        self.ui = View(Tk())

    def test_starting_ui_creates_canvas(self):
        self.assertEqual(type(self.ui.sheet), type(Canvas()))
