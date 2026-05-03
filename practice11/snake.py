import pygame
import random

# ─── Инициализация ────────────────────────────────────────────────────────────
pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Цвета
WHITE    = (255, 255, 255)
BLACK    = (0,   0,   0)
GREEN    = (0,   200, 100)
DARK_GREEN = (0, 140, 70)
BG       = (245, 245, 230)

# Размер одной клетки
BLOCK = 20

# Шрифт
font       = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)

clock = pygame.time.Clock()

# ─── Типы еды ─────────────────────────────────────────────────────────────────
# weight  — очки за съедение
# color   — цвет квадратика
# label   — буква внутри
# chance  — вероятность появления (сумма всех = 100)
# lifetime — сколько секунд живёт до исчезновения (None = не исчезает)

FOOD_TYPES = [
    {"weight": 1, "color": (220, 50,  50),  "label": "1", "chance": 50, "lifetime": None},  # обычная
    {"weight": 2, "color": (255, 160, 0),   "label": "2", "chance": 30, "lifetime": 5.0},   # исчезает за 5 сек
    {"weight": 3, "color": (180, 0,  220),  "label": "3", "chance": 15, "lifetime": 3.5},   # исчезает за 3.5 сек
    {"weight": 5, "color": (0,  180, 220),  "label": "5", "chance": 5,  "lifetime": 2.0},   # редкая, 2 сек
]

# Веса для random.choices
FOOD_CHANCES = [ft["chance"] for ft in FOOD_TYPES]


def pick_food_type():
    """Случайно выбирает тип еды с учётом вероятности."""
    return random.choices(FOOD_TYPES, weights=FOOD_CHANCES, k=1)[0]


def generate_food(snake_body, existing_foods):
    """
    Генерирует новую еду в случайной клетке.
    Не ставит еду туда, где уже есть тело змейки или другая еда.
    """
    occupied = set(snake_body) | {f["pos"] for f in existing_foods}
    while True:
        x = random.randrange(0, WIDTH,  BLOCK)
        y = random.randrange(BLOCK * 2, HEIGHT, BLOCK)  # ниже панели HUD
        if (x, y) not in occupied:
            ft = pick_food_type()
            return {
                "pos":      (x, y),
                "type":     ft,
                "born":     pygame.time.get_ticks() / 1000.0,  # время появления (сек)
            }


def draw_food(food_item):
    """
    Рисует квадратик еды.
    Если еда исчезающая — мигает когда остаётся < 1.5 сек.
    """
    ft       = food_item["type"]
    x, y     = food_item["pos"]
    lifetime = ft["lifetime"]
    now      = pygame.time.get_ticks() / 1000.0
    age      = now - food_item["born"]

    # Мигание: скрываем еду каждые 0.25 сек если время на исходе
    if lifetime is not None:
        remaining = lifetime - age
        if remaining < 1.5 and int(remaining / 0.25) % 2 == 0:
            return  # пропускаем отрисовку (мигание)

    # Основной квадрат еды
    pygame.draw.rect(screen, ft["color"], (x, y, BLOCK, BLOCK), border_radius=4)

    # Буква с весом внутри
    lbl = small_font.render(ft["label"], True, WHITE)
    screen.blit(lbl, (x + BLOCK // 2 - lbl.get_width() // 2,
                      y + BLOCK // 2 - lbl.get_height() // 2))

    # Таймер-полоска под едой (только для исчезающей)
    if lifetime is not None:
        remaining  = max(0, lifetime - age)
        bar_width  = int(BLOCK * remaining / lifetime)
        pygame.draw.rect(screen, (255, 255, 255), (x, y + BLOCK + 2, BLOCK, 3))
        pygame.draw.rect(screen, ft["color"],     (x, y + BLOCK + 2, bar_width, 3))


def draw_snake(snake):
    """Рисует змейку: голова чуть темнее, тело зелёное."""
    for i, seg in enumerate(snake):
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(screen, color, (seg[0], seg[1], BLOCK, BLOCK), border_radius=4)
        if i == 0:
            # Глаза на голове
            pygame.draw.circle(screen, WHITE, (seg[0] + 5,  seg[1] + 6), 3)
            pygame.draw.circle(screen, WHITE, (seg[0] + 15, seg[1] + 6), 3)
            pygame.draw.circle(screen, BLACK, (seg[0] + 5,  seg[1] + 6), 1)
            pygame.draw.circle(screen, BLACK, (seg[0] + 15, seg[1] + 6), 1)


def draw_hud(score, level, speed):
    """Рисует верхнюю панель с очками, уровнем и скоростью."""
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, BLOCK * 2))
    hud = font.render(f"Score: {score}   Level: {level}   Speed: {speed}", True, WHITE)
    screen.blit(hud, (10, 8))

    # Легенда типов еды справа
    legend_x = WIDTH - 320
    for i, ft in enumerate(FOOD_TYPES):
        pygame.draw.rect(screen, ft["color"], (legend_x + i * 78, 8, 14, 14), border_radius=3)
        info = small_font.render(
            f"+{ft['weight']}{'  ⏱' if ft['lifetime'] else ''}",
            True, WHITE
        )
        screen.blit(info, (legend_x + i * 78 + 18, 8))


