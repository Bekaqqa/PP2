import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Program")

font = pygame.font.SysFont(None, 26)

# Текущий цвет кисти
current_color = (0, 0, 0)

# Текущий инструмент: None = кисть, иначе название фигуры
current_tool = None

# Холст — отдельная поверхность, на которой хранится рисунок
# Это нужно чтобы при перетаскивании preview не оставлял следов
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# Точка начала перетаскивания
drag_start = None
# Флаг: зажата ли мышь прямо сейчас
dragging = False


def draw_hint():
    """Рисует серую полоску с подсказкой в верхней части экрана."""
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 36))
    tool_name = current_tool if current_tool else "кисть"
    hint = (
        f"Инструмент: [{tool_name}]   |   "
        "R-красный  G-зелёный  B-синий  E-ластик  |  "
        "F-кисть  1-прямоуг  2-круг  3-квадрат  4-прям▲  5-равн▲  6-ромб"
    )
    text = font.render(hint, True, (30, 30, 30))
    screen.blit(text, (8, 10))


def get_shape_points(tool, start, end):
    """
    Возвращает данные фигуры по двум точкам: start (откуда тянули) и end (куда).
    Возвращает словарь с типом фигуры и её параметрами.
    """
    x1, y1 = start
    x2, y2 = end

    if tool == "прямоуг":
        # Прямоугольник: от start до end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        return {"type": "rect", "rect": rect}

    elif tool == "квадрат":
        # Квадрат: сторона = минимум из ширины/высоты, выровнен по start
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx = x1 if x2 >= x1 else x1 - side
        sy = y1 if y2 >= y1 else y1 - side
        return {"type": "rect", "rect": pygame.Rect(sx, sy, side, side)}

    elif tool == "круг":
        # Круг: центр = start, радиус = расстояние до end
        r = int(math.hypot(x2 - x1, y2 - y1))
        return {"type": "circle", "center": (x1, y1), "radius": r}

    elif tool == "прям▲":
        # Прямоугольный треугольник: прямой угол в start
        points = [(x1, y1), (x2, y1), (x1, y2)]
        return {"type": "polygon", "points": points}

    elif tool == "равн▲":
        # Равносторонний треугольник: основание от start до end
        cx = (x1 + x2) / 2           # центр основания
        base = abs(x2 - x1)          # длина основания
        h = base * math.sqrt(3) / 2  # высота
        # Треугольник смотрит вверх если тянем вниз, и наоборот
        direction = 1 if y2 >= y1 else -1
        points = [
            (x1, y1),
            (x2, y1),
            (cx, y1 - direction * h),
        ]
        return {"type": "polygon", "points": [(int(px), int(py)) for px, py in points]}

    elif tool == "ромб":
        # Ромб: центр в start, правая вершина в end
        cx, cy = x1, y1
        hw = abs(x2 - x1)  # половина ширины
        hh = abs(y2 - y1)  # половина высоты
        points = [
            (cx,      cy - hh),
            (cx + hw, cy),
            (cx,      cy + hh),
            (cx - hw, cy),
        ]
        return {"type": "polygon", "points": points}

    return None


def draw_shape(surface, shape_data, color, width=2):
    """Рисует фигуру по данным из get_shape_points на указанную поверхность."""
    if shape_data is None:
        return
    t = shape_data["type"]
    if t == "rect":
        if shape_data["rect"].width > 0 and shape_data["rect"].height > 0:
            pygame.draw.rect(surface, color, shape_data["rect"], width)
    elif t == "circle":
        if shape_data["radius"] > 0:
            pygame.draw.circle(surface, color, shape_data["center"], shape_data["radius"], width)
    elif t == "polygon":
        if len(shape_data["points"]) >= 3:
            pygame.draw.polygon(surface, color, shape_data["points"], width)


# ─── Главный цикл ────────────────────────────────────────────────────────────
clock = pygame.time.Clock()
running = True

while running:
    mx, my = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # ── Выбор инструмента / цвета ─────────────────────────────────────
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                current_color = (220, 0, 0)
            elif e.key == pygame.K_g:
                current_color = (0, 180, 0)
            elif e.key == pygame.K_b:
                current_color = (0, 0, 220)
            elif e.key == pygame.K_e:
                current_color = (255, 255, 255)
            elif e.key == pygame.K_f:
                current_tool = None        # кисть
            elif e.key == pygame.K_1:
                current_tool = "прямоуг"
            elif e.key == pygame.K_2:
                current_tool = "круг"
            elif e.key == pygame.K_3:
                current_tool = "квадрат"
            elif e.key == pygame.K_4:
                current_tool = "прям▲"
            elif e.key == pygame.K_5:
                current_tool = "равн▲"
            elif e.key == pygame.K_6:
                current_tool = "ромб"

        # ── Нажатие ЛКМ — начало перетаскивания ──────────────────────────
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if my > 36:  # не реагируем на панель подсказки
                drag_start = (mx, my)
                dragging = True

        # ── Отпускание ЛКМ — фиксируем фигуру на холсте ──────────────────
        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            if dragging and drag_start and current_tool and my > 36:
                shape = get_shape_points(current_tool, drag_start, (mx, my))
                draw_shape(canvas, shape, current_color, 2)  # рисуем на холст навсегда
            dragging = False
            drag_start = None

    # ── Кисть: рисуем прямо на холст при зажатой ЛКМ ─────────────────────
    if dragging and current_tool is None and my > 36:
        pygame.draw.circle(canvas, current_color, (mx, my), 6)

    # ── Отрисовка кадра ───────────────────────────────────────────────────

    # 1. Копируем холст на экран
    screen.blit(canvas, (0, 0))

    # 2. Рисуем preview фигуры поверх (только пока тянем)
    if dragging and current_tool and drag_start and my > 36:
        shape = get_shape_points(current_tool, drag_start, (mx, my))
        # Рисуем пунктирный preview — просто тонкой линией поверх экрана (не на холст!)
        draw_shape(screen, shape, current_color, 1)

    # 3. Подсказка поверх всего
    draw_hint()

    pygame.display.update()
    clock.tick(60)

pygame.quit()