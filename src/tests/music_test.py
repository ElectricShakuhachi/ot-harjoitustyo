import unittest
from entities.music import Music, Note

class TestMusic(unittest.TestCase):
    def setUp(self):
        self.music = Music()
        notecount = 20
        notes = []
        self.music.set_composer("Professor Test")
        self.music.set_name("Fudaiji")
        test_texts = ["CHI", "TSU", "RE", "RO", "TSU", "RE", "RE", "RE"]
        test_lenghts = [4, 4, 8, 8, 8, 8, 2, 16]
        test_pitches = [4, 2, 3, 1, 2, 3, 3, 3]
        self.music.add_part(1)
        part = self.music.parts[-1]
        for i in range(notecount):
            notes.append(Note("RO", test_pitches[i], part.next_position(), test_lenghts[i]))
        self.music.add_part(2)
        part = self.music.parts[-1]
        for i in range(notecount):
            notes.append(Note("RO", test_pitches[i], part.next_position(), test_lenghts[i]))
        self.music.add_part(3)
        part = self.music.parts[-1]
        for i in range(notecount):
            notes.append(Note("RO", test_pitches[i], part.next_position(), test_lenghts[i]))
        self.music.add_part(4)
        part = self.music.parts[-1]
        for i in range(notecount):
            notes.append(Note("RO", test_pitches[i], part.next_position(), test_lenghts[i]))

    def test_convert_to_json_all_parts_created(self):
        data = self.music.convert_to_json()
        self.assertEqual(len(data['parts']), 4)

    def test_convert_to_json_music_name_in_json(self):
        data = self.music.convert_to_json()
        self.assertEqual(data['name'], "Fudaiji")

    def test_convert_to_json_music_composer_in_json(self):
        data = self.music.convert_to_json()
        self.assertEqual(data['composer'], "Professor Test")
