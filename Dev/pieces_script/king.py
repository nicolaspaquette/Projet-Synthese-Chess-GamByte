from piece import piece

class king(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "K"
        self.name = "king"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None

    def is_move_valid(self, starting_row, starting_column, final_row, final_column):
        if starting_row + 1 == final_row and starting_column == final_column:
            return True
        elif starting_row - 1 == final_row and starting_column == final_column:
            return True
        elif starting_column + 1 == final_column and starting_row == final_row:
            return True
        elif starting_column - 1 == final_column and starting_row == final_row:
            return True
        elif starting_row + 1 == final_row and starting_column + 1 == final_column:
            return True
        elif starting_row + 1 == final_row and starting_column - 1 == final_column:
            return True
       elif starting_row - 1 == final_row and starting_column + 1 == final_column:
            return True
        elif starting_row - 1 == final_row and starting_column - 1 == final_column:
            return True
        else:
            return False