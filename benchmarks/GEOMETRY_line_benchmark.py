import random

from pygame import Rect
from benchmark_utils import TestSuite
from geometry import Circle
from geometry import Line


def random_line():
    def random_pos():
        return random.randrange(0, 800), random.randrange(0, 800)

    return Line(random_pos(), random_pos())


# ====================================================
# Each test consists of a tuple of: (name, call)
# The name is a string containing the name of the test
# The call is a string containing the code to be timed
# every test is run CPT times and the average time is
# calculated across REP runs
# the formula is time = (time per CPT calls repeated REP times) / REP
# ====================================================

CPT = 1_000_000  # Calls per test
REP = 5  # Repetitions per test

l1 = Line(0, 0, 10, 10)
l2 = Line(0, 10, 10, 0)
l3 = Line(100, 100, 30, 22)
l4 = Line(0, 0, 1, 1)

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
general_test = [
    ("Instatiation", "Line(0, 0, 5, 5)"),
    ("x1 attrib", "l1.x1"),
    ("x1 attrib set", "l1.x1 = 1"),
    ("y1 attrib", "l1.y1"),
    ("y1 attrib set", "l1.y1 = 1"),
    ("x2 attrib", "l1.x2"),
    ("x2 attrib set", "l1.x2 = 1"),
    ("y2 attrib", "l1.y2"),
    ("y2 attrib set", "l1.y2 = 1"),
    ("a attrib", "l1.a"),
    ("a attrib set", "l1.a = (1, 1)"),
    ("b attrib", "l1.b"),
    ("b attrib set", "l1.b = (1, 1)"),
    ("copy", "l1.copy()"),
    ("update line", "l1.update(l2)"),
    ("update 1 tup", "l1.update((1, 1, 3, 3))"),
    ("update 1 tup 2 subtups", "l1.update(((1, 1), (3, 3)))"),
    ("update 2 args", "l1.update((1, 1),( 3, 3))"),
    ("update 4 args", "l1.update(1, 1, 3, 3)"),
    # ("move", "l1.move(1, 1)"),
    # ("move_ip", "l1.move_ip(1, 1)"),
    # ("move_to", "l1.move_to(1, 1)"),
    # ("move_to_ip", "l1.move_to_ip(1, 1)"),
    # ("scale_by", "l1.scale_by(1.2)"),
    # ("scale_by_ip", "l1.scale_by_ip(1.2)"),
    ("as_rect", "l1.as_rect()"),
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

# LR_collision_test = [
#     ("Colliding", "l1.colliderect(r1)"),
#     ("Non colliding", "l1.colliderect(r2)"),
#     ("inside rect", "l1.colliderect(r3)"),
# ]

LP_collision_test = [
    ("Colliding", "l4.collidepoint(p1)"),
    ("Non colliding", "l4.collidepoint(p2)"),
    ("Colliding 2", "l4.collidepoint(0.5, 0.5)"),
    ("Non colliding 2", "l4.collidepoint(3, 3)"),
]

raycast_test = [
    ("raycast", "l1.raycast(rand_lines)"),
]

TESTS = [
    ("General", general_test),
    ("Collision: Line-Line", LL_collision_test),
    ("Collision: Line-Circle", LC_collision_test),
    # ("Collision: Line-Rect", LR_collision_test),
    ("Collision: Line-Point", LP_collision_test),
    ("Raycast", raycast_test),
]

TestSuite("Geometry Module - Line", TESTS, GLOB, CPT, REP).run_suite()
