import pygame
from pygame.draw import circle as draw_circle, rect as draw_rect, line as draw_line
from geometry import Circle, Line
from random import randint

pygame.init()

# Constants
# -----------------------------------
FPS = 60
BACKGROUND_COLOR = (20, 20, 20)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
SCREEN_W, SCREEN_H = 840, 640
SCREEN_W_HALF, SCREEN_H_HALF = SCREEN_W // 2, SCREEN_H // 2
# -----------------------------------

# Game variables and fundamentals
# -----------------------------------
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Circle Collision Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22, bold=True)

text1 = font.render("R to randomize shapes", True, WHITE)
text1_r = text1.get_rect(center=(SCREEN_W // 4, 15))
text2 = font.render("MOUSE WHEEL to select size", True, WHITE)
text2_r = text2.get_rect(center=(3 * SCREEN_W // 4, 15))

keep = True
acc_amt = 0
acc_multiplier = 0.92

m_circle = Circle(0, 0, 50)

rects = []
lines = []
circles = []
points = []


def populate_rects(number):
    # in bottomleft quadrant
    for _ in range(number):
        dim_x = randint(15, 50)
        dim_y = randint(15, 50)
        x = randint(0, SCREEN_W_HALF - dim_x)
        y = randint(SCREEN_H_HALF, SCREEN_H - dim_y)
        rects.append(pygame.Rect(x, y, dim_x, dim_y))


def populate_lines(number):
    # in topleft quadrant
    for _ in range(number):
        x1 = randint(0, SCREEN_W_HALF - 1)
        y1 = randint(31, SCREEN_H_HALF - 1)
        x2 = randint(0, SCREEN_W_HALF - 1)
        y2 = randint(31, SCREEN_H_HALF - 1)
        lines.append(Line(x1, y1, x2, y2))


def populate_circles(number):
    # in bottomright quadrant
    for _ in range(number):
        radius = randint(10, 50)
        x = randint(radius + SCREEN_W_HALF, SCREEN_W - radius)
        y = randint(radius + SCREEN_H_HALF, SCREEN_H - radius)
        circles.append(Circle(x, y, radius))


def populate_points(number):
    # in topright quadrant
    for _ in range(number):
        x = randint(SCREEN_W_HALF + 15, SCREEN_W - 15)
        y = randint(31, SCREEN_H_HALF - 15)
        points.append((x, y))


def green_gray(colliding):
    return GREEN if colliding else GRAY


populate_rects(15)
populate_lines(15)
populate_circles(15)
populate_points(15)

# Game loop
while keep:
    # Update
    m_circle.center = pygame.mouse.get_pos()
    if abs(acc_amt) < 0.001:
        acc_amt = 0
    else:
        acc_amt *= acc_multiplier
        m_circle.r *= 1 + acc_amt

    # Draw
    screen.fill(BACKGROUND_COLOR)

    coll = 0

    for rect in rects:
        colliding = m_circle.colliderect(rect)
        coll |= colliding
        draw_rect(screen, green_gray(colliding), rect, 2)

    for line in lines:
        colliding = m_circle.collideline(line)
        coll |= colliding
        draw_line(screen, green_gray(colliding), line.a, line.b, 2)

    for circle in circles:
        colliding = m_circle.collidecircle(circle)
        coll |= colliding
        draw_circle(screen, green_gray(colliding), circle.center, circle.r, 2)

    for point in points:
        colliding = m_circle.collidepoint(point)
        coll |= colliding
        draw_circle(screen, green_gray(colliding), point, 3)

    draw_line(screen, WHITE, (SCREEN_W_HALF, 0), (SCREEN_W_HALF, SCREEN_H), 2)
    draw_line(screen, WHITE, (0, SCREEN_H_HALF), (SCREEN_W, SCREEN_H_HALF), 2)

    draw_circle(screen, BLACK, (m_circle.x + 2, m_circle.y + 2), m_circle.r, 3)
    draw_circle(screen, GREEN if coll else RED, m_circle.center, m_circle.r, 2)

    draw_rect(screen, BLACK, (0, 0, SCREEN_W, 30))

    screen.blit(text1, text1_r)
    screen.blit(text2, text2_r)

    pygame.display.update()

    clock.tick_busy_loop(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                acc_amt += 0.012
            else:
                if m_circle.r < 5:
                    continue
                acc_amt -= 0.014
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rects, lines, circles, points = [], [], [], []
                populate_rects(15)
                populate_lines(15)
                populate_circles(15)
                populate_points(15)

pygame.quit()
