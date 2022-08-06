from pygame import Rect
from benchmark_utils import TestSuite
from geometry import Circle

CPT = 1_000_000  # Calls Per Test

r1 = Rect(0, 0, 10, 10)
r2 = Rect(10, 10, 4, 4)
r3 = Rect(0, 0, 100, 100)

c1 = Circle(10, 10, 10)
c2 = Circle(20, 5, 15)
c3 = Circle(50, 50, 15)
c4 = Circle(10, 10, 15)

p1 = (10, 10)
p2 = (1000, 1000)

GLOB = {
    "Circle": Circle,
    "r1": r1,
    "r2": r2,
    "r3": r3,
    "c1": c1,
    "c2": c2,
    "c3": c3,
    "c4": c4,
    "p1": p1,
    "p2": p2,
}

# === Tests ===
general_test = [
    ("Instatiation", "Circle(0, 0, 5)"),
    ("x attrib", "c1.x"),
    ("y attrib", "c1.y"),
    ("radius attrib", "c1.r"),
    ("copy", "c1.copy()"),
    ("update", "c1.update(1, 1, 3)"),
    # ("move", "c1.move(1, 1)"),
    # ("move_ip", "c1.move_ip(1, 1)"),
    # ("move_to", "c1.move_to(1, 1)"),
    # ("move_to_ip", "c1.move_to_ip(1, 1)"),
    # ("scale_by", "c1.scale_by(1.2)"),
    # ("scale_by_ip", "c1.scale_by_ip(1.2)"),
    ("as_rect", "c1.as_rect()"),
]

CC_collision_test = [
    ("Colliding", "c1.collidecircle(c2)"),
    ("Non colliding", "c1.collidecircle(c3)"),
    ("A inside B", "c1.collidecircle(c4)"),
    ("B inside A", "c4.collidecircle(c1)"),
]

CR_collision_test = [
    ("Colliding", "c1.colliderect(r1)"),
    ("Non colliding", "c3.colliderect(r1)"),
    ("A inside B", "c3.colliderect(r3)"),
    ("B inside A", "c1.colliderect(r2)"),
]

CP_collision_test = [
    ("Colliding", "c1.collidepoint(p1)"),
    ("Non colliding", "c1.collidepoint(p2)"),
    ("A inside B", "c1.collidepoint(10, 10)"),
    ("B inside A", "c1.collidepoint(1000, 1000)"),
]

CS_collision_test = [
    ("RECT colliding", "c1.collideswith(r1)"),
    ("RECT non colliding", "c1.collideswith(r2)"),
    ("CIRCLE colliding", "c1.collideswith(c2)"),
    ("CIRCLE non colliding", "c1.collideswith(c2)"),
    ("POINT colliding", "c1.collideswith(p1)"),
    ("POINT non colliding", "c1.collideswith(p2)"),
]

TESTS = [
    ("General", general_test),
    ("Circle-Circle", CC_collision_test),
    ("Circle-Rect", CR_collision_test),
    ("Circle-Point", CP_collision_test),
    ("Circle-Shape", CS_collision_test),
]
# ==========================

TestSuite("Geometry Module - Circle", TESTS, GLOB, num=CPT).run_suite()
