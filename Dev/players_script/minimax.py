from move_strategy import move_strategy
import copy
import math
import random
import time

class minimax(move_strategy):
    def __init__(self, board, ai_color):
        self.board = board
        self.color = ai_color
        self.number_of_searches = 0
        self.depth = 3

    def select_move(self):
        depth = self.depth
        alpha = -math.inf
        beta = math.inf

        if self.color == "white":
            maximizing_player = True
        else:
            maximizing_player = False

        self.number_of_searches = 0
        start_time = time.time()
        score, move = self.minimax_search(self.board, depth, alpha, beta, maximizing_player)
        print("time to search:", time.time() - start_time, "seconds")
        print("number of searches:", self.number_of_searches)

        return score, move

    def minimax_search(self, board, depth, alpha, beta, maximizing_player):
        self.number_of_searches += 1

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        # white player side: maximizing
        if maximizing_player:
            best_evaluation = -math.inf
            all_valid_moves = board.get_all_moves_possible("white")

            for move in all_valid_moves:
                board.move_piece(move[0], move[1], move[2], move[3], [], True, False)
                evaluation = self.minimax_search(board, depth - 1, alpha, beta, False)[0]
                board.undo_last_move_done()

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
            all_valid_moves = board.get_all_moves_possible("black")
            
            for move in all_valid_moves:
                board.move_piece(move[0], move[1], move[2], move[3], [], True, False)
                evaluation = self.minimax_search(board, depth - 1, alpha, beta, True)[0]
                board.undo_last_move_done()

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
