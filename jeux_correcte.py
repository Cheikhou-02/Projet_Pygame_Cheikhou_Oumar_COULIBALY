import pygame
import random
import sys

# ----------------------------
# INITIALISATION
# ----------------------------
pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moto Adventure – Weather Edition")
clock = pygame.time.Clock()

# ----------------------------
# COULEURS & METEO
# ----------------------------
WEATHER_STATES = ["day", "night", "rain", "snow", "storm", "fog"]
current_weather_index = 0
current_weather = WEATHER_STATES[current_weather_index]

VOLCANO_GRAY = (120, 120, 120)
VOLCANO_RED = (255, 80, 0)
VOLCANO_SMOKE = (200, 200, 200)

# Zones
GROUND_Y = HEIGHT // 2 + 50
ROAD_HEIGHT = 180
ROAD_TOP = GROUND_Y - 30
ROAD_BOTTOM = ROAD_TOP + ROAD_HEIGHT

PLAYER_MAX_Y = ROAD_BOTTOM - 55
PLAYER_MIN_Y = ROAD_TOP - 10

MOTO_HEIGHT = 35
MOTO_WIDTH = 100

# ----------------------------
# VARIABLES DE JEU
# ----------------------------
player_y = (PLAYER_MIN_Y + PLAYER_MAX_Y) // 2
player_x = 200
velocity = 0
score = 0
OB_SPEED = 4
last_score_check = 0

obstacles = []
animals = []
skeletons = []
bridges = []

volcanos = [[200, GROUND_Y], [900, GROUND_Y], [1500, GROUND_Y]]

SPAWN_RATE = 90
road_offset = 0

