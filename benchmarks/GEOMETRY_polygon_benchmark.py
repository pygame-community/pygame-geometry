from benchmark_utils import TestSuite

from geometry import Polygon

p1_i = (50, 50)
p2_i = (50, 100)
p3_i = (70, 55)
p4_i = (100, 23)

p1_f = (50.0, 50.0)
p2_f = (50.0, 100.0)
p3_f = (70.0, 55.0)
p4_f = (100.0, 23.0)

po3 = Polygon([(50, 50), (50, 100), (70, 55)])
po4 = Polygon([(50, 50), (50, 100), (70, 55), (100, 23)])

GLOB = {
    "Polygon": Polygon,
    "po3": po3,
    "po4": po4,
    "p1_i": p1_i,
    "p2_i": p2_i,
    "p3_i": p3_i,
    "p4_i": p4_i,
    "p1_f": p1_f,
    "p2_f": p2_f,
    "p3_f": p3_f,
    "p4_f": p4_f,
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
    ("(3) poly", "Polygon(po3)"),
    ("(4) Polygon", "Polygon(po4)"),
    ("(3) int 3 args", "Polygon(p1_i, p2_i, p3_i)"),
    ("(3) float 3 args", "Polygon(p1_f, p2_f, p3_f)"),
    ("(4) int 4 args", "Polygon(p1_i, p2_i, p3_i, p4_i)"),
    ("(4) float 4 args", "Polygon(p1_f, p2_f, p3_f, p4_f)"),
    ("(3) int 1 arg", "Polygon([p1_i, p2_i, p3_i])"),
    ("(3) float 1 arg", "Polygon([p1_f, p2_f, p3_f])"),
    ("(4) int 1 arg", "Polygon([p1_i, p2_i, p3_i, p4_i])"),
    ("(4) float 1 arg", "Polygon([p1_f, p2_f, p3_f, p4_f])"),
]

getters_tests = [
    ("vertices 3", "po3.vertices"),
    ("verts_num 3", "po3.verts_num"),
    ("vertices 4", "po4.vertices"),
    ("verts_num 4", "po4.verts_num"),
]

setters_tests = [
    ("vertices int", "po4.vertices = [p1_i, p2_i, p3_i, p4_i]"),
    ("vertices float", "po4.vertices = [p1_f, p2_f, p3_f, p4_f]"),
]

copy_tests = [
    ("copy 3", "po3.copy()"),
    ("copy 4", "po4.copy()"),
]

GROUPS = [
    ("Creation", creation_tests),
    ("Attribute Getters", getters_tests),
    ("Copy", copy_tests),
]

if __name__ == "__main__":
    TestSuite("Geometry Module - Polygon", GROUPS, GLOB).run_suite()
