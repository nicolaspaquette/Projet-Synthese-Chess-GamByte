from piece import piece

class king(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "K"
        self.name = "king"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None
        self.can_be_captured_en_passant = False

    def get_valid_positions(self, board_positions, row, column):
        valid_positions = []

        directions = [(-1,0), (-1,-1), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

        for direction in directions:
            checking_row = row
            checking_column = column

            checking_row += direction[0]
            checking_column += direction[1]

            if checking_row < 8 and checking_row > -1 and checking_column < 8 and checking_column > -1:
                if board_positions[checking_row][checking_column].get_piece() == None or board_positions[checking_row][checking_column].get_piece().color != self.color:
                    valid_positions.append((checking_row, checking_column))

        #castling rules
        if not self.as_moved:
            if self.color == "white":
                if board_positions[row][0].get_piece().name == "rook" and not board_positions[row][0].get_piece().as_moved:
                    if board_positions[row][1].get_piece() == None and board_positions[row][2].get_piece() == None and board_positions[row][3].get_piece() == None:
                        valid_positions.append((row, column - 2))
                if board_positions[row][7].get_piece().name == "rook" and not board_positions[row][7].get_piece().as_moved:
                    if board_positions[row][5].get_piece() == None and board_positions[row][6].get_piece() == None:
                        valid_positions.append((row, column + 2))
            elif self.color == "black":
                if board_positions[row][0].get_piece().name == "rook" and not board_positions[row][0].get_piece().as_moved:
                    if board_positions[row][1].get_piece() == None and board_positions[row][2].get_piece() == None:
                        valid_positions.append((row, column - 2))
                if board_positions[row][7].get_piece().name == "rook" and not board_positions[row][7].get_piece().as_moved:
                    if board_positions[row][4].get_piece() == None and board_positions[row][5].get_piece() == None and board_positions[row][6].get_piece() == None:
                        valid_positions.append((row, column + 2))

        return valid_positions