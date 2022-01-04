from entities.shaku_note import ShakuNote
from entities.shaku_notation import ShakuNotation

class ShakuPart:
    """Class depicting a part in a multipartite or solo shakuhachi sheet music

    Attributes:
        part_no: number of part on musical notation sheet
        notes: list of musical notes contained in part
        notations: list of non-pitch, non-duration notations contained in part
        start_x: x-axis for positioning first note of the part
        measure_counter: value used in calculating note positioning with regards to musical measure
        spacing: value depicting how much x-axis room to leave between rows of notes
        rows: count of rows used on musical sheet by the part
        notation_at_current_pos: True if there is a notation related to next note position
    """
    def __init__(self, part_id: int):
        """Constructor, intializes class attributes

        Args:
            part_id: number of part on musical notation sheet
            start_x: x-axis for positioning first note of the part
            spacing: value depicting how much x-axis room to leave between rows of notes
        """
        self._part_no = part_id
        self._notes = []
        self._notations = []
        self._notation_at_current_pos = False

    @property
    def notation_at_current_pos(self):
        """Get notation_at_current_pos"""
        return self._notation_at_current_pos

    @notation_at_current_pos.setter
    def notation_at_current_pos(self, value: bool):
        """Set notation_at_current_pos"""
        self._notation_at_current_pos = value

    @property
    def notations(self):
        """Get misc notations on part"""
        return self._notations

    @notations.setter
    def notations(self, notations):
        """Set misc notations on part"""
        self._notations = notations

    @property
    def part_no(self):
        """Get part number"""
        return self._part_no

    @property
    def notes(self):
        """Get part notes"""
        return self._notes

    def clear_pre_existing_notation(self):
        """Remove last notation if it is at end of the part where next note is to be inserted"""
        if self.notation_at_current_pos:
            self._notations.pop(-1)

    def append_misc_notation(self, notation_type: str):
        """Adds a notation next to the position where next note will be

        Args:
            type: What type of notation will be inserted

        Returns:
            Reference to inserted notation
        """
        notation = ShakuNotation(notation_type, len(self.notes))
        self._notations.append(notation)
        self._notation_at_current_pos = True

    def add_note(self, pitch: int, lenght: int):
        """Adds a note on part

        Args:
            pitch: Note pitch
            lenght: Note lenght

        Returns:
            True if note was added, False if no space for it
        """
        self.notes.append(ShakuNote(pitch, lenght))
        self._notation_at_current_pos = False

    def get_duration_until(self, note_id: int):
        """Get duration until a specific note

        Args:
            note_id: number of note in question

        Returns:
            duration (sum of lenght of previous notes) until note specified
        """
        return sum([note.lenght for note in self.notes[:note_id]])
