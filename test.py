import pygame
import geometry
pygame.init()

dis = pygame.display.set_mode((600, 600))
line = geometry.Line((0, 0), (1, 0))
while True:
     dis.fill((0, 0, 0))
     keys = pygame.key.get_pressed()
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               quit()

          if event.type == pygame.KEYDOWN:
               line = line.scale(2.0)
     print(line.length)
     pygame.draw.line(dis, (255, 0, 0), line.a, line.b)
     pygame.display.update()