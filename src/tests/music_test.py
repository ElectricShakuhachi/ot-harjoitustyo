import unittest
from entities.music import Music, Note

class TestMusic(unittest.TestCase):
    def setUp(self):
        self.music = Music()

    def create_testing_part(self, partno):
        test_texts = ["CHI", "TSU", "RE", "RO", "TSU", "RE", "RE", "RE"]
        test_lenghts = [4, 4, 8, 8, 8, 8, 2, 16]
        test_pitches = [4, 2, 3, 1, 2, 3, 3, 3]
        self.music.add_part(partno)
        part = self.music.parts[partno]
        for i in range(len(test_texts)):
            part.add_note(Note(test_texts[i], test_pitches[i], part.next_position(), test_lenghts[i]))

    def create_4_parts(self):
        for i in range(1, 5):
            self.create_testing_part(i)

    def test_convert_to_json_all_parts_created(self):
        self.create_4_parts()
        data = self.music.convert_to_json()
        self.assertEqual(len(data['parts']), 4)

    def test_convert_to_json_music_name_in_json(self):
        self.create_testing_part(1)
        self.music.set_name("Fudaiji")
        data = self.music.convert_to_json()
        self.assertEqual(data['name'], "Fudaiji")

    def test_convert_to_json_music_composer_in_json(self):
        self.create_testing_part(1)
        self.music.set_composer("Professor Test")
        data = self.music.convert_to_json()
        self.assertEqual(data['composer'], "Professor Test")

    def test_add_part_creates_new_part(self):
        self.music.add_part(1)
        self.assertEqual(len(self.music.parts), 1)