def show_game_over(score, level):
    """Экран Game Over с итогами."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    go = font.render("GAME OVER", True, (255, 80, 80))
    sc = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    rs = small_font.render("Press R to restart or Q to quit", True, (200, 200, 200))

    screen.blit(go, go.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(sc, sc.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(rs, rs.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
    pygame.display.update()


def reset():
    """Сбрасывает все параметры игры и возвращает начальное состояние."""
    snake  = [(100, 100), (80, 100), (60, 100)]
    dx, dy = BLOCK, 0
    foods  = []
    foods.append(generate_food(snake, foods))
    return snake, dx, dy, foods, 0, 1, 7


# ─── Старт игры ───────────────────────────────────────────────────────────────
snake, dx, dy, foods, score, level, speed = reset()

# Таймер для спавна дополнительной еды каждые N секунд
EXTRA_FOOD_INTERVAL = 5000   # мс
MAX_FOODS           = 4      # максимум одновременной еды на поле
last_food_spawn     = pygame.time.get_ticks()

running    = True
game_over  = False

while running:
    clock.tick(speed)
    now_ms = pygame.time.get_ticks()

    # ── Обработка событий ─────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                # Управление змейкой (нельзя развернуться назад)
                if event.key == pygame.K_LEFT  and dx == 0:
                    dx, dy = -BLOCK, 0
                if event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy =  BLOCK, 0
                if event.key == pygame.K_UP    and dy == 0:
                    dx, dy = 0, -BLOCK
                if event.key == pygame.K_DOWN  and dy == 0:
                    dx, dy = 0,  BLOCK
            else:
                # Рестарт или выход после Game Over
                if event.key == pygame.K_r:
                    snake, dx, dy, foods, score, level, speed = reset()
                    last_food_spawn = now_ms
                    game_over = False
                if event.key == pygame.K_q:
                    running = False

    if game_over:
        show_game_over(score, level)
        continue

    # ── Движение змейки ───────────────────────────────────────────────────
    head_x = snake[0][0] + dx
    head_y = snake[0][1] + dy
    new_head = (head_x, head_y)

    # Столкновение со стеной
    if head_x < 0 or head_x >= WIDTH or head_y < BLOCK * 2 or head_y >= HEIGHT:
        game_over = True
        continue

    # Столкновение с собой
    if new_head in snake:
        game_over = True
        continue

    snake.insert(0, new_head)

    # ── Проверка поедания еды ─────────────────────────────────────────────
    eaten = None
    for f in foods:
        if new_head == f["pos"]:
            eaten = f
            break

    if eaten:
        score += eaten["type"]["weight"]   # очки = вес еды
        foods.remove(eaten)
        foods.append(generate_food(snake, foods))  # новая еда на замену

        # Повышение уровня каждые 5 очков
        new_level = score // 5 + 1
        if new_level > level:
            level  = new_level
            speed += 2  # ускорение при новом уровне
    else:
        snake.pop()  # убираем хвост если ничего не съели

    # ── Удаление просроченной еды ─────────────────────────────────────────
    now_sec = now_ms / 1000.0
    expired = [f for f in foods
               if f["type"]["lifetime"] is not None
               and now_sec - f["born"] >= f["type"]["lifetime"]]
    for f in expired:
        foods.remove(f)

    # ── Периодический спавн дополнительной еды ────────────────────────────
    if now_ms - last_food_spawn > EXTRA_FOOD_INTERVAL and len(foods) < MAX_FOODS:
        foods.append(generate_food(snake, foods))
        last_food_spawn = now_ms

    # ── Отрисовка ─────────────────────────────────────────────────────────
    screen.fill(BG)

    # Сетка (лёгкая, для удобства)
    for gx in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, (230, 230, 215), (gx, BLOCK * 2), (gx, HEIGHT))
    for gy in range(BLOCK * 2, HEIGHT, BLOCK):
        pygame.draw.line(screen, (230, 230, 215), (0, gy), (WIDTH, gy))

    # Еда (сначала, чтобы змейка была поверх)
    for f in foods:
        draw_food(f)

    # Змейка
    draw_snake(snake)

    # HUD поверх всего
    draw_hud(score, level, speed)

    pygame.display.update()

pygame.quit()