class ShakuButton:
    def __init__(self, text, data, type):
        self.text = text
        self.type = type
        if type == "note":
            self.pitch = data
        elif type == "lenght":
            self.lenght = data