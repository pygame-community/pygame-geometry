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


def rand_color(minv: int = 0, maxv: int = 255) -> Tuple[int, int, int]:
    """returns a random RGB color with min and max as min and max threshold"""
    return randint(minv, maxv), randint(minv, maxv), randint(minv, maxv)


def rand_bw_color(minv: int, maxv: int) -> Tuple[int, int, int]:
    """returns a random BW color"""
    shade = randint(minv, maxv)
    return shade, shade, shade


# Constants and font --------------------------
FONT = pygame.font.SysFont("Consolas", 25, True)
FPS = 120
ALPHA_VALUE = 80
SUB_TEXT_ALPHA = 180
SHAPES_NUMBER = 1000
MIN_CIRCLE_RADIUS = 3
MAX_CIRCLE_RADIUS = 15
MIN_RECT_WIDTH = 5
MAX_RECT_WIDTH = 25
MIN_RECT_HEIGHT = 5
MAX_RECT_HEIGHT = 25
BACKGROUND_COLOR = (66, 65, 112)
WIDTH, HEIGHT = 1422, 800
# --------------------------------------------

# Game variables and fundamentals --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
keep: bool = True

shapes: List[Circle] = []
colors: List[Tuple[int, int, int]] = []
colliding_colors: List[Tuple[int, int, int]] = []

feed_active: bool = True
mouse_circle: Circle = Circle((0, 0), 50)
border_color: str = "green"
# --------------------------------------------

# Useful surfaces setup ----------------------
txt_surf = FONT.render("RIGHT CLICK to toggle | MOUSE WHEEL to select size",
                       True, "white")
sub_text_surf = pygame.surface.Surface((WIDTH, txt_surf.get_height() + 5))
sub_text_surf.set_alpha(SUB_TEXT_ALPHA)
mouse_circle_surf = get_new_circle_surf(mouse_circle, "white", ALPHA_VALUE)
TXT_SURF_BLIT_POS = txt_surf.get_rect(
    center=(WIDTH / 2, txt_surf.get_height() / 2))
# ------------------------------------------

# Create the random shapes
for _ in range(SHAPES_NUMBER):
    colors.append(rand_bw_color(20, 130))
    colliding_colors.append(rand_color())
    obj = None
    if random() * 10 > 5:
        radius = randint(MIN_CIRCLE_RADIUS, MAX_CIRCLE_RADIUS)
        obj = Circle((randint(radius, WIDTH - radius),
                      randint(radius, HEIGHT - radius)), radius)
    else:
        dimx = randint(MIN_RECT_WIDTH, MAX_RECT_WIDTH)
        dimy = randint(MIN_RECT_HEIGHT, MAX_RECT_HEIGHT)
        obj = pygame.Rect((randint(0, WIDTH - dimx), randint(0, HEIGHT - dimy)),
                          (dimx, dimy))
    
    shapes.append(obj)

# Game loop
while keep:
    
    screen.fill(BACKGROUND_COLOR)
    clock.tick_busy_loop(FPS)
    
    mouse_circle.move_to_ip(*pygame.mouse.get_pos())
    
    # main update and draw loop, draw every shape and update their size
    for shape, color, coll_color in zip(shapes, colors, colliding_colors):
        
        is_circle = isinstance(shape, Circle)
        is_rect = isinstance(shape, pygame.Rect)
        
        if feed_active and mouse_circle.collides_with(shape):
            if is_circle:
                shape.scale_ip(shape.radius + 0.2)
                pygame.draw.circle(screen, coll_color, *shape())
            elif is_rect:
                pygame.draw.rect(screen, coll_color, shape)
        else:
            if is_circle:
                if shape.radius <= 1.5:
                    # this relocates the circle so there's no need to delete
                    # and create a new one
                    radius = randint(3, 15)
                    ind = shapes.index(shape)
                    shape.update((randint(radius, WIDTH - radius),
                                  randint(radius, HEIGHT - radius)),
                                 radius)
                shape.scale_ip(shape.radius - 0.25)
                pygame.draw.circle(screen, color, *shape())
            elif is_rect:
                pygame.draw.rect(screen, color, shape)
    
    # blit the mouse circle surface on the screen
    screen.blit(mouse_circle_surf, mouse_circle_surf.get_rect(
        center=(mouse_circle.x, mouse_circle.y)))
    
    # select and draw the mouse_circle border color
    if feed_active:
        border_color = "green"
    else:
        border_color = "white"
    
    pygame.draw.circle(screen, border_color, (mouse_circle.x, mouse_circle.y),
                       mouse_circle.radius, 2)
    
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
    
    # blit the text and black bar on the screen
    screen.blit(sub_text_surf, (0, 0))
    screen.blit(txt_surf, TXT_SURF_BLIT_POS)
    
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.update()

pygame.quit()
