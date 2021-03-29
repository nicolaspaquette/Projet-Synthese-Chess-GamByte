from player import player
from minimax import minimax
import copy

class ai(player):
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.move_strategy = minimax(self.board, self.color)

    def play_move(self):
        score, move = self.move_strategy.select_move()

        # move : [starting_row, starting_column, final_row, final_column]
        valid_positions = self.board.get_valid_piece_positions(move[0], move[1], True)
        valid_positions = self.board.move_piece(move[0], move[1], move[2], move[3], valid_positions, True)

        return valid_positions
