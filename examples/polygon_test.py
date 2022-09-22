from random import randint, random
from typing import List, Tuple, Union

import pygame, sys

from geometry import Polygon

pygame.init()

from random import randint
from typing import Tuple


def rand_color(minv: int = 0, maxv: int = 255) -> Tuple[int, int, int]:
    """returns a random RGB color with min and max as min and max threshold"""
    return randint(minv, maxv), randint(minv, maxv), randint(minv, maxv)


def rand_bw_color(minv: int, maxv: int) -> Tuple[int, int, int]:
    """returns a random RGB BW color"""
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
BACKGROUND_COLOR = (20, 30, 40)
WIDTH, HEIGHT = 1422, 800
# --------------------------------------------

# Game variables and fundamentals --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
keep: bool = True

shapes: List[Polygon] = []
colors: List[Tuple[int, int, int]] = []
colliding_colors: List[Tuple[int, int, int]] = []

feed_active: bool = True
some_polygon: Polygon = Polygon([100, 100], [150, 150], [200, 100])
border_color: str = "green"
acc_amt = 0
acc_multiplier = 0.92
# --------------------------------------------

mouse_rect = pygame.Rect(0, 0, 50, 65)
rect_color_0 = [0, 255, 100]
rect_color_1 = [255, 100, 50]

# Game loop
while keep:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_rect.center = mouse_pos
    
    screen.fill(BACKGROUND_COLOR)
    clock.tick_busy_loop(FPS)
    pygame.draw.polygon(screen, (250, 0, 250), some_polygon.vertices)
    pygame.draw.rect(screen, rect_color_1 if some_polygon.colliderect(mouse_rect) else rect_color_0, mouse_rect)
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.update()

pygame.quit()
