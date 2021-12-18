from midiutil import MIDIFile
from entities.music import Part

class MidiTrack:
    def __init__(self, channel, ro_pitch=62):
        self.channel = channel
        self.notes = []
        self.lenghts = []
        self.notemap = {}
        self.notemap[-1] = 0
        for i in range(0, 39):
            self.notemap[i] = i + ro_pitch

    def fill(self, part: Part):
        for note in part.notes:
            self.notes.append(self.notemap[note.pitch])
            self.lenghts.append(note.lenght)

class MidiCreator:
    def __init__(self, tempo=65):
        self.tempo = tempo
        self.time = 0
        self.tracks = []
        self.volume = 100

    def create_track(self, part, ro_pitch=62):
        track = MidiTrack(len(self.tracks), ro_pitch)
        track.fill(part)
        self.tracks.append(track)

    def write_file(self):
        file = MIDIFile(len(self.tracks))
        
        for track in range(len(self.tracks)):
            file.addProgramChange(track, self.tracks[track].channel, 0, 73)
            file.addTempo(track, self.time, self.tempo)
            for num, pitch in enumerate(self.tracks[track].notes):
                volume = 0 if pitch == -1 else self.volume
                file.addNote(track, self.tracks[track].channel, pitch, self.time, self.tracks[track].lenghts[num] / 8, volume)
                self.time += (self.tracks[track].lenghts[num]) / 8
            self.time = 0
        with open("music.mid", "wb") as f:
            file.writeFile(f)
