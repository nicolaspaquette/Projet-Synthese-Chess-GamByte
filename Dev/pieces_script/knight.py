from piece import piece

class knight(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "N"
        self.name = "knight"

    def get_valid_moves(self):
        pass