import json
from tkinter import filedialog

class FileManager:
    def save_shaku(self, data):
        with filedialog.asksaveasfile(mode='w', defaultextension=".shaku") as file:
            json.dump(data, file, indent=4)

    def load(self):
        with filedialog.askopenfile(mode='r', defaultextension=".shaku") as file:
            data = json.load(file)
            return data

    def save_pdf(self, image):
        with filedialog.asksaveasfile(mode='wb', defaultextension=".pdf") as file:
            image.save(file, format="pdf")