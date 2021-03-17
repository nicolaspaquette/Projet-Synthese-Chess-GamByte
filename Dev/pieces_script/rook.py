from piece import piece

class rook(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "R"
        self.name = "rook"

    def get_valid_moves(self):
        pass