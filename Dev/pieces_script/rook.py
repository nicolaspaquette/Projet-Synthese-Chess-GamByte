from piece import piece

class rook(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "R"
        self.name = "rook"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None

    def is_move_valid(self, starting_row, starting_column, final_row, final_column):
        elif starting_row == final_row or starting_column == final_column and (starting_row != final_row or starting_column != final_column):
            return True
        else:
            return False