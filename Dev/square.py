from bishop import bishop
from knight import knight
from rook import rook
from queen import queen
from king import king
from pawn import pawn

class square():
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.size = 90

    def add_piece(self, piece):
        self.piece = piece
