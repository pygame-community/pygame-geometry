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


class ObjWithPolyAttribute:
    def __init__(self, polygon=None):
        self.polygon = polygon


class ObjWithPolyMethodAttribute:
    def __init__(self, polygon=None):
        self._poly = polygon

    def polygon(self):
        return self._poly


triang_vertices = [(50, 50), (50, 100), (70, 55)]
GLOB = {
    "Polygon": Polygon,
    "po3": Polygon(triang_vertices),
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
    "poly3_int_list": triang_vertices,
    "poly4_int_list": [(50, 50), (50, 100), (70, 55), (100, 23)],
    "poly3_float_list": [(50.0, 50.0), (50.0, 100.0), (70.0, 55.0)],
    "poly4_float_list": [(50.0, 50.0), (50.0, 100.0), (70.0, 55.0), (100.0, 23.0)],
    "poly_attribute": ObjWithPolyAttribute(triang_vertices),
    "poly_method_attribute": ObjWithPolyMethodAttribute(triang_vertices),
    "poly_attribute_poly": ObjWithPolyAttribute(Polygon(triang_vertices)),
    "poly_method_attribute_poly": ObjWithPolyMethodAttribute(Polygon(triang_vertices)),
}

instatiation_tests = [
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
    ("Polygon from ObjWithPolyAttribute 3", "Polygon(poly_attribute)"),
    ("Polygon from ObjWithPolyMethodAttribute 3", "Polygon(poly_method_attribute)"),
    ("Polygon from ObjWithPolyAttribute poly 3", "Polygon(poly_attribute_poly)"),
    ("Polygon from ObjWithPolyMethodAttribute poly 3", "Polygon(poly_attribute_poly)"),
]

getters_tests = [
    ("vertices 3", "po3.vertices"),
    ("verts_num 3", "po3.verts_num"),
    ("vertices 4", "po4.vertices"),
    ("verts_num 4", "po4.verts_num"),
    ("centerx 3", "po3.centerx"),
    ("centery 3", "po3.centery"),
    ("centerx 4", "po4.centerx"),
    ("centery 4", "po4.centery"),
    ("center 3", "po3.center"),
    ("center 4", "po4.center"),
    ("perimeter 3", "po3.perimeter"),
    ("perimeter 4", "po4.perimeter"),
    ("perimeter 100", "po100.perimeter"),
]

setters_tests = [
    # ("vertices int", "po4.vertices = [p1_i, p2_i, p3_i, p4_i]"),
    # ("vertices float", "po4.vertices = [p1_f, p2_f, p3_f, p4_f]"),
    ("center int", "po4.center = p1_i"),
    ("center float", "po4.center = p1_f"),
    ("centerx int", "po4.centerx = 50"),
    ("centery int", "po4.centery = 50"),
    ("centerx float", "po4.centerx = 50.0"),
    ("centery float", "po4.centery = 50.0"),
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

rotate_tests = [
    ("0", "po100.rotate(0.0)"),
    ("-0", "po100.rotate(-0.0)"),
    ("90", "po100.rotate(90.0)"),
    ("-90", "po100.rotate(-90.0)"),
    ("180", "po100.rotate(180.0)"),
    ("-180", "po100.rotate(-180.0)"),
    ("270", "po100.rotate(270.0)"),
    ("-270", "po100.rotate(-270.0)"),
    ("360", "po100.rotate(360.0)"),
    ("-360", "po100.rotate(-360.0)"),
    ("12", "po100.rotate(12.0)"),
    ("-12", "po100.rotate(-12.0)"),
]

rotate_ip_tests = [
    ("0", "po100.rotate_ip(0.0)"),
    ("-0", "po100.rotate_ip(-0.0)"),
    ("90", "po100.rotate_ip(90.0)"),
    ("-90", "po100.rotate_ip(-90.0)"),
    ("180", "po100.rotate_ip(180.0)"),
    ("-180", "po100.rotate_ip(-180.0)"),
    ("270", "po100.rotate_ip(270.0)"),
    ("-270", "po100.rotate_ip(-270.0)"),
    ("360", "po100.rotate_ip(360.0)"),
    ("-360", "po100.rotate_ip(-360.0)"),
    ("12", "po100.rotate_ip(12.0)"),
    ("-12", "po100.rotate_ip(-12.0)"),
]

collidepoint_tests = [
    ("C int 2", "po100.collidepoint((0, 0))"),
    ("NC int 2", "po100.collidepoint((0, 1000))"),
    ("C float 2", "po100.collidepoint((0.0, 0.0))"),
    ("NC float 2", "po100.collidepoint((0.0, 1000.0))"),
    ("C int tuple", "po100.collidepoint((0, 0))"),
    ("NC int tuple", "po100.collidepoint((0, 1000))"),
    ("C float tuple", "po100.collidepoint((0.0, 0.0))"),
    ("NC float tuple", "po100.collidepoint((0.0, 1000.0))"),
    ("C int list", "po100.collidepoint([0, 0])"),
    ("NC int list", "po100.collidepoint([0, 1000])"),
    ("C float list", "po100.collidepoint([0.0, 0.0])"),
    ("NC float list", "po100.collidepoint([0.0, 1000.0])"),
]

as_rect_tests = [
    ("3", "po3.as_rect()"),
    ("4", "po4.as_rect()"),
    ("100", "po100.as_rect()"),
]

subscript_assignment_tests = [
    ("[0] = 10, int", "po100[0] = (10, 10)"),
    ("[0] = 10.0, float", "po100[0] = (10.0, 10.0)"),
    ("[10] = 10, int", "po100[10] = (10, 10)"),
    ("[10] = 10.0, float", "po100[10] = (10.0, 10.0)"),
    ("[-1] = 10, int", "po100[-1] = (10, 10)"),
    ("[-1] = 10.0, float", "po100[-1] = (10.0, 10.0)"),
]

subscript_tests = [
    ("[0]", "po100[0]"),
    ("[10]", "po100[10]"),
    ("[100]", "po100[99]"),
    ("[-1]", "po100[-1]"),
]

scale_tests = [
    ("2.0", "po100.scale(2)"),
    ("1.0", "po100.scale(1)"),
    ("0.5", "po100.scale(0.5)"),
    ("0.1", "po100.scale(0.1)"),
]

scale_ip_tests = [
    ("2.0", "po100.scale_ip(2)"),
    ("1.0", "po100.scale_ip(1)"),
    ("0.5", "po100.scale_ip(0.5)"),
    ("0.1", "po100.scale_ip(0.1)"),
]

GROUPS = [
    ("Instatiation", instatiation_tests),
    ("Attribute Getters", getters_tests),
    ("Attribute Setters", setters_tests),
    ("Copy", copy_tests),
    ("Move", move_tests),
    ("Move_ip", move_ip_tests),
    ("Rotate", rotate_tests),
    ("Rotate_ip", rotate_ip_tests),
    ("Collidepoint", collidepoint_tests),
    ("Get Bounding Box", as_rect_tests),
    ("Subscript", subscript_tests),
    ("Subscript Assignment", subscript_assignment_tests),
    ("Scale", scale_tests),
    ("Scale_ip", scale_ip_tests),
]

if __name__ == "__main__":
    TestSuite("Geometry Module - Polygon", GROUPS, GLOB).run_suite()
