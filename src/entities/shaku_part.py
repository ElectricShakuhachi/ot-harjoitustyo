from copy import copy
import config.shaku_constants as consts
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
    def __init__(self, part_id: int, start_x: int, spacing: int):
        """Constructor, intializes class attributes

        Args:
            part_id: number of part on musical notation sheet
            start_x: x-axis for positioning first note of the part
            spacing: value depicting how much x-axis room to leave between rows of notes
        """
        self._part_no = part_id
        self._notes = []
        self._notations = []
        self._start_x = start_x
        self._measure_counter = 0
        self._spacing = spacing
        self._rows = 0
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

    @property
    def measure_counter(self):
        """Get measure_counter"""
        return self._measure_counter

    @measure_counter.setter
    def measure_counter(self, value: int):
        """Get measure_counter"""
        self._measure_counter = value

    @property
    def start_x(self):
        """Get start_x, the x axis position where notes start on part"""
        return self._start_x

    @start_x.setter
    def start_x(self, value: int):
        """Set start_x, the x axis position where notes start on part"""
        self._start_x = value

    @property
    def rows(self):
        """Get amount of rows in part"""
        return self._rows

    @rows.setter
    def rows(self, value: int):
        """Set part row count"""
        self._rows = value

    @property
    def spacing(self):
        """Get part spacing"""
        return self._spacing

    @spacing.setter
    def spacing(self, spacing: int):
        """Set the spacing == amount of room on x-axis between rows on part.

        Args:
            spacing: Value depicting how much to create space
        """
        change = spacing - self._spacing
        self._spacing = spacing
        row = 0
        if spacing > 2:
            for i in range(1, len(self.notes)):
                previous = self.notes[i - 1].position[0] + row * change * consts.NOTE_ROW_SPACING
                if self.notes[i].position[0] < previous:
                    row += 1
                self.notes[i].position[0] -= row * change * consts.NOTE_ROW_SPACING

    def realign(self, spacing: int, start_x: int):
        """Change part spacing and x-axis alingment

        Args:
            spacing: New spacing between rows on part
            start_x: New x-axis alignment
        """
        self.spacing = spacing
        change = start_x - self._start_x
        self._start_x = start_x
        for note in self.notes:
            note.position[0] += change

    def clear_pre_existing_notation(self):
        """Remove last notation if it is at end of the part where next note is to be inserted"""
        if self.notation_at_current_pos:
            self._notations.pop(-1)

    def next_position(self):
        """Calculates position to be used for next note on part

        Returns:
            [x, y] - values depicting x and y -axis placing of next note to be added on part
        """
        if len(self.notes) == 0:
            return [self._start_x, 80]
        next_pos = copy(self.notes[-1].position)
        next_pos[1] += self.notes[-1].lenght * 6
        if self._measure_counter == 0:
            next_pos[1] += 14
        if next_pos[1] > 830:
            next_pos[1] = 80
            next_pos[0] -= self.spacing * consts.NOTE_ROW_SPACING
        return next_pos

    def append_misc_notation(self, notation_type: str):
        """Adds a notation next to the position where next note will be

        Args:
            type: What type of notation will be inserted

        Returns:
            Reference to inserted notation
        """
        position = self.next_position()
        position[0] = consts.NOTATION_APPENDIX_X_FROM_NOTE
        position[1] = consts.NOTATION_APPENDIX_Y_FROM_NOTE
        notation = ShakuNotation(notation_type, position, len(self.notes))
        self._notations.append(notation)
        self._notation_at_current_pos = True

    def add_note(self, note: ShakuNote):
        """Adds a note on part

        Args:
            note: a note instance depicting note to be added

        Returns:
            True if note was added, False if no space for it
        """
        if len(self.notes) == 0 or self.notes[-1].position[0] > note.position[0]:
            self._rows += 1
        if note.position[0] < 55:
            return False
        self.notes.append(note)
        if self._measure_counter == 0:
            note.first = True
        self._measure_counter += note.lenght
        if self._measure_counter == consts.MEASURE_LENGHT * 8:
            self._measure_counter = 0
        self._notation_at_current_pos = False
        return True

    def time_notation(self, note_n: int):
        """Generate rhythm notation for a single note

        Args:
            note_n: index of note on part's list of notes

        Returns:
            Coordinates for rhytm notation
        """
        def_x = consts.NOTE_TO_RHYTM_SPACING
        def_x2 = consts.RHYTM_LINE2_TO_LINE1_SPACING + def_x
        notation = []
        if self.notes[note_n].pitch < 0:
            return notation
        note = self.notes[note_n]
        x_axis = note.position[0]
        y_axis = note.position[1] + consts.RHTM_VERTICAL_LINE_START_TO_NOTE_Y
        if note_n > 0:
            previous = self.notes[note_n - 1]
        if note.lenght > 8:
            return notation
        notation.append(
            ((x_axis + def_x, y_axis),
            (x_axis + def_x, y_axis + consts.RHYTM_VERTICAL_LINE_LENGHT))
            )
        if note.lenght == 8:
            return notation
        if note_n != 0 and previous.lenght < 8 and not note.first:
            notation.append(
                ((x_axis + def_x, previous.position[1]),
                (x_axis + def_x, y_axis + consts.RHYTM_VERTICAL_LINE_LENGHT))
                )
        if note.lenght == 4:
            if note_n == 0 or note.first or previous.lenght > 4:
                note.dotted = True
                notation.append(
                    ((x_axis + def_x - 1, y_axis + 4),
                    (x_axis + def_x + 4, y_axis + 8))
                    )
            return notation
        notation.append(
            ((x_axis + def_x2, y_axis),
            (x_axis + def_x2, y_axis + consts.RHYTM_VERTICAL_LINE_LENGHT))
            )
        if note_n != 0 and previous.lenght < 3 and not note.first:
            notation.append(
                ((x_axis + def_x2, y_axis - 10),
                (x_axis + def_x2, y_axis + consts.RHYTM_VERTICAL_LINE_LENGHT))
                )
        if note.lenght == 1: #SPECIAL CASE -> NOT IN USE CURRENTLY
            notation.append(((def_x - 1, y_axis + 4), (def_x + 6, y_axis + 7)))
            note.dotted = True
        return notation

    def part_time_notations(self):
        """Generate note rhythm notation for all notes on part

        Returns:
            A depiction of all lines to be drawn for rhythms in part
        """
        notations = []
        for note_n in range(len(self._notes)):
            notations.append(self.time_notation(note_n))
            if self.notes[note_n].lenght == 4 and note_n > 0 and self.notes[note_n - 1].dotted:
                notations[-2] = notations[-2][:-1]
        return notations