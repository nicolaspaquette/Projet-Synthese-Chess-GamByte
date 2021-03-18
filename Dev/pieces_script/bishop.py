from piece import piece

class bishop(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "B"
        self.name = "bishop"
        self.as_moved = False
        self.starting_row = None
        self.starting_column = None

    def get_valid_moves(self):
        pass