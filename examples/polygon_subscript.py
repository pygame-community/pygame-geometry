import geometry

import pygame

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

polygon = geometry.Polygon([[100, 10], [600, 600], [10, 600]])

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    pygame.draw.polygon(screen, (255, 0, 0), polygon.vertices, 4)

    polygon[0] = pygame.mouse.get_pos()

    pygame.display.update()
    clock.tick(60)
