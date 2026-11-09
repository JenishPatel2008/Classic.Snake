import pygame
import random
import sys

pygame.init()

CELL_SIZE = 25
GRID_WIDTH = 24
GRID_HEIGHT = 20

WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT + 70

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

BLACK = (15, 18, 22)
DARK = (24, 29, 35)
GREEN = (80, 230, 120)
DARK_GREEN = (45, 170, 85)
RED = (255, 75, 85)
WHITE = (240, 240, 240)
GRAY = (140, 150, 160)
YELLOW = (255, 215, 90)

font = pygame.font.SysFont("consolas", 24, bold=True)
small_font = pygame.font.SysFont("consolas", 17)
large_font = pygame.font.SysFont("consolas", 42, bold=True)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def create_food(snake):
    while True:
        food = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

        if food not in snake:
            return food

def reset_game():
    snake = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
    ]

    return {
        "snake": snake,
        "direction": RIGHT,
        "next_direction": RIGHT,
        "food": create_food(snake),
        "score": 0,
        "speed": 8,
        "game_over": False,
        "paused": False
    }

def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))

    screen.blit(surface, rect)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK, (x, 70), (x, HEIGHT))

    for y in range(70, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK, (0, y), (WIDTH, y))

def draw_snake(snake):
    for index, segment in enumerate(snake):
        x, y = segment

        rect = pygame.Rect(
            x * CELL_SIZE + 2,
            y * CELL_SIZE + 72,
            CELL_SIZE - 4,
            CELL_SIZE - 4
        )

        color = GREEN if index == 0 else DARK_GREEN

        pygame.draw.rect(screen, color, rect, border_radius=6)

        if index == 0:
            if game["direction"] == RIGHT:
                eyes = [(rect.right - 7, rect.top + 6),
                        (rect.right - 7, rect.bottom - 6)]
            elif game["direction"] == LEFT:
                eyes = [(rect.left + 7, rect.top + 6),
                        (rect.left + 7, rect.bottom - 6)]
            elif game["direction"] == UP:
                eyes = [(rect.left + 6, rect.top + 7),
                        (rect.right - 6, rect.top + 7)]
            else:
                eyes = [(rect.left + 6, rect.bottom - 7),
                        (rect.right - 6, rect.bottom - 7)]

            for eye in eyes:
                pygame.draw.circle(screen, WHITE, eye, 4)

def draw_food(food):
    x, y = food

    center = (
        x * CELL_SIZE + CELL_SIZE // 2,
        y * CELL_SIZE + 72 + CELL_SIZE // 2
    )

    pygame.draw.circle(screen, RED, center, CELL_SIZE // 2 - 3)
    pygame.draw.circle(screen, (255, 160, 160),
                       (center[0] - 4, center[1] - 4), 3)

def draw_header():
    pygame.draw.rect(screen, DARK, (0, 0, WIDTH, 70))

    draw_text("SNAKE", large_font, GREEN, 20, 13, False)

    score_text = font.render(f"SCORE: {game['score']}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 15))

    draw_text("ARROW KEYS / WASD  |  SPACE: PAUSE",
              small_font, GRAY, WIDTH // 2, 48)

def draw_overlay(title, subtitle, color=GREEN):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))

    screen.blit(overlay, (0, 0))

    draw_text(title, large_font, color, WIDTH // 2, HEIGHT // 2 - 35)
    draw_text(subtitle, small_font, WHITE, WIDTH // 2, HEIGHT // 2 + 25)

def change_direction(key):
    current = game["direction"]

    if key in (pygame.K_UP, pygame.K_w) and current != DOWN:
        game["next_direction"] = UP

    elif key in (pygame.K_DOWN, pygame.K_s) and current != UP:
        game["next_direction"] = DOWN

    elif key in (pygame.K_LEFT, pygame.K_a) and current != RIGHT:
        game["next_direction"] = LEFT

    elif key in (pygame.K_RIGHT, pygame.K_d) and current != LEFT:
        game["next_direction"] = RIGHT

def update_game():
    if game["game_over"] or game["paused"]:
        return

    game["direction"] = game["next_direction"]

    head_x, head_y = game["snake"][0]
    dx, dy = game["direction"]

    new_head = (head_x + dx, head_y + dy)

    if (
        new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
    ):
        game["game_over"] = True
        return

    eating = new_head == game["food"]

    body = game["snake"] if eating else game["snake"][:-1]

    if new_head in body:
        game["game_over"] = True
        return

    game["snake"].insert(0, new_head)

    if eating:
        game["score"] += 10
        game["food"] = create_food(game["snake"])
        game["speed"] = min(8 + game["score"] // 50, 18)
    else:
        game["snake"].pop()

game = reset_game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                if not game["game_over"]:
                    game["paused"] = not game["paused"]

            elif event.key == pygame.K_r:
                game = reset_game()

            elif not game["game_over"]:
                change_direction(event.key)

    update_game()

    screen.fill(BLACK)

    draw_header()
    draw_grid()
    draw_food(game["food"])
    draw_snake(game["snake"])

    if game["paused"]:
        draw_overlay("PAUSED", "Press SPACE to continue", YELLOW)

    elif game["game_over"]:
        draw_overlay("GAME OVER",
                    f"Score: {game['score']}  |  Press R to restart",
                    RED)

    pygame.display.flip()
    clock.tick(game["speed"])

pygame.quit()
sys.exit()
