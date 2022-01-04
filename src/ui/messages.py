from tkinter import Label, Tk
import config.shaku_constants as consts

class ShakuMessage:
    def __init__(self, message_type):
        """Display a warning / error window

        Args:
            message_type: Type of message to display
        """
        self.state = "active"
        self.window = Tk()
        self.window.title("Warning: " + message_type)
        messages = {
            "Full Sheet": consts.MESSAGE_FULL_SHEET,
            "No Part Room": consts.MESSAGE_PART_ROOM,
            "No Access": consts.MESSAGE_NO_ACCESS_TO_AWS,
            "No Name": consts.MESSAGE_NO_NAME_TO_AWS,
            "Overwrite": consts.MESSAGE_OVERWRITE_ALERT,
            "long_name_and_composer": consts.MESSAGE_LONG_NAME_COMPOSER,
            "Incorrect File": consts.MESSAGE_INCORRECT_FILE,
            "dev": consts.MESSAGE_UNDER_DEVELOPMENT 
        }
        msgtext = messages[message_type]
        pads=consts.MESSAGE_PADDING
        self.message = Label(self.window, text=msgtext, padx=pads[0], pady=pads[1])
        self.message.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.disactivate)

    def disactivate(self):
        """Destroy message window if it isn't already destroyed"""
        if self.state != "destroyed":
            self.state = "destroyed"
            self.window.destroy()
