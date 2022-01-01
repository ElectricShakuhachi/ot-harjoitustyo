from midi2audio import FluidSynth
import config.shaku_constants as consts

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

class GraphicsConverter:
    """Class for scaling items from app-internal sheet size to export sheet size"""
    def scale(self, item):
        """Multiplies (recursively) by the difference of ui sheet versus export sheet size

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
        if type(item) in [int, float]:
            return item * multiplicator
        raise ValueError("Can only scale integers, floats, tuples and lists")

    def rgb_to_hex(self, rgb: tuple):
        return "#%02x%02x%02x" % rgb