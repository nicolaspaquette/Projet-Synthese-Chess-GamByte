from piece import piece

class bishop(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "B"
        self.name = "bishop"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None
        self.can_be_captured_en_passant = False

    def get_valid_positions(self, board_positions, row, column):
        valid_positions = []

        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]

        for direction in directions:
            checking_row = row
            checking_column = column
            while checking_row < 8 and checking_row > -1 and checking_column < 8 and checking_column > -1:
                checking_row += direction[0]
                checking_column += direction[1]

                if checking_row < 8 and checking_row > -1 and checking_column < 8 and checking_column > -1:
                    if board_positions[checking_row][checking_column].get_piece() == None:
                        valid_positions.append((checking_row, checking_column))
                    elif board_positions[checking_row][checking_column].get_piece().color != self.color:
                        valid_positions.append((checking_row, checking_column))
                        break
                    else:
                        break

        return valid_positions


