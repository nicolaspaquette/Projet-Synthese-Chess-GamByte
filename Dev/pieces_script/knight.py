from piece import piece

class knight(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "N"
        self.name = "knight"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None

    def is_move_valid(self, starting_row, starting_column, final_row, final_column):
        if starting_row + 2 == final_row and (starting_column - 1 == final_column or starting_column + 1 == final_column):
            return True
        elif starting_row + 1 == final_row and (starting_column - 2 == final_column or starting_column + 2 == final_column):
            return True
        elif starting_row - 2 == final_row and (starting_column - 1 == final_column or starting_column + 1 == final_column):
            return True
        elif starting_row - 1 == final_row and (starting_column - 2 == final_column or starting_column + 2 == final_column):
            return True
        else:
            return False