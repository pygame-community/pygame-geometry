import random

from pygame import Rect
from benchmark_utils import TestSuite
from geometry import Circle
from geometry import Line

# === Tests ===
# Each test consists of a tuple of: (name, call)
# The name is a string containing the name of the test
# The call is a string containing the code to be timed
# every test is run CPT times and the average time is
# calculated across REP runs
# the formula is time = (time per CPT calls repeated REP times) / REP
# ====================================================

GLOB = {
    "Line": Line,
    "l1": Line(0, 0, 10, 10),
    "l2": Line(0, 10, 10, 0),
    "l3": Line(100, 100, 30, 22),
    "l4": Line(0, 0, 1, 1),
    "c1": Circle(5, 5, 10),
    "c2": Circle(20, 20, 5),
    "c3": Circle(0, 0, 150),
    "r1": Rect(3, 5, 10, 10),
    "r2": Rect(100, 100, 4, 4),
    "r3": Rect(-30, -30, 100, 100),
    "lines": [
        Line((200, 74), (714, 474)),
        Line((275, 203), (622, 172)),
        Line((40, 517), (524, 662)),
        Line((91, 604), (245, 113)),
        Line((212, 165), (734, 386)),
        Line((172, 55), (112, 166)),
        Line((787, 130), (9, 453)),
        Line((637, 5), (423, 768)),
        Line((697, 658), (693, 410)),
        Line((20, 105), (205, 406))
    ],
}

creation_tests = [
    ("Line int", "Line(0, 0, 10, 10)"),
    ("Line float", "Line(0.0, 0.0, 10.0, 10.0)"),
]

copy_tests = [
    ("copy", "l1.copy()"),
]

conversion_tests = [
    ("as_rect", "l1.as_rect()"),
    # ("as_circle", "l1.as_circle()"),
]

getters_tests = [
    ("x1", "l1.x1"),
    ("y1", "l1.y1"),
    ("x2", "l1.x2"),
    ("y2", "l1.y2"),
    ("a", "l1.a"),
    ("b", "l1.b"),
]

setters_tests = [
    ("x1 int", "l1.x1 = 1"),
    ("x1 float", "l1.x1 = 1.0"),
    ("y1 int", "l1.y1 = 1"),
    ("y1 float", "l1.y1 = 1.0"),
    ("x2 int", "l1.x2 = 1"),
    ("x2 float", "l1.x2 = 1.0"),
    ("y2 int", "l1.y2 = 1"),
    ("y2 float", "l1.y2 = 1.0"),
    ("a int", "l1.a = (1, 1)"),
    ("a float", "l1.a = (1.0, 1.0)"),
    ("b int", "l1.b = (1, 1)"),
    ("b float", "l1.b = (1.0, 1.0)"),
]

update_tests = [
    ("update line", "l1.update(l2)"),
    ("update 1 tup", "l1.update((1, 1, 3, 3))"),
    ("update 1 tup 2 subtups", "l1.update(((1, 1), (3, 3)))"),
    ("update 2 args", "l1.update((1, 1),( 3, 3))"),
    ("update 4 args", "l1.update(1, 1, 3, 3)"),
]

move_tests = [
    ("move int", "l1.move(1, 1)"),
    ("move float", "l1.move(1.0, 1.0)"),
    ("move_ip int", "l1.move_ip(1, 1)"),
    ("move_ip float", "l1.move_ip(1.0, 1.0)"),
]

LL_collision_tests = [
    ("Colliding", "l1.collideline(l2)"),
    ("Non colliding", "l1.collideline(l3)"),
]

LC_collision_tests = [
    ("Colliding", "l1.collidecircle(c1)"),
    ("Non colliding", "l1.collidecircle(c2)"),
    ("inside circle", "l1.collidecircle(c3)"),
]

LR_collision_tests = [
    ("Colliding", "l1.colliderect(r1)"),
    ("Non colliding", "l1.colliderect(r2)"),
    ("inside rect", "l1.colliderect(r3)"),
]

LP_collision_tests = [
    ("Colliding 1 int", "l4.collidepoint((1, 1))"),
    ("Non colliding 1 int", "l4.collidepoint((3, 3))"),
    ("Colliding 1 float", "l4.collidepoint((1.0, 1.0))"),
    ("Non colliding 1 float", "l4.collidepoint((3.0, 3.0))"),
    ("Colliding 2 int", "l4.collidepoint(1, 1)"),
    ("Non colliding 2 int", "l4.collidepoint(3, 3)"),
    ("Colliding 2 float", "l4.collidepoint(1.0, 1.0)"),
    ("Non colliding 2 float", "l4.collidepoint(3.0, 3.0)"),
]

raycast_tests = [
    ("raycast", "l1.raycast(lines)"),
]

perpendicular_tests = [
    ("perp.", "l1.is_perpendicular(l3)"),
    ("not perp.", "l1.is_perpendicular(l4)"),
]

# === Test Suites ===
# If you want to add more tests to a suite, just add them to the list
# If you want to remove or skip tests from a suite, just remove or comment them out
GROUPS = [
    ("Creation", creation_tests),
    ("Attribute Getters", getters_tests),
    ("Attribute Setters", setters_tests),
    ("Copy", copy_tests),
    ("Conversion", conversion_tests),
    ("Update", update_tests),
    ("Move", move_tests),
    ("Collision: Line-Line", LL_collision_tests),
    ("Collision: Line-Circle", LC_collision_tests),
    ("Collision: Line-Rect", LR_collision_tests),
    ("Collision: Line-Point", LP_collision_tests),
    ("Raycast", raycast_tests),
    ("Perpendicular", perpendicular_tests),
]

TestSuite("Geometry Module - Line", GROUPS, GLOB).run_suite()
