
class square:
    def __init__(self, row, column, piece = None):
        self.row = row
        self.column = column
        self.size = 75
        self.piece = piece

    def add_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece
