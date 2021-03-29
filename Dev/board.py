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
import copy

class board:
    def __init__(self, human_color):
        self.human_player_color = human_color
        self.position = self.initialize_board()
        self.initialize_starting_positions()
        self.selected_square = None
        self.en_passant_piece = None
        self.move_list = {}
        self.white_king_pos = None
        self.black_king_pos = None
        self.color_to_play = "white"

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

    def choose_piece_to_move(self, row, column, player_color):
        square = self.position[row][column]
        piece = square.get_piece()

        if piece != None and piece.color == player_color: 
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

    def move_piece(self, starting_row, starting_column, final_row, final_column, valid_positions, in_minimax):
        if not in_minimax:
            moving_piece = self.selected_square.get_piece()
            self.selected_square.remove_piece()
        else:
            moving_piece = self.position[starting_row][starting_column].get_piece()
            self.position[starting_row][starting_column].remove_piece()
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

        #verify if king is checkmate
        self.get_kings_positions()
        if self.color_to_play == "white":
            king_pos = self.black_king_pos
        else:
            king_pos = self.white_king_pos

        in_check = self.is_king_in_check(self.position, king_pos[0], king_pos[1])
        if in_check:
            in_checkmate = self.is_king_in_checkmate(king_pos[0], king_pos[1])
            
        return valid_positions

    def get_valid_piece_positions(self, starting_row, starting_column, verify):
        possible_squares = []
        valid_positions = []
        if not verify:
            piece = self.selected_square.get_piece()
        else:
            piece = self.position[starting_row][starting_column].get_piece()

        if piece.color == "white":
            opponent_color = "black"
        else:
            opponent_color = "white"

        valid_positions = piece.get_valid_positions(self.position, starting_row, starting_column)

        #remove positions thad doesnt block checks if king in check and pinned pieces cannot move
        if piece.name != "king":
            valid_positions = self.get_block_check_positions(valid_positions, starting_row, starting_column)

        #remove valid position if king is in check
        if piece.name == "king":
            if piece.color == "white":
                opponent_color = "black"
            else:
                opponent_color = "white"

            all_opponent_moves = []
            all_opponent_moves = self.get_all_valid_positions(self.position, opponent_color)

            positions_to_remove = []
            for position in valid_positions:
                if position in all_opponent_moves:
                    positions_to_remove.append(position)

            for position in positions_to_remove:
                valid_positions.remove(position)

            #remove positions with black piece near the king that are protected from capturing
            positions_to_remove = []
            for position in valid_positions:
                board_copy = copy.deepcopy(self.position)
                board_copy[starting_row][starting_column].remove_piece()
                board_copy[position[0]][position[1]].add_piece(piece)
                if self.is_king_in_check(board_copy, position[0], position[1]):
                    positions_to_remove.append(position)
            
            for position in positions_to_remove:
                valid_positions.remove(position)

        return valid_positions

    def get_all_valid_positions(self, board, color):
        all_valid_positions = []

        #all squares being attacked
        for row in board:
            for square in row:
                if square.get_piece() != None:
                    if square.get_piece().color == color:
                        if square.get_piece().name != "pawn":
                            all_valid_positions += square.get_piece().get_valid_positions(board, square.row, square.column)
                        else:
                            all_valid_positions += square.get_piece().get_capture_positions(board, square.row, square.column)

        return all_valid_positions

    def get_block_check_positions(self, valid_positions, row, col):
        block_check_positions = []
        self.get_kings_positions()

        for position in valid_positions:
            board_copy = copy.deepcopy(self.position)
            piece = board_copy[row][col].get_piece()
            board_copy[row][col].remove_piece()
            board_copy[position[0]][position[1]].add_piece(piece)
            
            if piece.color == "white":
                if not self.is_king_in_check(board_copy, self.white_king_pos[0], self.white_king_pos[1]):
                    block_check_positions.append(position)
            else:
                if not self.is_king_in_check(board_copy, self.black_king_pos[0], self.black_king_pos[1]):
                    block_check_positions.append(position)

        return block_check_positions

    def is_king_in_check(self, board, king_row, king_column):
        king = board[king_row][king_column].get_piece()
        all_opponent_moves = []

        if king.color == "white":
            opponent_color = "black"
        else:
            opponent_color = "white"

        all_opponent_moves = self.get_all_valid_positions(board, opponent_color)

        #verify if king is attacked
        if (king_row, king_column) in all_opponent_moves:
            return True
        else:
            return False

    def is_king_in_checkmate(self, king_row, king_column): 
        king = self.position[king_row][king_column].get_piece()
        king_positions = self.get_valid_piece_positions(king_row, king_column, True)
        valid_positions = []
        block_positions = []

        for row in self.position:
            for square in row:
                if square.get_piece() != None and square.get_piece().color == king.color and square.get_piece().name != "king":
                    valid_positions = self.get_valid_piece_positions(square.row, square.column, True)
                    block_positions += self.get_block_check_positions(valid_positions, square.row, square.column)
        
        if len(block_positions) == 0 and len(king_positions) == 0:
            king = self.position[king_row][king_column].get_piece()
            return True
        else:
            return False

    def is_game_over(self):
        if self.white_king_pos != None and self.black_king_pos != None:
            if self.is_king_in_checkmate(self.white_king_pos[0], self.white_king_pos[1]) or self.is_king_in_checkmate(self.black_king_pos[0], self.black_king_pos[1]):
                return True
            else:
                return False

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
                            if starting_column != final_column:
                                self.position[final_row - 1][final_column].remove_piece()

                if self.position[final_row + 1][final_column].get_piece() != None:
                    if self.position[final_row][final_column].get_piece().name == "pawn" and self.position[final_row + 1][final_column].get_piece().name == "pawn":
                        if self.position[final_row][final_column].get_piece().color != self.position[final_row + 1][final_column].get_piece().color and self.position[final_row + 1][final_column].get_piece().can_be_captured_en_passant:
                            if starting_column != final_column:
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



