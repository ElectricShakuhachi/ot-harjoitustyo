import config.shaku_constants as consts

class Positioner:
    def _calculate_start(part: int, spacing: int):
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

    def position(self, parts: int, part: int, notes: list, mode:str):
        y = consts.PARTS_Y_START
        x = self._calculate_start(part, max(parts, 2))
        if mode == "Tozan":
            measure_skip = consts.MEASURE_SKIP_LENGHT
        y_spacing = consts.NOTE_Y_SPACING
        max_note_y = consts.SHEET_SIZE[1] - 47 #Get this dir from consts instead?




"""
What this class is supposed to do 

Receives:
- number of parts
- constant values for spacing etc.
- which notation system
- measure lenght if Tozan (None or ignored if others)
- starting x and y positions

- part number
- stream of notes 

RETURNS:


((page_no, (x, y)),
(page_no, (x, y)),
(page_no, (x, y))...
)

 -> which page, what coordinates to place each note of part to


ATTENTION:
- We could REFACTOR so that all other notations besides notes (and texts)
are in fact owned by each note, so that they can then easily be placed together with them.

"""