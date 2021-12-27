import unittest
from svgwrite import Drawing
from services.svg_creator import SvgCreator
from entities.shaku_music import ShakuMusic
from entities.shaku_note import ShakuNote

class TestMidiCreator(unittest.TestCase):
    def setUp(self):
        self.creator = SvgCreator()

    def test_create_svg_returns_drawing_instance(self):
        music = ShakuMusic()
        music.add_part(1)
        music.parts[1].add_note(ShakuNote(1, (100, 100), 8, True))
        result = self.creator.create_svg(music)
        self.assertIsInstance(result, Drawing)

    def test_create_svg_returns_drawing_with_empty_music(self):
        music = ShakuMusic()
        result = self.creator.create_svg(music)
        self.assertIsInstance(result, Drawing)

    def _send_none_to_create(self):
        self.creator.create_svg(None)

    def test_create_svg_generates_error_on_no_music(self):
        self.assertRaises(TypeError, self._send_none_to_create)