import geometry

import pygame
import random
import math

screen = pygame.display.set_mode((800, 800))
collisions = []


def generate_random_lines(amt):
    def random_pos():
        return random.randrange(0, 800), random.randrange(0, 800)

    for x in range(amt):
        line = geometry.Line(random_pos(), random_pos())
        collisions.append(line)


generate_random_lines(10)

running = True

while running:
    screen.fill((0, 0, 0))

    for x in range(90):
        origin_pos = pygame.mouse.get_pos()
        ray_endpoint = (
            pygame.Vector2(math.sin(math.degrees(x)), math.cos(math.degrees(x))) * 125
            + origin_pos
        )
        ray = geometry.Line(origin_pos, ray_endpoint)

        point = ray.raycast(collisions) or ray_endpoint
        pygame.draw.line(screen, (255, 0, 0), origin_pos, point, 1)

    for line in collisions:
        pygame.draw.line(screen, (0, 0, 255), line.a, line.b, 5)

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            running = False
