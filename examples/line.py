import geometry
import pygame
display = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
line = geometry.Line(300, 400, 400, 300)
while running:
    display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    pygame.draw.line(display, (0, 100, 0), line.a, line.b)
    pygame.display.update()