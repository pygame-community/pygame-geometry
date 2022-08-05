from pygame import Rect

from benchmark_utils import test_group
from shapes.circle import Circle
from geometry import Circle as CCircle

NUM = 1000000
r1 = Rect(0, 0, 10, 10)
r2 = Rect(10, 10, 4, 4)
r3 = Rect(0, 0, 100, 100)

c1 = Circle(10, 10, 10)
c2 = Circle(20, 5, 15)
c3 = Circle(50, 50, 15)
c4 = Circle(10, 10, 15)

GLOB = {
    "Circle": Circle,
    "CCircle": CCircle,
    "r1": r1,
    "r2": r2,
    "r3": r3,
    "c1": c1,
    "c2": c2,
    "c3": c3,
    "c4": c4,
}

# === Test Names ===
general_test_names = (
    "Instatiation",
    "x attrib",
    "y attrib",
    "radius attrib",
    "copy",
    "update",
    # "move",
    # "move_ip",
    # "move_to",
    # "move_to_ip",
    # "scale_by",
    # "scale_by_ip",
    "as_rect",
)
T_collision_names = (
    "colliding",
    "non colliding",
    "a inside b",
    "b inside a",
)
T_collision_names_2 = (
    "rect",
    "circle",
    "point"
)
# ==========================

# === Test Function Calls ===
general_test_stmts = [
    "Circle(0, 0, 5)",
    "c1.x",
    "c1.y",
    "c1.r",
    "c1.copy()",
    "c1.update(1, 1, 3)",
    # "c1.move(1, 1)",
    # "c1.move_ip(1, 1)",
    # "c1.move_to(1, 1)",
    # "c1.move_to_ip(1, 1)",
    # "c1.scale_by(1.2)",
    # "c1.scale_by_ip(1.01)",
    "c1.as_rect()",
]

T1_calls = (
    "c1.collidecircle(c2)",
    "c1.collidecircle(c3)",
    "c1.collidecircle(c4)",
    "c4.collidecircle(c1)",
)
T2_calls = (
    "c1.colliderect(r1)",
    "c3.colliderect(r1)",
    "c3.colliderect(r3)",
    "c1.colliderect(r2)",
)

T3_calls = (
    "c1.collideswith(r1)",
    "c1.collideswith(c2)",
    "c1.collideswith((10, 10))",
)
# ==========================

test_group("Py Circle General Tests", general_test_stmts, GLOB, general_test_names, NUM)
test_group("Py Circle-Circle", T1_calls, GLOB, T_collision_names, NUM)
test_group("Py Circle-Rect", T2_calls, GLOB, T_collision_names, NUM)
test_group("Py Circle-Shape", T3_calls, GLOB, T_collision_names_2, NUM)

GLOB["c1"] = CCircle(10, 10, 10)
GLOB["c2"] = CCircle(20, 5, 15)
GLOB["c3"] = CCircle(50, 50, 15)
GLOB["c4"] = CCircle(10, 10, 15)
general_test_stmts[0] = "CCircle(0, 0, 5)"

test_group("C Circle General Tests", general_test_stmts, GLOB, general_test_names, NUM)
test_group("C Circle-Circle", T1_calls, GLOB, T_collision_names, NUM)
test_group("C Circle-Rect", T2_calls, GLOB, T_collision_names, NUM)
test_group("C Circle-Shape", T3_calls, GLOB, T_collision_names_2, NUM)
