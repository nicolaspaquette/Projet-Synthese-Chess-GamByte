from piece import piece

class king(piece):
    def __init__(self, color):
        self.color = color
        self.name = "K"

    def get_valid_moves(self):
        pass