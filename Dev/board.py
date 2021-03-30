from square import square
from move_done import move_done

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
        self.list_moves_done = []
        self.bottom_color = None

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

    def move_piece(self, starting_row, starting_column, final_row, final_column, valid_positions, is_verifying, ai_play_move):
        last_move_done = move_done(self.position[starting_row][starting_column].get_piece(), starting_row, starting_column, final_row, final_column)

        if not is_verifying:
            moving_piece = self.selected_square.get_piece()
            self.selected_square.remove_piece()
        else:
            moving_piece = self.position[starting_row][starting_column].get_piece()
            self.position[starting_row][starting_column].remove_piece()

        # regular capture
        if self.position[final_row][final_column].get_piece() != None:
            last_move_done.get_second_piece_altered(self.position[final_row][final_column].get_piece(), final_row, final_column, None, None)

        self.position[final_row][final_column].add_piece(moving_piece)

        self.get_kings_positions()

        #as moved only when a player makes the move, not during verification
        if not moving_piece.as_moved and not is_verifying:
            moving_piece.as_moved = True

        if ai_play_move:
            moving_piece.as_moved = True

        #pawn promotion to queen
        if (moving_piece.name == "pawn" and moving_piece.initialized_row == 6 and final_row == 0) or moving_piece.name == "pawn" and moving_piece.initialized_row == 1 and final_row == 7:
            self.position[final_row][final_column].remove_piece()
            self.position[final_row][final_column].add_piece(queen(moving_piece.color))

        #verify en passant
        last_move_done = self.en_passant_verification(moving_piece, starting_row, starting_column, final_row, final_column, last_move_done, is_verifying)

        #verify castling
        last_move_done = self.castling_verification(moving_piece, starting_row, starting_column, final_row, final_column, last_move_done, is_verifying)

        #do not show own square as potential move for the next move
        if self.selected_square in valid_positions:
            valid_positions.remove(self.selected_square)

        if not is_verifying:
            self.show_board_state()

        self.list_moves_done.append(last_move_done)
            
        return valid_positions

    def get_valid_piece_positions(self, starting_row, starting_column, is_verifying):
        possible_squares = []
        valid_positions = []
        if not is_verifying:
            piece = self.selected_square.get_piece()
        else:
            piece = self.position[starting_row][starting_column].get_piece()

        if piece.color == "white":
            opponent_color = "black"
        elif piece.color == "black":
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
            all_opponent_moves = self.get_all_valid_positions(opponent_color)

            positions_to_remove = []
            for position in valid_positions:
                if position in all_opponent_moves:
                    positions_to_remove.append(position)

            for position in positions_to_remove:
                valid_positions.remove(position)

            #remove positions with black piece near the king that are protected from capturing
            positions_to_remove = []
            for position in valid_positions:
                self.move_piece(starting_row, starting_column, position[0], position[1], valid_positions, True, False)
                self.get_kings_positions()

                if self.is_king_in_check(position[0], position[1]):
                    positions_to_remove.append(position)
                
                self.undo_last_move_done()
                self.get_kings_positions()
            
            for position in positions_to_remove:
                valid_positions.remove(position)

        return valid_positions

    def get_all_valid_positions(self, color):
        all_valid_positions = []

        #all squares being attacked
        for row in self.position:
            for square in row:
                if square.get_piece() != None:
                    if square.get_piece().color == color:
                        if square.get_piece().name != "pawn":
                            all_valid_positions += square.get_piece().get_valid_positions(self.position, square.row, square.column)
                        else:
                            all_valid_positions += square.get_piece().get_capture_positions(self.position, square.row, square.column)

        return all_valid_positions

    def get_block_check_positions(self, valid_positions, row, col):
        block_check_positions = []

        for position in valid_positions:
            self.move_piece(row, col, position[0], position[1], valid_positions, True, False)
            piece = self.position[position[0]][position[1]].get_piece()
            self.get_kings_positions()

            if piece.color == "white":
                if not self.is_king_in_check(self.white_king_pos[0], self.white_king_pos[1]):
                    block_check_positions.append(position)
            else:
                if not self.is_king_in_check(self.black_king_pos[0], self.black_king_pos[1]):
                    block_check_positions.append(position)

            self.undo_last_move_done()
            self.get_kings_positions()

        return block_check_positions

    def is_king_in_check(self, king_row, king_column):
        king = self.position[king_row][king_column].get_piece()
        all_opponent_moves = []

        if king.color == "white":
            opponent_color = "black"
        else:
            opponent_color = "white"

        all_opponent_moves = self.get_all_valid_positions(opponent_color)

        #verify if king is attacked
        if (king_row, king_column) in all_opponent_moves:
            return True
        else:
            return False

    def is_king_in_checkmate(self, color):
        self.get_kings_positions()
        if color == "white":
            king =  self.position[self.white_king_pos[0]][self.white_king_pos[1]].get_piece()
            king_positions = self.get_valid_piece_positions(self.white_king_pos[0], self.white_king_pos[1], True)
        else:
            king =  self.position[self.black_king_pos[0]][self.black_king_pos[1]].get_piece()
            king_positions = self.get_valid_piece_positions(self.black_king_pos[0], self.black_king_pos[1], True)

        valid_positions = []
        block_positions = []

        for row in self.position:
            for square in row:
                if square.get_piece() != None and square.get_piece().color == king.color and square.get_piece().name != "king":
                    valid_positions = self.get_valid_piece_positions(square.row, square.column, True)
                    block_positions += self.get_block_check_positions(valid_positions, square.row, square.column)
        
        if len(block_positions) == 0 and len(king_positions) == 0:
            return True
        else:
            return False

    def is_game_over(self):
        if self.white_king_pos != None and self.black_king_pos != None:
            if self.is_king_in_checkmate("white") or self.is_king_in_checkmate("black"):
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

    def en_passant_verification(self, moving_piece, starting_row, starting_column, final_row, final_column, move_done, is_verifying):
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
                                move_done.get_second_piece_altered(self.position[final_row - 1][final_column].get_piece(), final_row - 1, final_column, None, None)
                                self.position[final_row - 1][final_column].remove_piece()

                if self.position[final_row + 1][final_column].get_piece() != None:
                    if self.position[final_row][final_column].get_piece().name == "pawn" and self.position[final_row + 1][final_column].get_piece().name == "pawn":
                        if self.position[final_row][final_column].get_piece().color != self.position[final_row + 1][final_column].get_piece().color and self.position[final_row + 1][final_column].get_piece().can_be_captured_en_passant:
                            if starting_column != final_column:
                                move_done.get_second_piece_altered(self.position[final_row + 1][final_column].get_piece(), final_row + 1, final_column, None, None)
                                self.position[final_row + 1][final_column].remove_piece()

        return move_done

    def castling_verification(self, moving_piece, starting_row, starting_column, final_row, final_column, move_done, is_verifying):
        if moving_piece.name == "king" and starting_row == final_row:
            if starting_column - final_column == 2: # left side castling
                if self.bottom_color == "white": 
                    rook_col = 3
                else: 
                    rook_col = 2

                rook = self.position[final_row][0].get_piece()
                if not is_verifying:
                    rook.as_moved = True

                move_done.get_second_piece_altered(self.position[final_row][0].get_piece(), final_row, 0, final_row, rook_col)
                self.position[final_row][0].remove_piece()
                self.position[final_row][rook_col].add_piece(rook)

            elif starting_column - final_column == -2: #right right castling
                if self.bottom_color == "white": 
                    rook_col = 5  
                else: 
                    rook_col = 4 

                rook = self.position[final_row][7].get_piece()
                if not is_verifying:
                    rook.as_moved = True

                move_done.get_second_piece_altered(self.position[final_row][7].get_piece(), final_row, 7, final_row, rook_col)
                self.position[final_row][7].remove_piece()
                self.position[final_row][rook_col].add_piece(rook)

        return move_done

    def undo_last_move_done(self):
        last_move_done = self.list_moves_done[-1]

        #one piece: movement only
        if last_move_done.second_piece_altered == None:
            self.position[last_move_done.piece_move_final_row][last_move_done.piece_move_final_column].remove_piece()
            self.position[last_move_done.piece_move_starting_row][last_move_done.piece_move_starting_column].add_piece(last_move_done.piece_moved)
        #two piece : capture
        elif last_move_done.second_piece_altered != None and last_move_done.second_piece_move_final_row == None:
            self.position[last_move_done.piece_move_final_row][last_move_done.piece_move_final_column].remove_piece()
            self.position[last_move_done.piece_move_starting_row][last_move_done.piece_move_starting_column].add_piece(last_move_done.piece_moved)

            self.position[last_move_done.second_piece_move_starting_row][last_move_done.second_piece_move_starting_column].add_piece(last_move_done.second_piece_altered)
        #two piece : castling
        elif last_move_done.second_piece_altered != None and last_move_done.second_piece_move_final_row != None:
            self.position[last_move_done.piece_move_final_row][last_move_done.piece_move_final_column].remove_piece()
            self.position[last_move_done.piece_move_starting_row][last_move_done.piece_move_starting_column].add_piece(last_move_done.piece_moved)

            self.position[last_move_done.second_piece_move_final_row][last_move_done.second_piece_move_final_column].remove_piece()
            self.position[last_move_done.second_piece_move_starting_row][last_move_done.second_piece_move_starting_column].add_piece(last_move_done.second_piece_altered)

        self.get_kings_positions()

        self.list_moves_done.pop()

    def get_all_moves_possible(self, color):

        all_valid_moves = []
        for row in self.position:
            for square in row:
                valid_piece_positions = []
                if square.get_piece() != None and square.get_piece().color == color:
                    valid_piece_positions = self.get_valid_piece_positions(square.row, square.column, True)

                    for piece_position in valid_piece_positions:
                        move = [square.row, square.column, piece_position[0], piece_position[1]]
                        all_valid_moves.append(move)

        return all_valid_moves

    def show_board_state(self):
        board = []
        for row in self.position:
            pos = []
            for square in row:
                if square.get_piece() != None:
                    pos.append(square.get_piece().color[0] + "_" + square.get_piece().sign)
                else:
                    pos.append("   ")
            board.append(pos)

        print("---------------------------------------------------------------------------------------")
        for pos in board:
            print(pos)




