from piece import piece

class queen(piece):
    def __init__(self, color):
        self.color = color
        self.name = "Q"

    def get_valid_moves(self):
        pass