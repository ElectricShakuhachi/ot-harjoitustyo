import config.shaku_constants as consts
from midi2audio import FluidSynth

class MusicConverter:
    """Converts MIDI music representation to .wav audio -format"""
    def convert(self, source: str, target: str):
        """Converts MIDI music representation to .wav audio -format

        Args:
            source: relative path of MIDI file
            target: relative path of .wav file
        """
        synth = FluidSynth()
        synth.midi_to_audio(source, target)

class ImageScaler:
    """Class for scaling items from app-internal sheet size to export sheet size"""
    def scale(self, item):
        """Multiplies any int, or all list / tuple values (recursively) by the difference of configured sheet versus export sheet size

        Args:
            item: value or values to be converted

        Returns:
            converted value or values
        """
        multiplicator = consts.EXPORT_SHEET_SIZE[0] // consts.SHEET_SIZE[0]
        if type(item) in [tuple, list]:
            result = []
            for i in item:
                result.append(self.scale(i))
            return tuple(result)
        elif type(item) in [int, float]:
            return item * multiplicator
        else:
            raise ValueError("Can only scale integers, floats, tuples and lists")