import unittest
from entities.shaku_music import ShakuMusic
import config.shaku_constants as consts

class TestShakuMusic(unittest.TestCase):
    def setUp(self):
        self.music = ShakuMusic()

    def test_composer_name_can_be_read(self):
        self.assertEqual(self.music.composer, "")

    def test_composer_name_can_be_set(self):
        self.music.composer = "Ding"
        self.assertEqual(self.music.composer, "Ding")

    def test_composition_name_can_be_read(self):
        self.assertEqual(self.music.name, "")

    def test_composition_name_can_be_set(self):
        self.music.name = "Great Composer"
        self.assertEqual(self.music.name, "Great Composer")

    def _add_too_long_composer(self):
        self.music.composer = """
        Valtavan Pitkä Nimi Tällä Henkilöllä Voi Joskus Olla"""

    def test_adding_long_composer_raises_error(self):
        self.assertRaises(ValueError, self._add_too_long_composer)

    def _add_too_long_name(self):
        self.music.name = """
        Valtavan Pitkä Nimi Tällä Henkilöllä Voi Joskus Olla"""

    def test_adding_long_name_raises_error(self):
        self.assertRaises(ValueError, self._add_too_long_name)

    def _add_too_long_combo(self):
        self.music.composer = "Valtavan Pitkä Nimi Tällä"
        self.music.name = "Henkilöllä Voi Joskus Olla"

    def test_adding_long_combo_of_texts_raises_error(self):
        self.assertRaises(ValueError, self._add_too_long_combo)

    def test_parts_can_be_gotten(self):
        parts = self.music.parts
        self.assertEqual(parts, {})

    def test_spacing_can_be_gotten(self):
        spacing = self.music.spacing
        self.assertEqual(spacing, 1)

    def test_spacing_can_be_set(self):
        self.music.spacing = 2
        self.assertEqual(self.music.spacing, 2)

    def _set_negative_spacing(self):
        self.music.spacing = -1

    def test_cannot_set_negative_spacing(self):
        self.assertRaises(ValueError, self._set_negative_spacing)

    def test_can_add_part(self):
        count = len(self.music.parts)
        self.music.add_part(1)
        self.assertEqual(len(self.music.parts), count + 1)

    def test_adding_part_increments_spacing(self):
        spacing = self.music.spacing
        self.music.add_part(2)
        self.assertEqual(self.music.spacing, spacing + 1)

    def test_cannot_add_duplicate_part_id(self):
        self.music.add_part(1)
        part_count = len(self.music.parts)
        self.music.add_part(1)
        self.assertEqual(len(self.music.parts), part_count)

    def _get_max_rows(self):
        size = consts.NOTE_ROW_SPACING * (self.music.spacing + 1)
        max_rows = (consts.GRID_X[1] - consts.GRID_X[0]) // size
        return max_rows

    def test_cannot_add_part_if_max_rows_1_part(self):
        self.music.add_part(1)
        max_rows = self._get_max_rows()
        self.music.parts[1].rows = max_rows + 1
        count = len(self.music.parts)
        self.music.add_part(2)
        self.assertEqual(len(self.music.parts), count)

    def test_cannot_add_part_if_max_rows_on_1_of_2_parts(self):
        self.music.add_part(1)
        self.music.add_part(2)
        max_rows = self._get_max_rows()
        self.music.parts[1].rows = max_rows + 1
        count = len(self.music.parts)
        self.music.add_part(3)
        self.assertEqual(len(self.music.parts), count)

    def test_cannot_add_part_if_max_rows_on_2_of_2_parts(self):
        self.music.add_part(1)
        self.music.add_part(2)
        max_rows = self._get_max_rows()
        self.music.parts[2].rows = max_rows + 1
        count = len(self.music.parts)
        self.music.add_part(3)
        self.assertEqual(len(self.music.parts), count)

    def test_cannot_add_part_if_max_rows_on_1_of_3_parts(self):
        self.music.add_part(1)
        self.music.add_part(2)
        self.music.add_part(3)
        max_rows = self._get_max_rows()
        self.music.parts[1].rows = max_rows + 1
        count = len(self.music.parts)
        self.music.add_part(4)
        self.assertEqual(len(self.music.parts), count)

    def test_cannot_add_part_if_max_rows_on_2_of_3_parts(self):
        self.music.add_part(1)
        self.music.add_part(2)
        self.music.add_part(3)
        max_rows = self._get_max_rows()
        self.music.parts[2].rows = max_rows + 1
        count = len(self.music.parts)
        self.music.add_part(4)
        self.assertEqual(len(self.music.parts), count)

    def test_cannot_add_part_if_max_rows_on_3_of_3_parts(self):
        self.music.add_part(1)
        self.music.add_part(2)
        self.music.add_part(3)
        max_rows = self._get_max_rows()
        self.music.parts[3].rows = max_rows + 1
        count = len(self.music.parts)
        self.music.add_part(4)
        self.assertEqual(len(self.music.parts), count)

    def test_part_1_gets_correct_position(self):
        self.music.add_part(1)

#continue