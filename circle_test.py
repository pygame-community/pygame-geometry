from random import randint, random
from typing import List, Tuple

import pygame

from circle import Circle


def get_new_circle_surf(circle_obj: Circle) -> pygame.Surface:
    surf = pygame.surface.Surface(
        (circle_obj.diameter, circle_obj.diameter)
    )
    surf.set_colorkey("black")
    pygame.draw.circle(
        surf,
        "white",
        (circle_obj.radius, circle_obj.radius),
        circle_obj.radius)
    surf.set_alpha(ALPHA_VALUE)
    return surf


pygame.init()

ALPHA_VALUE = 100
CIRCLES_NUMBER = 1000
BACKGROUND_COLOR = (66, 65, 112)
WIDTH, HEIGHT = 650, 650
win = pygame.display.set_mode((WIDTH, HEIGHT))

shapes: List[Circle] = []
colors: List[Tuple[int, int, int]] = []
colliding_colors: List[Tuple[int, int, int]] = []

clock = pygame.time.Clock()
keep = True

for _ in range(CIRCLES_NUMBER):
    shade = randint(20, 130)
    colors.append((shade, shade, shade))
    colliding_colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    obj = None
    if random() * 10 > 5:
        radius = randint(3, 15)
        obj = Circle((randint(radius, WIDTH - radius),
                      randint(radius, HEIGHT - radius)), radius)
    else:
        dimx = randint(5, 25)
        dimy = randint(5, 25)
        obj = pygame.Rect((randint(0, WIDTH - dimx), randint(0, HEIGHT - dimy)),
                          (dimx, dimy))
    
    shapes.append(obj)

mouse_circle = Circle((0, 0), 50)
mouse_circle_surf = get_new_circle_surf(mouse_circle)

mouse = None
while keep:
    
    win.fill(BACKGROUND_COLOR)
    clock.tick_busy_loop(120)
    
    mouse_circle.move_to_ip(*pygame.mouse.get_pos())
    
    for shape, color, coll_color in zip(shapes, colors, colliding_colors):
        if isinstance(shape, Circle):
            if mouse_circle.collidecircle(shape):
                pygame.draw.circle(win, coll_color, *shape())
            else:
                pygame.draw.circle(win, color, *shape())
        elif isinstance(shape, pygame.Rect):
            if mouse_circle.colliderect(shape):
                pygame.draw.rect(win, coll_color, shape)
            else:
                pygame.draw.rect(win, color, shape)
    
    win.blit(mouse_circle_surf, mouse_circle_surf.get_rect(
        center=(mouse_circle.x, mouse_circle.y)))
    
    for pgevent in pygame.event.get():
        if pgevent.type == pygame.QUIT:
            keep = False
        if pgevent.type == pygame.MOUSEWHEEL:
            if pgevent.y > 0:
                mouse_circle.scale_ip(mouse_circle.radius + 10)
            else:
                mouse_circle.scale_ip(mouse_circle.radius - 10)
            mouse_circle_surf = get_new_circle_surf(mouse_circle)
    
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.update()

pygame.quit()
