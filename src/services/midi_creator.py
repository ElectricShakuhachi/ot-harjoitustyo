from midiutil import MIDIFile
from entities.shaku_part import ShakuPart
import config.shaku_constants as consts

class MidiTrack:
    """Class instance represents track information to be written as a track to MIDI file

    Attributes:
        channel: Channel to be used for track in MIDI file
        notes: Notes as integers that represent pitches in MIDI format
        lenghts: Lenght of each note in notes
        notemap: Pitch conversion table
    """
    def __init__(self, channel: int, ro_daimeri_pitch: int=60):
        """Sets up pitch conversion table and initializes attributes

        Args:
            channel: Channel to be used in MIDI file for track
            ro_pitch: Base pitch of Shakuhachi in MIDI format. Defaults to 62.
        """
        self._channel = channel
        self._notes = []
        self._lenghts = []
        self._notemap = {}
        self._notemap[-1] = 0 # -1 represents break
        for i in range(0, 42):
            self._notemap[i] = i + ro_daimeri_pitch

    @property
    def channel(self):
        """Get channel for MIDI track"""
        return self._channel

    @property
    def notes(self):
        """Get list of notes on track with pitches converted into MIDI pitches"""
        return self._notes

    @property
    def lenghts(self):
        """Get list of note lenghts on track scaled for MIDI"""
        return self._lenghts

    def fill(self, part: ShakuPart):
        """Pre-processes musical part information for MIDI conversion

        Args:
            part: ShakuPart instance with note information to be filled to track
        """
        for note in part.notes:
            self._notes.append(self._notemap[note.pitch])
            self._lenghts.append(note.lenght / 8)

class MidiCreator:
    """Class for generating MIDI -format audio representation from ShakuNotator's music format

    Attributes:
        tempo: Tempo for MIDI file
        tracks: List of MidiTrack instances containing pitch and lenght data for each track
        volume: Volume for MIDI file
    """
    def __init__(self, tempo: int=consts.DEFAULT_TEMPO):
        """Constructor, sets up attributes for writing midi data

        Args:
            tempo: Tempo for MIDI file. Defaults to 65.
        """
        self._tempo = tempo
        self._tracks = {}
        self._volume = consts.DEFAULT_VOLUME

    def create_track(self, part: ShakuPart, ro_daimeri_pitch: int=60):
        """Generates track and adds it to list of tracks to be written together into MIDI format

        Args:
            part: ShakuPart instance containing necessary note pitch and lenght data
            ro_pitch: Base pitch of Shakuhachi in MIDI format. Defaults to 62.
        """
        track = MidiTrack(len(self._tracks), ro_daimeri_pitch)
        track.fill(part)
        self._tracks[len(self._tracks)] = track

    def generate_midi(self):
        """Generates a MIDI -format audio representation from track data in tracks (class attribute)

        Returns:
            MIDI -format music representation
        """
        file = MIDIFile(len(self._tracks))
        time = 0
        for track_id, track in self._tracks.items():
            file.addProgramChange(track_id, track.channel, 0, consts.MIDI_INSTRUMENT_NUMBER)
            file.addTempo(track_id, time, self._tempo)
            for num, pitch in enumerate(track.notes):
                volume = 0 if pitch < 0 else self._volume # negative pitch represents break
                file.addNote(track_id, track.channel, pitch, time, track.lenghts[num], volume)
                time += (track.lenghts[num])
            time = 0
        return file
