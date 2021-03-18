from square import square

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent) + '/pieces_script')

from knight import knight
from bishop import bishop
from rook import rook
from queen import queen
from king import king
from pawn import pawn

class board:
    def __init__(self, player_color):
        self.player_color = player_color
        self.is_game_over = False
        self.position = self.initialize_board()
        self.get_board_layout()
        self.is_board_flipped = False

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

        if self.player_color == "black":
            position.reverse()

        return position

    def get_board_layout(self):
        show_pieces = []
        for row in self.position:
            for sqr in row:
                if sqr.get_piece() == None:
                    show_pieces.append("      ")
                else:
                    show_pieces.append(sqr.get_piece().color + sqr.get_piece().sign)
            print(show_pieces)
            show_pieces = []          

        # 8 ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        # 7 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        # 6 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        # 5 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        # 4 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        # 3 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        # 2 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        # 1 ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        #     A    B    C    D    E    F    G    H
        
        #      human player always on the bottom


