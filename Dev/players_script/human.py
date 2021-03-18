from player import player

class human(player):
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.move_choosed = False

    def choose_move(self):
        pass