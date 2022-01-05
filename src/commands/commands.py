import os
import pygame
from services.filing import FileManager
from services.image_creator import ImageCreator
from services.svg_creator import SvgCreator
from services.midi_creator import MidiCreator
from services.conversions import MusicConverter
from services.music_player import MusicPlayer
from ui.messages import ShakuMessage
from ui.ui import UI
from entities.shaku_music import ShakuMusic

class Commands:
    def __init__(self, main_ui: UI):
        self._main_ui = main_ui
        self._shaku_filename = None

    def new(self):
        pass

    def save(self, music: ShakuMusic):
        """Save currently edited music sheet to previously saved file, prompt if none"""
        filemanager = FileManager()
        data = music.convert_to_json()
        result = filemanager.save_shaku(data, filename=self._shaku_filename)
        if not result:
            return False
        self._shaku_filename = str(result)
        return True

    def save_as(self, music: ShakuMusic):
        """Save currently edited music sheet to file, prompt for filename"""
        filemanager = FileManager()
        data = music.convert_to_json()
        result = filemanager.save_shaku(data, filename=None)
        if not result:
            return False
        self._shaku_filename = result
        return True

    def load(self, filename=None):
        """Load a .shaku (JSON) -file to edit in software"""
        filemanager = FileManager()
        data = filemanager.load_shaku(filename=filename)
        self._main_ui.clear_messages()
        if data is None:
            return
        filename = data[0]
        data = data[1]
        if data == "JSON Error" or not self._main_ui.music.data_correct(data):
            self._main_ui.messages.append(ShakuMessage("Incorrect File"))
            return
        self._shaku_filename = filename
        return data

    def export_pdf(self, music: ShakuMusic, grid_option):
        filemanager = FileManager()
        image_creator = ImageCreator()
        images = image_creator.create_images(music, grid_option)
        filemanager.save_pdf(images)

    def export_svg(self, music: ShakuMusic, grid_option):
        filemanager = FileManager()
        svg_creator = SvgCreator()
        svgs = svg_creator.create_svg(music, grid_option)
        filemanager.save_svg(svgs)

    def export_midi(self, music: ShakuMusic):
        filemanager = FileManager()
        creator = MidiCreator()
        for part in music.parts.values():
            creator.create_track(part)
        midi = creator.generate_midi() 
        filemanager.save_midi(midi)

    def save_wav(self, music: ShakuMusic):
        filemanager = FileManager()
        creator = MidiCreator()
        converter = MusicConverter()
        for part in music.parts.values():
            creator.create_track(part)
        midi = creator.generate_midi()
        tmp_filename = "shakutmp"
        filename = filemanager.save_midi(midi)
        converter.convert(filename, filename[:-4] + " .wav")
        os.remove(filename)

    def upload_to_aws_s3(self, music: ShakuMusic):
        filemanager = FileManager()
        data = music.convert_to_json()
        name = music.name
        if not name or name == "":
            return "No Name"
        elif not filemanager.upload_to_aws_s3(data, name=name):
            return "No Access"
        return "Successful Upload"

    def download_from_aws_s3(self, item):
        filemanager = FileManager()
        result = filemanager.download_from_aws_s3(item)
        if not result:
            return "No Access"
        return result

    def list_files_in_aws_s3(self):
        filemanager = FileManager()
        result = filemanager.list_files_in_aws_s3()
        if not result:
            return "No Access"
        return result

    def add_part(self, music: ShakuMusic):
        i = len(music.parts) + 1
        music.add_part(i)
        return i

    def play_music(self, music: ShakuMusic):
        player = MusicPlayer()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        else:
            player.play(music.parts.values())