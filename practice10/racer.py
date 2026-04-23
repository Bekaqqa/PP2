import pygame
import random

# Инициализация
pygame.init()

# Размер окна
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифт
font = pygame.font.SysFont(None, 36)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Скорость игры
speed = 5

# Игрок (машина)
player_width = 50
player_height = 100
player_x = WIDTH // 2
player_y = HEIGHT - 120

# Монета
coin_size = 30
coin_x = random.randint(50, WIDTH - 50)
coin_y = -50

# Счет
coins = 0

# Основной цикл
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление машиной
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 7
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += 7

    # Движение монеты вниз
    coin_y += speed

    # Если монета ушла вниз — создаем новую
    if coin_y > HEIGHT:
        coin_y = -50
        coin_x = random.randint(50, WIDTH - 50)

    # Прямоугольники для столкновения
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)

    # Проверка столкновения
    if player_rect.colliderect(coin_rect):
        coins += 1
        coin_y = -50
        coin_x = random.randint(50, WIDTH - 50)

    # Отрисовка
    screen.fill(WHITE)

    # Машина (синий прямоугольник)
    pygame.draw.rect(screen, (0, 0, 255), player_rect)

    # Монета (желтый круг)
    pygame.draw.circle(screen, (255, 215, 0), (coin_x, coin_y), coin_size // 2)

    # Счетчик (в правом верхнем углу)
    text = font.render(f"Coins: {coins}", True, BLACK)
    screen.blit(text, (WIDTH - 120, 10))

    pygame.display.update()

pygame.quit()