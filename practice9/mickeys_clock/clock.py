import pygame
import math
import datetime

class MickeyClock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.cx = width // 2
        self.cy = height // 2
        self.radius = 160

        self.BLACK = (30, 30, 30)
        self.WHITE = (255, 255, 255)
        self.RED = (220, 50, 50)
        self.GRAY = (180, 180, 180)

    def _angle(self, value, total):
        return math.radians(value / total * 360 - 90)

    def _draw_hand(self, angle, length, color, width):
        end_x = self.cx + math.cos(angle) * length
        end_y = self.cy + math.sin(angle) * length

        # тень
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (self.cx + 2, self.cy + 2),
            (int(end_x + 2), int(end_y + 2)),
            width + 1
        )

        # стрелка
        pygame.draw.line(
            self.screen,
            color,
            (self.cx, self.cy),
            (int(end_x), int(end_y)),
            width
        )

        # круг на конце
        pygame.draw.circle(self.screen, self.WHITE, (int(end_x), int(end_y)), 10)
        pygame.draw.circle(self.screen, self.BLACK, (int(end_x), int(end_y)), 10, 2)

    def draw(self):
        now = datetime.datetime.now()

        hours = now.hour
        minutes = now.minute
        seconds = now.second

        # фон
        self.screen.fill((245, 245, 245))

        # циферблат
        pygame.draw.circle(self.screen, self.WHITE, (self.cx, self.cy), self.radius)
        pygame.draw.circle(self.screen, self.BLACK, (self.cx, self.cy), self.radius, 4)

        # 🐭 уши Микки (снаружи)
        pygame.draw.circle(self.screen, self.BLACK, (self.cx - 140, self.cy - 180), 60)
        pygame.draw.circle(self.screen, self.BLACK, (self.cx + 140, self.cy - 180), 60)

        # деления (оставляем как у настоящих часов)
        for i in range(60):
            angle = math.radians(i * 6 - 90)

            outer = self.radius - 10
            inner = self.radius - (20 if i % 5 == 0 else 15)

            x1 = self.cx + math.cos(angle) * outer
            y1 = self.cy + math.sin(angle) * outer
            x2 = self.cx + math.cos(angle) * inner
            y2 = self.cy + math.sin(angle) * inner

            color = self.BLACK if i % 5 == 0 else self.GRAY
            width = 3 if i % 5 == 0 else 1

            pygame.draw.line(
                self.screen,
                color,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                width
            )

        # ⏱ углы
        hour_angle = self._angle(hours % 12, 12)
        min_angle = self._angle(minutes, 60)
        sec_angle = self._angle(seconds, 60)

        # 🕒 стрелки
        self._draw_hand(hour_angle, 80, self.BLACK, 6)
        self._draw_hand(min_angle, 115, self.BLACK, 4)
        self._draw_hand(sec_angle, 135, self.RED, 2)

        # центр
        pygame.draw.circle(self.screen, self.BLACK, (self.cx, self.cy), 8)

        # 🧾 цифровое время (единственное число снизу)
        font = pygame.font.SysFont("arial", 28, bold=True)
        text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        img = font.render(text, True, self.BLACK)
        rect = img.get_rect(center=(self.cx, self.cy + self.radius + 30))
        self.screen.blit(img, rect)