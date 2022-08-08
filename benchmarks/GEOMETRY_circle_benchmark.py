from pygame import Rect
from benchmark_utils import TestSuite
from geometry import Circle

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
# Each test consists of a tuple of: (name, call)
# The name is a string containing the name of the test
# The call is a string containing the code to be timed
# every test is run CPT times and the average time is
# calculated across REP runs
# the formula is time = (time per CPT calls repeated REP times) / REP
# ====================================================
creation_tests = [
    ("Circle int", "Circle(0, 0, 5)"),
    ("Circle float", "Circle(0.0, 0.0, 5.0)"),
]

copy_tests = [
    ("Circle copy", "c1.copy()"),
]

conversion_tests = [
    ("as_rect", "c1.as_rect()"),
]

attributes_tests = [
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
]

update_tests = [
    ("update circle", "c1.update(c2)"),
    ("update 3 int", "c1.update(1, 1, 3)"),
    ("update 3 float", "c1.update(1.0, 1.0, 3.0)"),
    ("update 1 tup int", "c1.update((1, 1, 3))"),
    ("update 1 tup float", "c1.update((1.0, 1.0, 3.0))"),
]

move_tests = [
    ("move int", "c1.move(1, 1)"),
    ("move float", "c1.move(1.0, 1.0)"),
    ("move_ip int", "c1.move_ip(1, 1)"),
    ("move_ip float", "c1.move_ip(1.0, 1.0)"),
]

CC_collision_tests = [
    ("Colliding", "c1.collidecircle(c2)"),
    ("Non colliding", "c1.collidecircle(c3)"),
    ("A inside B", "c1.collidecircle(c4)"),
    ("B inside A", "c4.collidecircle(c1)"),
]

CR_collision_tests = [
    ("Colliding", "c1.colliderect(r1)"),
    ("Non colliding", "c3.colliderect(r1)"),
    ("A inside B", "c3.colliderect(r3)"),
    ("B inside A", "c1.colliderect(r2)"),
]

CP_collision_tests = [
    ("Colliding 1 int", "c1.collidepoint(p1)"),
    ("Non colliding 1 int", "c1.collidepoint(p2)"),
    ("Colliding 1 float", "c1.collidepoint(p3)"),
    ("Non colliding 1 float", "c1.collidepoint(p4)"),
    ("Colliding 2 int", "c1.collidepoint(10, 10)"),
    ("Non colliding 2 int", "c1.collidepoint(1000, 1000)"),
    ("Colliding 2 float", "c1.collidepoint(10.0, 10.0)"),
    ("Non colliding 2 float", "c1.collidepoint(1000.0, 1000.0)"),
]

CS_collision_tests = [
    ("RECT colliding", "c1.collideswith(r1)"),
    ("RECT non colliding", "c1.collideswith(r2)"),
    ("CIRCLE colliding", "c1.collideswith(c2)"),
    ("CIRCLE non colliding", "c1.collideswith(c2)"),
    ("POINT colliding", "c1.collideswith(p1)"),
    ("POINT non colliding", "c1.collideswith(p2)"),
]

# === Test Suites ===
# If you want to add more tests to a suite, just add them to the list
# If you want to remove or skip tests from a suite, just remove or comment them out
GROUPS = [
    ("Creation", creation_tests),
    ("Attributes", attributes_tests),
    ("Copy", copy_tests),
    ("Conversion", conversion_tests),
    ("Update", update_tests),
    # ("Move", move_tests),
    ("Circle-Circle", CC_collision_tests),
    ("Circle-Rect", CR_collision_tests),
    ("Circle-Point", CP_collision_tests),
    ("Circle-Shape", CS_collision_tests),
]

TestSuite("Geometry Module - Circle", GROUPS, GLOB).run_suite()
