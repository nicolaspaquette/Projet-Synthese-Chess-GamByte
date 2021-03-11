import pygame

WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    isRunning = True

    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

    pygame.quit()

if __name__ == "__main__":
    main()