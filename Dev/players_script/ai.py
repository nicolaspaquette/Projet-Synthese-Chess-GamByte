from player import player
from minimax import minimax

class ai(player):
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.move_strategy = minimax(self.board, self.color)

    def play_move(self):
        self.move_strategy.select_move()