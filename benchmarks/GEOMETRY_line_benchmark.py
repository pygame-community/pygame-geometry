import random

from pygame import Rect
from benchmark_utils import TestSuite
from geometry import Circle
from geometry import Line

# ====================================================
# Each test consists of a tuple of: (name, call)
# The name is a string containing the name of the test
# The call is a string containing the code to be timed
# every test is run CPT times and the average time is
# calculated across REP runs
# the formula is time = (time per CPT calls repeated REP times) / REP
# ====================================================

l1 = Line(0, 0, 10, 10)
l2 = Line(0, 10, 10, 0)
l3 = Line(100, 100, 30, 22)
l4 = Line(0, 0, 1, 1)


def random_line():
    def random_pos():
        return random.randrange(0, 800), random.randrange(0, 800)

    return Line(random_pos(), random_pos())


rand_lines = [random_line() for _ in range(100)]

c1 = Circle(5, 5, 10)
c2 = Circle(20, 20, 5)
c3 = Circle(0, 0, 150)

r1 = Rect(3, 5, 10, 10)
r2 = Rect(100, 100, 4, 4)
r3 = Rect(-30, -30, 100, 100)

p1 = (0.5, 0.5)
p2 = (3, 3)

GLOB = {
    "Line": Line,
    "l1": l1,
    "l2": l2,
    "l3": l3,
    "l4": l4,
    "c1": c1,
    "c2": c2,
    "c3": c3,
    "p1": p1,
    "p2": p2,
    "rand_lines": rand_lines,
}

# === Tests ===
creation_test = [
    ("Line int", "Line(0, 0, 10, 10)"),
    ("Line float", "Line(0.0, 0.0, 10.0, 10.0)"),
]

copy_test = [
    ("copy", "l1.copy()"),
]

conversion_test = [
    ("as_rect", "l1.as_rect()"),
    # ("as_circle", "l1.as_circle()"),
]

attributes_test = [
    ("x1 get", "l1.x1"),
    ("x1 set int", "l1.x1 = 1"),
    ("x1 set float", "l1.x1 = 1.0"),
    ("y1 get", "l1.y1"),
    ("y1 set int", "l1.y1 = 1"),
    ("y1 set float", "l1.y1 = 1.0"),
    ("x2 get", "l1.x2"),
    ("x2 set int", "l1.x2 = 1"),
    ("x2 set float", "l1.x2 = 1.0"),
    ("y2 get", "l1.y2"),
    ("y2 set int", "l1.y2 = 1"),
    ("y2 set float", "l1.y2 = 1.0"),
    ("a get", "l1.a"),
    ("a set int", "l1.a = (1, 1)"),
    ("a set float", "l1.a = (1.0, 1.0)"),
    ("b get", "l1.b"),
    ("b set int", "l1.b = (1, 1)"),
    ("b set float", "l1.b = (1.0, 1.0)"),
]

update_test = [
    ("update line", "l1.update(l2)"),
    ("update 1 tup", "l1.update((1, 1, 3, 3))"),
    ("update 1 tup 2 subtups", "l1.update(((1, 1), (3, 3)))"),
    ("update 2 args", "l1.update((1, 1),( 3, 3))"),
    ("update 4 args", "l1.update(1, 1, 3, 3)"),
]

move_test = [
    ("move int", "l1.move(1, 1)"),
    ("move float", "l1.move(1.0, 1.0)"),
    ("move_ip int", "l1.move_ip(1, 1)"),
    ("move_ip float", "l1.move_ip(1.0, 1.0)"),
]

LL_collision_test = [
    ("Colliding", "l1.collideline(l2)"),
    ("Non colliding", "l1.collideline(l3)"),
]

LC_collision_test = [
    ("Colliding", "l1.collidecircle(c1)"),
    ("Non colliding", "l1.collidecircle(c2)"),
    ("inside circle", "l1.collidecircle(c3)"),
]

LR_collision_test = [
    ("Colliding", "l1.colliderect(r1)"),
    ("Non colliding", "l1.colliderect(r2)"),
    ("inside rect", "l1.colliderect(r3)"),
]

LP_collision_test = [
    ("Colliding", "l4.collidepoint(p1)"),
    ("Non colliding", "l4.collidepoint(p2)"),
    ("Colliding 2", "l4.collidepoint(0.5, 0.5)"),
    ("Non colliding 2", "l4.collidepoint(3, 3)"),
]

raycast_test = [
    ("raycast", "l1.raycast(rand_lines)"),
]

# === Test Suites ===
# If you want to add more tests to a suite, just add them to the list
# If you want to remove or skip tests from a suite, just remove or comment them out
TESTS = [
    ("Creation", creation_test),
    ("Attributes", attributes_test),
    ("Copy", copy_test),
    ("Conversion", conversion_test),
    ("Update", update_test),
    # ("Move", move_test),
    ("Collision: Line-Line", LL_collision_test),
    ("Collision: Line-Circle", LC_collision_test),
    # ("Collision: Line-Rect", LR_collision_test),
    ("Collision: Line-Point", LP_collision_test),
    ("Raycast", raycast_test),
]

TestSuite("Geometry Module - Line", TESTS, GLOB).run_suite()
