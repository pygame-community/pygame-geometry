from typing import Tuple

import pygame

from geometry import Circle

pygame.init()

# Constants--------------------------
FPS = 120
TEST_CIRCLE_RADIUS = 70
TEST_RECT_WIDTH = 50
TEST_RECT_HEIGHT = 50
NON_COLL_COLOR = (255, 133, 63)
COLL_COLOR = (100, 255, 63)
BACKGROUND_COLOR = (66, 65, 112)
WIDTH, HEIGHT = 600, 600
# -----------------------------------

# Game variables and fundamentals --------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
keep: bool = True

feed_active: bool = True

test_c = Circle(3 * WIDTH // 4, HEIGHT // 2, TEST_CIRCLE_RADIUS)
test_r = pygame.Rect(
    (WIDTH // 4 - TEST_RECT_WIDTH, HEIGHT // 2 - TEST_RECT_HEIGHT),
    (2 * TEST_RECT_WIDTH, 2 * TEST_RECT_HEIGHT),
)
colliding_c = False
colliding_r = False
mouse_shape = Circle(0, 0, 50)

acc_amt = 0
acc_multiplier = 0.92


# --------------------------------------------
def colorc() -> Tuple[int, int, int]:
    return COLL_COLOR if colliding_c else NON_COLL_COLOR


def colorr() -> Tuple[int, int, int]:
    return COLL_COLOR if colliding_r else NON_COLL_COLOR


# Game loop
while keep:
    screen.fill(BACKGROUND_COLOR)
    clock.tick_busy_loop(FPS)

    pygame.draw.circle(screen, colorc(), test_c.center, test_c.r)
    pygame.draw.rect(screen, colorr(), test_r)

    mouse_shape.center = pygame.mouse.get_pos()
    pygame.draw.circle(
        screen,
        (198, 255, 130) if colliding_c or colliding_r else (89, 130, 255),
        mouse_shape.center,
        mouse_shape.r,
    )

    if mouse_shape.colliderect(test_r):
        colliding_r = True
    else:
        colliding_r = False

    if mouse_shape.collidecircle(test_c):
        colliding_c = True
    else:
        colliding_c = False

    if abs(acc_amt) < 0.001:
        acc_amt = 0
    else:
        acc_amt *= acc_multiplier
        mouse_shape.r *= 1 + acc_amt

    # event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            keep = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if acc_amt <= 0:
                    acc_amt = 0
                acc_amt += 0.005
            else:
                if acc_amt >= 0:
                    acc_amt = 0
                acc_amt -= 0.007

    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.update()

pygame.quit()
