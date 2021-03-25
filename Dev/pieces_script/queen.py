from piece import piece

class queen(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "Q"
        self.name = "queen"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None

    def is_move_valid(self, starting_row, starting_column, final_row, final_column):
        if abs(starting_row - final_row) == abs(starting_column - final_column) and (starting_row != final_row or starting_column != final_column):
            return True
        elif starting_row == final_row or starting_column == final_column and (starting_row != final_row or starting_column != final_column):
            return True
        else:
            return False