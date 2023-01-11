import unittest

from pygame import Vector2, Vector3

import geometry
from geometry import Polygon, Line

import math

p1 = (12.0, 12.0)
p2 = (32.0, 43.0)
p3 = (22.0, 4.0)
p4 = (332.0, 64.0)
_some_vertices = [(10.0, 10.0), (20.0, 20.0), (30.0, 10.0)]


def _rotate_vertices(poly: Polygon, angle: float):
    """Rotates the vertices of a polygon by the given angle."""
    angle = math.radians(angle)
    rotated_vertices = []

    cos_a = math.cos(angle) - 1
    sin_a = math.sin(angle)
    for vertex in poly.vertices:
        dx = vertex[0] - poly.c_x
        dy = vertex[1] - poly.c_y
        rotated_vertices.append(
            (
                vertex[0] + dx * cos_a - dy * sin_a,
                vertex[1] + dx * sin_a + dy * cos_a,
            )
        )

    return rotated_vertices


def _calculate_center(poly: Polygon):
    """Calculates the center of a polygon."""
    x = 0
    y = 0
    for vertex in poly.vertices:
        x += vertex[0]
        y += vertex[1]
    return x / poly.verts_num, y / poly.verts_num


class PolygonTypeTest(unittest.TestCase):
    def test_Construction_invalid_type(self):
        """Checks whether passing wrong types to the constructor
        raises the appropriate errors
        """
        invalid_types = (
            None,
            [],
            "1",
            "123",
            (1,),
            [1, 2, 3],
            Vector2(1, 1),
            [p1, p2, p3, 32],
            [p1, p2, "(1, 1)"],
        )

        for value in invalid_types:
            with self.assertRaises(TypeError):
                po = Polygon(value)

    def test_Construction_invalid_arguments_number(self):
        """Checks whether passing the wrong number of arguments to the constructor
        raises the appropriate errors
        """

        arguments = (([p1, p2, p3], [p1, p4, p3]),)  # two args

        # No args
        with self.assertRaises(TypeError):
            po = Polygon()

        for arg_seq in arguments:
            with self.assertRaises(TypeError):
                po = Polygon(*arg_seq)

    def test_construction_invalid_polygon(self):
        """Checks whether the constructor works correctly with invalid polygons"""
        invalid_polygons = (
            [p1],  # 1
            [p1, p2],  # 2
        )

        for polygon in invalid_polygons:
            with self.assertRaises(TypeError):
                po = Polygon(polygon)

    def test_construction_tuple(self):
        """Checks whether the constructor works correctly with tuples"""
        po = Polygon((p1, p2, p3, p4))

        self.assertEqual(po.vertices, [p1, p2, p3, p4])

    def test_construction_list(self):
        """Checks whether the constructor works correctly with lists"""
        po = Polygon([p1, p2, p3, p4])
        po_2 = Polygon([p1, p2, p3])

        self.assertEqual(po.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, [p1, p2, p3])

    def test_construction_n_args(self):
        """Checks whether the constructor works correctly with n arguments"""
        po = Polygon(p1, p2, p3, p4)
        po_2 = Polygon(p1, p2, p3)

        self.assertEqual(po.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, [p1, p2, p3])

    def test_construction_frompolygon(self):
        """Checks whether the constructor works correctly with another polygon"""
        po = Polygon([p1, p2, p3, p4])
        po_2 = Polygon(po)

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, po.vertices)

    def test_perimeter(self):
        def get_perimeter(poly: geometry.Polygon) -> float:
            """Return the perimeter of the polygon."""

            def distance(p1, p2):
                return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

            perimeter = 0
            vertices = poly.vertices
            for i in range(len(vertices) - 1):
                perimeter += distance(vertices[i], vertices[i + 1])
            perimeter += distance(vertices[-1], vertices[0])
            return perimeter

        po = Polygon([p1, p2, p3, p4])
        expected_perimeter = get_perimeter(po)
        self.assertEqual(po.perimeter, expected_perimeter)

        po = Polygon([10.0, 10.0], [20.0, 20.0], [40.0, 50.0], [70.0, 900.0])
        expected_perimeter = get_perimeter(po)
        self.assertEqual(po.perimeter, expected_perimeter)

        po = Polygon((10.0, 45.0), (20.0, 4.5), (40.0, 77.45), (70.0, 900.0))
        expected_perimeter = get_perimeter(po)
        self.assertEqual(po.perimeter, expected_perimeter)

        po = Polygon([[6.0, 12.0], [95.0, 634.3], [21.0, 21.0]])
        expected_perimeter = get_perimeter(po)
        self.assertEqual(po.perimeter, expected_perimeter)

        po = Polygon(
            [[6.0, 12.0], [95.0, 634.3], [21.0, 21.0], [42.0, 1.0], [9.0, 72.0]]
        )
        expected_perimeter = get_perimeter(po)
        self.assertEqual(po.perimeter, expected_perimeter)

    def test_subscript(self):
        """Checks whether reassigning a vertex works correctly"""
        po = Polygon([p1, p2, p3, p4])

        po[0] = (70.0, 80.0)
        self.assertEqual(po[0], (70.0, 80.0))

        po[1] = [45.0, 38.0]
        self.assertEqual(po[1], (45.0, 38.0))

        po = Polygon([p1, p2, p3, p4])

        self.assertEqual(po[0], p1)
        self.assertEqual(po[1], p2)
        self.assertEqual(po[2], p3)
        self.assertEqual(po[3], p4)

        self.assertEqual(po[-3], p2)
        self.assertEqual(po[-2], p3)
        self.assertEqual(po[-1], p4)

        invalid_indexes = [4, 7, 100, -5, -7, -100]
        for invalid_index in invalid_indexes:
            with self.assertRaises(IndexError):
                po[invalid_index]

        po[0] = po[0]
        self.assertEqual(po[0], po[0])

        po2 = Polygon([p1, p2, p3, p4])

        valid_indexes = [0, 1, 2, 3, -1, -2, -3, -4]
        for valid_index in valid_indexes:
            self.assertEqual(po[valid_index], po2[valid_index])

    def test_length(self):
        po = Polygon((p1, p2, p3, p4))
        self.assertEqual(len(po), 4)

        po = Polygon([p1, p2, p3, p4, (54.0, 39.0)])
        self.assertEqual(len(po), 5)

        po = Polygon([p1, p2, p3, p4, (75.0, 83.0), [23.0, 12.0], [90.0, 134.0]])
        self.assertEqual(len(po), 7)

    def test_contains(self):
        po = Polygon([p1, p2, p3, p4])
        self.assertTrue(p1 in po)
        self.assertTrue(p2 in po)
        self.assertTrue(p3 in po)
        self.assertTrue(p4 in po)

        self.assertFalse([90.0, 47.0] in po)
        self.assertFalse((35.0, 9.0) in po)

        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1, (1, 2, 3))

        for value in invalid_types:
            with self.assertRaises(TypeError):
                value in po

        invalid_values = (
            [17.0, None],
            ["1", 47.0],
            (None, None),
            ("123", "456"),
            (17.0, "12"),
        )

        for value in invalid_values:
            with self.assertRaises(TypeError):
                value in po

    def test_construction_objwithpolygonattr(self):
        """Checks whether the constructor works correctly with an object with a polygon
        attribute"""

        class Test:
            def __init__(self, poly):
                self.polygon = poly

        test = Test([p1, p2, p3, p4])  # list
        test_2 = Test((p1, p2, p3, p4))  # tuple
        test_3 = Test(Polygon([p1, p2, p3, p4]))  # polygon

        po = Polygon(test)
        po_2 = Polygon(test_2)
        po_3 = Polygon(test_3)

        self.assertEqual(po.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_3.vertices, [p1, p2, p3, p4])

    def test_copy_invalid_args(self):
        """Checks whether the copy method raises the appropriate errors with invalid
        args"""

        args = [
            (1,),
            (1, 2),
            (1, 2, 3),
            (1, 2, 3, 4),
        ]
        po = Polygon([p1, p2, p3, p4])

        for value in args:
            with self.assertRaises(TypeError):
                po.copy(*value)

    def test_static_normal_polygon(self):
        center = (150.5, 100.1)
        radius = 50.2
        sides = 10
        angle = 20.6

        polygon_pg = geometry.regular_polygon(sides, center, radius, angle)
        vertices_pg = polygon_pg.vertices

        vertices = list(range(sides))

        fac = math.tau / sides
        radang = math.radians(angle)
        for i in range(sides // 2):
            ang = radang + i * fac
            radi_cos_a = radius * math.cos(ang)
            radi_sin_a = radius * math.sin(ang)
            vertices[i] = (center[0] + radi_cos_a, center[1] + radi_sin_a)

            vertices[sides // 2 + i] = (center[0] - radi_cos_a, center[1] - radi_sin_a)

        self.assertEqual(vertices_pg, vertices)

        invalid_types = [
            None,
            [],
            "1",
            "123",
            (1,),
            [1, 2, 3],
            [p1, p2, p3, 32],
            [p1, p2, "(1, 1)"],
        ]

        for invalid_type in invalid_types + [(1, 2)]:
            with self.assertRaises(TypeError):
                geometry.regular_polygon(invalid_type, (1, 2.2), 5.5, 1)

        for invalid_type in invalid_types:
            with self.assertRaises(TypeError):
                geometry.regular_polygon(5, invalid_type, 5.5, 1)

        for invalid_type in invalid_types + [(1, 2)]:
            with self.assertRaises(TypeError):
                geometry.regular_polygon(5, (1, 2.2), invalid_type, 1)

        for invalid_type in invalid_types + [(1, 2)]:
            with self.assertRaises(TypeError):
                geometry.regular_polygon(5, (1, 2.2), 5.5, invalid_type)

        with self.assertRaises(TypeError):
            geometry.regular_polygon(1, (1, 2.2), 5.5, 1, 5)

        with self.assertRaises(TypeError):
            geometry.regular_polygon()

        with self.assertRaises(ValueError):
            geometry.regular_polygon(-1, center, radius, angle)

        with self.assertRaises(ValueError):
            geometry.regular_polygon(2, center, radius, angle)

    def test_copy_return_type(self):
        """Checks whether the copy method returns a polygon."""
        po = Polygon([p1, p2, p3, p4])

        self.assertIsInstance(po.copy(), Polygon)
        self.assertEqual(type(po.copy()), Polygon)

    def test_copy(self):
        """Checks whether the copy method works correctly."""
        po = Polygon([p1, p2, p3, p4])
        po_center_x = po.c_x
        po_center_y = po.c_y
        po_2 = po.copy()

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, po.vertices)
        self.assertEqual(po_2.c_x, po_center_x)
        self.assertEqual(po_2.c_y, po_center_y)

    def test_center_x(self):
        """Makes sure changing center x component does change the positions of vertices properly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        poly_c_x = poly.c_x
        poly.c_x = 100.0

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 100.0 - poly_c_x
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(poly.vertices, vertices)

    def test_center_x__invalid_value(self):
        """Ensures the function can handle the polygon center x component by invalid data types."""
        poly = Polygon(_some_vertices.copy())
        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                poly.c_x = value

    def test_center_x__del(self):
        """Ensures that x component cannot be deleted."""
        poly = Polygon(_some_vertices.copy())
        with self.assertRaises(AttributeError):
            del poly.c_x

    def test_center_y(self):
        """Makes sure changing center y component does change the positions of vertices properly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        poly_c_y = poly.c_y
        poly.c_y = 100.0

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[1] += 100.0 - poly_c_y

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(poly.vertices, vertices)

    def test_center_y__invalid_value(self):
        """Ensures the function can handle the polygon center y component by invalid data types."""
        poly = Polygon(_some_vertices)
        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                poly.c_y = value

    def test_center_y__del(self):
        """Ensures that y component cannot be deleted."""
        poly = Polygon(_some_vertices)
        with self.assertRaises(AttributeError):
            del poly.c_y

    def test_center(self):
        """Makes sure that setting new center moves the vertices properly."""
        poly = Polygon(_some_vertices.copy())
        poly_center = poly.center
        poly.center = (200.0, 200.0)
        vertices = _some_vertices.copy()

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 200.0 - poly_center[0]
            vertex[1] += 200.0 - poly_center[1]

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.c_x, 200.0)
        self.assertEqual(poly.c_y, 200.0)

        pre_poly_vertices = poly.vertices
        poly.center = poly.center
        self.assertEqual(poly.vertices, pre_poly_vertices)

    def test_center__invalid_value(self):
        """Ensures the function can handle the polygon center component by invalid data types."""
        poly = Polygon(_some_vertices.copy())
        for value in (None, [], "1", (1,), [1, 2, 3], (1, "s"), (None, 3), (2, (3,))):
            with self.assertRaises(TypeError):
                poly.center = value

    def test_center__del(self):
        """Ensures that center component cannot be deleted."""
        poly = Polygon(_some_vertices.copy())
        with self.assertRaises(AttributeError):
            del poly.center

    def test__str__(self):
        """Checks whether the __str__ method works correctly."""
        p_str = "<Polygon(3, [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)])>"
        polygon = Polygon([(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)])
        self.assertEqual(str(polygon), p_str)
        self.assertEqual(polygon.__str__(), p_str)

    def test__repr__(self):
        """Checks whether the __repr__ method works correctly."""
        p_repr = "<Polygon(3, [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)])>"
        polygon = Polygon([(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)])
        self.assertEqual(repr(polygon), p_repr)
        self.assertEqual(polygon.__repr__(), p_repr)

    def test_as_segments(self):
        """Checks whether polygon segments are correct"""
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        self.assertEqual(
            poly.as_segments(),
            [
                Line((0, 0), (1, 0)),
                Line((1, 0), (1, 1)),
                Line((1, 1), (0, 1)),
                Line((0, 1), (0, 0)),
            ],
        )
        poly = Polygon([(123.23, 35.6), (56.4, 87.45), (43.1, 12.3)])
        self.assertEqual(
            poly.as_segments(),
            [
                Line((123.23, 35.6), (56.4, 87.45)),
                Line((56.4, 87.45), (43.1, 12.3)),
                Line((43.1, 12.3), (123.23, 35.6)),
            ],
        )
        poly = Polygon([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(
            poly.as_segments(),
            [Line((1, 2), (3, 4)), Line((3, 4), (5, 6)), Line((5, 6), (1, 2))],
        )

    def test_move(self):
        """Checks whether polygon moved correctly."""
        poly = Polygon(_some_vertices.copy())
        center_x = poly.c_x
        center_y = poly.c_y

        new_poly = poly.move(10.0, 10.0)
        vertices = _some_vertices.copy()

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 10.0
            vertex[1] += 10.0
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(vertices, new_poly.vertices)
        self.assertNotEqual(poly.vertices, new_poly.vertices)
        self.assertEqual(poly.vertices, _some_vertices)
        self.assertAlmostEqual(new_poly.c_x, center_x + 10.0)
        self.assertAlmostEqual(new_poly.c_y, center_y + 10.0)

    def test_move_inplace(self):
        """Checks whether polygon moved by (0, 0) and is the returned polygon identical."""
        poly = Polygon(_some_vertices.copy())
        poly_new = poly.move(0, 0)

        ##self.assertAlmostEquals(poly_new, poly)
        self.assertEqual(poly_new.c_x, poly.c_x)
        self.assertEqual(poly_new.c_y, poly.c_y)
        self.assertEqual(poly_new.vertices, poly.vertices)

    def test_move_invalid_args(self):
        """Tests whether function can handle invalid parameter types correctly."""
        vertices = _some_vertices.copy()
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Polygon(vertices))

        poly = Polygon(vertices)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.move(value)

    def test_move_argnum(self):
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.move(*arg)

    def test_move_return_type(self):
        poly = Polygon(_some_vertices.copy())

        self.assertIsInstance(poly.move(1, 1), Polygon)

    def test_move_ip(self):
        """Ensures that the vertices are moved correctly"""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        center_x = poly.c_x
        center_y = poly.c_y

        poly.move_ip(10.0, 10.0)
        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 10.0
            vertex[1] += 10.0
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.c_x, center_x + 10.0)
        self.assertEqual(poly.c_y, center_y + 10.0)

    def test_move_ip_inplace(self):
        """Ensures that moving the polygon by (0, 0) will not change its position."""
        poly = Polygon(_some_vertices.copy())
        vertices = _some_vertices.copy()
        center_x = poly.c_x
        center_y = poly.c_y

        poly.move_ip(0, 0)

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.c_x, center_x)
        self.assertEqual(poly.c_y, center_y)

    def test_move_ip_return_type(self):
        poly = Polygon(_some_vertices.copy())

        self.assertEqual(type(poly.move_ip(0, 0)), type(None))

    def test_move_ip_invalid_args(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (
            None,
            [],
            "1",
            (1,),
            Vector3(1, 1, 3),
            Polygon(_some_vertices.copy()),
        )

        poly = Polygon(_some_vertices.copy())

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.move_ip(value)

    def test_move_ip_argnum(self):
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.move_ip(*arg)

    def test_rotate(self):
        """Tests whether the polygon rotates correctly."""
        vertices = _some_vertices.copy()
        gen_poly = Polygon(vertices)

        angles = [
            0.0,
            -0.0,
            1.0,
            -1.0,
            90.0,
            -90.0,
            180.0,
            -180.0,
            360.0,
            -360.0,
            720.0,
            -720.0,
            23.31545,
            -23.31545,
        ]

        for angle in angles:
            poly = gen_poly.copy()
            rotated_vertices = _rotate_vertices(poly, angle)
            p2 = poly.rotate(angle)
            for v1, v2 in zip(p2.vertices, rotated_vertices):
                self.assertAlmostEqual(v1[0], v2[0])
                self.assertAlmostEqual(v1[1], v2[1])

    def test_rotate_invalid_args(self):
        """Tests whether the function can handle invalid parameter types correctly."""
        invalid_types = (
            None,
            [],
            "1",
            (1,),
            Vector2(1, 1),
            Vector3(1, 1, 3),
            Polygon(_some_vertices.copy()),
        )

        poly = Polygon(_some_vertices.copy())

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.rotate(value)

    def test_rotate_argnum(self):
        """Tests whether the function can handle invalid parameter number correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.rotate(*arg)

    def test_rotate_return_type(self):
        """Tests whether the function returns the correct type."""
        poly = Polygon(_some_vertices.copy())

        angles = [-0.0, 0.0, 1.0, 90.0, 180.0, 360.0, 720.0, 23.31545, -23.31545]

        for angle in angles:
            self.assertIsInstance(poly.rotate(angle), Polygon)

        class TestPolygon(Polygon):
            pass

        poly2 = TestPolygon(_some_vertices.copy())
        for angle in angles:
            self.assertIsInstance(poly2.rotate(angle), TestPolygon)

    def test_rotate_ip(self):
        """Tests whether the polygon rotates correctly."""
        vertices = _some_vertices.copy()
        gen_poly = Polygon(vertices)

        angles = [
            0.0,
            -0.0,
            1.0,
            -1.0,
            90.0,
            -90.0,
            180.0,
            -180.0,
            360.0,
            -360.0,
            720.0,
            -720.0,
            23.31545,
            -23.31545,
        ]

        for angle in angles:
            poly = gen_poly.copy()
            rotated_vertices = _rotate_vertices(poly, angle)
            poly.rotate_ip(angle)
            for v1, v2 in zip(poly.vertices, rotated_vertices):
                self.assertAlmostEqual(v1[0], v2[0])
                self.assertAlmostEqual(v1[1], v2[1])

    def test_rotate_ip_conjugate(self):
        vertices = _some_vertices.copy()
        gen_poly = Polygon(vertices)

        angles = [-90, -180, -270]

        for angle in angles:

            poly1 = gen_poly.copy()
            poly1.rotate_ip(angle)

            conjugate_angle = angle + 360
            poly2 = gen_poly.copy()
            poly2.rotate_ip(conjugate_angle)

            for v1, v2 in zip(poly1.vertices, poly2.vertices):
                self.assertAlmostEqual(v1[0], v2[0])
                self.assertAlmostEqual(v1[1], v2[1])

    def test_rotate_conjugate(self):

        vertices = _some_vertices.copy()
        gen_poly = Polygon(vertices)

        angles = [-90, -180, -270]

        for angle in angles:

            poly1 = gen_poly.copy()
            po1 = poly1.rotate(angle)

            conjugate_angle = angle + 360
            poly2 = gen_poly.copy()
            po2 = poly2.rotate(conjugate_angle)

            for v1, v2 in zip(po1.vertices, po2.vertices):
                self.assertAlmostEqual(v1[0], v2[0])
                self.assertAlmostEqual(v1[1], v2[1])

    def test_rotate_ip_invalid_args(self):
        """Tests whether the function can handle invalid parameter types correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_types = (
            None,
            [],
            "1",
            (1,),
            Vector2(1, 1),
            Vector3(1, 1, 3),
            Polygon(_some_vertices.copy()),
        )

        poly = Polygon(_some_vertices.copy())

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.rotate_ip(value)

    def test_collidepoint(self):
        """Tests whether the collidepoint method works correctly."""
        poly = Polygon(_some_vertices.copy())

        # check that the center of the polygon collides with the polygon
        self.assertTrue(poly.collidepoint(poly.center))
        self.assertTrue(poly.collidepoint(*poly.center))

        # check that each vertex collides with the polygon
        for vertex in poly.vertices:
            self.assertTrue(poly.collidepoint(vertex))
            self.assertTrue(poly.collidepoint(*vertex))

        # check that a point outside the polygon does not collide with the polygon
        self.assertFalse(poly.collidepoint((100.0, 100.0)))
        self.assertFalse(poly.collidepoint(100.0, 100.0))

        # check that a point on the edge of the polygon collides with the polygon
        self.assertTrue(poly.collidepoint((15.0, 15.0)))
        self.assertTrue(poly.collidepoint(15.0, 15.0))

        # check that a point sligtly outside the polygon does not collide with the polygon
        e = 0.000000000000001
        self.assertFalse(poly.collidepoint((15.0 - e, 15.0)))
        self.assertFalse(poly.collidepoint(15.0 - e, 15.0))

    def test_collidepoint_invalid_args(self):
        """Tests whether the collidepoint method correctly handles invalid parameters."""
        poly = Polygon(_some_vertices.copy())

        invalid_types = (
            None,
            [],
            "1",
            (1,),
            Vector3(1, 1, 3),
            Polygon(_some_vertices.copy()),
        )

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.collidepoint(value)

    def test_rotate_ip_argnum(self):
        """Tests whether the function can handle invalid parameter number correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1), (1, 1, 1, 1)]

        with self.assertRaises(TypeError):
            poly.rotate_ip()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.rotate_ip(*arg)

    def test_rotate_ip_return_type(self):
        """Tests whether the function returns the correct type."""
        poly = Polygon(_some_vertices.copy())

        self.assertEqual(type(poly.rotate_ip(0.0)), type(None))
        self.assertEqual(type(poly.rotate_ip(1.0)), type(None))
        self.assertEqual(type(poly.rotate_ip(-1.0)), type(None))

    def test_rotate_ip_inplace(self):
        """Ensures that rotating the polygon by 0 degrees will not change its position."""
        poly = Polygon(_some_vertices.copy())
        vertices = _some_vertices.copy()
        center_x = poly.c_x
        center_y = poly.c_y

        poly.rotate_ip(0)

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.c_x, center_x)
        self.assertEqual(poly.c_y, center_y)

    def test_rotate_inplace(self):
        """Ensures that rotating the polygon by 0 degrees will not change its position."""
        poly = Polygon(_some_vertices.copy())
        vertices = _some_vertices.copy()
        center_x = poly.c_x
        center_y = poly.c_y

        new_poly = poly.rotate(0)

        self.assertEqual(new_poly.vertices, poly.vertices)
        self.assertEqual(new_poly.c_x, poly.c_x)
        self.assertEqual(new_poly.c_y, poly.c_y)

        self.assertEqual(new_poly.vertices, vertices)
        self.assertEqual(new_poly.c_x, center_x)
        self.assertEqual(new_poly.c_y, center_y)

    def test_collidepoint_argnum(self):
        """Tests whether the collidepoint method correctly handles invalid parameter
        numbers."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [((1, 1), (1, 1)), ((1, 1), (1, 1), (1, 1))]

        with self.assertRaises(TypeError):
            poly.collidepoint()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.collidepoint(*arg)

    def test_collidepoint_return_type(self):
        """Tests whether the collidepoint method returns a boolean."""

        poly = Polygon(_some_vertices.copy())

        self.assertIsInstance(poly.collidepoint(poly.center), bool)
        self.assertIsInstance(poly.collidepoint(*poly.center), bool)

        for vertex in poly.vertices:
            self.assertIsInstance(poly.collidepoint(vertex), bool)
            self.assertIsInstance(poly.collidepoint(*vertex), bool)

        self.assertIsInstance(poly.collidepoint((100.0, 100.0)), bool)
        self.assertIsInstance(poly.collidepoint(100.0, 100.0), bool)

        e = 0.000000000000001
        self.assertIsInstance(poly.collidepoint((15.0 - e, 15.0)), bool)
        self.assertIsInstance(poly.collidepoint(15.0 - e, 15.0), bool)

    def test_assign_subscript(self):
        """Tests whether assigning to a subscript works correctly."""
        new_vertices = [(1.11, 32), (-2, 2.0), (3.23, 3.0)]
        poly = Polygon(_some_vertices.copy())

        for i, vertex in enumerate(new_vertices):
            poly[i] = vertex

            self.assertEqual(poly[i], vertex)

            expected_center = _calculate_center(poly)

            # check that the new center of the polygon is correct
            self.assertAlmostEqual(expected_center[0], poly.c_x, places=14)
            self.assertAlmostEqual(expected_center[1], poly.c_y, places=14)

    def test_get_subscript(self):
        """Tests whether subscripting a polygon works correctly."""
        poly = Polygon(_some_vertices.copy())

        for i, vertex in enumerate(poly.vertices):
            self.assertEqual(poly[i], vertex)

        # test for negative indices
        poly_vertices = poly.vertices
        for i in range(poly.verts_num):
            self.assertEqual(poly[-i], poly_vertices[-i])

    def test_get_subscript_invalid_args(self):
        """Tests whether getting a subscript with invalid arguments works correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = ["1", (1,), Vector3(1, 1, 3), Polygon(_some_vertices.copy())]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly[arg]

    def test_assign_subscript_invalid_assignment(self):
        """Tests whether assigning invalid types to a subscript with behaves correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = ["1", (1,), Vector3(1, 1, 3), Polygon(_some_vertices.copy())]

        # test for positive indices
        for i, arg in enumerate(invalid_args):
            with self.assertRaises(TypeError):
                poly[i] = arg

        # test for negative indices
        for i in range(poly.verts_num):
            with self.assertRaises(TypeError):
                poly[-i] = invalid_args[i]


if __name__ == "__main__":
    unittest.main()
