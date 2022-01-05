from tkinter import Label, Tk, Listbox, Scrollbar, Frame, constants
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
            "dev": consts.MESSAGE_UNDER_DEVELOPMENT,
            "Successful Upload": consts.MESSAGE_SUCCESFUL_UPLOAD
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

class ShakuQuery: # maybe make this a subclass of Message?
    def __init__(self, query_type, query_list, buttons):
        self.buttons = buttons
        self.query_type = query_type
        self.state = "active"
        self.window = Tk()
        self.window.title("Compositions")
        text = "Downloadable music:"
        self.label = Label(self.window, text=text, padx=20, pady=20)
        self.label.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.disactivate)

        self.scrollframe = Frame(self.window, background="dark gray")
        self.scrollframe.pack(side=constants.LEFT, padx=20, pady=(0, 20), fill=constants.BOTH, expand=constants.YES)
        self.listbox = Listbox(self.scrollframe)
        self.listbox.pack(side = constants.LEFT, expand=constants.YES, fill=constants.BOTH)
        scroll = Scrollbar(self.scrollframe, command=self.listbox.yview)
        scroll.pack(side=constants.RIGHT, fill=constants.Y)
        longest = 0
        for item in query_list:
            longest = max(len(item), longest)
            self.listbox.insert(constants.END, item)
        self.listbox.config(yscrollcommand=scroll.set)
        box_size = 8 * longest + 50
        box_size = max(min(box_size, 410), 300)
        self.window.geometry(f"{box_size}x{box_size}")
        self.listbox.bind("<<ListboxSelect>>", self.select)

    def select(self, event):
        item = self.listbox.get(self.listbox.curselection())
        self.buttons._relay_to_download_aws_s3(item)

    def disactivate(self):
        if self.state != "destroyed":
            self.state = "destroyed"
            self.window.destroy()
