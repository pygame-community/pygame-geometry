from math import radians, sin, cos

import pygame
from pygame.draw import line as draw_line, polygon as draw_polygon
from geometry import Line, regular_polygon


# using this because we're missing line.rotate()
def rotate_line(line, angle):
    angle = radians(angle)

    x = line.x2 - line.x1
    y = line.y2 - line.y1

    x1 = x * cos(angle) - y * sin(angle)
    y1 = x * sin(angle) + y * cos(angle)

    line.b = (x1 + line.x1, y1 + line.y1)


pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
SHAPE_THICKNESS = 3
FPS = 60
WIDTH, HEIGHT = 800, 800
WIDTH2, HEIGHT2 = WIDTH // 2, HEIGHT // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polygon-Line Collision Visualization")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 25, bold=True)
colliding_text = font.render("Colliding", True, RED)
colliding_textr = colliding_text.get_rect(center=(WIDTH2, 50))
not_colliding_text = font.render("Not colliding", True, WHITE)
not_colliding_textr = not_colliding_text.get_rect(center=(WIDTH2, 50))

modei_text = font.render("Right click to toggle collision mode", True, WHITE)
modei_textr = modei_text.get_rect(center=(WIDTH2, HEIGHT - 50))

modei2_text = font.render("Left click to rotate", True, WHITE)
modei2_textr = modei2_text.get_rect(center=(WIDTH2, HEIGHT - 80))

mode0_txt = font.render("Current: EDGES ONLY", True, YELLOW)
mode0_txtr = mode0_txt.get_rect(center=(WIDTH2, HEIGHT - 25))

mode1_txt = font.render("Current: FULL", True, YELLOW)
mode1_txtr = mode1_txt.get_rect(center=(WIDTH2, HEIGHT - 25))

polygon = regular_polygon(6, (WIDTH2, HEIGHT2), 180)
line = Line((0, 0), (135, 135))
only_edges = False
running = True
color = WHITE

rotating = False

while running:
    delta = (clock.tick(FPS) / 1000) * 60

    line.midpoint = pygame.mouse.get_pos()

    colliding = line.collidepolygon(polygon, only_edges)
    # Alternative:
    # colliding = polygon.collideline(line, only_edges)

    if rotating:
        rotate_line(line, 2)

    color = RED if colliding else WHITE

    screen.fill((10, 10, 10))

    draw_polygon(screen, color, polygon.vertices, SHAPE_THICKNESS)
    draw_line(screen, color, line.a, line.b, SHAPE_THICKNESS)

    screen.blit(
        colliding_text if colliding else not_colliding_text,
        colliding_textr if colliding else not_colliding_textr,
    )

    screen.blit(modei2_text, modei2_textr)
    screen.blit(modei_text, modei_textr)

    screen.blit(
        mode0_txt if only_edges else mode1_txt, mode0_txtr if only_edges else mode1_txtr
    )

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rotating = True
            elif event.button == 3:
                only_edges = not only_edges
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rotating = False
pygame.quit()
