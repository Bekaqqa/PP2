import pygame
from clock import MickeyClock

def main():
    pygame.init()

    WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    clock = pygame.time.Clock()
    mickey = MickeyClock(screen, WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((240, 240, 240))

        mickey.draw()

        pygame.display.flip()
        clock.tick(60)  # плавное обновление

    pygame.quit()


if __name__ == "__main__":
    main()