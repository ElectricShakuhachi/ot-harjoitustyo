import unittest
from tkinter import *
from entities.music import Music

class TestMusic(unittest.TestCase):
    def setUp(self):
        self.music = Music()

    def test_next_position_returns_500_80_on_first_note(self):
        position = self.music.next_position()
        self.assertEqual([500, 80], position)