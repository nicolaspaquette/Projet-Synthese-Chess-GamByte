from piece import piece

class pawn(piece):
    def __init__(self, color):
        self.color = color
        self.sign = "P"
        self.name = "pawn"
        self.as_moved = False
        self.initialized_row = None
        self.initialized_column = None
        self.can_be_captured_en_passant = False
        self.value = 100

    def get_valid_positions(self, board_positions, row, column):
        valid_positions = []

        if self.initialized_row == 1: #top pawns
            if row == self.initialized_row:
                if board_positions[row + 1][column].get_piece() == None and board_positions[row + 2][column].get_piece() == None:
                    valid_positions.append((row + 2, column))

            if board_positions[row + 1][column].get_piece() == None:
                valid_positions.append((row + 1, column))

            #captures
            if column > 0:
                if board_positions[row + 1][column - 1].get_piece() != None and board_positions[row + 1][column - 1].get_piece().color != self.color:
                    valid_positions.append((row + 1, column - 1))
                if board_positions[row][column - 1].get_piece() != None and board_positions[row][column - 1].get_piece().color != self.color and board_positions[row][column - 1].get_piece().can_be_captured_en_passant and board_positions[row + 1][column - 1].get_piece() == None:
                    valid_positions.append((row + 1, column - 1))
                    
            if column < 7:
                if board_positions[row + 1][column + 1].get_piece() != None and board_positions[row + 1][column + 1].get_piece().color != self.color:
                    valid_positions.append((row + 1, column + 1))
                if board_positions[row][column + 1].get_piece() != None and board_positions[row][column + 1].get_piece().color != self.color and board_positions[row][column + 1].get_piece().can_be_captured_en_passant and board_positions[row + 1][column + 1].get_piece() == None:
                    valid_positions.append((row + 1, column + 1))

        elif self.initialized_row == 6: #bottom pawns
            if row == self.initialized_row:
                if board_positions[row - 1][column].get_piece() == None and board_positions[row - 2][column].get_piece() == None:
                    valid_positions.append((row - 2, column))

            if board_positions[row - 1][column].get_piece() == None:
                valid_positions.append((row - 1, column))

            #captures
            if column > 0:
                if board_positions[row - 1][column - 1].get_piece() != None and board_positions[row - 1][column - 1].get_piece().color != self.color:
                    valid_positions.append((row - 1, column - 1))
                if board_positions[row][column - 1].get_piece() != None and board_positions[row][column - 1].get_piece().color != self.color and board_positions[row][column - 1].get_piece().can_be_captured_en_passant and board_positions[row - 1][column - 1].get_piece() == None:
                    valid_positions.append((row - 1, column - 1))

            if column < 7:        
                if board_positions[row - 1][column + 1].get_piece() != None and board_positions[row - 1][column + 1].get_piece().color != self.color:
                    valid_positions.append((row - 1, column + 1))
                if board_positions[row][column + 1].get_piece() != None and board_positions[row][column + 1].get_piece().color != self.color and board_positions[row][column + 1].get_piece().can_be_captured_en_passant and board_positions[row - 1][column + 1].get_piece() == None:
                    valid_positions.append((row - 1, column + 1))

        return valid_positions

    def get_capture_positions(self, board_positions, row, column):
        valid_positions = []
        if self.initialized_row == 1: #top pawns
            #captures
            if column > 0:
                if board_positions[row + 1][column - 1].get_piece() == None or board_positions[row + 1][column - 1].get_piece().color != self.color:
                    valid_positions.append((row + 1, column - 1))
                if board_positions[row][column - 1].get_piece() == None or board_positions[row][column - 1].get_piece().color != self.color:
                    valid_positions.append((row + 1, column - 1))
                    
            if column < 7:
                if board_positions[row + 1][column + 1].get_piece() == None or board_positions[row + 1][column + 1].get_piece().color != self.color:
                    valid_positions.append((row + 1, column + 1))
                if board_positions[row][column + 1].get_piece() == None or board_positions[row][column + 1].get_piece().color != self.color:
                    valid_positions.append((row + 1, column + 1))

        elif self.initialized_row == 6: #bottom pawns
            #captures
            if column > 0:
                if board_positions[row - 1][column - 1].get_piece() == None or board_positions[row - 1][column - 1].get_piece().color != self.color:
                    valid_positions.append((row - 1, column - 1))
                if board_positions[row][column - 1].get_piece() == None or board_positions[row][column - 1].get_piece().color != self.color:
                    valid_positions.append((row - 1, column - 1))

            if column < 7:        
                if board_positions[row - 1][column + 1].get_piece() == None or board_positions[row - 1][column + 1].get_piece().color != self.color:
                    valid_positions.append((row - 1, column + 1))
                if board_positions[row][column + 1].get_piece() == None or board_positions[row][column + 1].get_piece().color != self.color:
                    valid_positions.append((row - 1, column + 1))

        return valid_positions
            