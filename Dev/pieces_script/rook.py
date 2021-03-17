from piece import piece

class rook(piece):
    def __init__(self, color):
        self.color = color
        self.name = "R"

    def get_valid_moves(self):
        pass