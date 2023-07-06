import pygame
from geometry import *
from pygame.draw import circle as draw_circle, line as draw_line

WIDTH, HEIGHT = 800, 600
WIDTH2, HEIGHT2 = WIDTH / 2, HEIGHT / 2
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
keep = True
N = 50
# Create a line
line = Line((WIDTH / 4, HEIGHT2), (3 * WIDTH / 4, HEIGHT2))

while keep:
    screen.fill((30, 30, 30))
    # Draw the line
    # draw_line(screen, (255, 255, 255), line.a, line.b, 2)
    # Draw the points
    for i, segment in enumerate(line.as_segments(N)):
        draw_line(
            screen,
            ((100 + 45 * (i + 1)) % 255, 15 * (i + 1) % 255, (135 * (i + 1)) % 255),
            segment.a,
            segment.b,
            3,
        )
    for point in line.as_points(N - 1):
        draw_circle(screen, (255, 255, 255), point, 1)

    line.b = pygame.mouse.get_pos()

    pygame.display.flip()
    clock.tick(165)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                N += 1
            else:
                if N > 2:
                    N -= 1
