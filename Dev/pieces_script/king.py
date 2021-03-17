from piece import piece

class king(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "K"
        self.name = "king"

    def get_valid_moves(self):
        pass