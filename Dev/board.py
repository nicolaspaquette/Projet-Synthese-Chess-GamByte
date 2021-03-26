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
        self.en_passant_piece = None

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
        if piece != None: #and piece.color == self.human_player_color:
        #if piece != None and piece.color == self.human_player_color:
            print("you choose your piece: " + piece.name + " at " + str(row) + " " + str(column))
            self.selected_square = square
            return True
        else:
            return False

    def verify_move(self, valid_positions, row, column):
        move = (row, column)
        if move in valid_positions:
            return True
        else:
            return False

    def move_piece(self, starting_row, starting_column, final_row, final_column, valid_positions):
        moving_piece = self.selected_square.get_piece()
        self.selected_square.remove_piece()
        self.position[final_row][final_column].add_piece(moving_piece)

        if self.en_passant_piece != moving_piece and self.en_passant_piece != None:
            if self.en_passant_piece.color == moving_piece.color:
                self.en_passant_piece.can_be_captured_en_passant = False
                self.en_passant_piece = None

        if moving_piece.name == "pawn" and starting_row == moving_piece.initialized_row and (final_row - starting_row == 2 or final_row - starting_row == -2):
            print("double move")
            moving_piece.can_be_captured_en_passant = True
            self.en_passant_piece = moving_piece


        if final_column - 1 >= 0 and final_column + 1 <= 7:
            if self.position[final_row][final_column].get_piece() != None and (self.position[final_row - 1][final_column].get_piece() != None or self.position[final_row + 1][final_column].get_piece() != None):
                if self.position[final_row - 1][final_column].get_piece() != None:
                    if self.position[final_row][final_column].get_piece().name == "pawn" and self.position[final_row - 1][final_column].get_piece().name == "pawn":
                        if self.position[final_row][final_column].get_piece().color != self.position[final_row - 1][final_column].get_piece().color and self.position[final_row - 1][final_column].get_piece().can_be_captured_en_passant:
                            self.position[final_row - 1][final_column].remove_piece()

                if self.position[final_row + 1][final_column].get_piece() != None:
                    if self.position[final_row][final_column].get_piece().name == "pawn" and self.position[final_row + 1][final_column].get_piece().name == "pawn":
                        if self.position[final_row][final_column].get_piece().color != self.position[final_row + 1][final_column].get_piece().color and self.position[final_row + 1][final_column].get_piece().can_be_captured_en_passant:
                            self.position[final_row + 1][final_column].remove_piece()
                    
        if self.selected_square in valid_positions:
            valid_positions.remove(self.selected_square)

        return valid_positions

    def unmake_move(self, actual_row, actual_column, original_row, original_column): # or board copy
        pass

    def get_valid_positions(self, starting_row, starting_column):
        possible_squares = []
        valid_positions = []
        piece = self.selected_square.get_piece()

        valid_positions = piece.get_valid_positions(self.position, starting_row, starting_column)
        return valid_positions

    def is_king_in_check(self):
        pass
        



