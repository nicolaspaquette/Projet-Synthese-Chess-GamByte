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
        self.human_player_color = player_color
        self.is_game_over = False
        self.position = self.initialize_board()
        #self.get_board_layout()
        self.initialize_starting_positions()

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

        if self.human_player_color == "black":
            position.reverse()

        return position

    def initialize_starting_positions(self):
        for i in range(8):
            for j in range(8):
                square = self.position[i][j]
                piece = square.get_piece()
                if piece != None:
                    piece.starting_row = i
                    piece.starting_column = j

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

    def get_piece_in_square(self, row , column):
        square = self.position[row][column]
        piece = square.get_piece()
        if piece != None:
            print(piece.color, piece.name, piece.starting_row, piece.starting_column)

    def choose_piece_to_move(self, row, column):
        square = self.position[row][column]
        piece = square.get_piece()
        if piece != None and piece.color == self.human_player_color:
            print("you choose your piece: " + piece.name + " at " + str(row) + " " + str(column))

        



