import geometry
from random import randint
import pygame

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

polygon = geometry.regular_polygon(10, (400, 400), 300, 23)
index = 0
running = True
color = (255, 0, 0)
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.MOUSEWHEEL:
            color = (randint(30, 255), randint(30, 255), randint(30, 255))
            if event.y > 0:
                index = (index + 1) % polygon.verts_num

            else:
                index = (index - 1) % polygon.verts_num

    pygame.draw.polygon(screen, color, polygon.vertices, 4)

    polygon[index] = pygame.mouse.get_pos()

    pygame.display.update()
    clock.tick(60)
