import unittest
from midiutil import MIDIFile
from services.midi_creator import MidiCreator
from entities.shaku_part import ShakuPart
from entities.shaku_note import ShakuNote

class TestMidiCreator(unittest.TestCase):
    def setUp(self):
        self.creator = MidiCreator()

    def test_generate_midi_raises_error_if_no_data(self):
        self.assertRaises(ValueError, self.creator.generate_midi)

    def test_generate_midi_raises_error_on_no_notes(self):
        part = ShakuPart(1, 10, 1)
        self.creator.create_track(part)
        self.assertRaises(ValueError, self.creator.generate_midi)      

    def test_generate_midi_returns_midi_file(self):
        note = ShakuNote(1, (100, 100), 8, True)
        part = ShakuPart(1, 10, 1)
        part.add_note(note)
        self.creator.create_track(part)
        self.assertIsInstance(self.creator.generate_midi(), MIDIFile)