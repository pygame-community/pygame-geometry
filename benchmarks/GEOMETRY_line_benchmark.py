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
        Line((20, 105), (205, 406)),
    ],
    "circles": [
        Circle((200, 74), 21),
        Circle((275, 203), 89),
        Circle((40, 517), 5),
        Circle((91, 604), 43),
        Circle((212, 165), 13),
        Circle((172, 55), 43),
        Circle((787, 130), 3),
        Circle((637, 5), 133),
        Circle((697, 658), 4),
        Circle((20, 105), 23),
    ],
    "rects": [
        Rect(200, 74, 21, 109),
        Rect(42, 203, 32, 89),
        Rect(40, 517, 5, 5),
        Rect(24, 13, 23, 43),
        Rect(212, 14, 13, 13),
        Rect(44, 55, 43, 231),
        Rect(53, 5, 3, 3),
        Rect(637, 5, 57, 53),
        Rect(654, 658, 4, 87),
        Rect(20, 105, 23, 3),
    ],
    "mixed": [
        Line((200, 42), (755, 474)),
        Circle((275, 53), 2),
        Rect(40, 517, 5, 5),
        Line((91, 604), (5, 42)),
        Circle((31, 165), 13),
        Rect(172, 55, 64, 231),
        Line((787, 52), (9, 453)),
        Circle((637, 5), 133),
        Rect(697, 658, 33, 87),
        Line((20, 555), (113, 12)),
        Circle((20, 533), 23),
        Rect(20, 13, 6, 3),
    ],
}

instatiation_tests = [
    ("Line", "Line(l1)"),
    ("4 int", "Line(0, 0, 10, 10)"),
    ("4 float", "Line(0.0, 0.0, 10.0, 10.0)"),
    ("2 tuple int", "Line((0, 0), (10, 10))"),
    ("2 tuple float", "Line((0.0, 0.0), (10.0, 10.0))"),
    ("1 tuple int", "Line((0, 0, 10, 10))"),
    ("1 tuple float", "Line((0.0, 0.0, 10.0, 10.0))"),
    ("1 tuple 2 sub tuple int", "Line(((0, 0), (10, 10)))"),
    ("1 tuple 2 sub tuple float", "Line(((0.0, 0.0), (10.0, 10.0)))"),
    ("2 list int", "Line([0, 0], [10, 10])"),
    ("2 list float", "Line([0.0, 0.0], [10.0, 10.0])"),
    ("1 list int", "Line([0, 0, 10, 10])"),
    ("1 list float", "Line([0.0, 0.0, 10.0, 10.0])"),
    ("1 list 2 sub list int", "Line([[0, 0], [10, 10]])"),
    ("1 list 2 sub list float", "Line([[0.0, 0.0], [10.0, 10.0]])"),
    ("1 list 2 sub tuple int", "Line([(0, 0), (10, 10)])"),
    ("1 list 2 sub tuple float", "Line([(0.0, 0.0), (10.0, 10.0)])"),
    ("1 tuple 2 sub list int", "Line(([0, 0], [10, 10]))"),
    ("1 tuple 2 sub list float", "Line(([0.0, 0.0], [10.0, 10.0]))"),
    ("4 int tuple inside tuple", "Line(((0, 0, 10, 10),))"),
    ("4 float tuple inside tuple", "Line(((0.0, 0.0, 10.0, 10.0),))"),
    ("4 int list inside list", "Line([[0, 0, 10, 10]])"),
    ("4 float list inside list", "Line([[0.0, 0.0, 10.0, 10.0]])"),
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
    ("line", "l1.update(l2)"),
    ("4 int", "l1.update(1, 1, 3, 3)"),
    ("4 float", "l1.update(1.0, 1.0, 3.0, 3.0)"),
    ("1 tup 4 int", "l1.update((1, 1, 3, 3))"),
    ("1 tup 4 float", "l1.update((1.0, 1.0, 3.0, 3.0))"),
    ("1 tup 2 subtups int", "l1.update(((1, 1), (3, 3)))"),
    ("1 tup 2 subtups float", "l1.update(((1.0, 1.0), (3.0, 3.0)))"),
    ("2 tup int", "l1.update((1, 1), (3, 3))"),
    ("2 tup float", "l1.update((1.0, 1.0), (3.0, 3.0))"),
]

