from square import square

import sys
from pathlib import Path
#sys.path.insert(0, str(Path(__file__).parent) + '/pieces_script')
sys.path.append(str(Path(__file__).parent) + '/pieces_script')

from knight import knight
from bishop import bishop
from rook import rook
from queen import queen
from king import king
from pawn import pawn

class board:
    def __init__(self):
        self.is_game_over = False
        self.position = self.initialize_board()
        self.sq = None
        self.piece = None

    def initialize_board(self):
        position = []
        row = []
        piece = None
        sq = None
        for i in range(8):
            for j in range(8):
                if i == 0 or i == 7:
                    if i == 0:
                        piece_color = "black"
                    elif i == 7:
                        piece_color = "white"

                    if j == 0 or j == 7:
                        piece = rook(piece_color)
                        sq = square(i, j, piece)
                        row.append(sq)
                    elif j == 1 or j == 6:
                        piece = knight(piece_color)
                        sq = square(i, j, piece)
                        row.append(sq)
                    elif j == 2 or j == 5:
                        piece = bishop(piece_color)
                        sq = square(i, j, piece)
                        row.append(sq)
                    elif j == 3:
                        piece = queen(piece_color)
                        sq = square(i, j, piece)
                        row.append(sq)
                    elif j == 4:
                        piece = king(piece_color)
                        sq = square(i, j, piece)
                        row.append(sq)
                elif i == 1 or i == 6:
                    if i == 1:
                        piece_color = "black"
                    elif i == 6:
                        piece_color = "white"

                    piece = pawn(piece_color)
                    sq = square(i, j, piece)
                    row.append(sq)
                else:
                    sq = square(i, j)
                    row.append(sq)
            position.append(row)
            row = []

        show_pieces = [] 
        for row in position:
            for sqr in row:
                if sqr.get_piece() == None:
                    show_pieces.append(" ")
                else:
                    show_pieces.append(sqr.get_piece().name)
            print(show_pieces)
            show_pieces = []

        return position
                    

        #[0,   1,  2,  3,  4,  5,  6,  7]
        #[8,   9, 10, 11, 12, 13, 14, 15]
        #[16, 17, 18, 19, 20, 21, 22, 23]
        #[24, 25, 26, 27, 28, 29, 30, 31]
        #[32, 33, 34, 35, 36, 37, 38, 39]
        #[40, 41, 42, 43, 44, 45, 46, 47]
        #[48, 49, 50, 51, 52, 53, 54, 55]
        #[56, 57, 58, 59, 60, 61, 62, 63]

        # ex: self.position[4][3] = 35
        # joueur blanc en bas de la matrice, joueur noir en haut


