import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 24)

player = MusicPlayer("music")

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.prev_track()

            elif event.key == pygame.K_q:
                running = False

    # UI текст
    track_text = font.render("Track: " + player.current_track_name(), True, (255, 255, 255))
    status_text = font.render("Playing" if player.is_playing else "Stopped", True, (0, 255, 0))

    screen.blit(track_text, (20, 100))
    screen.blit(status_text, (20, 150))

    pygame.display.update()

pygame.quit()