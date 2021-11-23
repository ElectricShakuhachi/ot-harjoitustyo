from tkinter import Tk
from ui.ui import UI


window = Tk()
window.title("Shakuhachi Music Maker")
ui = UI(window)
ui.start()
window.mainloop()
