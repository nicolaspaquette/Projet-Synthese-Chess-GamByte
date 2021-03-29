from move_strategy import move_strategy
import copy
import math

class minimax(move_strategy):
    def __init__(self, board, ai_color):
        self.board = board
        self.color = ai_color

    def select_move(self):
        depth = 2
        alpha = -math.inf
        beta = math.inf

        if self.color == "white":
            maximizing_player = True
        else:
            maximizing_player = False

        #board = copy.deepcopy(self.board)
        score, move = self.minimax_search(self.board, depth, alpha, beta, maximizing_player)

        return score, move

    def minimax_search(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        if maximizing_player:
            color = "white"
        else:
            color = "black"

        all_valid_moves = []
        for row in board.position:
            for square in row:
                valid_piece_positions = []
                if square.get_piece() != None and square.get_piece().color == color:
                    valid_piece_positions = board.get_valid_piece_positions(square.row, square.column, True)

                    for piece_position in valid_piece_positions:
                        move = [square.row, square.column, piece_position[0], piece_position[1]]
                        all_valid_moves.append(move)

        move_chosen = None

        # white player side: maximizing
        if maximizing_player:
            best_evaluation = -math.inf
            
            for move in all_valid_moves:
                board_copy = copy.deepcopy(board)
                valid_positions = board_copy.get_valid_piece_positions(move[0], move[1], True)
                board_copy.move_piece(move[0], move[1], move[2], move[3], valid_positions, True)

                evaluation = self.minimax_search(board_copy, depth - 1, alpha, beta, False)[0]

                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    move_chosen = move

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            return best_evaluation, move_chosen

        # black player side: minimizing
        else:
            worse_evaluation = math.inf
            
            for move in all_valid_moves:
                board_copy = copy.deepcopy(board)

                # move : [starting_row, starting_column, final_row, final_column]
                valid_positions = board_copy.get_valid_piece_positions(move[0], move[1], True)
                board_copy.move_piece(move[0], move[1], move[2], move[3], valid_positions, True)

                evaluation = self.minimax_search(board_copy, depth - 1, alpha, beta, True)[0]

                if evaluation < worse_evaluation:
                    worse_evaluation = evaluation
                    move_chosen = move

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            return worse_evaluation, move_chosen

    def evaluate_position(self, board):
        # for white, maximizing the score
        # for black, minimizing the score

        ai_score = 0
        opponent_score = 0
        for row in board.position:
            for square in row:
                if square.get_piece() != None and square.get_piece().color == self.color:
                    ai_score += square.get_piece().value
                elif  square.get_piece() != None and square.get_piece().color != self.color:
                    opponent_score += square.get_piece().value

        # board_score = white_score - black_score
        if self.color == "white":
            board_score = ai_score - opponent_score
        else:
            board_score = opponent_score - ai_score

        return board_score
