from services.filing import FileManager
from ui.messages import ShakuMessage
from ui.ui import UI

class Commands:
    def __init__(self, main_ui: UI):
        self._main_ui = main_ui
        self._shaku_filename = None
        self._saved = True

    def save(self):
        """Save currently edited music sheet to previously saved file, prompt if none"""
        filemanager = FileManager()
        data = self._main_ui.music.convert_to_json()
        result = filemanager.save_shaku(data, filename=self._shaku_filename)
        if result is not False:
            self._shaku_filename = str(result)
            self._saved = True
            return True
        return False

    def save_as(self):
        """Save currently edited music sheet to file, prompt for filename"""
        filemanager = FileManager()
        data = self._main_ui.music.convert_to_json()
        result = filemanager.save_shaku(data, filename=self._shaku_filename)
        if result is not False:
            self._shaku_filename = result
            self._saved = True
            return True
        return False

    def load(self):
        """Load a .shaku (JSON) -file to edit in software"""
        if not self._saved:
            self._main_ui.messages.append(ShakuMessage("Overwrite"))
        filemanager = FileManager()
        data = filemanager.load()
        self._main_ui.clear_messages()
        if data is None:
            return
        if data == "JSON Error" or not self._main_ui.music.data_correct(data):
            self._main_ui.messages.append(ShakuMessage("Incorrect File"))
            return
        return data

    def set_unsaved(self): # perhaps not to be used finally
        self._saved = False
