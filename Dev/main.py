import pygame
pygame.init()

from random import randrange
import math

from board import board

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent) + '/players_script')

from ai import ai
from human import human

class chess_game():
    def __init__(self):

        self.width, self.height = 1200, 700
        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.Surface(self.window.get_size())
        self.screen = self.screen.convert()
        self.fps = 5

        self.grey = (125, 125, 125)
        self.black = (0, 0, 0)
        self.light_black = (50, 50, 50)
        self.white = (255, 255, 255)
        self.beige = (204, 174, 92)
        self.orange = (176, 106, 26)
        self.green = (0, 130, 0)
        self.red = (130, 0, 0)

        self.is_menu = True
        self.is_game = False
        self.is_visualize_game = False
        self.is_history = False
        self.select_color = False

        self.button_positions = []
        self.color_button_positions = True
        self.menu_button_positions = True
        self.mouse = None

        self.selected_color = None
        self.path = str(Path(__file__).parent) + '/assets/pieces/'

        self.white_human_row_values = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        self.white_human_column_values = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
        self.black_human_row_values = {0: "H", 1: "G", 2: "F", 3: "E", 4: "D", 5: "C", 6: "B", 7: "A"}
        self.black_human_column_values = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}

        self.players = []
        self.are_players_initialized = False

        self.player_turn = None
        self.game_started = False

        self.starting_pos_left = 50
        self.starting_pos_top = 50

        self.starting_row = None
        self.starting_column = None

    def main(self):
        is_running = True
        clock = pygame.time.Clock()

        while is_running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse = pygame.mouse.get_pos()

            if self.is_menu:
                self.show_menu()
                if self.mouse != None:
                    for button in self.button_positions: # button: [texte, left, top, width, height]
                        if self.mouse[0] >= button[1] and self.mouse[0] <= button[1] + button[3] and self.mouse[1] >= button[2] and self.mouse[1] <= button[2] + button[4]:

                            #click on button
                            if button[0] == "PLAY":
                                self.select_color = True
                            elif button[0] == "White":
                                self.selected_color = "white"
                                self.is_menu = False
                                self.is_game = True
                            elif button[0] == "Random":
                                random = randrange(10)
                                if random % 2 == 0:
                                    self.selected_color = "white"
                                else:
                                    self.selected_color = "black"
                                self.is_menu = False
                                self.is_game = True
                            elif button[0] == "Black":
                                self.selected_color = "black"
                                self.is_menu = False
                                self.is_game = True
                            elif button[0] == "HISTORY":
                                pass

            elif self.is_game:
                if not self.are_players_initialized:
                    self.board = board(self.selected_color)
                    self.initialize_players()
                    self.are_players_initialized = True

                self.show_game()

                if not self.game_started:
                    self.game_started = True
                    self.start_game()

                if self.mouse != None:
                    square_size = self.board.position[0][0].size
                    if self.mouse[0] >= self.starting_pos_left and self.mouse[0] <= self.starting_pos_left + (8 *  square_size):
                        if self.mouse[1] >= self.starting_pos_left and self.mouse[1] <= self.starting_pos_top + (8 *  square_size):

                            #row and column selection
                            row = math.floor((self.mouse[1]-self.starting_pos_top)/square_size)
                            column = math.floor((self.mouse[0]-self.starting_pos_left)/square_size)

                            #piece is selected
                            if self.board.choose_piece_to_move(row, column):
                                self.starting_row = row
                                self.starting_column = column
                                valid_positions = self.board.get_valid_positions(self.starting_row, self.starting_column)
                            
                            #piece destination is selected
                            if self.starting_row != None and self.starting_column != None and (row != self.starting_row or column != self.starting_column):
                                if self.board.verify_move(valid_positions, row, column):
                                    valid_positions = self.board.move_piece(self.starting_row, self.starting_column, row, column, valid_positions)
                                    self.starting_row = None
                                    self.starting_column = None

                #show possible moves
                if self.starting_row != None and self.starting_column != None:
                    self.show_valid_positions(valid_positions)

            elif self.is_visualize_game:
                self.show_visualize_game()

            elif self.is_history:
                self.show_history()
            
            self.window.blit(self.screen, (0,0))
            pygame.display.update()

            self.mouse = None

        pygame.quit()