move_tests = [
    ("2 int", "l1.move(1, 1)"),
    ("2 float", "l1.move(1.0, 1.0)"),
    ("tuple int", "l1.move((1, 1))"),
    ("tuple float", "l1.move((1.0, 1.0))"),
]

move_ip_tests = [
    ("2 int", "l1.move_ip(1, 1)"),
    ("2 float", "l1.move_ip(1.0, 1.0)"),
    ("tuple int", "l1.move_ip((1, 1))"),
    ("tuple float", "l1.move_ip((1.0, 1.0))"),
]

collideline_tests = [
    ("C line", "l1.collideline(l2)"),
    ("NC line", "l1.collideline(l3)"),
    ("C 4 int", "l1.collideline(1, 1, 3, 3)"),
    ("NC 4 int", "l1.collideline(1, 1, 3, 4)"),
    ("C 4 float", "l1.collideline(1.0, 1.0, 3.0, 3.0)"),
    ("NC 4 float", "l1.collideline(1.0, 1.0, 3.0, 4.0)"),
    ("C 1 tup 4 int", "l1.collideline((1, 1, 3, 3))"),
    ("NC 1 tup 4 int", "l1.collideline((1, 1, 3, 4))"),
    ("C 1 tup 4 float", "l1.collideline((1.0, 1.0, 3.0, 3.0))"),
    ("NC 1 tup 4 float", "l1.collideline((1.0, 1.0, 3.0, 4.0))"),
    ("C 1 tup 2 subtups int", "l1.collideline(((1, 1), (3, 3)))"),
    ("NC 1 tup 2 subtups int", "l1.collideline(((1, 1), (3, 4)))"),
    ("C 1 tup 2 subtups float", "l1.collideline(((1.0, 1.0), (3.0, 3.0)))"),
    ("NC 1 tup 2 subtups float", "l1.collideline(((1.0, 1.0), (3.0, 4.0)))"),
    ("C 2 tup int", "l1.collideline((1, 1), (3, 3))"),
    ("NC 2 tup int", "l1.collideline((1, 1), (3, 4))"),
    ("C 2 tup float", "l1.collideline((1.0, 1.0), (3.0, 3.0))"),
    ("NC 2 tup float", "l1.collideline((1.0, 1.0), (3.0, 4.0))"),
]

collidecircle_tests = [
    ("C circle", "l1.collidecircle(c1)"),
    ("NC circle", "l1.collidecircle(c2)"),
    ("inside circle", "l1.collidecircle(c3)"),
    ("C 3 int", "l1.collidecircle(5, 5, 10)"),
    ("NC 3 int", "l1.collidecircle(20, 20, 5)"),
    ("inside 3 int", "l1.collidecircle(0, 0, 150)"),
    ("C 3 float", "l1.collidecircle(5.0, 5.0, 10.0)"),
    ("NC 3 float", "l1.collidecircle(20.0, 20.0, 5.0)"),
    ("inside 3 float", "l1.collidecircle(0.0, 0.0, 150.0)"),
    ("C 1 tup 3 int", "l1.collidecircle((5, 5, 10))"),
    ("NC 1 tup 3 int", "l1.collidecircle((20, 20, 5))"),
    ("inside 1 tup 3 int", "l1.collidecircle((0, 0, 150))"),
    ("C 1 tup 3 float", "l1.collidecircle((5.0, 5.0, 10.0))"),
    ("NC 1 tup 3 float", "l1.collidecircle((20.0, 20.0, 5.0))"),
    ("inside 1 tup 3 float", "l1.collidecircle((0.0, 0.0, 150.0))"),
    ("C 2 tup int", "l1.collidecircle((5, 5), 10)"),
    ("NC 2 tup int", "l1.collidecircle((20, 20), 5)"),
    ("inside 2 tup int", "l1.collidecircle((0, 0), 150)"),
    ("C 2 tup float", "l1.collidecircle((5.0, 5.0), 10.0)"),
    ("NC 2 tup float", "l1.collidecircle((20.0, 20.0), 5.0)"),
    ("inside 2 tup float", "l1.collidecircle((0.0, 0.0), 150.0)"),
]

