import pygame
from pygame.draw import circle as draw_circle, polygon as draw_polygon
from geometry import regular_polygon, Circle

pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
SHAPE_THICKNESS = 3
FPS = 60
WIDTH, HEIGHT = 800, 800
WIDTH2, HEIGHT2 = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polygon-Circle Collision Visualization")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 25, bold=True)
colliding_text = font.render("Colliding", True, RED)
colliding_textr = colliding_text.get_rect(center=(WIDTH2, 50))
not_colliding_text = font.render("Not colliding", True, WHITE)
not_colliding_textr = not_colliding_text.get_rect(center=(WIDTH2, 50))

modei_text = font.render("Right click to toggle collision mode", True, WHITE)
modei_textr = modei_text.get_rect(center=(WIDTH2, HEIGHT - 50))

mode0_txt = font.render("Current: EDGES ONLY", True, YELLOW)
mode0_txtr = mode0_txt.get_rect(center=(WIDTH2, HEIGHT - 25))

mode1_txt = font.render("Current: FULL", True, YELLOW)
mode1_txtr = mode1_txt.get_rect(center=(WIDTH2, HEIGHT - 25))

circle = Circle((WIDTH2, HEIGHT2), 80)
polygon = regular_polygon(10, (WIDTH2, HEIGHT2), 165)
only_edges = False
running = True

while running:

    circle.center = pygame.mouse.get_pos()

    colliding = circle.collidepolygon(polygon, only_edges)
    # Alternative:
    # colliding = polygon.collidecircle(circle, only_edges)

    color = RED if colliding else WHITE

    screen.fill((0, 0, 0))

    draw_circle(screen, color, circle.center, circle.r, SHAPE_THICKNESS)
    draw_polygon(screen, color, polygon.vertices, SHAPE_THICKNESS)

    screen.blit(
        colliding_text if colliding else not_colliding_text,
        colliding_textr if colliding else not_colliding_textr,
    )

    screen.blit(modei_text, modei_textr)

    screen.blit(
        mode0_txt if only_edges else mode1_txt, mode0_txtr if only_edges else mode1_txtr
    )

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                only_edges = not only_edges

    clock.tick(FPS)

pygame.quit()
