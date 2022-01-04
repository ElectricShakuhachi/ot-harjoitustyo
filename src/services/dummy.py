import tkinter as tk
import math

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.pack(fill="both", expand=True)

    def create(self, x_start, y_start, x_end, y_end, arch=10):
        tangent = math.atan2(y_end - y_start, x_end - x_start)
        x_mid = (x_start + x_end)/2 + math.sin(tangent) * arch
        y_mid = (y_start + y_end)/2 - math.cos(tangent) * arch
        return (x_start, y_start, x_mid, y_mid, x_end, y_end)

    def draw_line(self, *args, **kwargs):
        self.canvas.create_line(*args, **kwargs)

if __name__ == "__main__": #THIS IS NEEDED FOR HANDLING AT TKINTER (and pil etc.) end
    app = SampleApp()
    res = app.create(100, 100, 100, 200)
    var = len(res) > 4
    app.draw_line(res, smooth=var)
    app.mainloop()
