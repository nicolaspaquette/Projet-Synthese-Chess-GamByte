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
        self.value = 1000

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
        if not self.as_moved and row == self.initialized_row and column == self.initialized_column:
            if self.initialized_row == 7 and self.initialized_column == 4: # white bottom
                if board_positions[7][0].get_piece() != None:
                    if board_positions[7][0].get_piece().name == "rook" and not board_positions[7][0].get_piece().as_moved:
                        if board_positions[7][1].get_piece() == None and board_positions[7][2].get_piece() == None and board_positions[7][3].get_piece() == None:
                            valid_positions.append((row, 2))

                if board_positions[7][7].get_piece() != None:
                    if board_positions[7][7].get_piece().name == "rook" and not board_positions[7][7].get_piece().as_moved:
                        if board_positions[7][5].get_piece() == None and board_positions[7][6].get_piece() == None:
                            valid_positions.append((row, 6))
            
            elif self.initialized_row == 0 and self.initialized_column == 4: # black top
                if board_positions[0][0].get_piece() != None:
                    if board_positions[0][0].get_piece().name == "rook" and not board_positions[0][0].get_piece().as_moved:
                        if board_positions[0][1].get_piece() == None and board_positions[0][2].get_piece() == None and board_positions[0][3].get_piece() == None:
                            valid_positions.append((row, 2))

                if board_positions[0][7].get_piece() != None:
                    if board_positions[0][7].get_piece().name == "rook" and not board_positions[0][7].get_piece().as_moved:
                        if board_positions[0][5].get_piece() == None and board_positions[0][6].get_piece() == None:
                            valid_positions.append((row, 6))

            elif self.initialized_row == 7 and self.initialized_column == 3: # black bottom
                if board_positions[7][0].get_piece() != None:
                    if board_positions[7][0].get_piece().name == "rook" and not board_positions[7][0].get_piece().as_moved:
                        if board_positions[7][1].get_piece() == None and board_positions[7][2].get_piece() == None:
                            valid_positions.append((row, 1))

                if board_positions[7][7].get_piece() != None:
                    if board_positions[7][7].get_piece().name == "rook" and not board_positions[7][7].get_piece().as_moved:
                        if board_positions[7][4].get_piece() == None and board_positions[7][5].get_piece() == None and board_positions[7][6].get_piece() == None:
                            valid_positions.append((row, 5))

            elif self.initialized_row == 0 and self.initialized_column == 3: # white top
                if board_positions[0][0].get_piece() != None:
                    if board_positions[0][0].get_piece().name == "rook" and not board_positions[0][0].get_piece().as_moved:
                        if board_positions[0][1].get_piece() == None and board_positions[0][2].get_piece() == None:
                            valid_positions.append((row, 1))

                if board_positions[0][7].get_piece() != None:
                    if board_positions[0][7].get_piece().name == "rook" and not board_positions[0][7].get_piece().as_moved:
                        if board_positions[0][4].get_piece() == None and board_positions[0][5].get_piece() == None and board_positions[0][6].get_piece() == None:
                            valid_positions.append((row, 5))

        return valid_positions