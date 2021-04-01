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
        valid_positions = self.board.move_piece(move[1], move[2], move[3], move[4], [], False, True)

        return valid_positions
