from geometry import regular_polygon
import pygame
from pygame.draw import polygon as draw_polygon

pygame.init()

SCREEN_W, SCREEN_H = 800, 600
SCREEN_W2, SCREEN_H2 = SCREEN_W // 2, SCREEN_H // 2
FPS = 60

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Polygon Scaling Visualization")
clock = pygame.time.Clock()
keep = True

GREEN = (0, 150, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
BACKGROUND = (10, 10, 10)
current_color = GREEN

polygons = [
    regular_polygon(3, (SCREEN_W2, SCREEN_H2 + 25), 100),
    regular_polygon(4, (SCREEN_W2, SCREEN_H2 + 25), 50),
    regular_polygon(5, (SCREEN_W2, SCREEN_H2 + 25), 25),
    regular_polygon(6, (SCREEN_W2, SCREEN_H2 + 25), 15, 45),
    regular_polygon(7, (SCREEN_W2, SCREEN_H2 + 25), 10, 90),
    regular_polygon(8, (SCREEN_W2, SCREEN_H2 + 25), 5, 135),
]

SCALING_DEC = 0.002
SCALING_BOOST = 0.03
ROTATION_SPEED = 0.8
scaling_factor = 1

font = pygame.font.SysFont("Arial", 20, True)

wheel_text = font.render("MOUSE WHEEL to scale", True, WHITE)
wheel_text_r = wheel_text.get_rect(center=(SCREEN_W2, 50))
scaling_up_text = font.render("Scaling up", True, GREEN)
scaling_up_text_r = scaling_up_text.get_rect(center=(SCREEN_W2, 100))
scaling_down_text = font.render("Scaling down", True, RED)
scaling_down_text_r = scaling_down_text.get_rect(center=(SCREEN_W2, 100))

while keep:
    for i, poly in enumerate(polygons, start=1):
        poly.rotate_ip(i * ROTATION_SPEED / len(polygons))

    if scaling_factor != 1:
        if scaling_factor < 1:
            scaling_factor += SCALING_DEC
        else:
            scaling_factor -= SCALING_DEC
        current_color = GREEN if scaling_factor > 1 else RED
        for poly in polygons:
            poly.scale_ip(scaling_factor)
    else:
        current_color = GRAY

    screen.fill(BACKGROUND)
    for poly in polygons:
        draw_polygon(screen, current_color, poly.vertices, 2)

    screen.blit(wheel_text, wheel_text_r)

    if scaling_factor != 1:
        if scaling_factor > 1:
            screen.blit(scaling_up_text, scaling_up_text_r)
        else:
            screen.blit(scaling_down_text, scaling_down_text_r)

    pygame.display.flip()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                scaling_factor += SCALING_BOOST
            else:
                scaling_factor -= SCALING_BOOST

pygame.quit()
