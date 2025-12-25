from pygame import Rect
from benchmark_utils import TestSuite
from geometry import Circle, Line, Polygon


# === Tests ===
# Each test consists of a tuple of: (name, call)
# The name is a string containing the name of the test
# The call is a string containing the code to be timed
# every test is run CPT times and the average time is
# calculated across REP runs
# the formula is time = (time per CPT calls repeated REP times) / REP
# ====================================================

GLOB = {
    "Circle": Circle,
    "r1": Rect(0, 0, 10, 10),
    "r2": Rect(10, 10, 4, 4),
    "r3": Rect(0, 0, 100, 100),
    "c1": Circle(10, 10, 10),
    "c2": Circle(20, 5, 15),
    "c3": Circle(50, 50, 15),
    "c4": Circle(10, 10, 15),
    "c5": Circle(0, 0, 15),
    "l1": Line(0, 0, 10, 10),
    "l2": Line(0, 0, 10, -10),
    "l3": Line(10, 10, 100, 43),
    "p1": (10, 10),
    "p2": (1000, 1000),
    "p3": (10.0, 10.0),
    "p4": (1000.0, 1000.0),
    "poly1": Polygon([(-5, 0), (5, 0), (0, 5)]),
    "poly2": Polygon([(100, 150), (200, 225), (150, 200)]),
    "poly3": Polygon([(0, 0), (50, 50), (50, -50), (0, -50)]),
}

instatiation_tests = [
    ("Circle", "Circle(c1)"),
    ("3 int", "Circle(0, 0, 5)"),
    ("3 float", "Circle(0.0, 0.0, 5.0)"),
    ("2 args tup+int", "Circle((0, 0), 5)"),
    ("2 args tup+float", "Circle((0.0, 0.0), 5.0)"),
    ("2 args lst+int", "Circle([0, 0], 5)"),
    ("2 args lst+float", "Circle([0.0, 0.0], 5.0)"),
    ("1 tuple int", "Circle((0, 0, 5))"),
    ("1 tuple float", "Circle((0.0, 0.0, 5.0))"),
    ("1 list int", "Circle([0, 0, 5])"),
    ("1 list float", "Circle([0.0, 0.0, 5.0])"),
    ("1 list 2 args tup+int", "Circle([(0, 0), 5])"),
    ("1 list 2 args tup+float", "Circle([(0.0, 0.0), 5.0])"),
    ("1 tuple 2 args lst+int", "Circle(([0, 0], 5))"),
    ("1 tuple 2 args lst+float", "Circle(([0.0, 0.0], 5.0))"),
    ("1 list 2 args lst+int", "Circle([[0, 0], 5])"),
    ("1 list 2 args lst+float", "Circle([[0.0, 0.0], 5.0])"),
    ("1 tuple 2 args tup+int", "Circle(((0, 0), 5))"),
    ("1 tuple 2 args tup+float", "Circle(((0.0, 0.0), 5.0))"),
    ("3 int list inside list", "Circle([[0, 0, 5]])"),
    ("3 float list inside list", "Circle([[0.0, 0.0, 5.0]])"),
    ("3 int tuple inside tuple", "Circle(((0, 0, 5)))"),
    ("3 float tuple inside tuple", "Circle(((0.0, 0.0, 5.0)))"),
    ("3 int tuple inside list", "Circle([(0, 0, 5)])"),
    ("3 float tuple inside list", "Circle([(0.0, 0.0, 5.0)])"),
    ("3 int list inside tuple", "Circle(([0, 0, 5]))"),
    ("3 float list inside tuple", "Circle(([0.0, 0.0, 5.0]))"),
]

copy_tests = [
    ("Circle copy", "c1.copy()"),
]

conversion_tests = [
    ("as_rect", "c1.as_rect()"),
]

getters_tests = [
    ("x", "c1.x"),
    ("y", "c1.y"),
    ("radius", "c1.r"),
    ("diameter", "c1.diameter"),
    ("d", "c1.d"),
    ("center", "c1.center"),
    ("area", "c1.area"),
    ("circumference", "c1.circumference"),
]

