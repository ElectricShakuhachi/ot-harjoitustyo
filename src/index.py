from tkinter import Tk, PhotoImage
from ui.ui import UI
from ui.buttons import Buttons

window = Tk()
window.title("Shakuhachi Music Maker")
img = PhotoImage(file='src/graphics/shakuicon.png')
window.tk.call('wm', 'iconphoto', window._w, img)
ui = UI(window)
controls = Buttons(ui)

def clear_messages():
    """Clear all message windows and main window"""
    for i in ui.messages:
        if i.state == "active":
            i.window.destroy()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", clear_messages)
window.mainloop()
