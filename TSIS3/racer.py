import pygame, random, time, math
from persistence import save_score

LANES = [200, 300, 400, 500]

# ── Colour palette ───────────────────────────────────────────────────────────
C_BG        = (8, 6, 18)
C_ROAD      = (14, 12, 28)
C_LANE_MARK = (40, 38, 70)
C_DASH      = (60, 200, 255)
C_DASH_DIM  = (20, 60, 90)
C_PLAYER    = (30, 180, 255)
C_PLAYER_H  = (120, 230, 255)
C_ENEMY     = (255, 60, 80)
C_ENEMY_H   = (255, 120, 100)
C_OBSTACLE  = (255, 30, 60)
C_GLOW_P    = (0, 140, 220, 80)
C_GLOW_E    = (220, 0, 40, 60)
C_COIN      = (255, 210, 0)
C_COIN_GLOW = (255, 180, 0, 70)
C_NITRO     = (255, 200, 0)
C_SHIELD    = (80, 255, 180)
C_REPAIR    = (180, 100, 255)
C_WHITE     = (230, 235, 255)
C_YELLOW    = (255, 220, 60)

ROAD_LEFT  = 170
ROAD_RIGHT = 570
ROAD_W     = ROAD_RIGHT - ROAD_LEFT

MAX_OBSTACLES = 3
MAX_TRAFFIC   = 3
MIN_GAP       = 130   # min vertical gap between any two road objects
COIN_VALUE    = 10


def _surf(w, h, alpha=True):
    return pygame.Surface((w, h), pygame.SRCALPHA if alpha else 0)


# ── Drawing helpers ──────────────────────────────────────────────────────────

def draw_glow(surf, rect, color, radius=22):
    cx, cy = rect.centerx, rect.centery
    for r in range(radius, 0, -4):
        a = int(color[3] * (r / radius) ** 1.4) if len(color) == 4 else 60
        glow = _surf(r * 2 + 4, r * 2 + 4)
        pygame.draw.ellipse(glow, (*color[:3], a), (0, 0, r * 2 + 4, r * 2 + 4))
        surf.blit(glow, (cx - r - 2, cy - r - 2), special_flags=pygame.BLEND_RGBA_ADD)