setters_tests = [
    ("x int", "c1.x = 3"),
    ("x float", "c1.x = 3.0"),
    ("y int", "c1.y = 3"),
    ("y float", "c1.y = 3.0"),
    ("radius int", "c1.r = 3"),
    ("radius float", "c1.r = 3.0"),
    ("diameter int", "c1.diameter = 3"),
    ("diameter float", "c1.diameter = 3.0"),
    ("d int", "c1.d = 3"),
    ("d float", "c1.d = 3.0"),
    ("center int", "c1.center = (3, 3)"),
    ("center float", "c1.center = (3.0, 3.0)"),
    ("area int", "c1.area = 3"),
    ("area float", "c1.area = 3.0"),
    ("circumference int", "c1.circumference = 3"),
    ("circumference float", "c1.circumference = 3.0"),
]

update_tests = [
    ("circle", "c1.update(c2)"),
    ("3 int", "c1.update(1, 1, 3)"),
    ("3 float", "c1.update(1.0, 1.0, 3.0)"),
    ("1 tup 3 int", "c1.update((1, 1, 3))"),
    ("1 tup 3 float", "c1.update((1.0, 1.0, 3.0))"),
    ("2 tuple-int", "c1.update((1, 1), 3)"),
    ("2 tuple-float", "c1.update((1.0, 1.0), 3.0)"),
    ("1 tup 2 int", "c1.update(((1, 1), 3))"),
    ("1 tup 2 float", "c1.update(((1.0, 1.0), 3.0))"),
]

move_tests = [
    ("x-x int", "c1.move(1, 1)"),
    ("x-x float", "c1.move(1.0, 1.0)"),
    ("x-x tup int", "c1.move((1, 1))"),
    ("x-x tup float", "c1.move((1.0, 1.0))"),
    ("x-x lst int", "c1.move([1, 1])"),
    ("x-x lst float", "c1.move([1.0, 1.0])"),
    ("0-x int", "c1.move(0, 1)"),
    ("0-x float", "c1.move(0.0, 1.0)"),
    ("0-x tup int", "c1.move((0, 1))"),
    ("0-x tup float", "c1.move((0.0, 1.0))"),
    ("0-x lst int", "c1.move([0, 1])"),
    ("0-x lst float", "c1.move([0.0, 1.0])"),
    ("x-0 int", "c1.move(1, 0)"),
    ("x-0 float", "c1.move(1.0, 0.0)"),
    ("x-0 tup int", "c1.move((1, 0))"),
    ("x-0 tup float", "c1.move((1.0, 0.0))"),
    ("x-0 lst int", "c1.move([1, 0])"),
    ("x-0 lst float", "c1.move([1.0, 0.0])"),
    ("0-0 int", "c1.move(0, 0)"),
    ("0-0 float", "c1.move(0.0, 0.0)"),
    ("0-0 tup int", "c1.move((0, 0))"),
    ("0-0 tup float", "c1.move((0.0, 0.0))"),
    ("0-0 lst int", "c1.move([0, 0])"),
    ("0-0 lst float", "c1.move([0.0, 0.0])"),
]

move_ip_tests = [
    ("x-x int", "c1.move_ip(1, 1)"),
    ("x-x float", "c1.move_ip(1.0, 1.0)"),
    ("x-x tup int", "c1.move_ip((1, 1))"),
    ("x-x tup float", "c1.move_ip((1.0, 1.0))"),
    ("x-x lst int", "c1.move_ip([1, 1])"),
    ("x-x lst float", "c1.move_ip([1.0, 1.0])"),
    ("0-x int", "c1.move_ip(0, 1)"),
    ("0-x float", "c1.move_ip(0.0, 1.0)"),
    ("0-x tup int", "c1.move_ip((0, 1))"),
    ("0-x tup float", "c1.move_ip((0.0, 1.0))"),
    ("0-x lst int", "c1.move_ip([0, 1])"),
    ("0-x lst float", "c1.move_ip([0.0, 1.0])"),
    ("x-0 int", "c1.move_ip(1, 0)"),
    ("x-0 float", "c1.move_ip(1.0, 0.0)"),
    ("x-0 tup int", "c1.move_ip((1, 0))"),
    ("x-0 tup float", "c1.move_ip((1.0, 0.0))"),
    ("x-0 lst int", "c1.move_ip([1, 0])"),
    ("x-0 lst float", "c1.move_ip([1.0, 0.0])"),
    ("0-0 int", "c1.move_ip(0, 0)"),
    ("0-0 float", "c1.move_ip(0.0, 0.0)"),
    ("0-0 tup int", "c1.move_ip((0, 0))"),
    ("0-0 tup float", "c1.move_ip((0.0, 0.0))"),
    ("0-0 lst int", "c1.move_ip([0, 0])"),
    ("0-0 lst float", "c1.move_ip([0.0, 0.0])"),
]

