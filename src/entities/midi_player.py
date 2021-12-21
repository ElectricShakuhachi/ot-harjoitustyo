import pygame
from midi2audio import FluidSynth

class MidiPlayer:
    def __init__(self):
        self.freq = 44180
        self.bitsize = -16
        self.buffer = 1024

    def convert(self, source, target):
        fs = FluidSynth()
        fs.midi_to_audio(source, target)

    def play(self, channels, name):
        self.channels = channels
        pygame.mixer.init()
        self.convert(name, "tmpshaku.wav")
        pygame.mixer.music.load("tmpshaku.wav") # this is what causes segfault when loading midi, but doesn seem to be so for mp3
        pygame.mixer.music.play(0, 0.0)
        while pygame.mixer.music.get_busy():
            pass