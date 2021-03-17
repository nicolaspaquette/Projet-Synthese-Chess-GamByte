from piece import piece

class knight(piece):
    def __init__(self, color):
        self.color = color
        self.name = "N"

    def get_valid_moves(self):
        pass