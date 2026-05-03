import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

clock = pygame.time.Clock()
FPS = 60

# Цвета
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GRAY    = (60, 60, 60)
DKGRAY  = (30, 30, 30)
YELLOW  = (255, 210, 0)
GREEN   = (0, 210, 80)
RED     = (220, 50, 50)
DKRED   = (150, 20, 20)
BLUE    = (30, 100, 220)
DKBLUE  = (10, 50, 140)
LBLUE   = (120, 190, 255)
SILVER  = (180, 185, 195)
ORANGE  = (240, 120, 0)
DKORANGE= (160, 70, 0)

font    = pygame.font.SysFont("Arial", 32, bold=True)
sfont   = pygame.font.SysFont("Arial", 20)

PW, PH = 48, 88
SPEED_PLR = 7

coin_types = [
    {"size": 13, "color": GREEN,  "value": 5},
    {"size": 21, "color": YELLOW, "value": 3},
    {"size": 29, "color": RED,    "value": 1},
]

high_score = 0

def update_high_score(score):
    global high_score
    if score > high_score:
        high_score = score


# ── Машинка ──────────────────────────────────────────────────────────────────
def draw_car(x, y, is_player):
    body  = BLUE   if is_player else RED
    dark  = DKBLUE if is_player else DKRED
    glass = LBLUE  if is_player else ORANGE

    # тень
    pygame.draw.ellipse(screen, (20, 20, 20),
                        (x + 4, y + PH - 6, PW - 8, 10))

    # багажник / зад
    pygame.draw.rect(screen, dark,
                     (x + 5, y + PH - 16, PW - 10, 12), border_radius=4)

    # основной кузов
    pygame.draw.rect(screen, body,
                     (x + 4, y + 20, PW - 8, PH - 34), border_radius=6)

    # капот
    pygame.draw.rect(screen, body,
                     (x + 7, y + 5, PW - 14, 18), border_radius=5)

    # кабина / крыша
    pygame.draw.rect(screen, dark,
                     (x + 9, y + 15, PW - 18, 36), border_radius=7)

    # лобовое стекло
    pygame.draw.rect(screen, glass,
                     (x + 11, y + 18, PW - 22, 14), border_radius=4)
    # блик на стекле
    pygame.draw.rect(screen, WHITE,
                     (x + 13, y + 20, 7, 7), border_radius=2)

    # заднее стекло
    pygame.draw.rect(screen, glass,
                     (x + 11, y + 35, PW - 22, 12), border_radius=3)

    # фары (спереди = сверху)
    for hx in (x + 7, x + PW - 17):
        pygame.draw.ellipse(screen, YELLOW, (hx, y + 3, 10, 6))
        pygame.draw.ellipse(screen, WHITE,  (hx + 2, y + 4, 6, 4))

    # стоп-огни (сзади = снизу)
    for tx in (x + 6, x + PW - 16):
        pygame.draw.rect(screen, (230, 20, 20),
                         (tx, y + PH - 14, 10, 6), border_radius=2)

    # колёса (4 штуки)
    for wx, wy in [(x - 3, y + 14), (x + PW - 5, y + 14),
                   (x - 3, y + PH - 34), (x + PW - 5, y + PH - 34)]:
        pygame.draw.rect(screen, BLACK,  (wx, wy, 8, 18), border_radius=3)
        pygame.draw.rect(screen, SILVER, (wx + 1, wy + 3, 6, 12), border_radius=2)
        pygame.draw.circle(screen, GRAY, (wx + 4, wy + 9), 2)

    # номерной знак
    pygame.draw.rect(screen, WHITE,
                     (x + 10, y + PH - 22, PW - 20, 8), border_radius=2)
    lbl = sfont.render("P" if is_player else "X", True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=(x + PW // 2, y + PH - 18)))


# ── Монета ────────────────────────────────────────────────────────────────────
def draw_coin(coin):
    r  = coin["type"]["size"] // 2
    cx, cy = coin["x"], coin["y"]
    col = coin["type"]["color"]

    # простое свечение
    pygame.draw.circle(screen, col, (cx, cy), r + 4, 3)
    pygame.draw.circle(screen, col, (cx, cy), r)
    pygame.draw.circle(screen, WHITE, (cx, cy), r, 1)

    txt = sfont.render(f"+{coin['type']['value']}", True, BLACK)
    screen.blit(txt, txt.get_rect(center=(cx, cy)))


# ── Дорога ────────────────────────────────────────────────────────────────────
def draw_road(offset):
    screen.fill(DKGRAY)

    # полотно дороги
    pygame.draw.rect(screen, GRAY, (25, 0, WIDTH - 50, HEIGHT))

    # разметка по центру
    for i in range(-40, HEIGHT, 40):
        y = (i + int(offset)) % HEIGHT
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y, 6, 24))

    # белые края
    pygame.draw.line(screen, WHITE, (44, 0), (44, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (WIDTH - 44, 0), (WIDTH - 44, HEIGHT), 2)

    # бордюры красно-белые
    sh = 22
    for i in range(-sh * 2, HEIGHT + sh, sh * 2):
        y = (i + int(offset)) % (sh * 2) - sh
        pygame.draw.rect(screen, RED,   (0,          y,      25, sh))
        pygame.draw.rect(screen, WHITE, (0,          y + sh, 25, sh))
        pygame.draw.rect(screen, RED,   (WIDTH - 25, y,      25, sh))
        pygame.draw.rect(screen, WHITE, (WIDTH - 25, y + sh, 25, sh))


# ── Спавн ─────────────────────────────────────────────────────────────────────
def new_enemies():
    return [
        {"x": random.randint(44, WIDTH - 44 - PW), "y": random.randint(-280, -100)},
        {"x": random.randint(44, WIDTH - 44 - PW), "y": random.randint(-480, -290)},
    ]

def spawn_coin(enemies):
    for _ in range(20):
        t = random.choice(coin_types)
        x = random.randint(50, WIDTH - 50)
        y = -40
        if all(abs(x - e["x"]) > 60 or abs(y - e["y"]) > 120 for e in enemies):
            return {"type": t, "x": x, "y": y}
    return {"type": coin_types[1], "x": WIDTH // 2, "y": -40}

def reset():
    en = new_enemies()
    return {
        "px": WIDTH // 2 - PW // 2,
        "py": HEIGHT - 130,
        "coins": 0,
        "speed": 5,
        "over":  False,
        "off":   0,
        "enemies": en,
        "coin": spawn_coin(en),
    }


# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(coins, best):
    # тёмная панелька
    pygame.draw.rect(screen, (0, 0, 0), (6, 6, 155, 62), border_radius=10)
    pygame.draw.rect(screen, YELLOW,    (6, 6, 155, 62), 2, border_radius=10)

    screen.blit(font.render(f"★ {coins}", True, YELLOW), (16, 12))
    screen.blit(sfont.render(f"Рекорд: {best}", True, SILVER), (16, 46))


def draw_gameover(coins, best):
    # затемнение
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 170))
    screen.blit(ov, (0, 0))

    # рамка
    pygame.draw.rect(screen, RED,   (WIDTH//2-120, HEIGHT//2-100, 240, 200), border_radius=14)
    pygame.draw.rect(screen, BLACK, (WIDTH//2-118, HEIGHT//2-98,  236, 196), border_radius=13)

    go  = font.render("КОНЕЦ!", True, RED)
    sc  = font.render(f"★ {coins}", True, YELLOW)
    bs  = sfont.render(f"Рекорд: {best}", True, SILVER)
    rst = sfont.render("R  —  заново", True, WHITE)

    screen.blit(go,  go.get_rect(center=(WIDTH//2, HEIGHT//2 - 64)))
    screen.blit(sc,  sc.get_rect(center=(WIDTH//2, HEIGHT//2 - 18)))
    screen.blit(bs,  bs.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))

    pygame.draw.rect(screen, BLUE,  (WIDTH//2-80, HEIGHT//2+50, 160, 40), border_radius=8)
    screen.blit(rst, rst.get_rect(center=(WIDTH//2, HEIGHT//2 + 70)))


# ── Главный цикл ──────────────────────────────────────────────────────────────
game = reset()
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game["over"]:
                game = reset()
                continue  # сразу начинаем новый кадр

    keys = pygame.key.get_pressed()

    if not game["over"]:
        # движение игрока
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and game["px"] > 44:
            game["px"] -= SPEED_PLR
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and game["px"] < WIDTH - PW - 44:
            game["px"] += SPEED_PLR

        sp = game["speed"]
        game["off"] = (game["off"] + sp) % 40

        # двигаем всё вниз
        game["coin"]["y"] += sp
        for e in game["enemies"]:
            e["y"] += sp

        # пересоздаём монету если ушла
        if game["coin"]["y"] > HEIGHT + 30:
            game["coin"] = spawn_coin(game["enemies"])

        # пересоздаём врагов
        for e in game["enemies"]:
            if e["y"] > HEIGHT + 20:
                e["y"] = random.randint(-300, -100)
                e["x"] = random.randint(44, WIDTH - 44 - PW)

        # прямоугольники для столкновений
        pr = pygame.Rect(game["px"] + 4, game["py"] + 8, PW - 8, PH - 14)

        # монета
        c  = game["coin"]
        r2 = c["type"]["size"] // 2
        if pr.colliderect(pygame.Rect(c["x"]-r2, c["y"]-r2, r2*2, r2*2)):
            game["coins"] += c["type"]["value"]
            game["coin"]   = spawn_coin(game["enemies"])

        # враги
        for e in game["enemies"]:
            if pr.colliderect(pygame.Rect(e["x"]+4, e["y"]+8, PW-8, PH-14)):
                game["over"] = True
                update_high_score(game["coins"])

        # ускорение
        game["speed"] = 5 + game["coins"] / 10

    # ── рисуем ────────────────────────────────────────────────────────────────
    draw_road(game["off"])
    draw_coin(game["coin"])
    for e in game["enemies"]:
        draw_car(e["x"], e["y"], is_player=False)
    draw_car(game["px"], game["py"], is_player=True)
    draw_hud(game["coins"], high_score)

    if game["over"]:
        draw_gameover(game["coins"], high_score)

    pygame.display.update()

pygame.quit()