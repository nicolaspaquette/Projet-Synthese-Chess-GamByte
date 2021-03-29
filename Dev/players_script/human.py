from player import player

class human(player):
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.starting_row = None
        self.starting_column = None
        self.valid_positions = None

    def choose_move(self, row, column):
        if self.board.choose_piece_to_move(row, column, self.color):
            self.starting_row = row
            self.starting_column = column
            self.board.get_kings_positions()
            self.valid_positions = self.board.get_valid_piece_positions(self.starting_row, self.starting_column, False)

    def verify_move(self, row, column):
        if self.board.verify_move(self.valid_positions, row, column):
            return True
        else:
            return False

    def play_move(self, row, column):
        valid_positions = self.board.move_piece(self.starting_row, self.starting_column, row, column, self.valid_positions, False, False)
        return valid_positions