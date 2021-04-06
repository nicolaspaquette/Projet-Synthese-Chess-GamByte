from square import square
from move_done import move_done
from piece_square_tables import piece_square_table

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
        self.white_king_pos = None
        self.black_king_pos = None
        self.list_moves_done = []
        self.bottom_color = None
        self.piece_square_table = piece_square_table
        self.is_endgame = False
        self.color_to_play = "white"

        self.game_over = False
        self.winner = None
        self.game_over_result = None
        self.game_information = {}
        self.move = []
        self.number_of_moves = 0
        self.white_bottom_column_values = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        self.white_bottom_row_values = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        self.black_bottom_column_values = {0: "H", 1: "G", 2: "F", 3: "E", 4: "D", 5: "C", 6: "B", 7: "A"}
        self.black_bottom_row_values = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}

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

        # to register in the move_list
        is_capturing = False
        is_castling = False
        is_checking = False
        is_checkmating = False

        # real player move
        if not is_verifying and not ai_play_move:
            moving_piece = self.selected_square.get_piece()
            self.selected_square.remove_piece()
        else: # verify move or ai move
            moving_piece = self.position[starting_row][starting_column].get_piece()
            self.position[starting_row][starting_column].remove_piece()
        
        # regular capture
        if self.position[final_row][final_column].get_piece() != None:
            last_move_done.get_second_piece_altered(self.position[final_row][final_column].get_piece(), final_row, final_column, None, None)
            is_capturing = True

        self.position[final_row][final_column].add_piece(moving_piece)

        #as moved only when a player makes the move, not during verification
        if not is_verifying and not moving_piece.as_moved:
            moving_piece.as_moved = True

        #pawn promotion to queen
        if (moving_piece.name == "pawn" and moving_piece.initialized_row == 6 and final_row == 0) or moving_piece.name == "pawn" and moving_piece.initialized_row == 1 and final_row == 7:
            self.position[final_row][final_column].remove_piece()
            self.position[final_row][final_column].add_piece(queen(moving_piece.color))

        self.list_moves_done.append(last_move_done)

        #verify en passant
        self.en_passant_verification(moving_piece, starting_row, starting_column, final_row, final_column, last_move_done, is_verifying)

        #verify castling
        self.castling_verification(moving_piece, starting_row, starting_column, final_row, final_column, last_move_done, is_verifying)

        # register move in move_list if a real move is played
        if not is_verifying:
            self.get_kings_positions()
            
            if moving_piece.name == "king" and starting_row == final_row and (starting_column + 2 == final_column or starting_column - 2 == final_column):
                is_castling = True

            if moving_piece.color == "white":
                is_checking = self.is_king_in_check(self.black_king_pos[0], self.black_king_pos[1])
            else:
                is_checking = self.is_king_in_check(self.white_king_pos[0], self.white_king_pos[1])

            if moving_piece.color == "white":
                opponent_color = "black"
            else:
                opponent_color = "white"
            checkmate = self.is_king_in_checkmate(opponent_color)

            if checkmate == "Checkmate":
                is_checkmating = True

            self.register_move(moving_piece.sign, final_row, final_column, is_capturing, is_castling, is_checking, is_checkmating)

        return valid_positions

    def get_valid_piece_positions(self, starting_row, starting_column, is_verifying):
        self.get_kings_positions()
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
        if piece.color == "white" and piece.name != "king" and self.is_king_in_check(self.white_king_pos[0], self.white_king_pos[1]):
            valid_positions = self.get_block_check_positions(valid_positions, starting_row, starting_column)
        elif piece.color == "black" and piece.name != "king" and self.is_king_in_check(self.black_king_pos[0], self.black_king_pos[1]):
            valid_positions = self.get_block_check_positions(valid_positions, starting_row, starting_column)
        elif piece.name != "king":
            if self.is_piece_pinned(starting_row, starting_column, piece):
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
                self.move_piece(starting_row, starting_column, position[0], position[1], [], True, False)
                self.get_kings_positions()

                if self.is_king_in_check(position[0], position[1]):
                    positions_to_remove.append(position)
                
                self.undo_last_move_done()
                self.get_kings_positions()
            
            #cannot castle if king in check or if king is going to be in check between the move
            if self.is_king_in_check(starting_row, starting_column) and (starting_row, starting_column + 2) in valid_positions and (starting_row, starting_column + 2) not in positions_to_remove:
                positions_to_remove.append((starting_row, starting_column + 2))
            if self.is_king_in_check(starting_row, starting_column) and (starting_row, starting_column - 2) in valid_positions and (starting_row, starting_column - 2) not in positions_to_remove:
                positions_to_remove.append((starting_row, starting_column - 2))
            if (starting_row, starting_column + 1) not in valid_positions and (starting_row, starting_column + 2) in valid_positions and (starting_row, starting_column + 2) not in positions_to_remove:
                positions_to_remove.append((starting_row, starting_column + 2))
            if (starting_row, starting_column - 1) not in valid_positions and (starting_row, starting_column - 2) in valid_positions and (starting_row, starting_column - 2) not in positions_to_remove:
                positions_to_remove.append((starting_row, starting_column - 2))

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

    def get_block_check_positions(self, valid_positions, starting_row, starting_column):
        block_check_positions = []
        self.get_kings_positions()

        for position in valid_positions:
            self.move_piece(starting_row, starting_column, position[0], position[1], valid_positions, True, False)
            piece = self.position[position[0]][position[1]].get_piece()

            if piece.color == "white":
                if not self.is_king_in_check(self.white_king_pos[0], self.white_king_pos[1]):
                    block_check_positions.append(position)
            else:
                if not self.is_king_in_check(self.black_king_pos[0], self.black_king_pos[1]):
                    block_check_positions.append(position)

            self.undo_last_move_done()

        return block_check_positions

    def is_piece_pinned(self, starting_row, starting_column, piece):
        verify_piece = piece
        self.position[starting_row][starting_column].remove_piece()

        if verify_piece.color == "white":
            check = self.is_king_in_check(self.white_king_pos[0], self.white_king_pos[1])
        else:
            check = self.is_king_in_check(self.black_king_pos[0], self.black_king_pos[1])
        
        self.position[starting_row][starting_column].add_piece(verify_piece)

        if check:
            return True
        else:
            return False
    
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
                    valid_positions += self.get_valid_piece_positions(square.row, square.column, True)

        if color == "white":       
            check = self.is_king_in_check(self.white_king_pos[0], self.white_king_pos[1])
        else:
            check = self.is_king_in_check(self.black_king_pos[0], self.black_king_pos[1])

        if len(king_positions) == 0 and len(valid_positions) == 0 and check:
            return "Checkmate"
        elif len(king_positions) == 0 and len(valid_positions) == 0 and not check:
            return "Stalemate"
        else:
            return False

    def is_game_over(self):
        if self.white_king_pos != None and self.black_king_pos != None:
            if self.is_king_in_checkmate("white") != False or self.is_king_in_checkmate("black") != False:
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
                if moving_piece.initialized_row == 2:
                    if self.position[final_row - 1][final_column].get_piece() != None:
                        if self.position[final_row][final_column].get_piece().name == "pawn" and self.position[final_row - 1][final_column].get_piece().name == "pawn":
                            if self.position[final_row][final_column].get_piece().color != self.position[final_row - 1][final_column].get_piece().color and self.position[final_row - 1][final_column].get_piece().can_be_captured_en_passant:
                                if starting_column != final_column:
                                    move_done.get_second_piece_altered(self.position[final_row - 1][final_column].get_piece(), final_row - 1, final_column, None, None)
                                    self.position[final_row - 1][final_column].remove_piece()
                if moving_piece.initialized_row == 6:
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
                elif self.bottom_color == "black": 
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
                elif self.bottom_color == "black": 
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

            if last_move_done.piece_moved.color == "white":
                self.white_king_pos = (last_move_done.piece_move_starting_row, last_move_done.piece_move_starting_column)
            else:
                self.black_king_pos = (last_move_done.piece_move_starting_row, last_move_done.piece_move_starting_column)

        self.list_moves_done.pop()

    def get_all_moves_possible(self, color):
        all_valid_moves = []
        for row in self.position:
            for square in row:
                valid_piece_positions = []
                move_score = 0

                piece = square.get_piece()
                if piece != None and piece.color == color:
                    valid_piece_positions = self.get_valid_piece_positions(square.row, square.column, True)

                    for piece_position in valid_piece_positions:
                        if self.position[piece_position[0]][piece_position[1]].get_piece() != "king": # cannot land on a king

                            #pawn promotion is usually very good
                            if piece.name == "pawn" and piece.initialized_row == 6 and piece_position[0] == 0:
                                move_score += 900
                            elif piece.name == "pawn" and piece.initialized_row == 1 and piece_position[0] == 7:
                                move_score += 900

                            #capturing a more valuable piece with a pawn is usually good
                            if piece.name == "pawn" and piece.initialized_row == 6:
                                if square.row > 0 and square.column > 0:
                                    if self.position[square.row - 1][square.column - 1].get_piece() != None and self.position[square.row - 1][square.column - 1].get_piece().color != piece.color and self.position[square.row - 1][square.column - 1].get_piece().value > piece.value:
                                        move_score += 10 * (self.position[square.row - 1][square.column - 1].get_piece().value - piece.value)
                                if square.row > 0 and square.column < 7:
                                    if self.position[square.row - 1][square.column + 1].get_piece() != None and self.position[square.row - 1][square.column + 1].get_piece().color != piece.color and self.position[square.row - 1][square.column + 1].get_piece().value > piece.value:
                                        move_score += 10 * (self.position[square.row - 1][square.column + 1].get_piece().value - piece.value)
                            elif piece.name == "pawn" and piece.initialized_row == 1:
                                if square.row < 7 and square.column > 0:
                                    if self.position[square.row + 1][square.column - 1].get_piece() != None and self.position[square.row + 1][square.column - 1].get_piece().color != piece.color and self.position[square.row + 1][square.column - 1].get_piece().value > piece.value:
                                        move_score += 10 * (self.position[square.row + 1][square.column - 1].get_piece().value - piece.value)
                                if square.row < 7 and square.column < 7:
                                    if self.position[square.row + 1][square.column + 1].get_piece() != None and self.position[square.row + 1][square.column + 1].get_piece().color != piece.color and self.position[square.row + 1][square.column + 1].get_piece().value > piece.value:
                                        move_score += 10 * (self.position[square.row + 1][square.column + 1].get_piece().value - piece.value)

                            #capturing pieces that value more are usually good moves
                            if piece.name != "pawn":
                                if self.position[piece_position[0]][piece_position[1]].get_piece() != None and self.position[piece_position[0]][piece_position[1]].get_piece().color != piece.color:
                                    move_score += (self.position[piece_position[0]][piece_position[1]].get_piece().value - piece.value)

                            #putting your piece on a square attacked by a pawn is usually bad
                            if piece.initialized_row == 7:
                                if square.row > 0 and square.column > 0:
                                    if self.position[square.row - 1][square.column - 1].get_piece() != None and self.position[square.row - 1][square.column - 1].get_piece().color != piece.color and self.position[square.row - 1][square.column - 1].get_piece().name == "pawn":
                                        move_score -= piece.value
                                if square.row > 0 and square.column < 7:
                                    if self.position[square.row - 1][square.column + 1].get_piece() != None and self.position[square.row - 1][square.column + 1].get_piece().color != piece.color and self.position[square.row - 1][square.column + 1].get_piece().name == "pawn":
                                        move_score -= piece.value
                            elif piece.initialized_row == 0:
                                if square.row < 7 and square.column > 0:
                                    if self.position[square.row + 1][square.column - 1].get_piece() != None and self.position[square.row + 1][square.column - 1].get_piece().color != piece.color and self.position[square.row + 1][square.column - 1].get_piece().name == "pawn":
                                        move_score -= piece.value
                                if square.row < 7 and square.column < 7:
                                    if self.position[square.row + 1][square.column + 1].get_piece() != None and self.position[square.row + 1][square.column + 1].get_piece().color != piece.color and self.position[square.row + 1][square.column + 1].get_piece().name == "pawn":
                                        move_score -= piece.value

                            move = [move_score, square.row, square.column, piece_position[0], piece_position[1]]
                            all_valid_moves.append(move)

        return sorted(all_valid_moves, reverse=True)

    def evaluate_position(self, ai_color):
        # for white, maximizing the score
        # for black, minimizing the score
        # for piece_square_tables: human player always on the bottom

        # for the king, endgame begins when players have maximum two majors pieces (knight, bishop, rook, queen) and some pawns
        if not self.is_endgame:
            white_major_pieces = 0
            black_major_pieces = 0
            for row in self.position:
                for square in row:
                    piece = square.get_piece()
                    if piece != None:
                        if piece.color == "white" and (piece.name == "knight" or piece.name == "bishop" or piece.name == "rook" or piece.name == "queen"):
                            white_major_pieces += 1
                        elif piece.color == "black" and (piece.name == "knight" or piece.name == "bishop" or piece.name == "rook" or piece.name == "queen"):
                            black_major_pieces += 1
            if white_major_pieces <= 2 and black_major_pieces <= 2:
                self.is_endgame = True

        ai_score = 0
        human_score = 0
        for row in self.position:
            for square in row:
                if square.get_piece() != None and square.get_piece().color == ai_color:
                    if square.get_piece().name != "king":
                        ai_score += square.get_piece().value + self.piece_square_table["top_" + square.get_piece().name + "_table"][square.row][square.column]
                    else:
                        if self.is_endgame:
                            ai_score += square.get_piece().value + self.piece_square_table["top_" + square.get_piece().name + "_end_game_table"][square.row][square.column]
                        else:
                            ai_score += square.get_piece().value + self.piece_square_table["top_" + square.get_piece().name + "_middle_game_table"][square.row][square.column]
                elif  square.get_piece() != None and square.get_piece().color != ai_color:
                    if square.get_piece().name != "king":
                        human_score += square.get_piece().value + self.piece_square_table["bottom_" + square.get_piece().name + "_table"][square.row][square.column]
                    else:
                        if self.is_endgame:
                            human_score += square.get_piece().value + self.piece_square_table["bottom_" + square.get_piece().name + "_end_game_table"][square.row][square.column]
                        else:
                            human_score += square.get_piece().value + self.piece_square_table["bottom_" + square.get_piece().name + "_middle_game_table"][square.row][square.column]

        # board_score = white_score - black_score
        if ai_color == "white":
            board_score = ai_score - human_score
        else:
            board_score =   human_score - ai_score

        return board_score

    def register_move(self, piece_sign, final_row, final_column, is_capturing, is_castling, is_checking, is_checkmating):
        if self.human_player_color == "white":
            if is_capturing:
                move_name = piece_sign + "x" + self.white_bottom_column_values[final_column] + self.white_bottom_row_values[final_row]
            elif is_castling:
                move_name = "O-O"
            else:
                move_name = piece_sign + self.white_bottom_column_values[final_column] + self.white_bottom_row_values[final_row]

            if is_checkmating:
                move_name += "#"
            elif is_checking:
                move_name += "+"
        else:
            if is_capturing:
                move_name = piece_sign + "x" + self.black_bottom_column_values[final_column] + self.black_bottom_row_values[final_row]
            elif is_castling:
                move_name = "O-O"
            else:
                move_name = piece_sign + self.black_bottom_column_values[final_column] + self.black_bottom_row_values[final_row]

            if is_checkmating:
                move_name += "#"
            elif is_checking:
                move_name += "+"

        self.number_of_moves += 1
        board_information = []
        for row in self.position:
            for square in row:
                piece_information = []
                if square.get_piece() != None:
                    piece_information.append(square.get_piece().color)
                    piece_information.append(square.get_piece().name)
                    piece_information.append(square.row)
                    piece_information.append(square.column)
                    board_information.append(piece_information)

        self.game_information[str(self.number_of_moves) + ". " + move_name] = board_information





