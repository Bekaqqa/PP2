import pygame
from racer import RacerGame
from ui import MainMenu, LeaderboardScreen, GameOverScreen, SettingsScreen, NameInputScreen
from persistence import load_settings

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Racer MAX")

settings = load_settings()

menu = MainMenu(screen)
game = RacerGame(screen, settings)

state = "menu"
result = None
player_name = "Player"

while True:
    if state == "menu":
        state = menu.run()

    elif state == "play":
        state = "name"

    elif state == "name":
        player_name = NameInputScreen(screen).run()
        result = game.run(player_name)
        state = "gameover"

    elif state == "leaderboard":
        state = LeaderboardScreen(screen).run()

    elif state == "settings":
        settings = SettingsScreen(screen, settings).run()
        game.settings = settings
        state = "menu"

    elif state == "gameover":
        state = GameOverScreen(screen, result).run()

    elif state == "quit":
        break

pygame.quit()