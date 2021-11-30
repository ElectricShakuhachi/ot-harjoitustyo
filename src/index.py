from tkinter import Tk
from ui.ui import UI

window = Tk()
window.title("Shakuhachi Music Maker")
ui = UI(window)
ui.start()
def clear_messages():
    for i in ui.messages:
        if i.state == "active":
            i.window.destroy()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", clear_messages)
window.mainloop()

