class move_done():
    def __init__(self, piece, starting_row, starting_column, final_row, final_column):
        self.piece_moved = piece
        self.piece_move_starting_row = starting_row
        self.piece_move_starting_column = starting_column
        self.piece_move_final_row = final_row
        self.piece_move_final_column = final_column

        self.second_piece_altered = None

    def get_second_piece_altered(self, piece, starting_row, starting_column, final_row, final_column):
        self.second_piece_altered = piece
        self.second_piece_move_starting_row = starting_row
        self.second_piece_move_starting_column = starting_column
        self.second_piece_move_final_row = final_row
        self.second_piece_move_final_column = final_column