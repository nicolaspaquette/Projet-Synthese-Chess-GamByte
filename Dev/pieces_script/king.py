from piece import piece

class king(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "K"
        self.name = "king"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None
        self.can_be_captured_en_passant = False

    def get_valid_positions(self, board_positions, row, column):
        pass