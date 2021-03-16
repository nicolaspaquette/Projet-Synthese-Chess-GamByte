
#import sys
#from pathlib import Path
#sys.path.insert(0, str(Path(__file__).parent) + '/pieces_script')
#sys.path.append(str(Path(__file__).parent) + '/pieces_script')

from square import square
from bishop import bishop
from knight import knight
from rook import rook
from queen import queen
from king import king
from pawn import pawn

class board():
    def __init__(self):
        self.is_game_over = False
        self.initialize_board()

    def initialize_board(self):
        self.position = []
        self.row = []
        self.piece_color = None

        for i in range(8):
            for j in range(8):
                if i == 0 or i == 7:
                    if i == 0:
                        self.piece_color = "black"
                    elif i == 7:
                        self.piece_color = "white"

                    if j == 0 or j == 7:
                        piece = rook(self.piece_color)
                        sq = square(i, j, piece)
                        self.row.append(sq)
                    elif j == 1 or j == 6:
                        self.row.append(square(i,j,knight(self.piece_color)))
                    elif j == 2 or j == 5:
                        self.row.append(square(i,j,bishop(self.piece_color)))
                    elif j == 3:
                        self.row.append(square(i,j,queen(self.piece_color)))
                    elif j == 4:
                        self.row.append(square(i,j,king(self.piece_color)))
                elif i == 1 or i == 6:
                    if i == 1:
                        self.piece_color = "black"
                    elif i == 6:
                        self.piece_color = "white"

                    self.row.append(square(i,j,pawn(self.piece_color)))
                else:
                    self.row.append(square(i,j))
            self.position.append(self.row)
            self.row = []

        list_pieces = []
        for row in self.position:
            for square in row:
                if square.get_piece() != None:
                    list_pieces.append(square.get_piece().name)
                else:
                    liste_pieces.append(" ")
            print(list_pieces)
            list_pieces = []
                    
                    


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


