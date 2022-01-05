import os
from dotenv import load_dotenv
from tkinter import Tk, PhotoImage
from ui.ui import UI
from ui.buttons import Buttons

dirname = os.path.dirname(__file__)
try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    print("not found")
window = Tk()
window.title("Shakuhachi Music Maker")
img = PhotoImage(file='src/graphics/shakuicon.png')
window.tk.call('wm', 'iconphoto', window._w, img)
ui = UI(window)
controls = Buttons(ui)
window.protocol("WM_DELETE_WINDOW", ui.destroy_all_windows)
window.mainloop()
