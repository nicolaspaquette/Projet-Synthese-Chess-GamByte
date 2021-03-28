from move_strategy import move_strategy
import copy
import math

class minimax(move_strategy):
    def __init__(self, board, ai_color):
        self.board = board
        self.color = ai_color

    def select_move(self):
        depth = 3
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        board = copy.deepcopy(self.board)

        #self.minimax_search(board, depth, alpha, beta, maximizing_player)

    def minimax_search(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over:
            return self.evaluate_position(board)

        if maximizing_player:
            best_evaluation = -math.inf
            
            all_valid_positions = []
            for row in board:
                for square in row:
                    if square.get_piece() != None and square.get_piece().color == self.color:
                        all_valid_positions += board.get_valid_piece_positions(square.row, square.column, True)
            
            for position in all_valid_positions:
                evaluation = minimax_search(position, depth - 1, alpha, beta, False)
                best_evaluation = max(best_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return best_evaluation

        else:
            worse_evaluation = math.inf
            
            all_valid_positions = []
            for row in board:
                for square in row:
                    if square.get_piece() != None and square.get_piece().color != self.color:
                        all_valid_positions += board.get_valid_piece_positions(square.row, square.column, True)
            
            for position in all_valid_positions:
                evaluation = minimax_search(position, depth - 1, alpha, beta, True)
                worse_evaluation = min(worse_evaluation, evaluation)
                beta = max(beta, evaluation)
                if beta <= alpha:
                    break
            return worse_evaluation


    def evaluate_position(self, board):
        score = 0
        for row in board:
            for square in row:
                if square.get_piece() != None and square.get_piece().color == self.color:
                    score += square.get_piece().value

        return score
