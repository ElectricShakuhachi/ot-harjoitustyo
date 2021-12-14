from tkinter import Tk, PhotoImage
from ui.ui import UI

window = Tk()
window.title("Shakuhachi Music Maker")
img = PhotoImage(file='graphics/shakuicon.png')
window.tk.call('wm', 'iconphoto', window._w, img)
ui = UI(window)
def clear_messages():
    for i in ui.messages:
        if i.state == "active":
            i.window.destroy()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", clear_messages)
window.mainloop()
