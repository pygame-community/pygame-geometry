import geometry

import pygame
import random
import math

screen = pygame.display.set_mode((800, 800))

collisions_lines = []
collisions_circles = []
collisions_rects = []


def generate_random_lines(amt):
    def random_pos():
        return random.randrange(0, 800), random.randrange(0, 800)

    for x in range(amt):
        line = geometry.Line(random_pos(), random_pos())
        collisions_lines.append(line)


def generate_random_circles(amt):
    def random_pos(rad):
        return random.randrange(rad, 800 - rad), random.randrange(rad, 800 - rad)

    for x in range(amt):
        radius = random.randrange(5, 50)
        circle = geometry.Circle(*random_pos(radius), radius)
        collisions_circles.append(circle)


def generate_random_rect(amt):
    def random_pos(width, height):
        return random.randrange(0, 800 - width), random.randrange(0, 800 - height)

    for x in range(amt):
        width = random.randrange(5, 50)
        height = random.randrange(5, 50)
        rect = pygame.Rect(random_pos(width, height), (width, height))
        collisions_rects.append(rect)


generate_random_lines(15)
generate_random_circles(15)
generate_random_rect(15)

colliders = collisions_lines + collisions_circles + collisions_rects

running = True

ray_count = 360

directions = [
    (math.cos(x / ray_count * 360), math.sin(x / ray_count * 360))
    for x in range(ray_count)
]

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
            raise SystemExit

    screen.fill((0, 0, 0))

    for x in range(ray_count):
        origin_pos = pygame.mouse.get_pos()

        direction = directions[x]

        point = geometry.raycast(
            origin_pos,
            (origin_pos[0] + direction[0], origin_pos[1] + direction[1]),
            -1,
            colliders,
        )
        if point:
            pygame.draw.line(screen, (255, 0, 0), origin_pos, point, 1)

    line_width = 3

    for line in collisions_lines:
        pygame.draw.line(screen, (0, 0, 255), line.a, line.b, line_width)

    for circle in collisions_circles:
        pygame.draw.circle(
            screen, (0, 0, 255), (circle.x, circle.y), circle.r, line_width
        )

    for rect in collisions_rects:
        pygame.draw.rect(screen, (0, 0, 255), rect, line_width)

    pygame.display.flip()
