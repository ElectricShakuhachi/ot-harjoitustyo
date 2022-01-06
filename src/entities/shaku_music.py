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

    def add_part(self, part_id: int):
        """Adds a new musical part into the composition if there is room

        Args:
            part_id: id for new part

        Returns:
            True if part was added, False if there is no room to add part
        """
        if part_id in self.parts:
            raise ValueError(f"Part already exists for given id: {part_id}")
        self.spacing += 1
        self._parts[part_id] = ShakuPart(part_id)

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
                "notes": [],
                "notations": [],
                "notation_at_current_pos": part_data.notation_at_current_pos
            }
            for note in part_data.notes:
                data["parts"][part_n]["notes"].append({
                    "pitch": note.pitch,
                    "lenght": note.lenght,
                })
            for notation in part_data.notations:
                data["parts"][part_n]["notations"].append({
                    "type": notation.notation_type,
                    "relative_note": notation.relative_note
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
                )
            part.notation_at_current_pos = part_data["notation_at_current_pos"]
            for note in part_data["notes"]:
                recovered_note = ShakuNote(
                    int(note["pitch"]),
                    int(note["lenght"])
                    )
                part.notes.append(recovered_note)
            for notation in part_data["notations"]:
                recovered_notation = ShakuNotation(
                    notation["type"],
                    notation["relative_note"]
                    )
                part.notations.append(recovered_notation)
