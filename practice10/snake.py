import pygame
import random

# Инициализация
pygame.init()

# Размер окна
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Размер блока
BLOCK = 20

# Шрифт
font = pygame.font.SysFont(None, 36)

# Скорость (будет расти)
speed = 7
clock = pygame.time.Clock()

# Начальная позиция змейки
snake = [(100, 100)]
dx, dy = BLOCK, 0

# Генерация еды (не на змейке)
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, BLOCK)
        y = random.randrange(0, HEIGHT, BLOCK)
        if (x, y) not in snake:
            return x, y
food = generate_food()
score = 0
level = 1
running = True
while running:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -BLOCK, 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = BLOCK, 0
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -BLOCK
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, BLOCK

    # Новая голова
    head_x = snake[0][0] + dx
    head_y = snake[0][1] + dy
    new_head = (head_x, head_y)

    # Столкновение со стеной
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        running = False

    # Столкновение с собой
    if new_head in snake:
        running = False

    # Добавляем голову
    snake.insert(0, new_head)

    # Проверка еды
    if new_head == food:
        score += 1
        food = generate_food()

        # 🎯 Уровни (каждые 3 очка)
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  # удаляем хвост если не съели еду

    # Отрисовка
    screen.fill(WHITE)

    # Змейка
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK, BLOCK))

    # Еда
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK, BLOCK))

    # Текст (счет и уровень)
    text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()