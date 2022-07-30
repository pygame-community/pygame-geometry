from random import randint, random
from typing import List, Tuple, Union

import pygame

from circle import Circle

pygame.init()


def get_new_circle_surf(circle_obj: Circle,
                        color: Union[str, Tuple[int, int, int]],
                        surface_alpha: int) -> pygame.Surface:
    surf = pygame.surface.Surface(
        (circle_obj.diameter, circle_obj.diameter)
    )
    surf.set_colorkey("black")
    pygame.draw.circle(
        surf,
        color,
        (circle_obj.radius, circle_obj.radius),
        circle_obj.radius)
    surf.set_alpha(surface_alpha)
    return surf


# Constants and font --------------------------
FONT = pygame.font.SysFont("Consolas", 25, True)
FPS = 120
ALPHA_VALUE = 80
SUB_TEXT_ALPHA = 180
SHAPES_NUMBER = 1000
BACKGROUND_COLOR = (66, 65, 112)
WIDTH, HEIGHT = 1422, 800
# --------------------------------------------

# Game variables and fundamentals --------------------------
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
keep = True

shapes: List[Circle] = []
colors: List[Tuple[int, int, int]] = []
colliding_colors: List[Tuple[int, int, int]] = []

feed_active = True
mouse_circle = Circle((0, 0), 50)

# Useful surfaces --------------------------
txt_surf = FONT.render("RIGHT CLICK to toggle | MOUSE WHEEL to select size",
                       True, "white")
sub_text_surf = pygame.surface.Surface((WIDTH, txt_surf.get_height() + 5))
sub_text_surf.set_alpha(SUB_TEXT_ALPHA)
mouse_circle_surf = get_new_circle_surf(mouse_circle, "white", ALPHA_VALUE)
# ------------------------------------------

# Create the random shapes
for _ in range(SHAPES_NUMBER):
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

# Game loop
while keep:
    
    win.fill(BACKGROUND_COLOR)
    clock.tick_busy_loop(FPS)
    
    mouse_circle.move_to_ip(*pygame.mouse.get_pos())
    
    # main update and draw loop, draw every shape and update their size
    for shape, color, coll_color in zip(shapes, colors, colliding_colors):
        
        if feed_active and mouse_circle.collides_with(shape):
            if isinstance(shape, Circle):
                shape.scale_ip(shape.radius + 0.2)
                pygame.draw.circle(win, coll_color, *shape())
            
            elif isinstance(shape, pygame.Rect):
                pygame.draw.rect(win, coll_color, shape)
        else:
            if isinstance(shape, Circle):
                if shape.radius <= 1.5:
                    radius = randint(3, 15)
                    ind = shapes.index(shape)
                    shape.update((randint(radius, WIDTH - radius),
                                  randint(radius, HEIGHT - radius)),
                                 radius)
                shape.scale_ip(shape.radius - 0.25)
                pygame.draw.circle(win, color, *shape())
            elif isinstance(shape, pygame.Rect):
                pygame.draw.rect(win, color, shape)
    
    win.blit(mouse_circle_surf, mouse_circle_surf.get_rect(
        center=(mouse_circle.x, mouse_circle.y)))
    
    # select and draw the mouse_circle border color
    if feed_active:
        pygame.draw.circle(
            win,
            "green",
            (mouse_circle.x, mouse_circle.y),
            mouse_circle.radius,
            2)
    else:
        pygame.draw.circle(
            win,
            "white",
            (mouse_circle.x, mouse_circle.y),
            mouse_circle.radius,
            2)
    
    # event loop
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            keep = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                mouse_circle.scale_by_ip(1.1)
            else:
                mouse_circle.scale_by_ip(0.9)
            mouse_circle_surf = get_new_circle_surf(mouse_circle, "white",
                                                    ALPHA_VALUE)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            feed_active = not feed_active
    
    win.blit(sub_text_surf, (0, 0))
    win.blit(txt_surf,
             txt_surf.get_rect(center=(WIDTH // 2, txt_surf.get_height() // 2)))
    
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.update()

pygame.quit()
