from piece import piece

class queen(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "Q"
        self.name = "queen"

    def get_valid_moves(self):
        pass