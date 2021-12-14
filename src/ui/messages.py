from tkinter import Tk, Label

class ShakuMessage:
    def __init__(self, message_type):
        self.state = "active"
        self.window = Tk()
        self.window.title("Warning: " + message_type)
        if message_type == "Full Sheet":
            msgtext = "  Sheet full, current version does not support multiple pages.\nSave sheet and create new one\nfor any additional pages."
        if message_type == "No Access":
            msgtext = "You have not configured credentials to the Shakunotator AWS Storage.\nIf necessary, please request access from admin."
        if message_type == "No Name":
            msgtext = "You have to add a name to your composition to upload."
        self.message = Label(self.window, text=msgtext)
        self.message.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.disactivate)

    def disactivate(self):
        self.state = 'destroyed'
        self.window.destroy()