# ---------------------------------------------------
# DESSIN MOTO
# ---------------------------------------------------
def draw_moto(x, y):
    w = MOTO_WIDTH
    h = MOTO_HEIGHT

    # Corps de la moto
    pygame.draw.polygon(screen, (255, 165, 0), [
        (x, y + h // 2),
        (x + w - 10, y + h // 2),
        (x + w - 5, y + 5),
        (x + 10, y)
    ])

    pygame.draw.rect(screen, (20, 20, 20), (x + 30, y + 5, w - 40, h // 2), border_radius=5)

    pygame.draw.polygon(screen, (50, 50, 50), [
        (x + 10, y),
        (x + 40, y - 5),
        (x + 70, y - 5),
        (x + 80, y + 5)
    ])

    pygame.draw.circle(screen, (15, 15, 15), (x + 20, y + h), 20)
    pygame.draw.circle(screen, (15, 15, 15), (x + 80, y + h), 20)

    pygame.draw.rect(screen, (255, 255, 150), (x + w - 10, y + 5, 15, 10), border_radius=3)

# ---------------------------------------------------
# OBSTACLES (VOITURES)
# ---------------------------------------------------
def draw_car(rect, color):
    x, y, w, h = rect
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), (x + 10, y + 5, w - 20, 15), border_radius=5)
    pygame.draw.circle(screen, (0, 0, 0), (x + 15, y + h - 5), 10)
    pygame.draw.circle(screen, (0, 0, 0), (x + w - 15, y + h - 5), 10)

# ---------------------------------------------------
# VOLCANS
# ---------------------------------------------------
def draw_volcano(x, y):
    h_volcano = 250
    w_volcano = 500
    peak = x + w_volcano // 2

    pygame.draw.polygon(screen, VOLCANO_GRAY, [(x, y), (peak, y - h_volcano), (x + w_volcano, y)])
    pygame.draw.circle(screen, VOLCANO_RED, (peak, y - h_volcano), 15)

    for _ in range(10):
        pygame.draw.circle(screen, (255, random.randint(80, 160), 0),
            (peak + random.randint(-20, 20), y - h_volcano - random.randint(10, 80)),
            random.randint(5, 15))

    pygame.draw.circle(screen, VOLCANO_SMOKE, (peak + 40, y - h_volcano - 120), 30)
    pygame.draw.circle(screen, VOLCANO_SMOKE, (peak - 30, y - h_volcano - 150), 25)

# ---------------------------------------------------
# ANIMAUX (corrigés)
# ---------------------------------------------------
def draw_animal(x, y):
    pygame.draw.circle(screen, (160, 110, 60), (x, y), 18)
    pygame.draw.circle(screen, (0, 0, 0), (x - 5, y - 5), 4)
    pygame.draw.circle(screen, (0, 0, 0), (x + 5, y - 5), 4)

def draw_skeleton(x, y):
    pygame.draw.circle(screen, (230, 230, 230), (x, y), 15)
    pygame.draw.rect(screen, (230, 230, 230), (x - 8, y, 16, 25))
    pygame.draw.line(screen, (0, 0, 0), (x - 5, y - 3), (x - 1, y + 1), 2)
    pygame.draw.line(screen, (0, 0, 0), (x + 5, y - 3), (x + 1, y + 1), 2)

# ---------------------------------------------------
# PONTS
# ---------------------------------------------------
def draw_bridge():
    pygame.draw.rect(screen, (150, 75, 0), (0, ROAD_TOP + 20, WIDTH, 30))
    for i in range(0, WIDTH, 80):
        pygame.draw.rect(screen, (120, 60, 0), (i, ROAD_TOP + 50, 20, 60))

# ---------------------------------------------------
# METEO
# ---------------------------------------------------
def change_weather():
    global current_weather_index, current_weather
    current_weather_index = (current_weather_index + 1) % len(WEATHER_STATES)
    current_weather = WEATHER_STATES[current_weather_index]

# ---------------------------------------------------
# ENVIRONNEMENT
# ---------------------------------------------------
def draw_environment():
    global road_offset

    # Couleurs selon météo
    if current_weather == "day":
        sky, grass = (135, 206, 235), (160, 255, 160)
    elif current_weather == "night":
        sky, grass = (10, 10, 40), (30, 60, 30)
    elif current_weather == "rain":
        sky, grass = (80, 100, 120), (100, 150, 120)
    elif current_weather == "snow":
        sky, grass = (200, 200, 255), (230, 240, 255)
    elif current_weather == "storm":
        sky, grass = (30, 30, 50), (80, 80, 80)
    else:
        sky, grass = (180, 180, 180), (220, 220, 220)

    screen.fill(sky)
    pygame.draw.rect(screen, grass, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

    # Volcans
    for v in volcanos:
        draw_volcano(v[0], v[1])
        v[0] -= 1

    volcanos[:] = [v for v in volcanos if v[0] > -600]
    if len(volcanos) < 3:
        volcanos.append([WIDTH + random.randint(300, 800), GROUND_Y])

    # Route
    pygame.draw.rect(screen, (60, 60, 60), (0, ROAD_TOP, WIDTH, ROAD_HEIGHT))
    road_offset = (road_offset - OB_SPEED) % 40

    for x in range(-road_offset, WIDTH, 40):
        pygame.draw.rect(screen, (255, 255, 0), (x, ROAD_TOP + ROAD_HEIGHT // 2, 20, 8))

    # Animaux & squelettes
    for a in animals: draw_animal(a[0], a[1])
    for s in skeletons: draw_skeleton(s[0], s[1])

    # Ponts
    for br in bridges:
        if br:
            draw_bridge()

# ---------------------------------------------------
# SPAWN ENVIRONNEMENT (CORRIGÉ)
# ---------------------------------------------------
def spawn_environment():

    # ANIMAUX : UNIQUEMENT SUR TROTTOIR (JAMAIS SUR LA ROUTE)
    if random.random() < 0.004:
        y = random.randint(ROAD_BOTTOM + 10, HEIGHT - 20)
        animals.append([WIDTH, y])

    # SQUELETTES : pareil
    if random.random() < 0.003:
        y = random.randint(ROAD_BOTTOM + 10, HEIGHT - 30)
        skeletons.append([WIDTH, y])

    # Pont
    if random.random() < 0.002:
        bridges.append(True)

# ---------------------------------------------------
# GAME OVER
# ---------------------------------------------------
def game_over(score):
    print("GAME OVER — Score:", score)
    pygame.quit()
    sys.exit()

# ---------------------------------------------------
# BOUCLE PRINCIPALE
# ---------------------------------------------------
def game_loop():
    global player_y, velocity, score, last_score_check

    obstacles.clear()
    animals.clear()
    skeletons.clear()
    bridges.clear()

    player_y = (PLAYER_MIN_Y + PLAYER_MAX_Y) // 2
    score = 0
    velocity = 0
    last_score_check = 0

    running = True
    while running:

        clock.tick(60)

        # INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: velocity -= 0.5
        if keys[pygame.K_DOWN]: velocity += 0.5

        velocity *= 0.94
        player_y += velocity
        player_y = max(PLAYER_MIN_Y, min(player_y, PLAYER_MAX_Y))

        # Changement météo
        if score >= last_score_check + 12:
            change_weather()
            last_score_check += 12

        # Obstacles
        if random.randint(1, SPAWN_RATE) == 1:
            h = random.randint(30, 45)
            w = random.randint(80, 110)
            rect = pygame.Rect(WIDTH, random.randint(ROAD_TOP + 20, ROAD_BOTTOM - h), w, h)
            obstacles.append({"rect": rect, "color": random.choice([(255, 0, 0), (0, 120, 255), (255, 165, 0)])})

        for obs in obstacles:
            obs["rect"].x -= OB_SPEED
            if obs["rect"].x < player_x and "scored" not in obs:
                score += 1
                obs["scored"] = True

        obstacles[:] = [o for o in obstacles if o["rect"].x > -200]

        # Décor
        spawn_environment()
        for a in animals: a[0] -= 1
        for s in skeletons: s[0] -= 1
        for i in range(len(bridges)): bridges[i] = False

        # COLLISIONS
        moto_rect = pygame.Rect(player_x, player_y, MOTO_WIDTH, MOTO_HEIGHT)
        for o in obstacles:
            if moto_rect.colliderect(o["rect"]):
                game_over(score)

        # DESSIN
        draw_environment()

        for o in obstacles:
            draw_car(o["rect"], o["color"])

        draw_moto(player_x, player_y)

        font = pygame.font.SysFont(None, 40)
        screen.blit(font.render(f"Score : {score}", True, (0, 0, 0)), (20, 20))

        pygame.display.update()

# ----------------------------
# START
# ----------------------------
if __name__ == "__main__":
    game_loop()
