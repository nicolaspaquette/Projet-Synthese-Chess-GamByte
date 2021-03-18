from piece import piece

class rook(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "R"
        self.name = "rook"
        self.as_moved = False
        self.starting_row = None
        self.starting_column = None

    def get_valid_moves(self):
        pass