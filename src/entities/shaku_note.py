class ShakuNote:
    """Representation of a musical note on shakuhachi sheet music

    Attributes:
        pitch: note pitch on pentatonic scale, 0 representing the base note of the scale
        lenght: Relative duration of musical note depicted. Defaults to 8
    """
    def __init__(self, pitch: int, lenght: int):
        """Constructor, sets up attributes depicting a musical note

        Args:
            pitch: note pitch, 0 representing the base note of the scale, (1 unit == semitone)
            lenght: Relative duration of musical note depicted. Defaults to 8
        """
        self._pitch = pitch
        self._lenght = lenght

    @property
    def pitch(self):
        """Get note pitch"""
        return self._pitch

    @pitch.setter
    def pitch(self, pitch):
        """Set note pitch"""
        self._pitch = pitch

    @property
    def lenght(self):
        """Get note lenght"""
        return self._lenght

    @lenght.setter
    def lenght(self, lenght):
        """Set note lenght"""
        self._lenght = lenght
