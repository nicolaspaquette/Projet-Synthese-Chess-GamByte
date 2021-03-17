from piece import piece

class bishop(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "B"
        self.name = "bishop"

    def get_valid_moves(self):
        pass