from tkinter import *

class UI:
    def __init__(self, window):
        self.window = window
        self.window.geometry("700x900")
        self.frame = Frame(self.window)
        self.frame.pack()
        self.top_frame = Frame(self.window)
        self.top_frame.pack(side=TOP)
        self.left_frame = Frame(self.window)
        self.left_frame.pack(side=LEFT)
        self.right_frame = Frame(self.window)
        self.right_frame.pack(side=RIGHT)
        self.buttons = []
        self.textboxes = []
        self.labels = []
        self.sheet = None

    def start(self):
        self.create_sheet()
        self.create_text_boxes()
        self.populate_buttons()

    def create_sheet(self):
        self.sheet = Canvas(
            self.left_frame,
            width=500,
            height=800,
            background="white",
        )
        self.sheet.pack(side = LEFT)

    def create_text_boxes(self):
        self.labels.append(Label(self.top_frame, text="Name"))
        self.textboxes.append(Entry(self.top_frame))
        for label in self.labels:
            label.pack(side = TOP)
        for box in self.textboxes:
            box.pack(side = TOP)

    def populate_buttons(self):
        button_texts = ["RO", "TSU", "RE", "CHI", "HA", "HI"]
        for b in button_texts:
            self.buttons.append(Button(self.right_frame, text=b))
        for button in self.buttons:
            button.pack(side=TOP)
