import pygame

class MidiPlayer:
    def __init__(self):
        self.midi_file = "music.mid"
        self.freq = 44180
        self.bitsize = -16
        self.buffer = 1024

    def play(self, channels):
        self.channels = channels
        pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        pygame.mixer.music.set_volume(0.8)
        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.load(self.midi_file)
        except pygame.error:
            print("Unable to load file")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(38)
