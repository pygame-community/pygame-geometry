from shapes import raycast
from shapes.line import LineSegment

import pygame
import math
import random

screen = pygame.display.set_mode((800, 800))
collisions = []

def generate_random_lines(amt):
    def random_pos():
        return (random.randrange(0, 800), random.randrange(0, 800))

    for x in range(amt):
        line = LineSegment(random_pos(), random_pos())
        collisions.append(line)

generate_random_lines(55)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
    
    screen.fill((0, 0, 0))
    
    for x in range(90):
        origin_pos = pygame.mouse.get_pos()
        ray_endpoint = pygame.Vector2(math.sin(math.degrees(x)), math.cos(math.degrees(x))) * 125 + origin_pos
        endpoint = raycast.raycast(origin_pos, ray_endpoint, collisions)
        pygame.draw.line(screen, (255, 0, 0), origin_pos, endpoint, 1)
    
    for c in collisions:
        pygame.draw.line(screen, (0, 0, 255), c.point1, c.point2, 5)

    pygame.display.flip()
