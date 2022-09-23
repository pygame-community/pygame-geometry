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

    pygame.draw.polygon(screen, (0, 0, 150), polygon.vertices, 4)

    mx, my = pygame.mouse.get_pos()
    polygon[0] = (mx, my)

    pygame.display.update()
    clock.tick(60)
