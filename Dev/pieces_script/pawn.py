from piece import piece

class pawn(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "P"
        self.name = "pawn"

    def get_valid_moves(self):
        pass