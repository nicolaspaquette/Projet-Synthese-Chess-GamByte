from piece import piece

class pawn(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "P"
        self.name = "pawn"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None

    def is_move_valid(self, starting_row, starting_column, final_row, final_column):
        if self.initialized_row == 1:
            if starting_row + 1 == final_row and starting_column == final_column:
                return True
            elif starting_row == self.initialized_row and starting_row + 2 == final_row and starting_column == final_column:
                return True
        elif self.initialized_row == 6:
            if starting_row - 1 == final_row and starting_column == final_column:
                return True
            elif starting_row == self.initialized_row and starting_row - 2 == final_row and starting_column == final_column:
                return True
        else:
            return False

    def is_move_capture(self, starting_row, starting_column, final_row, final_column):
        if self.initialized_row == 1:
            if starting_row + 1 == final_row and (starting_column - 1 == final_column or starting_column + 1 == final_column):
                return True
        elif self.initialized_row == 6:
            if starting_row - 1 == final_row and (starting_column - 1 == final_column or starting_column + 1 == final_column):
                return True
        else:
            return False