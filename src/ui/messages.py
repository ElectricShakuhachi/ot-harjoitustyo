from tkinter import *

class ShakuMessage:
    def __init__(self, message_type):
        self.state = "active"
        self.window = Tk()
        self.window.title("Warning: " + message_type)
        if message_type == "Full Sheet":
            msgtext = "  Sheet full, current version does\nnot support multiple pages.\nSave sheet and create new one\nfor any additional pages."
        self.message = Label(self.window, text=msgtext)
        self.message.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.disactivate)

    def disactivate(self):
        self.state = 'destroyed'
        self.window.destroy()