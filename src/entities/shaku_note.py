class ShakuNote:
    """Representation of a musical note on shakuhachi sheet music

    Attributes:
        pitch: note pitch on pentatonic scale, 0 representing the base note of the scale
        position: [x, y] -list of two values corresponding to coordinates of note on sheet music
        lenght: Relative duration of musical note depicted. Defaults to 8
        first: True if depicted note is the first note in its measure. Defaults to False.
        dotted: Boolean value used by parent class in rhythm notation generation
    """
    def __init__(self, pitch: int, position: tuple, lenght: int=8, first: bool=False):
        """Constructor, sets up attributes depicting a musical note

        Args:
            pitch: note pitch, 0 representing the base note of the scale, (1 unit == semitone)
            position: [x, y] -list of two values corresponding to coordinates of note on sheet music
            lenght: Relative duration of musical note depicted. Defaults to 8
            first: True if depicted note is the first note in its measure. Defaults to False.
        """
        self._pitch = pitch
        self._lenght = lenght
        self._position = position
        self._first = first
        self._dotted = False

    @property
    def pitch(self):
        """Get note pitch"""
        return self._pitch

    @property
    def lenght(self):
        """Get note lenght"""
        return self._lenght

    @property
    def position(self):
        """Get note position"""
        return self._position

    @position.setter
    def position(self, value):
        self._position = tuple(int(i) for i in value)

    @property
    def first(self):
        """Get boolean describing if note is first"""
        return self._first

    @first.setter
    def first(self, value: bool):
        """Set boolean describing if note is first"""
        if isinstance(value, bool):
            self._first = value
        else:
            raise ValueError("Cannot set note.first to non boolean value")

    @property
    def dotted(self):
        """Get boolean describing if note is dotted"""
        return self._dotted

    @dotted.setter
    def dotted(self, value: bool):
        """Set boolean describing if note is dotted"""
        if isinstance(value, bool):
            self._dotted = value
        else:
            raise ValueError("Cannot set note.dotted to non boolean value")
