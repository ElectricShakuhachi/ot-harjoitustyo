class ShakuNotation:
    """Representation of a non-pitch, non-duration related notation on shakuhachi sheet music

    Attributes:
        type: string identifying the type of notation sign
        position: relative coordinates of notation
        relative_note: ID of related shakuhachi pitch
    """
    def __init__(self, notation_type: str, position: list, note_id: int):
        """Constructor, sets up attributes depicting a notation

        Args:
            type: string identifying the type of notation sign
            position: relative coordinates of notation
            note_id: ID of related shakuhachi pitch
        """
        self._notation_type = notation_type
        self._position = position
        self._relative_note = note_id

    @property
    def relative_note(self):
        """Get ID of shakuhachi sheet music pitch notation the notation is relative to"""
        return self._relative_note

    @property
    def notation_type(self):
        """Get note pitch"""
        return self._notation_type

    @property
    def position(self):
        """Get note position"""
        return self._position
