from tkinter import Tk, PhotoImage
from ui.view import View

window = Tk()
window.title("Shakuhachi Music Maker")
img = PhotoImage(file='src/graphics/shakuicon.png')
window.tk.call('wm', 'iconphoto', window._w, img)
ui = View(window)
def clear_messages():
    for i in ui.messages:
        if i.state == "active":
            i.window.destroy()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", clear_messages)
window.mainloop()
