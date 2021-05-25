from player import player
from minimax import minimax
import copy
import random

class ai(player):
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.move_strategy = minimax(self.board, self.color)
        self.inititalize_playstyles()
        self.select_playstyle()
        self.previous_play_score = 0

    def play_move(self):
        if self.playstyle == None:
            score, move = self.move_strategy.select_move()
            print("board score", score/100)
            print("move", move)
            valid_positions = self.board.move_piece(move[1], move[2], move[3], move[4], [], False, True)
        else:
            self.board.get_kings_positions()

            #plays the move to see if its good or not and gets the score
            move = self.playstyle[self.playstyle_index]
            valid_positions = self.board.move_piece(move[0], move[1], move[2], move[3], [], True, True)

            game_over_result = self.board.is_game_over()
            score = self.board.evaluate_position(self.color, game_over_result)
            self.board.undo_last_move_done()

            # if the move is good, continue the opening. Otherwise, find a new move (+- 30 for variation purposes but still detects good vs bad moves)
            if (self.color == "white" and score >= self.previous_play_score - 30) or (self.color == "black" and score <= self.previous_play_score + 30): 
                valid_positions = self.board.move_piece(move[0], move[1], move[2], move[3], [], False, True)
                self.playstyle_index += 1
                if self.playstyle_index == len(self.playstyle):
                    self.playstyle = None

                self.previous_play_score = score
            else:
                self.playstyle = None
                score, move = self.move_strategy.select_move()
                print("board score", score/100)
                print("move", move)
                valid_positions = self.board.move_piece(move[1], move[2], move[3], move[4], [], False, True)

        return valid_positions

    def inititalize_playstyles(self):
        self.black_playstyles = []
        #king's indian defense
        self.black_playstyles.append([[0,6,2,5],[1,6,2,6],[0,5,1,6],[0,4,0,6]])
        #italian game
        self.black_playstyles.append([[1,4,3,4],[0,1,2,2],[0,6,2,5],[0,5,3,2],[1,3,2,3]])

        self.white_playstyles = []
        #ruy lopez
        self.white_playstyles.append([[1,3,3,3],[0,1,2,2],[0,2,4,6]])
        #london system
        self.white_playstyles.append([[1,4,3,4],[0,5,3,2],[1,3,2,3],[0,2,2,4],[0,1,2,2],[0,3,0,1],[1,5,2,5],[0,6,1,4]])

    def select_playstyle(self):
        if self.color == "white":
            choice = random.randint(0, len(self.white_playstyles))
            print(choice)
            if choice < len(self.white_playstyles):
                self.playstyle = self.white_playstyles[choice]
                self.playstyle_index = 0
            else:
                self.playstyle = None
        else:
            choice = random.randint(0, len(self.black_playstyles))
            if choice < len(self.black_playstyles):
                self.playstyle = self.black_playstyles[choice]
                self.playstyle_index = 0
            else:
                self.playstyle = None

        print("playstyle:", choice)

