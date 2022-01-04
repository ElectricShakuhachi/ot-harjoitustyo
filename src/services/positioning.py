import config.shaku_constants as consts
from services.conversions import GraphicsConverter

class ShakuPositions:
    def calculate_start(self, part: int, spacing: int):
        """Return x-axis start spot for given part on sheet music

        Args:
            part: part number 
            spacing: music spacing (row size multiplier)

        Returns:
            x-axis startpoint for part on sheet
        """
        section_size = consts.NOTE_ROW_SPACING * spacing
        grid_x = consts.GRID_X
        grid_width = grid_x[1] - grid_x[0]
        grid_width -= grid_width % section_size
        first_sect = grid_width - section_size
        half_of_note = consts.SHEET_NOTE_SIZE / 2
        subsection = consts.NOTE_ROW_SPACING
        subsection_count = section_size / subsection - part
        start_x = first_sect + subsection * subsection_count + grid_x[0] - half_of_note
        return start_x

    def get_row_count(self, spacing: int):
        """Counts how many rows there are going to be on a given page

        Args:
            spacing: music spacing (row size multiplier)

        Returns:
            Count of rows per page
        """
        row_size = consts.NOTE_ROW_SPACING * spacing
        grid_x = consts.GRID_X
        row_count = (grid_x[1] - grid_x[0]) // row_size
        return row_count

    def _get_measure_skip_count(self):
        """Internal function"""
        y_space = consts.GRID_Y[1] - consts.GRID_Y[0]
        measure_lenght = consts.MEASURE_LENGHT
        measure_y = consts.NOTE_Y_SPACING * 4 * measure_lenght
        measure_count = y_space // measure_y
        return measure_count - 1

    def get_slot_count(self, measures: bool):
        """Returns count of how many note slots there are per row

        Args:
            measures: whether or not the target system uses measures

        Returns:
            Count of how many slots per row there are
        """
        y_space = consts.GRID_Y[1] - consts.GRID_Y[0]
        smallest_slot = consts.NOTE_Y_SPACING
        if measures:
            skipcount = self._get_measure_skip_count()
            y_space -= skipcount * consts.MEASURE_SKIP_LENGHT
        return y_space // smallest_slot - 1

    def get_relative_positions(self, note_lenghts: list, rows: int, slots: int, by_lenght: bool, misc_notation: bool=False):
        """Get a list of relative positions where to place notes on sheet music

        Args:
            notes: list of notes (ShakuNote) in given part
            rows: Amount of rows per page on sheet music
            slots: Amount of shortest note slots per row
            by_lenght: Whether notes will take room based on their lenghts
            misc_notation: True if looking for misc notation position and not notes

        Returns:
            Dictionaries depicting page, row and slot for each note
        """
        note_positions = []
        page = 0
        row = 0
        slot = 0
        for note_lenght in note_lenghts:
            if not misc_notation:
                note_positions.append({"page": page, "row": row, "slot": slot})
            increment = 1 if not by_lenght else note_lenght / 2
            slot += increment
            while slot > slots:
                slot -= (slots + 1)
                row += 1
                if row >= rows:
                    row -= rows
                    page += 1
            if misc_notation:
                note_positions.append({"page": page, "row": row, "slot": slot})
        return tuple(note_positions)

    def get_coordinates(self, pos: dict, part: int, spacing: int, measures: bool):
        """Get absolute coordinates for a note on sheet

        Args:
            pos: dict depiction of notes relative position
            part: part number
            spacing: music spacing (row size multiplier)
            measures: whether or not to include measure spacing

        Returns:
            [type]: [description]
        """
        start_x = self.calculate_start(part, spacing)
        start_y = consts.PARTS_Y_START
        y_spacing = consts.NOTE_Y_SPACING
        if measures:
            measure_lenght = consts.MEASURE_LENGHT
            measure_skip = consts.MEASURE_SKIP_LENGHT
            skip = measure_skip * (pos["slot"] // (measure_lenght * 4))
        else:
            skip = 0
        row_dist = consts.NOTE_ROW_SPACING * spacing
        x = start_x - pos["row"] * row_dist
        y = start_y + pos["slot"] * y_spacing + skip
        return (x, y)
