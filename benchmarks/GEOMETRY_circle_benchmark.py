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
p3 = (10.0, 10.0)
p4 = (1000.0, 1000.0)

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
    "p3": p3,
    "p4": p4,
}

# === Tests ===
general_test = [
    ("Instatiation", "Circle(0, 0, 5)"),
    ("x get", "c1.x"),
    ("x set int", "c1.x = 3"),
    ("x set float", "c1.x = 3.0"),
    ("y get", "c1.y"),
    ("y set int", "c1.y = 3"),
    ("y set float", "c1.y = 3.0"),
    ("radius get", "c1.r"),
    ("radius set int", "c1.r = 3"),
    ("radius set float", "c1.r = 3.0"),
    ("center get", "c1.center"),
    ("center set int", "c1.center = (3, 3)"),
    ("center set float", "c1.center = (3.0, 3.0)"),
    ("area get", "c1.area"),
    ("area set int", "c1.area = 3"),
    ("area set float", "c1.area = 3.0"),
    ("circumference get", "c1.circumference"),
    ("circumference set int", "c1.circumference = 3"),
    ("circumference set float", "c1.circumference = 3.0"),
    ("copy", "c1.copy()"),
    ("update int", "c1.update(1, 1, 3)"),
    ("update float", "c1.update(1.0, 1.0, 3.0)"),
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
    ("Colliding 1 int", "c1.collidepoint(p1)"),
    ("Non colliding 1 int", "c1.collidepoint(p2)"),
    ("Colliding 1 float", "c1.collidepoint(p3)"),
    ("Non colliding 1 float", "c1.collidepoint(p4)"),
    ("Colliding 2 int", "c1.collidepoint(10, 10)"),
    ("Non colliding 2 int", "c1.collidepoint(1000, 1000)"),
    ("Colliding 2 float", "c1.collidepoint(10.0, 10.0)"),
    ("Non colliding 2 float", "c1.collidepoint(1000.0, 1000.0)"),
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
