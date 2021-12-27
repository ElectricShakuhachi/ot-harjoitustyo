import config.shaku_constants as consts
from entities.shaku_part import ShakuPart
from entities.shaku_note import ShakuNote
from entities.shaku_notation import ShakuNotation

class ShakuMusic:
    """Representation of notation and markings on a page of shakuhachi sheet music

    Attributes:
        name: Name of musical piece
        composer: Name of composer
        parts: Dictionary mapping each part name to a ShakuPart -instance
        measure_lenght: lenght of each measure in the sheet music (1 unit = 2 quarter notes)
        spacing: Multiplier for spacing between each row of music per part
    """
    def __init__(self):
        """Constructor, initializes class attributes"""
        self._name = ""
        self._composer = ""
        self._parts = {}
        self._measure_lenght = consts.MEASURE_LENGHT
        self._spacing = 1

    @property
    def name(self):
        """Get composition name"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Set composition name"""
        if len(name) + len(self._composer) < 50:
            self._name = name
        else:
            raise ValueError("Name & Composer combination too long")

    @property
    def composer(self):
        """Get composer name"""
        return self._composer

    @composer.setter
    def composer(self, composer: str):
        """Set composer name"""
        if len(composer) + len(self._name) < 50:
            self._composer = composer
        else:
            raise ValueError("Name & Composer combination too long")

    @property
    def parts(self):
        """Get parts"""
        return self._parts

    @property
    def spacing(self):
        """Get spacing"""
        return self._spacing

    @spacing.setter
    def spacing(self, spacing: str):
        """Set spacing"""
        if spacing > 0:
            self._spacing = spacing
        else:
            raise ValueError("Spacing has to be a positive value")

    def _maximum_rows_for_part_amount(self):
        next_section_size = consts.NOTE_ROW_SPACING * (self.spacing + 1)
        return (consts.GRID_X[1] - consts.GRID_X[0]) // next_section_size

    def _max_rows(self):
        maximum = self._maximum_rows_for_part_amount()
        for part in self._parts.values():
            if part.rows > maximum:
                return True
        return False

    def add_part(self, part_id: int):
        """Adds a new musical part into the composition if there is room

        Args:
            part_id: id for new part

        Returns:
            True if part was added, False if there is no room to add part
        """
        if self._max_rows() or part_id in self.parts:
            return False
        self.spacing += 1
        start_x = self._start_x_of_part(part_id)
        self._parts[part_id] = ShakuPart(part_id, start_x, self.spacing)
        self._realign_parts()
        return True

    def _start_x_of_part(self, part_id: int):
        section_size = consts.NOTE_ROW_SPACING * self.spacing
        grid_x = consts.GRID_X
        grid_width = grid_x[1] - grid_x[0]
        grid_width -= grid_width % section_size
        first_sect = grid_width - section_size
        half_of_note = consts.SHEET_NOTE_SIZE / 2
        subsection = consts.NOTE_ROW_SPACING
        subsection_count = section_size / subsection - part_id
        start_x = first_sect + subsection * subsection_count + grid_x[0] - half_of_note
        return start_x

    def _realign_parts(self):
        for key, part in self.parts.items():
            start_x = self._start_x_of_part(key)
            part.realign(self.spacing, start_x)

    def data_correct(self, data):
        """Runs a check if loaded JSON contains correct high level values

        Args:
            data: JSON data

        Returns:
            True if correct keys for .shaku -file exist in JSON data, otherwise False
        """
        keylist = ["name", "composer", "parts", "spacing"]
        for key in keylist:
            if key not in data.keys():
                return False
        return True

    def convert_to_json(self):
        """Convert data contained in ShakuMusic instance to JSON format

        Returns:
            Musical notation data in JSON format (no combatibility with other applications)
        """
        data = {
            "name": self._name,
            "composer": self._composer,
            "parts": {},
            "spacing": self.spacing
        }
        for part_n, part_data in self._parts.items():
            data['parts'][part_n] = {
                "part_no": part_data.part_no,
                "start_x": part_data.start_x,
                "measure_counter": part_data.measure_counter,
                "spacing": part_data.spacing,
                "rows": part_data.rows,
                "notes": [],
                "notations": [],
                "notation_at_current_pos": part_data.notation_at_current_pos
            }
            for note in part_data.notes:
                data["parts"][part_n]["notes"].append({
                    "pitch": note.pitch,
                    "lenght": note.lenght,
                    "position": note.position,
                    "first": note.first,
                    "dotted": note.dotted
                })
            for notation in part_data.notations:
                data["parts"][part_n]["notations"].append({
                    "type": notation.notation_type,
                    "position": notation.position,
                    "note_id": notation.note_id
                })
        return data

    def load_json(self, data: dict):
        """Receives JSON data and generates ShakuMusic class contents from it

        Args:
            data: A description of ShakuMusic instance contents in JSON -format
        """
        self.name = data["name"]
        self.composer = data["composer"]
        self.spacing = data["spacing"]
        for part_id, part_data in data['parts'].items():
            part = self._parts[int(part_id)] = ShakuPart(
                part_data["part_no"],
                part_data["start_x"],
                part_data["spacing"]
                )
            part.measure_counter = part_data["measure_counter"]
            part.rows = part_data["rows"]
            part.notation_at_current_pos = part_data["notation_at_current_pos"]
            for note in part_data["notes"]:
                recovered_note = ShakuNote(
                    int(note["pitch"]),
                    note["position"],
                    int(note["lenght"])
                    )
                recovered_note.first = note["first"]
                recovered_note.dotted = note["dotted"]
                part.notes.append(recovered_note)
            for notation in part_data["notations"]:
                recovered_notation = ShakuNotation(
                    notation["type"],
                    notation["position"],
                    notation["note_id"]
                    )
                part.notations.append(recovered_notation)