#########################################################################################################

    def show_menu(self):
        pygame.display.set_caption("Main Menu")
        self.screen.fill(self.grey)

        #titles
        font = pygame.font.SysFont("Arial", 75)
        title_1 = font.render("CHESS ENGINE", True, self.black)
        title_1_rect = title_1.get_rect(center=(self.width//2, 60))
        title_2 = font.render("GAMBYTE", True, self.black)
        title_2_rect = title_2.get_rect(center=(self.width//2, 140))
        self.screen.blit(title_1, title_1_rect)
        self.screen.blit(title_2, title_2_rect)

        #buttons
        pos_play = self.draw_button("PLAY", 30, self.white, self.black, 100, 300, 200, 10, True)
        pos_history = self.draw_button("HISTORY", 30, self.white, self.black, 100, 600, 175, 10, True)
        if self.select_color:
            pos_white = self.draw_button("White", 30, self.black, self.white, 450, 380, 10, 10, False)
            pos_random = self.draw_button("Random", 30, self.white, self.light_black, 100, 380, 10, 10, True)
            pos_black = self.draw_button("Black", 30, self.white, self.black, 750, 380, 10, 10, False)
            if self.color_button_positions:
                self.color_button_positions = False
                self.button_positions.append(pos_white)
                self.button_positions.append(pos_random)
                self.button_positions.append(pos_black)

        if self.menu_button_positions:
            self.menu_button_positions = False
            self.button_positions.append(pos_play)
            self.button_positions.append(pos_history)

    def show_game(self):
        pygame.display.set_caption("Game")
        self.screen.fill(self.grey)

        left = self.starting_pos_left
        top = self.starting_pos_top

        color_switch = False
        color = self.orange
        square_size = None

        value = 0
        letter_value = 0
        font = pygame.font.SysFont("Arial", 30)

        #letter/number of squares depending orientation of board
        if self.selected_color == "white":
            row_values = self.white_human_row_values
            column_values = self.white_human_column_values
        else:
            row_values = self.black_human_row_values
            column_values = self.black_human_column_values
        
        for row in self.board.position:

            #draw row value
            value_text = font.render(column_values[value], True, self.black)
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
                square_piece = square.get_piece()
                if square_piece != None:
                    path = str(self.path + square_piece.color + "_" + square_piece.name + ".png")
                    piece_image = pygame.image.load(path)
                    piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
                    piece_image.convert()
                    self.screen.blit(piece_image, (left, top, square_size, square_size))

                #draw column letter
                if value == 7:
                    letter_text = font.render(row_values[letter_value], True, self.black)
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

    def show_history(self):
        pass

    def show_visualize_game(self):
        pass

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
        if self.selected_color == "white":
            ai_color = "black"
        else:
            ai_color = "white"

        self.players.append(human(self.selected_color, self.board))
        self.players.append(ai(ai_color, self.board))

    def start_game(self):
        if self.players[0].color == "white":
            self.player_turn = self.players[0]
        else:
            self.player_turn = self.players[1]

        self.player_turn.choose_move()
    
    def change_player_turn(self):
        if self.player_turn == self.players[0]:
            self.player_turn = self.players[1]
        else:
            self.player_turn = self.players[0]

        self.player_turn.choose_move()

    def show_valid_positions(self, valid_positions):
        for position in valid_positions:
            pygame.draw.circle(self.screen, self.green, (self.starting_pos_left + (75 * position[1]) + 75 / 2, self.starting_pos_top + (75 * position[0]) + 75 / 2), 5)

     

####################################################################################

if __name__ == "__main__":
    chess_game = chess_game()
    chess_game.main()