colliderect_tests = [
    ("C rect", "l1.colliderect(r1)"),
    ("NC rect", "l1.colliderect(r2)"),
    ("inside rect", "l1.colliderect(r3)"),
    ("C 4 int", "l1.colliderect(3, 5, 10, 10)"),
    ("NC 4 int", "l1.colliderect(100, 100, 4, 4)"),
    ("inside 4 int", "l1.colliderect(-30, -30, 100, 100)"),
    ("C 4 float", "l1.colliderect(3.0, 5.0, 10.0, 10.0)"),
    ("NC 4 float", "l1.colliderect(100.0, 100.0, 4.0, 4.0)"),
    ("inside 4 float", "l1.colliderect(-30.0, -30.0, 100.0, 100.0)"),
    ("C 1 tup 4 int", "l1.colliderect((3, 5, 10, 10))"),
    ("NC 1 tup 4 int", "l1.colliderect((100, 100, 4, 4))"),
    ("inside 1 tup 4 int", "l1.colliderect((-30, -30, 100, 100))"),
    ("C 1 tup 4 float", "l1.colliderect((3.0, 5.0, 10.0, 10.0))"),
    ("NC 1 tup 4 float", "l1.colliderect((100.0, 100.0, 4.0, 4.0))"),
    ("inside 1 tup 4 float", "l1.colliderect((-30.0, -30.0, 100.0, 100.0))"),
    ("C 1 tup 2 subtups int", "l1.colliderect(((3, 5), (10, 10)))"),
    ("NC 1 tup 2 subtups int", "l1.colliderect(((100, 100), (4, 4)))"),
    ("inside 1 tup 2 subtups int", "l1.colliderect(((-30, -30), (100, 100)))"),
    ("C 1 tup 2 subtups float", "l1.colliderect(((3.0, 5.0), (10.0, 10.0)))"),
    ("NC 1 tup 2 subtups float", "l1.colliderect(((100.0, 100.0), (4.0, 4.0)))"),
    (
        "inside 1 tup 2 subtups float",
        "l1.colliderect(((-30.0, -30.0), (100.0, 100.0)))",
    ),
]

collidepoint_tests = [
    ("C 1 int", "l4.collidepoint((1, 1))"),
    ("NC 1 int", "l4.collidepoint((3, 3))"),
    ("C 1 float", "l4.collidepoint((1.0, 1.0))"),
    ("NC 1 float", "l4.collidepoint((3.0, 3.0))"),
    ("C 2 int", "l4.collidepoint(1, 1)"),
    ("NC 2 int", "l4.collidepoint(3, 3)"),
    ("C 2 float", "l4.collidepoint(1.0, 1.0)"),
    ("NC 2 float", "l4.collidepoint(3.0, 3.0)"),
]

raycast_tests = [
    ("lines-only", "l1.raycast(lines)"),
    ("circles-only", "l1.raycast(circles)"),
    ("rects-only", "l1.raycast(rects)"),
    ("mixed", "l1.raycast(mixed)"),
]

is_parallel_tests = [
    ("parallel", "l1.parallel(l4)"),
    ("not parallel", "l1.parallel(l2)"),
]

is_perpendicular_tests = [
    ("perp.", "l1.is_perpendicular(l3)"),
    ("not perp.", "l1.is_perpendicular(l4)"),
]

# === Test Suites ===
# If you want to add more tests to a suite, just add them to the list
# If you want to remove or skip tests from a suite, just remove or comment them out
GROUPS = [
    ("Instatiation", instatiation_tests),
    ("Attribute Getters", getters_tests),
    ("Attribute Setters", setters_tests),
    ("Copy", copy_tests),
    ("Conversion", conversion_tests),
    ("Update", update_tests),
    ("Move", move_tests),
    ("Move_ip", move_ip_tests),
    ("Collision: Line", collideline_tests),
    ("Collision: Circle", collidecircle_tests),
    ("Collision: Rect", colliderect_tests),
    ("Collision: Point", collidepoint_tests),
    ("Raycast", raycast_tests),
    ("Parallel", is_parallel_tests),
    ("Perpendicular", is_perpendicular_tests),
]

TestSuite("Geometry Module - Line", GROUPS, GLOB).run_suite()
