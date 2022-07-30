from pygame import Rect

from benchmark_utils import test_group
from shapes.circle import Circle

r1 = Rect(0, 0, 10, 10)
r2 = Rect(10, 10, 4, 4)
r3 = Rect(0, 0, 100, 100)

c1 = Circle((10, 10), 10)
c2 = Circle((20, 5), 15)
c3 = Circle((50, 50), 15)
c4 = Circle((10, 10), 15)

GLOB = {
    "Circle": Circle,
    "r1": r1,
    "r2": r2,
    "r3": r3,
    "c1": c1,
    "c2": c2,
    "c3": c3,
    "c4": c4
}

general_test_names = (
    "Instatiation",
    "x attrib",
    "y attrib",
    "radius attrib",
    "copy",
    "update",
    "move",
    "move_ip",
    "move_to",
    "move_to_ip",
    "scale",
    "scale_ip",
    "scale_by",
    "scale_by_ip",
    "as_rect"
)
general_test_stmts = (
    "Circle((0, 0), 5)",
    "c1.x",
    "c1.y",
    "c1.radius",
    "c1.copy()",
    "c1.update((1, 1), 3)",
    "c1.move(1, 1)",
    "c1.move_ip(1, 1)",
    "c1.move_to(1, 1)",
    "c1.move_to_ip(1, 1)",
    "c1.scale(10)",
    "c1.scale_ip(10)",
    "c1.scale_by(1.2)",
    "c1.scale_by(1.2)",
    "c1.scale_by_ip(1.01)",
    "c1.as_rect()",
)
test_group("Circle General Tests", general_test_stmts, GLOB, general_test_names)

collision_test_names = ("colliding", "non colliding",
                        "a inside b", "b inside a", "collides_with")
c_c_test_stmts = (
    "c1.collidecircle(c2)",
    "c1.collidecircle(c3)",
    "c1.collidecircle(c4)",
    "c4.collidecircle(c1)",
    "c1.collides_with(c2)"
)
test_group("Circle-Circle", c_c_test_stmts, GLOB, collision_test_names)

c_r_test_stmts = (
    "c1.colliderect(r1)",
    "c3.colliderect(r1)",
    "c3.colliderect(r3)",
    "c1.colliderect(r2)",
    "c1.collides_with(r1)",
)
test_group("Circle-Rect", c_r_test_stmts, GLOB, collision_test_names)
