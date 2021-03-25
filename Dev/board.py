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
        self.selected_square = None

    def initialize_board(self):
        position = []
        row = []
        piece = None
        sq = None

        for i in range(8):
            for j in range(8):
                if i == 0 or i == 7:
                    if self.human_player_color == "white":
                        if i == 0:
                            piece_color = "black"
                        elif i == 7:
                            piece_color = "white"
                    else:
                        if i == 0:
                            piece_color = "white"
                        elif i == 7:
                            piece_color = "black"

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
                        if self.human_player_color == "white":
                            piece = queen(piece_color)
                        else:
                            piece = king(piece_color)
                        sq = square(i, j, piece)
                        row.append(sq)
                    elif j == 4:
                        if self.human_player_color == "white":
                            piece = king(piece_color)
                        else:
                            piece = queen(piece_color)
                        sq = square(i, j, piece)
                        row.append(sq)
                elif i == 1 or i == 6:
                    if self.human_player_color == "white":
                        if i == 1:
                            piece_color = "black"
                        elif i == 6:
                            piece_color = "white"
                    else:
                        if i == 1:
                            piece_color = "white"
                        elif i == 6:
                            piece_color = "black"

                    piece = pawn(piece_color)
                    sq = square(i, j, piece)
                    row.append(sq)
                else:
                    sq = square(i, j)
                    row.append(sq)
            position.append(row)
            row = []

        return position

    def initialize_starting_positions(self):
        for i in range(8):
            for j in range(8):
                square = self.position[i][j]
                piece = square.get_piece()
                if piece != None:
                    piece.initialized_row = i
                    piece.initialized_column = j

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
            print(piece.color, piece.name, piece.initialized_row, piece.initialized_column)

    def get_square_position(self, row , column):
        square = self.position[row][column]

    def choose_piece_to_move(self, row, column):
        square = self.position[row][column]
        piece = square.get_piece()
        #if piece != None: #and piece.color == self.human_player_color:
        if piece != None and piece.color == self.human_player_color:
            print("you choose your piece: " + piece.name + " at " + str(row) + " " + str(column))
            self.selected_square = square
            return True
        else:
            return False

    def verify_move(self, starting_row, starting_column, final_row, final_column):
        piece = self.selected_square.get_piece()
        is_valid = piece.is_move_valid(starting_row, starting_column, final_row, final_column)
        return is_valid

    def move_piece(self, starting_row, starting_column, final_row, final_column, valid_positions):
        moving_piece = self.selected_square.get_piece()
        self.selected_square.remove_piece()
        self.position[final_row][final_column].add_piece(moving_piece)

        if self.selected_square in valid_positions:
            valid_positions.remove(self.selected_square)

        return valid_positions

    def get_valid_positions(self, starting_row, starting_column):
        possible_squares = []
        valid_positions = []
        piece = self.selected_square.get_piece()

        for row in self.position:
            for square in row:
                if piece.is_move_valid(starting_row, starting_column, square.row, square.column):
                    possible_squares.append(square)

        for square in possible_squares:
            if square.get_piece() != None:
                if square.get_piece().color != piece.color:
                    valid_positions.append(square)
            else:
                valid_positions.append(square)


        return valid_positions

    def capture_piece(row, column):
        pass
        