collidecircle_tests = [
    ("C circle", "c1.collidecircle(c2)"),
    ("NC circle", "c1.collidecircle(c3)"),
    ("A inside B", "c1.collidecircle(c4)"),
    ("B inside A", "c4.collidecircle(c1)"),
    ("C tup int", "c1.collidecircle((20, 5, 15))"),
    ("NC tup int", "c1.collidecircle((50, 50, 15))"),
    ("A inside B tup int", "c1.collidecircle((10, 10, 15))"),
    ("B inside A tup int", "c4.collidecircle((10, 10, 10))"),
    ("C tup 2 int", "c1.collidecircle(((20, 5), 15))"),
    ("NC tup 2 int", "c1.collidecircle(((50, 50), 15))"),
    ("A inside B tup 2 int", "c1.collidecircle(((10, 10), 15))"),
    ("B inside A tup 2 int", "c4.collidecircle(((10, 10), 10))"),
    ("C tup float", "c1.collidecircle((20.0, 5.0, 15.0))"),
    ("NC tup float", "c1.collidecircle((50.0, 50.0, 15.0))"),
    ("A inside B tup float", "c1.collidecircle((10.0, 10.0, 15.0))"),
    ("B inside A tup float", "c4.collidecircle((10.0, 10.0, 10.0))"),
    ("C tup 2 float", "c1.collidecircle(((20.0, 5.0), 15.0))"),
    ("NC tup 2 float", "c1.collidecircle(((50.0, 50.0), 15.0))"),
    ("A inside B tup 2 float", "c1.collidecircle(((10.0, 10.0), 15.0))"),
    ("B inside A tup 2 float", "c4.collidecircle(((10.0, 10.0), 10.0))"),
    ("C 2-tup int", "c1.collidecircle((20, 5), 15)"),
    ("NC 2-tup int", "c1.collidecircle((50, 50), 15)"),
    ("A inside B 2-tup int", "c1.collidecircle((10, 10), 15)"),
    ("B inside A 2-tup int", "c4.collidecircle((10, 10), 10)"),
    ("C 2-tup float", "c1.collidecircle((20.0, 5.0), 15.0)"),
    ("NC 2-tup float", "c1.collidecircle((50.0, 50.0), 15.0)"),
    ("A inside B 2-tup float", "c1.collidecircle((10.0, 10.0), 15.0)"),
    ("B inside A 2-tup float", "c4.collidecircle((10.0, 10.0), 10.0)"),
]

colliderect_tests = [
    ("C rect", "c1.colliderect(r1)"),
    ("NC rect", "c3.colliderect(r1)"),
    ("A inside B", "c3.colliderect(r3)"),
    ("B inside A", "c1.colliderect(r2)"),
    ("C tup int", "c1.colliderect((0, 0, 10, 10))"),
    ("NC tup int", "c3.colliderect((0, 0, 10, 10))"),
    ("A inside B tup int", "c3.colliderect((0, 0, 100, 100))"),
    ("B inside A tup int", "c1.colliderect((10, 10, 4, 4))"),
    ("C tup 2 int", "c1.colliderect(((0, 0), (10, 10)))"),
    ("NC tup 2 int", "c3.colliderect(((0, 0), (10, 10)))"),
    ("A inside B tup 2 int", "c3.colliderect(((0, 0), (100, 100)))"),
    ("B inside A tup 2 int", "c1.colliderect(((10, 10), (4, 4)))"),
    ("C tup float", "c1.colliderect((0.0, 0.0, 10.0, 10.0))"),
    ("NC tup float", "c3.colliderect((0.0, 0.0, 10.0, 10.0))"),
    ("A inside B tup float", "c3.colliderect((0.0, 0.0, 100.0, 100.0))"),
    ("B inside A tup float", "c1.colliderect((10.0, 10.0, 4.0, 4.0))"),
    ("C tup 2 float", "c1.colliderect(((0.0, 0.0), (10.0, 10.0)))"),
    ("NC tup 2 float", "c3.colliderect(((0.0, 0.0), (10.0, 10.0)))"),
    ("A inside B tup 2 float", "c3.colliderect(((0.0, 0.0), (100.0, 100.0)))"),
    ("B inside A tup 2 float", "c1.colliderect(((10.0, 10.0), (4.0, 4.0)))"),
]

