from piece import piece

class knight(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "N"
        self.name = "knight"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None
        self.can_be_captured_en_passant = False
        self.value = 30

    def get_valid_positions(self, board_positions, row, column):
        valid_positions = []

        directions = [(-2,-1), (-1,-2), (-2,1), (-1,2), (1,-2), (2,-1), (1,2), (2,1)]

        for direction in directions:
            checking_row = row
            checking_column = column

            checking_row += direction[0]
            checking_column += direction[1]

            if checking_row < 8 and checking_row > -1 and checking_column < 8 and checking_column > -1:
                if board_positions[checking_row][checking_column].get_piece() == None or board_positions[checking_row][checking_column].get_piece().color != self.color:
                    valid_positions.append((checking_row, checking_column))

        return valid_positions

