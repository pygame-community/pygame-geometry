from benchmark_utils import TestSuite

from geometry import Polygon, regular_polygon

# === Tests ===
# Each test consists of a tuple of: (name, call)
# The name is a string containing the name of the test
# The call is a string containing the code to be timed
# every test is run CPT times and the average time is
# calculated across REP runs
# the formula is time = (time per CPT calls repeated REP times) / REP
# ====================================================

GLOB = {
    "Polygon": Polygon,
    "po3": Polygon([(50, 50), (50, 100), (70, 55)]),
    "po4": Polygon([(50, 50), (50, 100), (70, 55), (100, 23)]),
    "po100": regular_polygon(100, (50, 50), 50),
    "p1_i": (50, 50),
    "p2_i": (50, 100),
    "p3_i": (70, 55),
    "p4_i": (100, 23),
    "p1_f": (50.0, 50.0),
    "p2_f": (50.0, 100.0),
    "p3_f": (70.0, 55.0),
    "p4_f": (100.0, 23.0),
    "poly3_int_list": [(50, 50), (50, 100), (70, 55)],
    "poly4_int_list": [(50, 50), (50, 100), (70, 55), (100, 23)],
    "poly3_float_list": [(50.0, 50.0), (50.0, 100.0), (70.0, 55.0)],
    "poly4_float_list": [(50.0, 50.0), (50.0, 100.0), (70.0, 55.0), (100.0, 23.0)],
}

creation_tests = [
    ("(3) polygon", "Polygon(po3)"),
    ("(4) polygon", "Polygon(po4)"),
    ("(3) int 3 args", "Polygon(p1_i, p2_i, p3_i)"),
    ("(3) float 3 args", "Polygon(p1_f, p2_f, p3_f)"),
    ("(4) int 4 args", "Polygon(p1_i, p2_i, p3_i, p4_i)"),
    ("(4) float 4 args", "Polygon(p1_f, p2_f, p3_f, p4_f)"),
    ("(3) int 1 arg", "Polygon(poly3_int_list)"),
    ("(3) float 1 arg", "Polygon(poly3_float_list)"),
    ("(4) int 1 arg", "Polygon(poly4_int_list)"),
    ("(4) float 1 arg", "Polygon(poly4_float_list)"),
]

getters_tests = [
    ("vertices 3", "po3.vertices"),
    ("verts_num 3", "po3.verts_num"),
    ("vertices 4", "po4.vertices"),
    ("verts_num 4", "po4.verts_num"),
    ("c_x 3", "po3.c_x"),
    ("c_y 3", "po3.c_y"),
    ("c_x 4", "po4.c_x"),
    ("c_y 4", "po4.c_y"),
    ("center 3", "po3.center"),
    ("center 4", "po4.center"),
]

setters_tests = [
    # ("vertices int", "po4.vertices = [p1_i, p2_i, p3_i, p4_i]"),
    # ("vertices float", "po4.vertices = [p1_f, p2_f, p3_f, p4_f]"),
    ("center int", "po4.center = p1_i"),
    ("center float", "po4.center = p1_f"),
    ("c_x int", "po4.c_x = 50"),
    ("c_y int", "po4.c_y = 50"),
    ("c_x float", "po4.c_x = 50.0"),
    ("c_y float", "po4.c_y = 50.0"),
]

copy_tests = [
    ("copy 3", "po3.copy()"),
    ("copy 4", "po4.copy()"),
]

move_tests = [
    ("int (x-x)", "po100.move((10, 10))"),
    ("int (0-x)", "po100.move((0, 10))"),
    ("int (x-0)", "po100.move((10, 0))"),
    ("int (0-0)", "po100.move((0, 0))"),
    ("float (x-x)", "po100.move((10.0, 10.0))"),
    ("float (0-x)", "po100.move((0.0, 10.0))"),
    ("float (x-0)", "po100.move((10.0, 0.0))"),
    ("float (0-0)", "po100.move((0.0, 0.0))"),
    ("int x-x", "po100.move(10, 10)"),
    ("int 0-x", "po100.move(0, 10)"),
    ("int x-0", "po100.move(10, 0)"),
    ("int 0-0", "po100.move(0, 0)"),
    ("float x-x", "po100.move(10.0, 10.0)"),
    ("float 0-x", "po100.move(0.0, 10.0)"),
    ("float x-0", "po100.move(10.0, 0.0)"),
    ("float 0-0", "po100.move(0.0, 0.0)"),
]

move_ip_tests = [
    ("int (x-x)", "po100.move_ip((10, 10))"),
    ("int (0-x)", "po100.move_ip((0, 10))"),
    ("int (x-0)", "po100.move_ip((10, 0))"),
    ("int (0-0)", "po100.move_ip((0, 0))"),
    ("float (x-x)", "po100.move_ip((10.0, 10.0))"),
    ("float (0-x)", "po100.move_ip((0.0, 10.0))"),
    ("float (x-0)", "po100.move_ip((10.0, 0.0))"),
    ("float (0-0)", "po100.move_ip((0.0, 0.0))"),
    ("int x-x", "po100.move_ip(10, 10)"),
    ("int 0-x", "po100.move_ip(0, 10)"),
    ("int x-0", "po100.move_ip(10, 0)"),
    ("int 0-0", "po100.move_ip(0, 0)"),
    ("float x-x", "po100.move_ip(10.0, 10.0)"),
    ("float 0-x", "po100.move_ip(0.0, 10.0)"),
    ("float x-0", "po100.move_ip(10.0, 0.0)"),
    ("float 0-0", "po100.move_ip(0.0, 0.0)"),
]

GROUPS = [
    ("Creation", creation_tests),
    ("Attribute Getters", getters_tests),
    ("Attribute Setters", setters_tests),
    ("Copy", copy_tests),
    ("Move", move_tests),
    ("Move_ip", move_ip_tests),
]

if __name__ == "__main__":
    TestSuite("Geometry Module - Polygon", GROUPS, GLOB).run_suite()
