import pygame

WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

GREY = (200, 200, 200)
BLACK = (0, 0, 0)

FPS = 10

def show_menu():
    WINDOW.fill(GREY)
    draw_button("boop", BLACK, 100, 100, 100, 100)

def show_game():
    WINDOW.fill(GREY)

def show_history():
    WINDOW.fill(GREY)

def show_visualize_game():
    WINDOW.fill(GREY)

def draw_button(text, color, left, top, width, height):
    font = pygame.font.SysFont("Arial", 20)
    button = pygame.draw.rect(WINDOW, color, (left, top, width, height))

def main():
    is_running = True
    clock = pygame.time.Clock()
    pygame.font.init()

    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        show_menu()
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()