def draw_player_car(surf, rect, shield=False):
    x, y, w, h = rect
    pygame.draw.rect(surf, C_PLAYER, (x, y + 10, w, h - 10), border_radius=9)
    pygame.draw.polygon(surf, C_PLAYER_H, [
        (x + 8, y + 10), (x + w - 8, y + 10),
        (x + w - 12, y + h // 2 - 5), (x + 12, y + h // 2 - 5)])
    pygame.draw.polygon(surf, C_DASH_DIM, [
        (x + 10, y + 13), (x + w - 10, y + 13),
        (x + w - 14, y + h // 2 - 7), (x + 14, y + h // 2 - 7)])
    hl = _surf(12, 6)
    hl.fill((255, 255, 180, 220))
    surf.blit(hl, (x + 3, y + h - 14), special_flags=pygame.BLEND_RGBA_ADD)
    surf.blit(hl, (x + w - 15, y + h - 14), special_flags=pygame.BLEND_RGBA_ADD)
    for tx in (x + 3, x + w - 13):
        pygame.draw.rect(surf, (255, 80, 40), (tx, y + 12, 10, 5), border_radius=2)
    for wx, wy in [(x-5, y+15), (x+w-5, y+15), (x-5, y+h-25), (x+w-5, y+h-25)]:
        pygame.draw.rect(surf, (20, 20, 40), (wx, wy, 10, 18), border_radius=3)
        pygame.draw.rect(surf, (60, 60, 90), (wx+2, wy+2, 6, 14), border_radius=2)
    if shield:
        s = _surf(w + 30, h + 30)
        pygame.draw.ellipse(s, (80, 255, 180, 55), (0, 0, w + 30, h + 30))
        pygame.draw.ellipse(s, (80, 255, 180, 120), (0, 0, w + 30, h + 30), 2)
        surf.blit(s, (x - 15, y - 15), special_flags=pygame.BLEND_RGBA_ADD)


def draw_enemy_car(surf, rect):
    x, y, w, h = rect
    pygame.draw.rect(surf, C_ENEMY, (x, y, w, h - 8), border_radius=9)
    pygame.draw.polygon(surf, C_ENEMY_H, [
        (x+8, y+h//2), (x+w-8, y+h//2),
        (x+w-12, y+h//2+20), (x+12, y+h//2+20)])
    for tx in (x+4, x+w-14):
        pygame.draw.rect(surf, (255, 220, 60), (tx, y+3, 10, 5), border_radius=2)
    for wx, wy in [(x-5, y+10), (x+w-5, y+10), (x-5, y+h-20), (x+w-5, y+h-20)]:
        pygame.draw.rect(surf, (20, 20, 40), (wx, wy, 10, 16), border_radius=3)


def draw_obstacle(surf, rect):
    x, y, w, h = rect
    pygame.draw.rect(surf, (200, 20, 30), (x, y, w, h), border_radius=5)
    for i in range(3):
        pygame.draw.rect(surf, (255, 200, 0), (x, y + i*(h//3), w, h//6))
    pygame.draw.rect(surf, (255, 80, 80), (x, y, w, h), 2, border_radius=5)


def draw_coin(surf, cx, cy, radius, spawn_time):
    t = time.time() - spawn_time
    squish = abs(math.sin(t * 4))
    rw = max(3, int(radius * squish))
    rh = radius
    # glow
    gs = _surf(rw * 4 + 20, rh * 2 + 20)
    pygame.draw.ellipse(gs, (*C_COIN_GLOW[:3], 60), (0, 0, rw*4+20, rh*2+20))
    surf.blit(gs, (cx - rw*2 - 10, cy - rh - 10), special_flags=pygame.BLEND_RGBA_ADD)
    # body
    cs = _surf(rw*2 + 2, rh*2 + 2)
    pygame.draw.ellipse(cs, C_COIN, (0, 0, rw*2+2, rh*2+2))
    shine_w = max(1, rw // 2)
    pygame.draw.ellipse(cs, (255, 240, 160), (rw - shine_w, 2, shine_w, rh))
    pygame.draw.ellipse(cs, (200, 150, 0), (0, 0, rw*2+2, rh*2+2), 2)
    surf.blit(cs, (cx - rw - 1, cy - rh - 1))


def draw_powerup(surf, rect, kind, now):
    x, y, w, h = rect
    pulse = 0.7 + 0.3 * abs((now % 1.0) - 0.5) * 2
    c = {"nitro": C_NITRO, "shield": C_SHIELD, "repair": C_REPAIR}.get(kind, C_WHITE)
    rs = _surf(w+20, h+20)
    pygame.draw.ellipse(rs, (*c, int(80*pulse)), (0, 0, w+20, h+20))
    surf.blit(rs, (x-10, y-10), special_flags=pygame.BLEND_RGBA_ADD)
    pygame.draw.rect(surf, c, (x, y, w, h), border_radius=10)
    pygame.draw.rect(surf, C_WHITE, (x, y, w, h), 2, border_radius=10)
    font = pygame.font.SysFont("consolas", 18, bold=True)
    txt = font.render({"nitro":"N","shield":"S","repair":"R"}.get(kind,"?"), True, C_BG)
    surf.blit(txt, txt.get_rect(center=(x+w//2, y+h//2)))


# ── Road renderer ────────────────────────────────────────────────────────────

class RoadRenderer:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.offset = 0

    def draw(self, surf, speed):
        self.offset = (self.offset + speed) % 60
        for row in range(self.h):
            t = row / self.h
            pygame.draw.line(surf,
                (int(8+10*t), int(6+8*t), int(18+20*t)), (0, row), (self.w, row))
        pygame.draw.rect(surf, C_ROAD, (ROAD_LEFT, 0, ROAD_W, self.h))
        for i in range(0, self.h, 8):
            a = 15 + 8*(i % 2)
            pygame.draw.line(surf, (a, a-2, a+10), (ROAD_LEFT, i), (ROAD_RIGHT, i))
        for ex in (ROAD_LEFT-2, ROAD_RIGHT):
            pygame.draw.rect(surf, C_DASH, (ex, 0, 3, self.h))
            ge = _surf(20, self.h)
            ge.fill((*C_DASH, 30))
            surf.blit(ge, (ex-8, 0), special_flags=pygame.BLEND_RGBA_ADD)
        for lx in (300, 400):
            y0 = -self.offset
            while y0 < self.h:
                pygame.draw.rect(surf, C_LANE_MARK, (lx-1, y0, 3, 30), border_radius=1)
                y0 += 60
        if speed > 6:
            for _ in range(int(speed * 0.6)):
                sx = random.choice([ROAD_LEFT-random.randint(10,60),
                                    ROAD_RIGHT+random.randint(10,60)])
                streak = _surf(3, random.randint(20, 60))
                streak.fill((180, 200, 255, random.randint(40, 100)))
                surf.blit(streak, (sx, random.randint(0, self.h)),
                          special_flags=pygame.BLEND_RGBA_ADD)


# ── HUD ──────────────────────────────────────────────────────────────────────

class HUD:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.font_lg = pygame.font.SysFont("consolas", 26, bold=True)
        self.font_sm = pygame.font.SysFont("consolas", 18)
        self.font_pw = pygame.font.SysFont("consolas", 20, bold=True)
        self.popups  = []   # [x, y, text, life]

    def add_popup(self, text, x, y):
        self.popups.append([x, y, text, 1.0])

    def draw(self, surf, score, level, coins, active_power):
        bar = _surf(self.w, 65)
        bar.fill((8, 6, 20, 210))
        surf.blit(bar, (0, 0))
        pygame.draw.line(surf, C_DASH, (0, 65), (self.w, 65), 1)

        surf.blit(self.font_sm.render("SCORE", True, C_DASH_DIM), (16, 8))
        surf.blit(self.font_lg.render(f"{score:06d}", True, C_WHITE), (16, 28))

        surf.blit(self.font_sm.render("COINS", True, C_DASH_DIM),
                  (self.w//2 - 36, 8))
        surf.blit(self.font_lg.render(str(coins), True, C_COIN),
                  (self.w//2 - 16, 28))

        surf.blit(self.font_sm.render("LVL", True, C_DASH_DIM), (self.w-80, 8))
        surf.blit(self.font_lg.render(str(level), True, C_YELLOW), (self.w-72, 28))

        if active_power:
            c = {"nitro": C_NITRO, "shield": C_SHIELD, "repair": C_REPAIR}.get(
                active_power, C_WHITE)
            ps = _surf(180, 32)
            ps.fill((*c, 30))
            pygame.draw.rect(ps, c, (0, 0, 180, 32), 1, border_radius=6)
            surf.blit(ps, (self.w//2 - 90, self.h - 48))
            pt = self.font_pw.render(f"◆ {active_power.upper()}", True, c)
            surf.blit(pt, pt.get_rect(center=(self.w//2, self.h-32)))

        alive = []
        for pp in self.popups:
            px, py, txt, life = pp
            if life > 0:
                s = self.font_pw.render(txt, True, (*C_COIN, int(life*255)))
                surf.blit(s, (px - s.get_width()//2, int(py)))
                pp[1] -= 1.5
                pp[3] -= 0.04
                alive.append(pp)
        self.popups = alive


# ── Spawn helper ─────────────────────────────────────────────────────────────

def _safe_spawn(lane, size, all_rects):
    rect = pygame.Rect(lane, -size[1] - 10, *size)
    for other in all_rects:
        if (abs(rect.centery - other.centery) < MIN_GAP and
                abs(rect.centerx - other.centerx) < 80):
            return None
    return rect


# ── Main Game ────────────────────────────────────────────────────────────────

class RacerGame:
    def __init__(self, screen, settings):
        self.screen   = screen
        self.settings = settings
        self.clock    = pygame.time.Clock()
        self.W        = screen.get_width()
        self.H        = screen.get_height()
        self.road     = RoadRenderer(self.W, self.H)
        self.hud      = HUD(self.W, self.H)

    def reset(self):
        self.player      = pygame.Rect(350, 500, 50, 80)
        self.speed       = 5
        self.distance    = 0
        self.score       = 0
        self.coins       = 0
        self.level       = 1
        self.obstacles   = []
        self.traffic     = []
        self.coin_objs   = []   # [cx, cy, radius, spawn_time]
        self.powerups    = []   # (Rect, kind, spawn_time)
        self.active_power = None
        self.power_timer  = 0
        self.particles    = []
        self._t_obstacle  = 0.0
        self._t_traffic   = 0.0
        self._t_coin      = 0.0

    # ── particles ────────────────────────────────────────────────────────────

    def _particles(self, rect, color, n=8):
        cx, cy = rect.centerx, rect.centery
        for _ in range(n):
            self.particles.append(
                [cx, cy, random.uniform(-3, 3), random.uniform(-5, 1), 1.0, color])

    def _exhaust(self):
        cx, cy = self.player.centerx, self.player.bottom
        for _ in range(2):
            c = random.choice([(60,200,255),(100,160,255),(200,230,255)])
            self.particles.append([cx, cy, random.uniform(-1,1), random.uniform(1,3), 0.5, c])

    def _tick_particles(self):
        alive = []
        for p in self.particles:
            p[0]+=p[2]; p[1]+=p[3]; p[4]-=0.04
            if p[4]>0: alive.append(p)
        self.particles = alive

    def _draw_particles(self):
        for p in self.particles:
            a = int(p[4]*255)
            r = max(1, int(p[4]*5))
            s = _surf(r*2+2, r*2+2)
            pygame.draw.circle(s, (*p[5], a), (r+1, r+1), r)
            self.screen.blit(s, (int(p[0])-r-1, int(p[1])-r-1),
                             special_flags=pygame.BLEND_RGBA_ADD)

    # ── spawn logic ──────────────────────────────────────────────────────────

    def _all_rects(self):
        return self.obstacles + self.traffic

    def _try_obstacle(self, now):
        cooldown = max(1.4 - self.level * 0.06, 0.55)
        if now - self._t_obstacle < cooldown: return
        if len(self.obstacles) >= MAX_OBSTACLES: return
        r = _safe_spawn(random.choice(LANES), (50, 50), self._all_rects())
        if r:
            self.obstacles.append(r)
            self._t_obstacle = now

    def _try_traffic(self, now):
        cooldown = max(1.8 - self.level * 0.06, 0.7)
        if now - self._t_traffic < cooldown: return
        if len(self.traffic) >= MAX_TRAFFIC: return
        r = _safe_spawn(random.choice(LANES), (50, 80), self._all_rects())
        if r:
            self.traffic.append(r)
            self._t_traffic = now

    def _try_coin(self, now):
        cooldown = max(0.55 - self.level * 0.01, 0.28)
        if now - self._t_coin < cooldown: return
        if random.random() > 0.6: return
        lane = random.choice(LANES)
        cr = pygame.Rect(lane, -30, 24, 24)
        for r in self._all_rects():
            if abs(cr.centery - r.centery) < MIN_GAP and abs(cr.centerx - r.centerx) < 80:
                return
        self.coin_objs.append([lane + 25, -20, 12, now])
        self._t_coin = now

    def _try_powerup(self):
        if random.random() < 0.004:
            r = _safe_spawn(random.choice(LANES), (40, 40), self._all_rects())
            if r:
                self.powerups.append((r, random.choice(["nitro","shield","repair"]), time.time()))

    # ── power ────────────────────────────────────────────────────────────────

    def _apply_power(self, kind):
        self.active_power = kind
        self.power_timer  = time.time()
        c = {"nitro":C_NITRO,"shield":C_SHIELD,"repair":C_REPAIR}.get(kind, C_WHITE)
        self._particles(self.player, c, 16)
        if kind == "nitro":
            self.speed = 10
        elif kind == "repair" and self.obstacles:
            self.obstacles.pop()

    def _update_power(self):
        if self.active_power == "nitro" and time.time() - self.power_timer > 4:
            self.speed = 5
            self.active_power = None

    # ── main loop ────────────────────────────────────────────────────────────

    def run(self, name):
        self.reset()

        while True:
            self.clock.tick(60)
            now = time.time()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return None

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:  self.player.x -= 6
            if keys[pygame.K_RIGHT]: self.player.x += 6
            self.player.x = max(ROAD_LEFT+2, min(self.player.x, ROAD_RIGHT-self.player.w-2))

            self.level = int(self.distance // 150 + 1)

            self._try_obstacle(now)
            self._try_traffic(now)
            self._try_coin(now)
            self._try_powerup()

            # obstacles
            for obj in self.obstacles[:]:
                obj.y += self.speed
                if obj.y > self.H:
                    self.obstacles.remove(obj)
                elif self.player.colliderect(obj):
                    self._particles(obj, C_OBSTACLE, 20)
                    return self.finish(name)

            # traffic
            for car in self.traffic[:]:
                car.y += self.speed
                if car.y > self.H:
                    self.traffic.remove(car)
                elif self.player.colliderect(car):
                    if self.active_power == "shield":
                        self._particles(car, C_SHIELD, 14)
                        self.active_power = None
                    else:
                        self._particles(car, C_ENEMY, 20)
                        return self.finish(name)

            # coins
            for coin in self.coin_objs[:]:
                coin[1] += self.speed
                cx, cy, cr = int(coin[0]), int(coin[1]), coin[2]
                hrect = pygame.Rect(cx-cr, cy-cr, cr*2, cr*2)
                if self.player.colliderect(hrect):
                    self.coins += 1
                    self.score += COIN_VALUE
                    self.hud.add_popup(f"+{COIN_VALUE}", cx, cy)
                    self._particles(hrect, C_COIN, 10)
                    self.coin_objs.remove(coin)
                elif cy > self.H + 40:
                    self.coin_objs.remove(coin)

            # powerups
            for pu in self.powerups[:]:
                rect, kind, st = pu
                rect.y += self.speed
                if self.player.colliderect(rect):
                    self._apply_power(kind)
                    self.powerups.remove(pu)
                elif rect.y > self.H or now - st > 8:
                    self.powerups.remove(pu)

            self._update_power()
            self._exhaust()
            self._tick_particles()

            self.distance += self.speed / 10
            self.score = int(self.distance) + self.coins * COIN_VALUE

            # draw
            self.road.draw(self.screen, self.speed)

            for o in self.obstacles:
                draw_glow(self.screen, o, C_GLOW_E)
                draw_obstacle(self.screen, o)

            for c in self.traffic:
                draw_glow(self.screen, c, C_GLOW_E)
                draw_enemy_car(self.screen, c)

            for coin in self.coin_objs:
                draw_coin(self.screen, int(coin[0]), int(coin[1]), coin[2], coin[3])

            for pu in self.powerups:
                draw_powerup(self.screen, pu[0], pu[1], now)

            draw_glow(self.screen, self.player, C_GLOW_P, 30)
            draw_player_car(self.screen, self.player,
                            shield=(self.active_power == "shield"))

            self._draw_particles()
            self.hud.draw(self.screen, self.score, self.level,
                          self.coins, self.active_power)

            pygame.display.flip()

    def finish(self, name):
        save_score(name, self.score, int(self.distance))
        return {"score": self.score, "coins": self.coins}