collidepoint_tests = [
    ("C int", "c1.collidepoint(p1)"),
    ("NC int", "c1.collidepoint(p2)"),
    ("C float", "c1.collidepoint(p3)"),
    ("NC float", "c1.collidepoint(p4)"),
    ("C 2 int", "c1.collidepoint(10, 10)"),
    ("NC 2 int", "c1.collidepoint(1000, 1000)"),
    ("C 2 float", "c1.collidepoint(10.0, 10.0)"),
    ("NC 2 float", "c1.collidepoint(1000.0, 1000.0)"),
    ("C tup int", "c1.collidepoint((10, 10))"),
    ("NC tup int", "c1.collidepoint((1000, 1000))"),
    ("C tup float", "c1.collidepoint((10.0, 10.0))"),
    ("NC tup float", "c1.collidepoint((1000.0, 1000.0))"),
    ("C lst int", "c1.collidepoint([10, 10])"),
    ("NC lst int", "c1.collidepoint([1000, 1000])"),
    ("C lst float", "c1.collidepoint([10.0, 10.0])"),
    ("NC lst float", "c1.collidepoint([1000.0, 1000.0])"),
]

collideline_tests = [
    ("C line", "c1.collideline(l1)"),
    ("NC line", "c1.collideline(l2)"),
    ("C 4 int", "c1.collideline(0, 0, 10, 10)"),
    ("NC 4 int", "c1.collideline(0, 0, 1000, 1000)"),
    ("C 4 float", "c1.collideline(0.0, 0.0, 10.0, 10.0)"),
    ("NC 4 float", "c1.collideline(0.0, 0.0, 1000.0, 1000.0)"),
    ("C 1 int", "c1.collideline((0, 0, 10, 10))"),
    ("NC 1 int", "c1.collideline((0, 0, 10, -10))"),
    ("C 1 float", "c1.collideline((0.0, 0.0, 10.0, 10.0))"),
    ("NC 1 float", "c1.collideline((0.0, 0.0, 10.0, -10.0))"),
    ("C 2 tup int", "c1.collideline((0, 0), (10, 10))"),
    ("NC 2 tup int", "c1.collideline((0, 0), (10, -10))"),
    ("C 2 tup float", "c1.collideline((0.0, 0.0), (10.0, 10.0))"),
    ("NC 2 tup float", "c1.collideline((0.0, 0.0), (10.0, -10.0))"),
    ("C 1 tup 2 subtup int", "c1.collideline(((0, 0), (10, 10)))"),
    ("NC 1 tup 2 subtup int", "c1.collideline(((0, 0), (10, -10)))"),
    ("C 1 tup 2 subtup float", "c1.collideline(((0.0, 0.0), (10.0, 10.0)))"),
    ("NC 1 tup 2 subtup float", "c1.collideline(((0.0, 0.0), (10.0, -10.0)))"),
]

collideswith_tests = [
    ("C rect", "c1.collide(r1)"),
    ("NC rect", "c1.collide(r2)"),
    ("C circle", "c1.collide(c2)"),
    ("NC circle", "c1.collide(c2)"),
    ("C point int", "c1.collide(p1)"),
    ("NC point int", "c1.collide(p2)"),
    ("C point float", "c1.collide(p3)"),
    ("NC point float", "c1.collide(p4)"),
    ("C line", "c1.collide(l1)"),
    ("NC line", "c1.collide(l2)"),
]

contains_tests = [
    ("circle self", "c1.contains(c1)"),
    ("circle contained", "c4.contains(c1)"),
    ("circle not contained", "c4.contains(c3)"),
    ("circle intersecting", "c1.contains(c2)"),
    ("line contained", "c1.contains(l1)"),
    ("line not contained", "c1.contains(l2)"),
    ("line intersecting", "c1.contains(l3)"),
    ("poly contained", "c5.contains(poly1)"),
    ("poly not contained", "c5.contains(poly2)"),
    ("poly intersecting", "c5.contains(poly3)"),
    ("rect contained", "c1.contains(r1)"),
    ("rect not contained", "c1.contains(r2)"),
    ("rect intersecting", "c1.contains(r3)"),
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
    ("Collision: Circle", collidecircle_tests),
    ("Collision: Rect", colliderect_tests),
    ("Collision: Point", collidepoint_tests),
    ("Collision: Line", collideline_tests),
    ("Collision: Shape-General", collideswith_tests),
    ("Contains", contains_tests),
]

TestSuite("Geometry Module - Circle", GROUPS, GLOB).run_suite()
