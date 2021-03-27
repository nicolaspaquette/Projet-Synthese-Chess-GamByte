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
        self.initialize_starting_positions()
        self.selected_square = None
        self.en_passant_piece = None
        self.move_list = {}
        self.white_king_pos = None
        self.black_king_pos = None

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

    def choose_piece_to_move(self, row, column):
        square = self.position[row][column]
        piece = square.get_piece()

        if piece != None: #and piece.color == self.human_player_color:
        #if piece != None and piece.color == self.human_player_color:
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

        self.get_kings_positions()

        #as moved
        if not moving_piece.as_moved:
            moving_piece.as_moved = True

        #pawn promotion to queen
        if (moving_piece.name == "pawn" and moving_piece.initialized_row == 6 and final_row == 0) or moving_piece.name == "pawn" and moving_piece.initialized_row == 1 and final_row == 7:
            self.position[final_row][final_column].remove_piece()
            self.position[final_row][final_column].add_piece(queen(moving_piece.color))

        #verify en passant
        self.en_passant_verification(moving_piece, starting_row, starting_column, final_row, final_column, valid_positions)

        #verify castling
        self.castling_verification(moving_piece, starting_row, starting_column, final_row, final_column, valid_positions)

        #do not show own square as potential move for the next move
        if self.selected_square in valid_positions:
            valid_positions.remove(self.selected_square)

        self.is_king_in_check(self.white_king_pos[0], self.white_king_pos[1])

        return valid_positions

    def unmake_move(self, actual_row, actual_column, original_row, original_column): # or board copy
        pass

    def get_valid_piece_positions(self, starting_row, starting_column):
        possible_squares = []
        valid_positions = []
        piece = self.selected_square.get_piece()

        valid_positions = piece.get_valid_positions(self.position, starting_row, starting_column)
        return valid_positions

    def get_all_valid_positions(self, color):
        all_valid_positions = []

        #all squares being attacked
        for row in self.position:
            for square in row:
                if square.get_piece() != None:
                    if square.get_piece().color == color:
                        all_valid_positions += square.get_piece().get_valid_positions(self.position, square.row, square.column)

        return all_valid_positions

    def is_king_in_check(self, king_row, king_column):
        king = self.position[king_row][king_column].get_piece()
        all_opponent_moves = []

        if king.color == "white":
            color = "black"
        else:
            color = "white"

        all_opponent_moves = self.get_all_valid_positions(color)
        print((king_row, king_column))
        print(all_opponent_moves)

        #verify is king is attacked
        if (king_row, king_column) in all_opponent_moves:
            print("KING IN CHECK")
            return True
        else:
            print("KING NOT IN CHECK")
            return False           

    def king_possible_positions(self, king_row, king_column):
        pass

    def get_kings_positions(self):

        for row in self.position:
            for square in row:
                if square.get_piece() != None:
                    if square.get_piece().name == "king" and square.get_piece().color == "white":
                        self.white_king_pos = (square.row, square.column)
                    elif square.get_piece().name == "king" and square.get_piece().color == "black":
                        self.black_king_pos = (square.row, square.column)

    def en_passant_verification(self, moving_piece, starting_row, starting_column, final_row, final_column, valid_positions):
        if self.en_passant_piece != moving_piece and self.en_passant_piece != None:
            if self.en_passant_piece.color == moving_piece.color:
                self.en_passant_piece.can_be_captured_en_passant = False
                self.en_passant_piece = None

        if moving_piece.name == "pawn" and starting_row == moving_piece.initialized_row and (final_row - starting_row == 2 or final_row - starting_row == -2):
            moving_piece.can_be_captured_en_passant = True
            self.en_passant_piece = moving_piece

        if final_row < 7 and final_row > 0 and final_column < 7 and final_column > 0:
            if self.position[final_row][final_column].get_piece() != None and (self.position[final_row - 1][final_column].get_piece() != None or self.position[final_row + 1][final_column].get_piece() != None):
                if self.position[final_row - 1][final_column].get_piece() != None:
                    if self.position[final_row][final_column].get_piece().name == "pawn" and self.position[final_row - 1][final_column].get_piece().name == "pawn":
                        if self.position[final_row][final_column].get_piece().color != self.position[final_row - 1][final_column].get_piece().color and self.position[final_row - 1][final_column].get_piece().can_be_captured_en_passant:
                            self.position[final_row - 1][final_column].remove_piece()

                if self.position[final_row + 1][final_column].get_piece() != None:
                    if self.position[final_row][final_column].get_piece().name == "pawn" and self.position[final_row + 1][final_column].get_piece().name == "pawn":
                        if self.position[final_row][final_column].get_piece().color != self.position[final_row + 1][final_column].get_piece().color and self.position[final_row + 1][final_column].get_piece().can_be_captured_en_passant:
                            self.position[final_row + 1][final_column].remove_piece()

    def castling_verification(self, moving_piece, starting_row, starting_column, final_row, final_column, valid_positions):
        if moving_piece.name == "king" and starting_row == final_row:
            if starting_column - final_column == 2: # left side castling
                if moving_piece.color == "white":
                    rook_col = 3 
                else:
                    rook_col = 2
                rook = self.position[final_row][0].get_piece()
                rook.as_moved = True
                self.position[final_row][0].remove_piece()
                self.position[final_row][rook_col].add_piece(rook)

            elif starting_column - final_column == -2: #right right castling
                if moving_piece.color == "white":
                    rook_col = 5 
                else:
                    rook_col = 4
                rook = self.position[final_row][7].get_piece()
                rook.as_moved = True
                self.position[final_row][7].remove_piece()
                self.position[final_row][rook_col].add_piece(rook)



