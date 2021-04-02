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
            return board.evaluate_position(self.color), None

        # white player side: maximizing
        if maximizing_player:
            best_evaluation = -math.inf
            all_valid_moves = board.get_all_moves_possible("white")

            for move in all_valid_moves:
                board.move_piece(move[1], move[2], move[3], move[4], [], True, False)
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
            #print("ALL THE MOVES", all_valid_moves, "\n")
            
            for move in all_valid_moves:
                board.move_piece(move[1], move[2], move[3], move[4], [], True, False)
                evaluation = self.minimax_search(board, depth - 1, alpha, beta, True)[0]
                board.undo_last_move_done()

                if evaluation < worse_evaluation:
                    worse_evaluation = evaluation
                    move_chosen = move

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            return worse_evaluation, move_chosen
