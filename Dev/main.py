import pygame
from random import randrange
from board import board

class chess_game():
    def __init__(self):
        pygame.init()

        self.width, self.height = 1200, 800
        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.Surface(self.window.get_size())

        self.grey = (125, 125, 125)
        self.black = (0, 0, 0)
        self.light_black = (50, 50, 50)
        self.white = (255, 255, 255)
        self.beige = (204, 174, 92)
        self.orange = (176, 106, 26)
        self.fps = 10

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

        self.board = board()

    def main(self):
        is_running = True
        clock = pygame.time.Clock()
        self.screen = self.screen.convert()

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

                    self.mouse = None

            elif self.is_game:
                self.show_game()
            elif self.is_visualize_game:
                self.show_visualize_game()
            elif self.is_history:
                self.show_history()
            
            self.window.blit(self.screen, (0,0))
            pygame.display.update()

        pygame.quit()

    def show_menu(self):
        pygame.display.set_caption("Main Menu")
        self.screen.fill(self.grey)

        font = pygame.font.SysFont("Arial", 75)
        title_1 = font.render("CHESS ENGINE", True, self.black)
        title_1_rect = title_1.get_rect(center=(self.width//2, 50))
        title_2 = font.render("GAMBYTE", True, self.black)
        title_2_rect = title_2.get_rect(center=(self.width//2, 120))
        self.screen.blit(title_1, title_1_rect)
        self.screen.blit(title_2, title_2_rect)

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

        starting_pos_left = 50
        starting_pos_top = 40
        left = starting_pos_left
        top = starting_pos_top

        color_switch = False
        color = self.orange
        square_size = None

        for row in self.board.position:
            for square in row:
                if color_switch:
                    color = self.beige
                    color_switch = False
                else:
                    color = self.orange
                    color_switch = True

                square_size = square.size
                pygame.draw.rect(self.screen, color, (left, top, square_size, square_size))
                left += square_size
            
            top += square_size
            left = starting_pos_left
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


####################################################################################

if __name__ == "__main__":
    chess_game = chess_game()
    chess_game.main()