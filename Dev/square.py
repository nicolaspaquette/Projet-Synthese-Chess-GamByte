
class square():
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.size = 90
        self.piece = None
    
    def __init__(self, row, column, piece):
        self.row = row
        self.column = column
        self.size = 90
        self.piece = piece

    def add_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece
