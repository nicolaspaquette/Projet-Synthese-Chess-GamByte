from player import player

class ai(player):
    def __init__(self, color, board):
        self.color = color
        self.board = board

    def choose_move(self):
        print("ai move")