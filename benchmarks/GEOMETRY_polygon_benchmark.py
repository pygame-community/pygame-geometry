from benchmark_utils import TestSuite

from geometry import Polygon

po3 = Polygon([(50, 50), (50, 100), (70, 55)])
po4 = Polygon([(50, 50), (50, 100), (70, 55), (100, 23)])

GLOB = {
    "Polygon": Polygon,
    "po3": po3,
    "po4": po4,
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
    ("(3) Polygon", "Polygon(po3)"),
    ("(3) int 1", "Polygon([(50, 50), (50, 100), (70, 55)])"),
    ("(3) float 1", "Polygon([(50.0, 50.0), (50.0, 100.0), (70.0, 55.0)])"),
    ("(3) int 3", "Polygon((50, 50), (50, 100), (70, 55))"),
    ("(3) float 3", "Polygon((50.0, 50.0), (50.0, 100.0), (70.0, 55.0))"),
    ("(4) Polygon", "Polygon(po4)"),
    ("(4) int 1", "Polygon([(50, 50), (50, 100), (70, 55), (100, 23)])"),
    (
        "(4) float 1",
        "Polygon([(50.0, 50.0), (50.0, 100.0), (70.0, 55.0), (100.0, 23.0)])",
    ),
    ("(4) int 3", "Polygon((50, 50), (50, 100), (70, 55), (100, 23))"),
    (
        "(4) float 3",
        "Polygon((50.0, 50.0), (50.0, 100.0), (70.0, 55.0), (100.0, 23.0))",
    ),
]

getters_tests = [
    ("vertices 3", "po3.vertices"),
    ("verts_num 3", "po3.verts_num"),
    ("vertices 4", "po4.vertices"),
    ("verts_num 4", "po4.verts_num"),
]

setters_tests = [
    ("vertices int", "po4.vertices = [(50, 50), (50, 100), (70, 55), (100, 23)]"),
    (
        "vertices float",
        "po4.vertices = [(50.0, 50.0), (50.0, 100.0), (70.0, 55.0), (100.0, 23.0)]",
    ),
]

GROUPS = [
    ("Creation", creation_tests),
    ("Attribute Getters", getters_tests),
]

TestSuite("Geometry Module - Polygon", GROUPS, GLOB).run_suite()
