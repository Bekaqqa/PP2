import pygame
from persistence import load_leaderboard, save_settings

pygame.font.init()

# ===== COLORS =====
BG = (15, 15, 25)
CARD = (30, 30, 50)
ACCENT = (0, 200, 255)
WHITE = (240, 240, 240)
HOVER = (60, 60, 90)

# ===== BUTTON =====
class Button:
    def __init__(self, text, x, y, w=260, h=60):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.hovered = False

    def draw(self, screen, font):
        color = HOVER if self.hovered else CARD
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, ACCENT, self.rect, 2, border_radius=15)

        txt = font.render(self.text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ===== MAIN MENU =====
class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(None, 80)
        self.font = pygame.font.Font(None, 40)

        self.buttons = [
            Button("PLAY", 270, 200),
            Button("LEADERBOARD", 270, 280),
            Button("SETTINGS", 270, 360),
            Button("QUIT", 270, 440)
        ]

    def run(self):
        while True:
            self.screen.fill(BG)

            title = self.title_font.render("RACER", True, ACCENT)
            self.screen.blit(title, (280, 80))

            mouse_pos = pygame.mouse.get_pos()

            for b in self.buttons:
                b.update(mouse_pos)
                b.draw(self.screen, self.font)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit"

                if e.type == pygame.MOUSEBUTTONDOWN:
                    for b in self.buttons:
                        if b.clicked(e.pos):
                            return b.text.lower()

            pygame.display.flip()

# ===== LEADERBOARD =====
class LeaderboardScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)

    def run(self):
        data = load_leaderboard()

        while True:
            self.screen.fill(BG)

            title = self.title_font.render("TOP 10", True, ACCENT)
            self.screen.blit(title, (300, 50))

            for i, e in enumerate(data):
                txt = f"{i+1}. {e['name']}  -  {e['score']}"
                self.screen.blit(self.font.render(txt, True, WHITE), (250, 140 + i*35))

            hint = self.font.render("Press any key to go back", True, (150,150,150))
            self.screen.blit(hint, (220, 550))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return "quit"
                if ev.type == pygame.KEYDOWN:
                    return "menu"

            pygame.display.flip()

# ===== GAME OVER =====
class GameOverScreen:
    def __init__(self, screen, result):
        self.screen = screen
        self.result = result
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 70)

    def run(self):
        while True:
            self.screen.fill(BG)

            title = self.title_font.render("GAME OVER", True, (255, 80, 80))
            self.screen.blit(title, (220, 150))

            score = self.font.render(f"Score: {self.result['score']}", True, WHITE)
            self.screen.blit(score, (300, 300))

            hint = self.font.render("Press any key", True, (150,150,150))
            self.screen.blit(hint, (310, 400))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit"
                if e.type == pygame.KEYDOWN:
                    return "menu"

            pygame.display.flip()

# ===== SETTINGS =====
class SettingsScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.Font(None, 40)

    def run(self):
        while True:
            self.screen.fill(BG)

            txt = self.font.render(f"Difficulty: {self.settings['difficulty']}", True, WHITE)
            self.screen.blit(txt, (250, 250))

            hint = self.font.render("Press SPACE to toggle", True, (150,150,150))
            self.screen.blit(hint, (250, 320))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "quit"

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.settings['difficulty'] = 'hard' if self.settings['difficulty']=='normal' else 'normal'
                        save_settings(self.settings)
                        return self.settings

            pygame.display.flip()

# ===== NAME INPUT =====
class NameInputScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)

    def run(self):
        name = ""

        while True:
            self.screen.fill(BG)

            title = self.font.render("Enter Name", True, ACCENT)
            self.screen.blit(title, (280, 150))

            box = pygame.Rect(200, 260, 400, 60)
            pygame.draw.rect(self.screen, CARD, box, border_radius=10)
            pygame.draw.rect(self.screen, ACCENT, box, 2, border_radius=10)

            txt = self.font.render(name, True, WHITE)
            self.screen.blit(txt, (box.x + 10, box.y + 15))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "Player"

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return name if name else "Player"
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 12:
                            name += e.unicode

            pygame.display.flip()
