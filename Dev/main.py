import pygame
pygame.init()
import json
from datetime import datetime
from random import randrange
import math
from board import board
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent) + '/players_script')
from ai import ai
from human import human
sys.path.append(str(Path(__file__).parent) + '/DAO_script')
from game_history_DAO import game_history_DAO

class chess_game():
    def __init__(self):

        self.width, self.height = 1200, 700
        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.Surface(self.window.get_size())
        self.screen = self.screen.convert()
        self.fps = 5

        self.gray = (125, 125, 125)
        self.black = (0, 0, 0)
        self.light_black = (50, 50, 50)
        self.white = (255, 255, 255)
        self.beige = (204, 174, 92)
        self.orange = (176, 106, 26)
        self.green = (0, 130, 0)
        self.red = (130, 0, 0)

        self.is_menu = True
        self.is_game = False
        self.is_history = False
        self.select_color = False

        self.history_button_positions = []
        self.game_button_positions = []
        self.game_buttons_init = True
        self.menu_button_positions = []
        self.color_buttons_init = True
        self.game_mode_buttons_init = True
        self.mouse = None

        self.selected_color = None
        self.path = str(Path(__file__).parent) + '/assets/'

        self.white_bottom_column_values = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        self.white_bottom_row_values = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        self.black_bottom_column_values = {0: "H", 1: "G", 2: "F", 3: "E", 4: "D", 5: "C", 6: "B", 7: "A"}
        self.black_bottom_row_values = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}

        self.are_players_initialized = False

        self.player_turn = None
        self.game_started = False

        self.starting_pos_left = 50
        self.starting_pos_top = 50

        self.starting_row = None
        self.starting_column = None
        self.game_mode = None
        self.game_saved = False

        self.viewing_current_move = True
        self.viewing_game_in_db = False
        self.current_game_in_bd_viewed = None
        self.viewing_index = 0

        self.game_history_DAO = game_history_DAO()
        self.list_games = []

        self.pawn_upgrade_chosen = None
        self.played_row = None
        self.played_column = None

    def main(self):
        is_running = True
        clock = pygame.time.Clock()
        wait_time = 0

        while is_running: # closes the window if checkmate
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse = pygame.mouse.get_pos()

            if self.is_menu:
                wait_time = 0
                self.show_menu()
                if self.mouse != None:
                    for button in self.menu_button_positions: # button: [texte, left, top, width, height]
                        if self.mouse[0] >= button[1] and self.mouse[0] <= button[1] + button[3] and self.mouse[1] >= button[2] and self.mouse[1] <= button[2] + button[4]:

                            #click on button
                            if button[0] == "Play vs Human" or button[0] == "Play vs AI":
                                self.viewing_current_move = True
                                self.select_color = True
                                if button[0] == "Play vs Human":
                                    self.game_mode = "Human"
                                else:
                                    self.game_mode = "AI"
                            elif button[0] == "White":
                                self.selected_color = "white"
                                self.is_menu = False
                                self.is_game = True
                                self.viewing_game_in_db = False
                                self.current_game_in_bd_viewed = None
                            elif button[0] == "Random":
                                random = randrange(10)
                                if random % 2 == 0:
                                    self.selected_color = "white"
                                else:
                                    self.selected_color = "black"
                                self.is_menu = False
                                self.is_game = True
                                self.viewing_game_in_db = False
                                self.current_game_in_bd_viewed = None
                            elif button[0] == "Black":
                                self.selected_color = "black"
                                self.is_menu = False
                                self.is_game = True
                                self.viewing_game_in_db = False
                                self.current_game_in_bd_viewed = None
                            elif button[0] == "Game History":
                                self.is_menu = False
                                self.is_game = False
                                self.is_history = True
                                self.list_games = self.game_history_DAO.get_all_games()
                                self.list_games.reverse()
                                self.first_game_DB = 0
                                self.last_game_DB = 7
                                self.page_chosen = False
                                self.tick = 0
                                self.viewing_game_in_db = True

            elif self.is_game:
                if not self.are_players_initialized:
                    self.board = board(self.selected_color)
                    self.initialize_players()
                    self.are_players_initialized = True
        
                if not self.game_started:
                    self.game_started = True
                    self.start_game()

                self.show_game()

                ##################################################### GAME LOOP ###################################################
                
                if not self.board.game_over and not self.viewing_game_in_db:
                    # human player turn
                    if self.player_turn == self.players[0]:
                        if self.mouse != None:
                            square_size = self.board.position[0][0].size
                            if self.mouse[0] >= self.starting_pos_left and self.mouse[0] <= self.starting_pos_left + (8 *  square_size):
                                if self.mouse[1] >= self.starting_pos_left and self.mouse[1] <= self.starting_pos_top + (8 *  square_size):

                                    #row and column selection
                                    row = math.floor((self.mouse[1]-self.starting_pos_top)/square_size)
                                    column = math.floor((self.mouse[0]-self.starting_pos_left)/square_size)

                                    #piece is selected
                                    self.player_turn.choose_move(row, column)

                                    #piece destination is selected
                                    if self.player_turn.starting_row != None and self.player_turn.starting_column != None and (row != self.player_turn.starting_row or column != self.player_turn.starting_column):
                                        if self.player_turn.verify_move(row, column):
                                            self.player_turn.valid_positions = self.player_turn.play_move(row, column)
                                            self.player_turn.starting_row = None
                                            self.player_turn.starting_column = None

                                            self.played_row = row
                                            self.played_column = column

                                            if not self.board.upgrading_pawn:
                                                    self.played_row = None
                                                    self.played_column = None
                                                    self.change_player_turn()
                                                    self.show_game()

                        #show possible moves
                        if self.player_turn == self.players[0]:
                            if self.player_turn.starting_row != None and self.player_turn.starting_column != None:
                                self.show_valid_positions(self.player_turn.valid_positions)
                    else:
                        # human opponent
                        if self.game_mode == "Human":
                            if self.mouse != None:
                                square_size = self.board.position[0][0].size
                                if self.mouse[0] >= self.starting_pos_left and self.mouse[0] <= self.starting_pos_left + (8 *  square_size):
                                    if self.mouse[1] >= self.starting_pos_left and self.mouse[1] <= self.starting_pos_top + (8 *  square_size):

                                        #row and column selection
                                        row = math.floor((self.mouse[1]-self.starting_pos_top)/square_size)
                                        column = math.floor((self.mouse[0]-self.starting_pos_left)/square_size)

                                        #piece is selected
                                        self.player_turn.choose_move(row, column)

                                        #piece destination is selected
                                        if self.player_turn.starting_row != None and self.player_turn.starting_column != None and (row != self.player_turn.starting_row or column != self.player_turn.starting_column):
                                            if self.player_turn.verify_move(row, column):
                                                self.player_turn.valid_positions = self.player_turn.play_move(row, column)
                                                self.player_turn.starting_row = None
                                                self.player_turn.starting_column = None

                                                self.played_row = row
                                                self.played_column = column

                                                if not self.board.upgrading_pawn:
                                                    self.played_row = None
                                                    self.played_column = None
                                                    self.change_player_turn()
                                                    self.show_game()

                            #show possible moves
                            if self.player_turn == self.players[1]:
                                if self.player_turn.starting_row != None and self.player_turn.starting_column != None:
                                    self.show_valid_positions(self.player_turn.valid_positions)

                        # ai opponent
                        else:
                            if wait_time > 0:
                                self.player_turn.play_move()
                                self.change_player_turn()

                    wait_time += 1

                if self.mouse != None:
                    for button in self.game_button_positions: # button: [texte, left, top, width, height]
                        if self.mouse[0] >= button[1] and self.mouse[0] <= button[1] + button[3] and self.mouse[1] >= button[2] and self.mouse[1] <= button[2] + button[4]:
                            
                            if button[0] == "<<":
                                if not self.viewing_game_in_db:
                                    if len(self.board.game_information["Moves"]) > 0:
                                        self.viewing_current_move = False
                                        self.board.viewing_index = 0
                                else:
                                    self.viewing_index = 0
                            elif button[0] == "<":
                                if not self.viewing_game_in_db:
                                    if len(self.board.game_information["Moves"]) > 0:
                                        self.viewing_current_move = False
                                        if self.board.viewing_index > 0:
                                            self.board.viewing_index -= 1
                                else:
                                    if self.viewing_index > 0:
                                        self.viewing_index -= 1
                            elif button[0] == ">":
                                if not self.viewing_game_in_db:
                                    self.viewing_current_move = False
                                    if len(self.board.game_information["Moves"]) > 0 and self.board.viewing_index < len(self.board.game_information["Moves"]) - 1:
                                        print("NOOOOOOOOO")
                                        self.board.viewing_index += 1
                                    if len(self.board.game_information["Moves"]) > 0 and self.board.viewing_index == len(self.board.game_information["Moves"]) - 1:
                                        self.viewing_current_move = True
                                else:
                                    if len(self.current_game_in_bd_viewed["Moves"]) > 0 and self.viewing_index < len(self.current_game_in_bd_viewed["Moves"]) - 1 :
                                        self.viewing_index += 1
                            elif button[0] == ">>":
                                if not self.viewing_game_in_db:
                                    if len(self.board.game_information["Moves"]) > 0:
                                        self.viewing_current_move = True
                                        self.board.viewing_index = len(self.board.game_information["Moves"]) - 1
                                else:
                                    self.viewing_index = len(self.current_game_in_bd_viewed["Moves"]) - 1
                            elif button[0] == "Forfeit Game":
                                self.board.game_over = True
                                self.board.game_over_result = "Forfeit"
                                if self.board.human_player_color == "white":
                                    self.board.winner = "Black"
                                else:
                                    self.board.winner = "White"
                            elif button[0] == "Main Menu":
                                self.is_menu = True
                                self.is_game = False
                                self.select_color = False
                                self.are_players_initialized = False
                                self.game_started = False
                                self.viewing_index = 0
                                self.select_color = False
                            elif button[0] == "Queen":
                                self.pawn_upgrade_chosen = "queen"
                            elif button[0] == "Rook":
                                self.pawn_upgrade_chosen = "rook"
                            elif button[0] == "Bishop":
                                self.pawn_upgrade_chosen = "bishop"
                            elif button[0] == "Knight":
                                self.pawn_upgrade_chosen = "knight"

                if self.board.upgrading_pawn and self.pawn_upgrade_chosen != None:
                    self.board.upgrade_pawn(self.played_row, self.played_column, self.board.upgrading_pawn_color, self.pawn_upgrade_chosen)
                    self.board.upgrading_pawn = False
                    self.pawn_upgrade_chosen = None
                    self.played_row = None
                    self.played_column = None
                    self.change_player_turn()
                    self.show_game()

                if self.board.game_over and not self.viewing_game_in_db:
                    if not self.game_saved:
                        self.save_game()
                        self.game_saved = True

                ##################################################### GAME LOOP ###################################################

            elif self.is_history:
                self.show_history()
                self.tick += 1

                if self.mouse != None:
                    for button in self.history_button_positions: # button: [texte, left, top, width, height]
                        if self.mouse[0] >= button[1] and self.mouse[0] <= button[1] + button[3] and self.mouse[1] >= button[2] and self.mouse[1] <= button[2] + button[4]:

                            if button[0] == "Main Menu":
                                self.is_menu = True
                                self.is_history = False
                                self.select_color = False
                            elif "View Game" in button[0]:
                                self.viewing_game_in_db = True
                                game_id = int(button[0].split()[-1])
                                for game in self.list_games:
                                    if game["_id"] == game_id:
                                        self.current_game_in_bd_viewed = game

                                self.is_history = False
                                self.is_game = True
                            elif button[0] == "Last page":
                                if self.first_game_DB > 0 and not self.page_chosen:
                                    self.first_game_DB -= 7
                                    self.last_game_DB -= 7
                                    self.page_chosen = True
                            elif button[0] == "Next page":
                                if self.last_game_DB < len(self.list_games) and not self.page_chosen:
                                    self.first_game_DB += 7
                                    self.last_game_DB += 7
                                    self.page_chosen = True

                            if self.tick >= 6:
                                self.page_chosen = False
                                self.tick = 0

            self.window.blit(self.screen, (0,0))
            pygame.display.update()
            self.mouse = None

        pygame.quit()



    ##################################################### FUNCTIONS ###################################################



    def show_menu(self):
        pygame.display.set_caption("Main Menu")
        self.screen.fill(self.gray)

        #titles
        font = pygame.font.SysFont("Arial", 75)
        title_1 = font.render("CHESS ENGINE", True, self.black)
        title_1_rect = title_1.get_rect(center=(self.width//2, 60))
        title_2 = font.render("GAMBYTE", True, self.black)
        title_2_rect = title_2.get_rect(center=(self.width//2, 140))
        self.screen.blit(title_1, title_1_rect)
        self.screen.blit(title_2, title_2_rect)

        #buttons
        pos_play_human = self.draw_button("Play vs Human", 30, self.white, self.black, 400, 300, 70, 10, False)
        pos_play_ai = self.draw_button("Play vs AI", 30, self.white, self.black, 800, 300, 100, 10, False)
        pos_history = self.draw_button("Game History", 30, self.white, self.black, 100, 550, 175, 10, True)
        if self.select_color:
            font = pygame.font.SysFont("Arial", 30)
            mode = "Game mode selected: Human VS " + self.game_mode
            game_mode = font.render(mode, True, self.black)
            game_mode_rect = game_mode.get_rect(center=(self.width//2, 240))

            choose_color = font.render("Choose color to start game:", True, self.black)
            choose_color_text = choose_color.get_rect(center=(self.width//2, 370))
            self.screen.blit(game_mode, game_mode_rect)
            self.screen.blit(choose_color, choose_color_text)

            pos_white = self.draw_button("White", 30, self.black, self.white, 450, 430, 10, 10, False)
            pos_random = self.draw_button("Random", 30, self.white, self.light_black, 100, 430, 10, 10, True)
            pos_black = self.draw_button("Black", 30, self.white, self.black, 750, 430, 10, 10, False)
            if self.color_buttons_init:
                self.color_buttons_init = False
                self.menu_button_positions.append(pos_white)
                self.menu_button_positions.append(pos_random)
                self.menu_button_positions.append(pos_black)

        if self.game_mode_buttons_init:
            self.game_mode_buttons_init = False
            self.menu_button_positions.append(pos_play_human)
            self.menu_button_positions.append(pos_play_ai)
            self.menu_button_positions.append(pos_history)

    def show_game(self):
        pygame.display.set_caption("Game")
        self.screen.fill(self.gray)

        left = self.starting_pos_left
        top = self.starting_pos_top

        color_switch = False
        color = self.orange
        square_size = None

        value = 0
        letter_value = 0
        font = pygame.font.SysFont("Arial", 30)

        #letter/number of squares depending orientation of board
        if not self.viewing_game_in_db:
            if self.selected_color == "white":
                col_text = self.white_bottom_column_values
                row_text = self.white_bottom_row_values
            else:
                col_text = self.black_bottom_column_values
                row_text = self.black_bottom_row_values
        else:
            moves = list(self.current_game_in_bd_viewed["Moves"].keys())
            if self.current_game_in_bd_viewed["Moves"][moves[0]][1][0] == "black":
                col_text = self.white_bottom_column_values
                row_text = self.white_bottom_row_values
            else:
                col_text = self.black_bottom_column_values
                row_text = self.black_bottom_row_values
        
        for row in self.board.position:

            #draw row value
            value_text = font.render(row_text[value], True, self.black)
            value_text_rect = value_text.get_rect(center=(self.starting_pos_left - 20 , top + 35))
            self.screen.blit(value_text, value_text_rect)
            value += 1
            for square in row:
                if color_switch:
                    color = self.beige
                    color_switch = False
                else:
                    color = self.orange
                    color_switch = True

                #draw squares
                square_size = square.size
                pygame.draw.rect(self.screen, color, (left, top, square_size, square_size))

                #show pieces on squares
                if self.viewing_current_move and not self.viewing_game_in_db: #if its the current move, otherwise show the positions of past moves
                    square_piece = square.get_piece()
                    if square_piece != None:
                        path = str(self.path + square_piece.color + "_" + square_piece.name + ".png")
                        piece_image = pygame.image.load(path)
                        piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
                        piece_image.convert()
                        self.screen.blit(piece_image, (left, top, square_size, square_size))
                else:
                    if not self.viewing_game_in_db:
                        piece_list = list(self.board.game_information["Moves"].values())[self.board.viewing_index]
                    else:
                        piece_list = list(self.current_game_in_bd_viewed["Moves"].values())[self.viewing_index]

                    counter = 0
                    for piece_info in piece_list:
                        counter += 1
                        if counter != 1:
                            if square.row == piece_info[2] and square.column == piece_info[3]:
                                path = str(self.path + piece_info[0] + "_" + piece_info[1] + ".png")
                                piece_image = pygame.image.load(path)
                                piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
                                piece_image.convert()
                                self.screen.blit(piece_image, (left, top, square_size, square_size))

                #draw column letter
                if value == 7:
                    letter_text = font.render(col_text[letter_value], True, self.black)
                    letter_text_rect = letter_text.get_rect(center=(left + square_size/2, top + square_size*2 + 20))
                    self.screen.blit(letter_text, letter_text_rect)
                    letter_value += 1

                left += square_size

            top += square_size
            left = self.starting_pos_left
            if color_switch:
                    color = self.beige
                    color_switch = False
            else:
                color = self.orange
                color_switch = True

        if self.current_game_in_bd_viewed:
            font = pygame.font.SysFont("Arial", 40)
            piece_list = list(self.current_game_in_bd_viewed["Moves"].values())
            piece_position_at_index = piece_list[self.viewing_index]
            evaluation_text = font.render("Evaluation: " + str((piece_position_at_index[0][0])), True, self.black)
            evaluation_text_rect = evaluation_text.get_rect(center=(800, 70))
            self.screen.blit(evaluation_text, evaluation_text_rect)

        #show the list of moves done
        info_square_left = square_size*8 + self.starting_pos_left*2
        info_square_top = square_size*2 + self.starting_pos_top
        info_square_width = square_size*6
        info_square_height = square_size*4
        pygame.draw.rect(self.screen, self.black, (info_square_left, info_square_top, info_square_width, info_square_height))
        
        move_names = self.get_move_names()
        font = pygame.font.SysFont("Arial", 15)
        top_pos = 10
        nb_rows = 0
        for row in move_names:
            nb_rows += 1
            names = font.render(row, True, self.white)
            names_rect = names.get_rect(center=(info_square_left + info_square_width/2, info_square_top + top_pos))
            self.screen.blit(names, names_rect)
            top_pos += 20
            if nb_rows == 15:
                break

        #buttons to move through the list
        first_move_button = self.draw_button("<<", 30, self.white, self.light_black, info_square_left + 80, info_square_top - square_size/2, info_square_width/15, 5, False)
        prior_move_button = self.draw_button("<", 30, self.white, self.light_black, info_square_left + (info_square_left/8)+ 80, info_square_top - square_size/2, info_square_width/15, 5, False)
        next_move_button = self.draw_button(">", 30, self.white, self.light_black, info_square_left + 2*(info_square_left/8)+ 120, info_square_top - square_size/2, info_square_width/15, 5, False)
        last_move_button = self.draw_button(">>", 30, self.white, self.light_black, info_square_left  + 3*(info_square_left/8)+ 120, info_square_top - square_size/2, info_square_width/15, 5, False)
        if not self.viewing_game_in_db:
            forfeit_button = self.draw_button("Forfeit Game", 30, self.white, self.light_black, info_square_left + info_square_width/2, info_square_top + info_square_height + 40, info_square_width/4, 10, False)
            self.game_button_positions.append(forfeit_button)

        if self.board.game_over and not self.viewing_game_in_db:
            return_menu_button = self.draw_button("Main Menu", 30, self.white, self.black, 1100, 45, 20, 10, False)
            self.game_button_positions.append(return_menu_button)
        elif self.viewing_game_in_db:
            return_menu_button = self.draw_button("Main Menu", 30, self.white, self.black, 1100, 45, 20, 10, False)
            self.game_button_positions.append(return_menu_button)

        if self.game_buttons_init:
            self.game_buttons_init = False
            self.game_button_positions.append(first_move_button)
            self.game_button_positions.append(prior_move_button)
            self.game_button_positions.append(next_move_button)
            self.game_button_positions.append(last_move_button)

        if self.game_started and self.viewing_current_move and not self.viewing_game_in_db:
            font = pygame.font.SysFont("Arial", 30)
            turn_to_play = "Turn to play: "+ self.player_turn.color
            turn_to_play_text = font.render(turn_to_play, True, self.black)
            turn_to_play_text_rect = turn_to_play_text.get_rect(center=(150, 25))
            self.screen.blit(turn_to_play_text, turn_to_play_text_rect)

            self.show_checks_and_checkmates()

        if (self.game_started and len(self.board.game_information["Moves"]) > 0) or self.viewing_game_in_db:
            font = pygame.font.SysFont("Arial", 30)
            if not self.viewing_game_in_db:
                keys_list = list(self.board.game_information["Moves"].keys())
                board_state = "Board state with last move: " + keys_list[self.board.viewing_index]
            else:
                keys_list = list(self.current_game_in_bd_viewed["Moves"].keys())
                board_state = "Board state with last move: " + keys_list[self.viewing_index]
            board_state_text = font.render(board_state, True, self.black)
            board_state_text_rect = board_state_text.get_rect(center=(info_square_left + info_square_width/2, info_square_top + info_square_height * 1.4))
            self.screen.blit(board_state_text, board_state_text_rect)

        if self.board.upgrading_pawn and not self.viewing_game_in_db:
        #if 1 == 1 and not self.viewing_game_in_db:
            upgrade_left = info_square_left-30
            upgrade_top = 10
            upgrade_width = info_square_width+60
            upgrade_height = 120

            pygame.draw.rect(self.screen, self.gray, (upgrade_left, upgrade_top, upgrade_width, upgrade_height))
            upgrade_pawn_text = font.render("Upgrade pawn", True, self.black)
            upgrade_pawn_text_rect = upgrade_pawn_text.get_rect(center=(upgrade_left + upgrade_width/2, 25))
            self.screen.blit(upgrade_pawn_text, upgrade_pawn_text_rect)

            queen_button = self.draw_button("Queen", 25, self.white, self.black, upgrade_left + 65, upgrade_top + upgrade_height/2 + 15, 12, 10, False)
            self.game_button_positions.append(queen_button)

            rook_button = self.draw_button("Rook", 25, self.white, self.black, upgrade_left + upgrade_width/4 + 67, upgrade_top + upgrade_height/2 + 15, 16, 10, False)
            self.game_button_positions.append(rook_button)

            bishop_button = self.draw_button("Bishop", 25, self.white, self.black, upgrade_left + upgrade_width/4*2 + 72, upgrade_top + upgrade_height/2 + 15, 10, 10, False)
            self.game_button_positions.append(bishop_button)

            knight_button = self.draw_button("Knight", 25, self.white, self.black, upgrade_left + upgrade_width/4*3 + 65, upgrade_top + upgrade_height/2 + 15, 10, 10, False)
            self.game_button_positions.append(knight_button)

            
    def show_history(self):
        pygame.display.set_caption("History")
        self.screen.fill(self.gray)

        return_menu_button = self.draw_button("Main Menu", 30, self.white, self.black, 1100, 45, 20, 10, False)
        self.history_button_positions.append(return_menu_button)

        last_page_button = self.draw_button("Last page", 30, self.white, self.black, 400, 655, 20, 10, False)
        self.history_button_positions.append(last_page_button)

        next_page_button = self.draw_button("Next page", 30, self.white, self.black, 800, 655, 20, 10, False)
        self.history_button_positions.append(next_page_button)

        font = pygame.font.SysFont("Arial", 25)
        page = "Page " + str(int(self.last_game_DB/7)) + " of " + str(int(len(self.list_games)/7 + 1))
        page_text = font.render(page, True, self.black)
        page_text_rect = page_text.get_rect(center=(600, 655))
        self.screen.blit(page_text, page_text_rect)

        font = pygame.font.SysFont("Arial", 40)
        date_text = font.render("Date", True, self.black)
        date_text_rect = date_text.get_rect(center=(150, 45))
        self.screen.blit(date_text, date_text_rect)
        result_text = font.render("Result", True, self.black)
        result_text_rect = result_text.get_rect(center=(350, 45))
        self.screen.blit(result_text, result_text_rect)
        winner_text = font.render("Winner", True, self.black)
        winner_text_rect = winner_text.get_rect(center=(550, 45))
        self.screen.blit(winner_text, winner_text_rect)
        nb_text = font.render("Number of moves", True, self.black)
        nb_text_rect = nb_text.get_rect(center=(800, 45))
        self.screen.blit(nb_text, nb_text_rect)

        font = pygame.font.SysFont("Arial", 25)
        top_pos = 150
        for i in range(self.first_game_DB, self.last_game_DB):
            if i == len(self.list_games):
                break

            game_date_text = font.render(self.list_games[i]["Date"], True, self.black)
            game_date_text_rect = game_date_text.get_rect(center=(150, top_pos))
            self.screen.blit(game_date_text, game_date_text_rect)
            game_result_text = font.render(self.list_games[i]["Result"], True, self.black)
            game_result_text_rect = game_result_text.get_rect(center=(350, top_pos))
            self.screen.blit(game_result_text, game_result_text_rect)
            game_winner_text = font.render(self.list_games[i]["Winner"], True, self.black)
            game_winner_text_rect = game_winner_text.get_rect(center=(550, top_pos))
            self.screen.blit(game_winner_text, game_winner_text_rect)
            game_nb_text = font.render(str(len(self.list_games[i]["Moves"])), True, self.black)
            game_nb_text_rect = game_nb_text.get_rect(center=(800, top_pos))
            self.screen.blit(game_nb_text, game_nb_text_rect)
            view_game_button = self.draw_button("View Game " + str(self.list_games[i]["_id"]), 25, self.white, self.light_black, 1000, top_pos, 10, 5, False)
            self.history_button_positions.append(view_game_button)
            top_pos += 60


    def draw_button(self, text, font_size, font_color, color, left, top, border_size_width, border_size_height, is_centered):
        font = pygame.font.SysFont("Arial", font_size)
        message = font.render(text, True, font_color)
        
        if is_centered:
            message_rect = message.get_rect(center=(self.width//2, top))
        else:
            message_rect = message.get_rect(center=(left, top))
        button = pygame.draw.rect(self.screen, color, (message_rect[0] - border_size_width, message_rect[1] - border_size_height, message.get_width() + (border_size_width * 2), message.get_height() + (border_size_height * 2)))
        self.screen.blit(message, message_rect)
        return [text, message_rect[0] - border_size_width, message_rect[1] - border_size_height, message.get_width() + (border_size_width * 2), message.get_height() + (border_size_height * 2)]

    def initialize_players(self):
        self.players = []
        if self.selected_color == "white":
            self.board.bottom_color = "white"
            opponent_color = "black"
        else:
            opponent_color = "white"
            self.board.bottom_color = "black"

        if self.game_mode == "Human":
            self.board.bottom_color = self.selected_color
            self.players.append(human(self.selected_color, self.board))
            self.players.append(human(opponent_color, self.board))
        else:
            self.players.append(human(self.selected_color, self.board))
            self.players.append(ai(opponent_color, self.board))

    def start_game(self):
        if self.players[0].color == "white":
            self.player_turn = self.players[0]
        else:
            self.player_turn = self.players[1]
        self.game_saved = False
    
    def change_player_turn(self):
        if self.player_turn == self.players[0]:
            self.player_turn = self.players[1]
        else:
            self.player_turn = self.players[0]

        if self.board.color_to_play == "white":
            self.board.color_to_play = "black"
        else:
            self.board.color_to_play = "white"

    def show_valid_positions(self, valid_positions):
        if self.viewing_current_move:
            for position in valid_positions:
                pygame.draw.circle(self.screen, self.green, (self.starting_pos_left + (75 * position[1]) + 75 / 2, self.starting_pos_top + (75 * position[0]) + 75 / 2), 5)

    def show_checks_and_checkmates(self):
        if self.board.white_king_pos != None and self.board.black_king_pos != None:
            font = pygame.font.SysFont("Arial", 30)
            if self.board.is_king_in_checkmate("white") != False:
                self.board.game_over = True
                if self.board.is_king_in_checkmate("white") == "Checkmate":
                    checkmate = font.render("White King Checkmate", True, self.black)
                    checkmate_rect = checkmate.get_rect(center=(525, 25))
                    self.screen.blit(checkmate, checkmate_rect)
                    self.board.game_over_result = "Checkmate"
                    self.board.winner = "Black"
                else:
                    stalemate = font.render("White King Stalemate", True, self.black)
                    stalemate_rect = stalemate.get_rect(center=(525, 25))
                    self.screen.blit(stalemate, stalemate_rect)
                    self.board.game_over_result = "Stalemate"
                    self.board.winner = "Draw"

            elif self.board.is_king_in_checkmate("black") != False:
                self.board.game_over = True
                if self.board.is_king_in_checkmate("black") == "Checkmate":
                    checkmate = font.render("Black King Checkmate", True, self.black)
                    checkmate_rect = checkmate.get_rect(center=(525, 25))
                    self.screen.blit(checkmate, checkmate_rect)
                    self.board.game_over_result = "Checkmate"
                    self.board.winner = "White"
                else:
                    stalemate = font.render("Black King Stalemate", True, self.black)
                    stalemate_rect = stalemate.get_rect(center=(525, 25))
                    self.screen.blit(stalemate, stalemate_rect)
                    self.board.game_over_result = "Stalemate"
                    self.board.winner = "Draw"

            elif self.board.is_king_in_check(self.board.white_king_pos[0], self.board.white_king_pos[1]):
                check = font.render("White King Check", True, self.black)
                check_rect = check.get_rect(center=(550, 25))
                self.screen.blit(check, check_rect)

            elif self.board.is_king_in_check(self.board.black_king_pos[0], self.board.black_king_pos[1]):
                check = font.render("Black King Check", True, self.black)
                check_rect = check.get_rect(center=(550, 25))
                self.screen.blit(check, check_rect)

    def save_game(self):
        self.board.game_information["_id"] = self.game_history_DAO.get_next_id()
        self.board.game_information["Winner"] = self.board.winner
        self.board.game_information["Result"] = self.board.game_over_result
        self.board.game_information["Date"] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.game_history_DAO.save_game(self.board.game_information)
        
    def get_move_names(self):
        if not self.viewing_game_in_db:
            keys = self.board.game_information["Moves"].keys()
        else:
            keys = self.current_game_in_bd_viewed["Moves"].keys()
        move_names = []
        row = []
        move_row = ""
        counter = 0
        #changes row after 9 moves for display
        for key in keys:
            if key != "Winner" or key != "Result" or key != "Date":
                counter += 1
                move_row += (" " + key)
                if counter >= 8:
                    move_names.append(move_row)
                    counter = 0
                    move_row = ""
        if len(move_row) > 0:
            move_names.append(move_row)

        return move_names

if __name__ == "__main__":
    chess_game = chess_game()
    chess_game.main()