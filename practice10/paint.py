from pygame import *
from pygame.sprite import *
from pygame.font import *

# Инициализация pygame
init()

# Создание окна
screen = display.set_mode((1200, 700))
display.set_caption("Paint Program")

# Цвет по умолчанию (черный)
current_color = (0, 0, 0)

# Заливка фона (делаем 1 раз, чтобы рисунок не стирался)
screen.fill((255, 255, 255))

# Шрифт
my_font = Font(None, 30)

# Основной цикл
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

        # Обработка клавиш
        if e.type == KEYDOWN:
            # Выбор цвета
            if e.key == K_r:
                current_color = (255, 0, 0)  # красный
            if e.key == K_g:
                current_color = (0, 255, 0)  # зеленый
            if e.key == K_b:
                current_color = (0, 0, 255)  # синий

            # Ластик (белый цвет)
            if e.key == K_e:
                current_color = (255, 255, 255)

            # Нарисовать прямоугольник
            if e.key == K_1:
                mx, my = mouse.get_pos()
                draw.rect(screen, current_color, (mx, my, 80, 60))

            # Нарисовать круг
            if e.key == K_2:
                mx, my = mouse.get_pos()
                draw.circle(screen, current_color, (mx, my), 40)

    # Рисование мышкой (удержание ЛКМ)
    if mouse.get_pressed()[0]:
        mx, my = mouse.get_pos()
        draw.circle(screen, current_color, (mx, my), 5)

    # Подсказка на экране
    info_text = my_font.render(
        "R/G/B - color | E - eraser | 1 - rectangle | 2 - circle",
        True,
        (0, 0, 0)
    )
    screen.blit(info_text, (10, 10))

    # Обновление экрана
    display.update()

# Выход
quit()