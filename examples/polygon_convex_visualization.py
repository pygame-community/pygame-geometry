from geometry import regular_polygon
import pygame

pygame.init()

SCREEN_W = 800
SCREEN_H = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Polygon Convex Visualization")
clock = pygame.time.Clock()
keep = True

GREEN = (0, 150, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BACKGROUND = (10, 10, 10)
current_color = GREEN

polygon = regular_polygon(5, (SCREEN_W / 2, SCREEN_H / 2), 200)
index = 0
is_convex = True

# setup text
font = pygame.font.SysFont("Arial", 25, bold=True)

is_convex_text = font.render("Convex polygon", True, WHITE)
is_convex_text_r = is_convex_text.get_rect(center=(SCREEN_W / 2, 50))
is_not_convex_text = font.render("Concave polygon", True, WHITE)
is_not_convex_text_r = is_not_convex_text.get_rect(center=(SCREEN_W / 2, 50))
scroll_text = font.render("Scroll wheel to select vertex", True, WHITE)
scroll_text_r = scroll_text.get_rect(center=(SCREEN_W / 2, SCREEN_H - 50))

while keep:

    screen.fill(BACKGROUND)

    polygon[index] = pygame.mouse.get_pos()

    is_convex = polygon.is_convex()

    if is_convex:
        current_color = GREEN
    else:
        current_color = RED

    pygame.draw.polygon(screen, current_color, polygon.vertices)

    for vertex in polygon.vertices:
        pygame.draw.circle(screen, WHITE, vertex, 5, 3)

    pygame.draw.circle(screen, YELLOW, polygon[index], 15, 3)

    if is_convex:
        screen.blit(is_convex_text, is_convex_text_r)
    else:
        screen.blit(is_not_convex_text, is_not_convex_text_r)

    screen.blit(scroll_text, scroll_text_r)

    pygame.display.flip()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                index = (index + 1) % polygon.verts_num
            else:
                index = (index - 1) % polygon.verts_num
            pygame.mouse.set_pos(polygon[index])

pygame.quit()