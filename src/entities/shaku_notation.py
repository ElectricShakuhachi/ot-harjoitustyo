class ShakuNotation:
    """Representation of a non-pitch, non-duration related notation on shakuhachi sheet music

    Attributes:
        type: string identifying the type of notation sign
        position: [x, y] -list of two values corresponding to coordinates of notation in relation to its relative note
        relative_note: ID of shakuhachi sheet music pitch notation the notation is relative to
    """
    def __init__(self, type: str, position: list, note_id: int):
        """Constructor, sets up attributes depicting a notation

        Args:
            type: string identifying the type of notation sign
            position: [x, y] -list of two values corresponding to coordinates of notation in relation to its relative note
            note_id: ID of shakuhachi sheet music pitch notation the notation is relative to
        """
        self._type = type
        self._position = position
        self._relative_note = note_id

    @property
    def relative_note(self):
        """Get ID of shakuhachi sheet music pitch notation the notation is relative to"""
        return self._relative_note

    @property
    def type(self):
        """Get note pitch"""
        return self._type

    @property
    def position(self):
        """Get note position"""
        return self._position
