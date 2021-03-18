from piece import piece

class pawn(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "P"
        self.name = "pawn"
        self.as_moved = False
        self.starting_row = None
        self.starting_column = None

    def get_valid_moves(self):
        pass