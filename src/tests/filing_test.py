import unittest
from PIL import Image
from services.filing import FileManager
from tkinter import filedialog
import config.shaku_constants as consts

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.filemanager = FileManager()

    def test_save_shaku_returns_false_on_no_file_specified(self):
        filename = ''
        filedialog.asksaveasfile = lambda *args, **kw: filename
        value = self.filemanager.save_shaku(data=None)
        self.assertEqual(value, False)
        
    def test_load_returns_none_on_no_file_specified(self):
        filename = ''
        filedialog.askopenfile = lambda *args, **kw: filename
        value = self.filemanager.load()
        self.assertEqual(value, None)

    def test_load_returns_message_on_wrong_file_specified(self):
        mock_file = consts.NOTE_FONT
        filedialog.askopenfile = lambda *args, **kw: mock_file
        value = self.filemanager.load()

    def test_save_pdf_returns_false_on_no_file_specified(self):
        filename = ''
        filedialog.asksaveasfile = lambda *args, **kw: filename
        value = self.filemanager.save_pdf(image=None)
        self.assertEqual(value, False)

    def test_save_svg_returns_false_no_file_specified(self):
        filename = ''
        filedialog.asksaveasfile = lambda *args, **kw: filename
        value = self.filemanager.save_svg(svg=None)
        self.assertEqual(value, False)

    def test_save_midi_returns_false_no_file_specified(self):
        filename = ''
        filedialog.asksaveasfile = lambda *args, **kw: filename
        value = self.filemanager.save_midi(midi=None)
        self.assertEqual(value, False)
