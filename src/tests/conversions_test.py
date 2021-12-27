import unittest
from services.conversions import ImageScaler
import config.shaku_constants as consts

class TestImageScaler(unittest.TestCase):
    def setUp(self):
        self.scaler = ImageScaler()
        self.ratio = consts.EXPORT_SHEET_SIZE[0] // consts.SHEET_SIZE[0]

    def test_scale_converts_1_correctly(self):
        orig = 1
        self.assertEqual(self.scaler.scale(orig), orig * self.ratio)

    def test_scale_converts_0_correctly(self):
        orig = 0
        self.assertEqual(self.scaler.scale(orig), orig * self.ratio)

    def test_scale_converts_2_correctly(self):
        orig = 2
        self.assertEqual(self.scaler.scale(orig), orig * self.ratio)

    def test_scale_converts_1000_correctly(self):
        orig = 1000
        self.assertEqual(self.scaler.scale(orig), orig * self.ratio)

    def test_scale_converts_neg_1_correctly(self):
        orig = -1
        self.assertEqual(self.scaler.scale(orig), orig * self.ratio)

    def test_scale_converts_neg_5_correctly(self):
        orig = -5
        self.assertEqual(self.scaler.scale(orig), orig * self.ratio)

    def test_scale_converts_tuple_correctly(self):
        orig = (1, 2, 3, 0)
        converted = self.scaler.scale(orig)
        converted2 = tuple(self.ratio * i for i in orig)
        self.assertEqual(converted, converted2)

    def test_scale_converts_list_correctly(self):
        orig = (1, 100, 2, 0, -1)
        converted = self.scaler.scale(orig)
        converted2 = tuple(self.ratio * i for i in orig)
        self.assertEqual(converted, converted2)
    
    def _convert(self, value):
        if isinstance(value, int):
            return self.ratio * value
        if isinstance(value, float):
            return self.ratio * value
        if isinstance(value, tuple):
            return tuple(self._convert(i) for i in value)
        if isinstance(value, list):
            return tuple(self._convert(i) for i in value)

    def test_scale_converts_tuple_recursive_depht_3(self):
        orig = ((1, 2, (5, -9)), 3, 0)
        converted = self.scaler.scale(orig)
        converted2 = self._convert(orig)
        self.assertEqual(converted, converted2)

    def test_scale_converts_list_recursive_depht_3(self):
        orig = [[1, 2, [5, -9]], 3, 0]
        converted = self.scaler.scale(orig)
        converted2 = self._convert(orig)
        self.assertEqual(converted, converted2)

    def _str_imput_to_scale(self):
        self.scaler.scale("thing")

    def test_scale_raises_exception_on_str(self):
        self.assertRaises(ValueError, self._str_imput_to_scale)

    #test different possible ratios