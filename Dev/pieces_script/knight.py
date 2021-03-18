from piece import piece

class knight(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "N"
        self.name = "knight"
        self.as_moved = False
        self.starting_row = None
        self.starting_column = None

    def get_valid_moves(self):
        pass