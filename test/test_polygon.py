import unittest
import random

from pygame import Vector2, Vector3, Rect

import geometry
from geometry import Polygon, Circle, Line, regular_polygon

import math

p1 = (12.0, 12.0)
p2 = (32.0, 43.0)
p3 = (22.0, 4.0)
p4 = (332.0, 64.0)
_some_vertices = [(10.0, 10.0), (20.0, 20.0), (30.0, 10.0)]


def _rotate_vertices(poly: Polygon, angle: float, center=None):
    """Rotates the vertices of a polygon by the given angle."""
    angle = math.radians(angle)
    rotated_vertices = []

    cos_a = math.cos(angle) - 1
    sin_a = math.sin(angle)

    cx = poly.centerx if center is None else center[0]
    cy = poly.centery if center is None else center[1]

    for vertex in poly.vertices:
        dx = vertex[0] - cx
        dy = vertex[1] - cy
        rotated_vertices.append(
            (
                vertex[0] + dx * cos_a - dy * sin_a,
                vertex[1] + dx * sin_a + dy * cos_a,
            )
        )

    return rotated_vertices


def _calculate_bounding_box(vertices) -> Rect:
    """Calculates the bounding box of a polygon."""
    min_x = min(vertices, key=lambda x: x[0])[0]
    min_y = min(vertices, key=lambda x: x[1])[1]
    max_x = max(vertices, key=lambda x: x[0])[0]
    max_y = max(vertices, key=lambda x: x[1])[1]

    return Rect(
        math.floor(min_x),
        math.floor(min_y),
        math.ceil(max_x - min_x + 1),
        math.ceil(max_y - min_y + 1),
    )


def _calculate_center(poly: Polygon):
    """Calculates the center of a polygon."""
    x = 0
    y = 0
    for vertex in poly.vertices:
        x += vertex[0]
        y += vertex[1]
    return x / poly.verts_num, y / poly.verts_num


def _scale_polygon(vertices, num_verts, cx, cy, fac):
    one_m_fac = 1 - fac
    omf_cx = one_m_fac * cx
    omf_cy = one_m_fac * cy

    new_vertices = []

    for i in range(num_verts):
        x, y = vertices[i]
        new_vertices.append((x * fac + omf_cx, y * fac + omf_cy))

    return new_vertices


def _flip_polygon(polygon, flip_x, flip_y=False, flip_center=None):
    flipped_vertices = []

    f_x, f_y = flip_center if flip_center is not None else polygon.center

    for vertex in polygon.vertices:
        new_x = vertex[0] if not flip_x else f_x - (vertex[0] - f_x)
        new_y = vertex[1] if not flip_y else f_y - (vertex[1] - f_y)

        flipped_vertices.append((new_x, new_y))

    return flipped_vertices


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
            (p1, p2, "(1, 1)"),
            (p1, p2, 32),
            (p for p in [p1, p2, 32]),
            (p for p in [p1, p2, "(1, 1)"]),
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
            [],
            [p1],  # 1
            [p1, p2],  # 2
            (p1,),  # 1
            (p1, p2),  # 2
            (p for p in []),
            (p for p in [p1]),  # generator
            (p for p in [p1, p2]),  # generator
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

    def test_construction_polygon_attribute(self):
        """Ensures that you can construct a polygon from another object that has a
        polygon attribute"""

        # polygon attribute is a list of vertices
        class PolygonObject:
            def __init__(self, polygon):
                self.polygon = polygon

        po = PolygonObject([p1, p2, p3, p4])
        po_2 = Polygon(po)

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, po.polygon)

        # polygon attribute is a callable that returns a list of vertices
        class PolygonObject1:
            def __init__(self, polygon):
                self._poly = polygon

            def polygon(self):
                return self._poly

        po = PolygonObject1([p1, p2, p3, p4])
        po_2 = Polygon(po)

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])

        # polygon attribute is a callable that returns a Polygon object
        class PolygonObject2:
            def __init__(self, polygon):
                self._poly = polygon

            def polygon(self):
                return Polygon(self._poly)

        po = PolygonObject2(Polygon([p1, p2, p3, p4]))
        po_2 = Polygon(po)

        self.assertEqual(po_2.vertices, po.polygon().vertices)

        # polygon attribute is a polygon object
        class PolygonObject3:
            def __init__(self, polygon):
                self.polygon = polygon

        po = PolygonObject3(Polygon([p1, p2, p3, p4]))
        po_2 = Polygon(po)

        self.assertEqual(po_2.vertices, po.polygon.vertices)

    def test_construction_frompolygon(self):
        """Checks whether the constructor works correctly with another polygon"""
        po = Polygon([p1, p2, p3, p4])
        po_2 = Polygon(po)

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, po.vertices)

    def test_construction_generator(self):
        """Checks whether the constructor works correctly with a generator object"""

        def generator():
            yield p1
            yield p2
            yield p3
            yield p4

        po = Polygon(generator())

        self.assertEqual(po.vertices, [p1, p2, p3, p4])

    def test_construction_iterator(self):
        """Checks whether the constructor works correctly with an iterator object"""

        class Iterator:
            def __init__(self, points):
                self.points = points
                self.index = 0

            def __next__(self):
                if self.index >= len(self.points):
                    raise StopIteration
                result = self.points[self.index]
                self.index += 1
                return result

            def __iter__(self):
                return self

        it = Iterator([p1, p2, p3, p4])
        po = Polygon(it)

        self.assertEqual(po.vertices, [p1, p2, p3, p4])

    def test_construction_iterable(self):
        """Checks whether the constructor works correctly with an object that implements the __iter__ method"""

        it = iter([p1, p2, p3, p4])
        po = Polygon(it)

        self.assertEqual(po.vertices, [p1, p2, p3, p4])

    def test_construction_generator_expression(self):
        """Checks whether the constructor works correctly with a generator expression"""
        po = Polygon(p for p in [p1, p2, p3, p4])

        self.assertEqual(po.vertices, [p1, p2, p3, p4])

    def test_construction_generator_expression2(self):
        """Checks whether the constructor works correctly with a generator expression"""
        po = Polygon((p for p in [p1, p2, p3, p4]))

        self.assertEqual(po.vertices, [p1, p2, p3, p4])

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
        po_center_x = po.centerx
        po_center_y = po.centery
        po_2 = po.copy()

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, po.vertices)
        self.assertEqual(po_2.centerx, po_center_x)
        self.assertEqual(po_2.centery, po_center_y)

    def test_center_x(self):
        """Makes sure changing center x component does change the positions of vertices properly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        poly_centerx = poly.centerx
        poly.centerx = 100.0

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 100.0 - poly_centerx
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(poly.vertices, vertices)

    def test_center_x__invalid_value(self):
        """Ensures the function can handle the polygon center x component by invalid data types."""
        poly = Polygon(_some_vertices.copy())
        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                poly.centerx = value

    def test_center_x__del(self):
        """Ensures that x component cannot be deleted."""
        poly = Polygon(_some_vertices.copy())
        with self.assertRaises(AttributeError):
            del poly.centerx

    def test_center_y(self):
        """Makes sure changing center y component does change the positions of vertices properly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        poly_centery = poly.centery
        poly.centery = 100.0

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[1] += 100.0 - poly_centery

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(poly.vertices, vertices)

    def test_center_y__invalid_value(self):
        """Ensures the function can handle the polygon center y component by invalid data types."""
        poly = Polygon(_some_vertices)
        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                poly.centery = value

    def test_center_y__del(self):
        """Ensures that y component cannot be deleted."""
        poly = Polygon(_some_vertices)
        with self.assertRaises(AttributeError):
            del poly.centery

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
        self.assertEqual(poly.centerx, 200.0)
        self.assertEqual(poly.centery, 200.0)

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

    def test_move_xy(self):
        """Checks whether polygon move function works correctly with an x-y pair."""
        poly = Polygon(_some_vertices.copy())
        center_x = poly.centerx
        center_y = poly.centery

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
        self.assertAlmostEqual(new_poly.centerx, center_x + 10.0)
        self.assertAlmostEqual(new_poly.centery, center_y + 10.0)

    def test_move_x(self):
        """Checks whether polygon move function works correctly with an x component."""
        poly = Polygon(_some_vertices.copy())
        center_x = poly.centerx
        center_y = poly.centery

        new_poly = poly.move(10.0, 0.0)
        vertices = _some_vertices.copy()

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 10.0
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(vertices, new_poly.vertices)
        self.assertNotEqual(poly.vertices, new_poly.vertices)
        self.assertEqual(poly.vertices, _some_vertices)
        self.assertAlmostEqual(new_poly.centerx, center_x + 10.0)
        self.assertAlmostEqual(new_poly.centery, center_y)

    def test_move_y(self):
        """Checks whether polygon move function works correctly with a y component."""
        poly = Polygon(_some_vertices.copy())
        center_x = poly.centerx
        center_y = poly.centery

        new_poly = poly.move(0.0, 10.0)
        vertices = _some_vertices.copy()

        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[1] += 10.0
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(vertices, new_poly.vertices)
        self.assertNotEqual(poly.vertices, new_poly.vertices)
        self.assertEqual(poly.vertices, _some_vertices)
        self.assertAlmostEqual(new_poly.centerx, center_x)
        self.assertAlmostEqual(new_poly.centery, center_y + 10.0)

    def test_move_inplace(self):
        """Checks whether polygon moved by (0, 0) and is the returned polygon identical."""
        poly = Polygon(_some_vertices.copy())
        poly_new = poly.move(0, 0)

        ##self.assertAlmostEquals(poly_new, poly)
        self.assertEqual(poly_new.centerx, poly.centerx)
        self.assertEqual(poly_new.centery, poly.centery)
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
        """Tests whether the move function returns a Polygon type/subtype object"""
        move_amounts = [
            (1, 1),
            (0, 1),
            (1, 0),
            (0, 0),
            (1.0, 1.0),
            (0.0, 1.0),
            (1.0, 0.0),
            (0.0, 0.0),
            (-1, -1),
            (0, -1),
            (-1, 0),
            (-1.0, -1.0),
            (0.0, -1.0),
            (-1.0, 0.0),
        ]

        poly = Polygon(_some_vertices.copy())

        for move_amount in move_amounts:
            self.assertIsInstance(poly.move(*move_amount), Polygon)
            self.assertIsInstance(poly.move(move_amount), Polygon)

        class TestPolygon(Polygon):
            pass

        polysub = TestPolygon(_some_vertices.copy())

        for move_amount in move_amounts:
            self.assertIsInstance(polysub.move(*move_amount), TestPolygon)
            self.assertIsInstance(polysub.move(move_amount), TestPolygon)

    def test_move_ip_xy(self):
        """Checks whether polygon move_ip function works correctly with an x-y pair."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        center_x = poly.centerx
        center_y = poly.centery

        poly.move_ip(10.0, 10.0)
        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 10.0
            vertex[1] += 10.0
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.centerx, center_x + 10.0)
        self.assertEqual(poly.centery, center_y + 10.0)

    def test_move_ip_x(self):
        """Checks whether polygon move_ip function works correctly with an x component."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        center_x = poly.centerx
        center_y = poly.centery

        poly.move_ip(10.0, 0.0)
        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[0] += 10.0
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.centerx, center_x + 10.0)
        self.assertEqual(poly.centery, center_y)

    def test_move_ip_y(self):
        """Checks whether polygon move_ip function works correctly with a y component."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        center_x = poly.centerx
        center_y = poly.centery

        poly.move_ip(0.0, 10.0)
        vertices = [list(vertex) for vertex in vertices]
        for vertex in vertices:
            vertex[1] += 10.0
        vertices = [tuple(vertex) for vertex in vertices]

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.centerx, center_x)
        self.assertEqual(poly.centery, center_y + 10.0)

    def test_move_ip_inplace(self):
        """Ensures that moving the polygon by (0, 0) will not change its position."""
        poly = Polygon(_some_vertices.copy())
        vertices = _some_vertices.copy()
        center_x = poly.centerx
        center_y = poly.centery

        poly.move_ip(0, 0)

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.centerx, center_x)
        self.assertEqual(poly.centery, center_y)

    def test_move_ip_return_type(self):
        """Tests whether the move_ip function returns a Polygon type/subtype object"""
        move_amounts = [
            (1, 1),
            (0, 1),
            (1, 0),
            (0, 0),
            (1.0, 1.0),
            (0.0, 1.0),
            (1.0, 0.0),
            (0.0, 0.0),
            (-1, -1),
            (0, -1),
            (-1, 0),
            (-1.0, -1.0),
            (0.0, -1.0),
            (-1.0, 0.0),
        ]

        poly = Polygon(_some_vertices.copy())

        for move_amount in move_amounts:
            self.assertEqual(type(poly.move_ip(*move_amount)), type(None))
            self.assertEqual(type(poly.move_ip(move_amount)), type(None))

        class TestPolygon(Polygon):
            pass

        polysub = TestPolygon(_some_vertices.copy())

        for move_amount in move_amounts:
            self.assertEqual(type(polysub.move_ip(*move_amount)), type(None))
            self.assertEqual(type(polysub.move_ip(move_amount)), type(None))

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

        rot_centers = [
            gen_poly.center,
            (0, 0),
            (1, 1),
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (-1, -1),
        ] + vertices

        for angle in angles:
            for c in rot_centers:
                poly = gen_poly.copy()
                rotated_vertices = _rotate_vertices(poly, angle, c)
                p2 = poly.rotate(angle, c)
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

        for value in [t for t in invalid_types if not isinstance(t, Vector2)]:
            with self.assertRaises(TypeError):
                poly.rotate(2, value)

    def test_rotate_argnum(self):
        """Tests whether the function can handle invalid parameter number correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, (1, 1), (1, 1)), (1, (1, 1), (1, 1), (1, 1))]

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

        rot_centers = [
            gen_poly.center,
            (0, 0),
            (1, 1),
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (-1, -1),
        ] + vertices

        for angle in angles:
            for c in rot_centers:
                poly = gen_poly.copy()
                rotated_vertices = _rotate_vertices(poly, angle, c)
                poly.rotate_ip(angle, c)
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

        for value in [t for t in invalid_types if not isinstance(t, Vector2)]:
            with self.assertRaises(TypeError):
                poly.rotate_ip(2, value)

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

        invalid_args = [(1, (1, 1), (1, 1)), (1, (1, 1), (1, 1), (1, 1))]

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
        center_x = poly.centerx
        center_y = poly.centery

        poly.rotate_ip(0)

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.centerx, center_x)
        self.assertEqual(poly.centery, center_y)

    def test_rotate_inplace(self):
        """Ensures that rotating the polygon by 0 degrees will not change its position."""
        poly = Polygon(_some_vertices.copy())
        vertices = _some_vertices.copy()
        center_x = poly.centerx
        center_y = poly.centery

        new_poly = poly.rotate(0)

        self.assertEqual(new_poly.vertices, poly.vertices)
        self.assertEqual(new_poly.centerx, poly.centerx)
        self.assertEqual(new_poly.centery, poly.centery)

        self.assertEqual(new_poly.vertices, vertices)
        self.assertEqual(new_poly.centerx, center_x)
        self.assertEqual(new_poly.centery, center_y)

        new_poly = poly.rotate(0, poly.center)

        self.assertEqual(new_poly.vertices, poly.vertices)
        self.assertEqual(new_poly.centerx, poly.centerx)
        self.assertEqual(new_poly.centery, poly.centery)

        self.assertEqual(new_poly.vertices, vertices)
        self.assertEqual(new_poly.centerx, center_x)
        self.assertEqual(new_poly.centery, center_y)

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

    def test_insert_vertex(self):
        """Checks whether a vertex is added correctly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        vertices.append((4.21, -34.0))
        poly.insert_vertex(3, (4.21, -34.0))

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.verts_num, 4)

    def test_insert_vertex_invalid_args(self):
        """Checks whether the function can handle invalid types correctly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        invalid_types = (
            1.332,
            None,
            [],
            "1",
            (1,),
            Vector3(1, 1, 3),
            Polygon(vertices),
        )

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.insert_vertex(1, value)

    def test_insert_vertex_argnum(self):
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.insert_vertex(*arg)

    def test_insert_vertex_return_type(self):
        poly = Polygon(_some_vertices.copy())

        self.assertEqual(type(poly.insert_vertex(1, (1, 1))), type(None))

    def test_insert_vertex_invalid_index_type(self):
        """Checks whether the function can handle invalid indices correctly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Polygon(vertices))

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.insert_vertex(value, (1, 1))

    def test_insert_vertex_permanence(self):
        """Ensures that the polygon's vertices are not modified when a vertex is added."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]
        poly = Polygon(vertices)
        poly.insert_vertex(1, (1.5, 1.5))
        new_vertices = [(1, 1), (1.5, 1.5), (2, 2), (3, 3), (4, 4)]
        self.assertEqual(poly.vertices, new_vertices)

    def test_remove_vertex(self):
        """Checks whether a vertex is removed correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))

        poly = Polygon(vertices)
        vertices.pop(1)
        poly.remove_vertex(1)

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.verts_num, 3)

        # triangle
        poly = Polygon(_some_vertices.copy())
        for i in range(poly.verts_num):
            with self.assertRaises(TypeError):
                poly.remove_vertex(i)

    def test_remove_vertex_invalid_args(self):
        """Checks whether the function can handle invalid types correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))
        poly = Polygon(vertices)
        invalid_types = (
            1.332,
            None,
            [],
            "1",
            (1,),
            Vector3(1, 1, 3),
            Polygon(vertices),
        )

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.remove_vertex(value)

    def test_remove_vertex_argnum(self):
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.remove_vertex(*arg)

    def test_remove_vertex_return_type(self):
        verts = _some_vertices.copy()
        verts.append((1, 1))
        poly = Polygon(verts)

        self.assertEqual(type(poly.remove_vertex(1)), type(None))

    def test_remove_vertex_invalid_index(self):
        """Checks whether the function can handle invalid indices correctly."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]
        poly = Polygon(vertices)
        invalid_indices = (4, 5, 6)

        for index in invalid_indices:
            with self.assertRaises(IndexError):
                poly.remove_vertex(index)

    def test_remove_vertex_permanence(self):
        """Ensures that the polygon's vertices are not modified when a vertex is removed."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]
        poly = Polygon(vertices)
        poly.remove_vertex(1)
        self.assertEqual(poly.vertices, [v for v in vertices if v != (2, 2)])

    def test_pop_vertex(self):
        """Checks whether a vertex is removed correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))

        poly = Polygon(vertices)
        real_vert = vertices.pop(1)
        vert = poly.pop_vertex(1)

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.verts_num, 3)
        self.assertEqual(vert, real_vert)

        # triangle
        poly = Polygon(_some_vertices.copy())
        for i in range(poly.verts_num):
            with self.assertRaises(TypeError):
                poly.pop_vertex(i)

    def test_pop_vertex_invalid_args(self):
        """Checks whether the function can handle invalid types correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))
        poly = Polygon(vertices)
        invalid_types = (
            1.332,
            None,
            [],
            "1",
            (1,),
            Vector3(1, 1, 3),
            Polygon(vertices),
        )

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.pop_vertex(value)

    def test_pop_vertex_argnum(self):
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.pop_vertex(*arg)

    def test_pop_vertex_return_type(self):
        verts = _some_vertices.copy()
        verts.append((1, 1))
        poly = Polygon(verts)

        self.assertEqual(type(poly.pop_vertex(1)), tuple)

    def test_pop_vertex_invalid_index(self):
        """Checks whether the function can handle invalid indices correctly."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]
        poly = Polygon(vertices)
        invalid_indices = (4, 5, 6)

        for index in invalid_indices:
            with self.assertRaises(IndexError):
                poly.pop_vertex(index)

    def test_pop_vertex_center(self):
        """Checks whether the center is updated correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))

        poly = Polygon(vertices)
        poly.pop_vertex(1)

        self.assertEqual((14.736666666666665, -4.666666666666667), poly.center)

    def test_pop_vertex_permanence(self):
        """Ensures that the polygon's vertices are not modified when a vertex is removed."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]
        poly = Polygon(vertices)
        poly.pop_vertex(1)
        self.assertEqual(poly.vertices, [v for v in vertices if v != (2, 2)])

    def test_remove_vertex_center(self):
        """Checks whether the center is updated correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))

        poly = Polygon(vertices)
        poly.remove_vertex(1)

        self.assertEqual((14.736666666666665, -4.666666666666667), poly.center)

        vertices = _some_vertices.copy()
        vertices.append(Vector2(4.21, -34.0))

        poly = Polygon(vertices)
        poly.remove_vertex(1)

        self.assertEqual((14.736666666666665, -4.666666666666667), poly.center)

    def test_insert_vertex_center(self):
        """Checks whether the center is updated correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))

        poly = Polygon(vertices)
        poly.insert_vertex(1, (1, 1))

        self.assertEqual(poly.center, (13.041999999999998, 1.4))

    def test_insert_vertex_allindex(self):
        """Checks whether the function can handle negative indices correctly."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]

        for i in range(-len(vertices), len(vertices) + 1):
            poly = Polygon(vertices)
            poly.insert_vertex(i, (5, 5))
            self.assertEqual(poly.vertices[i], (5, 5))

    def test_remove_vertex_allindex(self):
        """Checks whether the function can handle negative indices correctly."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]

        for i in range(-len(vertices), len(vertices)):
            poly = Polygon(vertices)
            poly.remove_vertex(i)
            vertices_comp = vertices.copy()
            vertices_comp.pop(i)
            self.assertEqual(poly.vertices, vertices_comp)

    def test_pop_vertex_allindex(self):
        """Checks whether the function can handle negative indices correctly."""
        vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]

        for i in range(-len(vertices), len(vertices)):
            poly = Polygon(vertices)
            poly.pop_vertex(i)
            vertices_comp = vertices.copy()
            vertices_comp.pop(i)
            self.assertEqual(poly.vertices, vertices_comp)

    def test_assign_vertices(self):
        """Checks whether the vertices are assigned correctly."""
        poly = Polygon(_some_vertices.copy())
        new_vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]

        poly.vertices = new_vertices

        self.assertEqual(poly.vertices, new_vertices)
        self.assertEqual(poly.verts_num, 4)

        poly.vertices = poly.vertices
        self.assertEqual(poly.vertices, new_vertices)

        new_vertices.pop(0)
        poly.vertices = new_vertices
        self.assertEqual(poly.vertices, new_vertices)
        self.assertEqual(poly.verts_num, 3)

    def test_assign_vertices_Vector2(self):
        """Checks whether the vertices are assigned correctly."""
        poly = Polygon(_some_vertices.copy())
        new_vertices = [Vector2(1, 1), Vector2(2, 2), Vector2(3, 3), Vector2(4, 4)]

        poly.vertices = new_vertices

        self.assertEqual(poly.vertices, new_vertices)
        self.assertEqual(poly.verts_num, 4)

        poly.vertices = poly.vertices
        self.assertEqual(poly.vertices, new_vertices)

        new_vertices.pop(0)
        poly.vertices = new_vertices
        self.assertEqual(poly.vertices, new_vertices)
        self.assertEqual(poly.verts_num, 3)

    def test_assign_vertices_center(self):
        """Checks whether the center is updated correctly."""
        poly = Polygon(_some_vertices.copy())
        new_vertices = [(1, 1), (2, 2), (3, 3), (4, 4)]

        poly.vertices = new_vertices

        self.assertEqual((2.5, 2.5), poly.center)

    def test_assign_vertices_center_Vector2(self):
        """Checks whether the center is updated correctly."""
        poly = Polygon(_some_vertices.copy())
        new_vertices = [Vector2(1, 1), Vector2(2, 2), Vector2(3, 3), Vector2(4, 4)]

        poly.vertices = new_vertices

        self.assertEqual((2.5, 2.5), poly.center)

    def test_as_rect_horizontal_line(self):
        vertices = [(0, 0), (1, 0), (2, 0), (3, 0)]
        poly = Polygon(vertices)

        bounding_box = poly.as_rect()
        expected_bounding_box = _calculate_bounding_box(vertices)

        self.assertTrue(bounding_box.width > 0)
        self.assertTrue(bounding_box.height > 0)
        self.assertEqual(bounding_box, expected_bounding_box)

        for vertex in vertices:
            self.assertTrue(bounding_box.collidepoint(vertex))

    def test_as_rect_vertical_line(self):
        vertices = [(0, 0), (0, 1), (0, 2), (0, 3)]
        poly = Polygon(vertices)

        bounding_box = poly.as_rect()
        expected_bounding_box = _calculate_bounding_box(vertices)

        self.assertTrue(bounding_box.width > 0)
        self.assertTrue(bounding_box.height > 0)
        self.assertEqual(bounding_box, expected_bounding_box)

        for vertex in vertices:
            self.assertTrue(bounding_box.collidepoint(vertex))

    def test_as_rect_square(self):
        vertices = [(0, 0), (0, 1), (1, 1), (1, 0)]
        poly = Polygon(vertices)

        bounding_box = poly.as_rect()
        expected_bounding_box = _calculate_bounding_box(vertices)

        self.assertTrue(bounding_box.width > 0)
        self.assertTrue(bounding_box.height > 0)
        self.assertEqual(bounding_box, expected_bounding_box)

        for vertex in vertices:
            self.assertTrue(bounding_box.collidepoint(vertex))

    def test_as_rect_diagonal_line(self):
        vertices = [(0, 0), (1, 1), (2, 2), (3, 3)]
        poly = Polygon(vertices)

        bounding_box = poly.as_rect()
        expected_bounding_box = _calculate_bounding_box(vertices)

        self.assertTrue(bounding_box.width > 0)
        self.assertTrue(bounding_box.height > 0)
        self.assertEqual(bounding_box, expected_bounding_box)

        for vertex in vertices:
            self.assertTrue(bounding_box.collidepoint(vertex))

    def test_as_rect_negative_positions(self):
        vertices = [(0.5, 0.5), (-0.5, -0.5), (1.5, 1.5), (-1.5, -1.5)]
        poly = Polygon(vertices)

        bounding_box = poly.as_rect()
        expected_bounding_box = _calculate_bounding_box(vertices)

        self.assertTrue(bounding_box.width > 0)
        self.assertTrue(bounding_box.height > 0)
        self.assertEqual(bounding_box, expected_bounding_box)

        for vertex in vertices:
            self.assertTrue(bounding_box.collidepoint(vertex))

    def test_as_rect_nonsimple_random_positions(self):
        vertices = []
        for i in range(1000):
            vertices.append((random.uniform(-100, 100), random.uniform(-100, 100)))
        poly = Polygon(vertices)

        bounding_box = poly.as_rect()
        expected_bounding_box = _calculate_bounding_box(vertices)

        self.assertTrue(bounding_box.width > 0)
        self.assertTrue(bounding_box.height > 0)
        self.assertEqual(bounding_box, expected_bounding_box)

        for vertex in vertices:
            self.assertTrue(bounding_box.collidepoint(vertex))

    def test_as_rect_return_type(self):
        """Tests whether the as_rect method returns a Rect."""
        poly = Polygon(_some_vertices.copy())
        self.assertIsInstance(poly.as_rect(), Rect)

    def test_as_rect_argnum(self):
        """Tests whether the as_rect method correctly handles invalid parameter
        numbers."""
        poly = Polygon(_some_vertices.copy())

        with self.assertRaises(TypeError):
            poly.as_rect(1)

    def test_assign_subscript(self):
        """Tests whether assigning to a subscript works correctly."""
        new_vertices = [(1.11, 32), (-2, 2.0), (3.23, 3.0)]
        poly = Polygon(_some_vertices.copy())

        for i, vertex in enumerate(new_vertices):
            poly[i] = vertex

            self.assertEqual(poly[i], vertex)

            expected_center = _calculate_center(poly)

            # check that the new center of the polygon is correct
            self.assertAlmostEqual(expected_center[0], poly.centerx, places=14)
            self.assertAlmostEqual(expected_center[1], poly.centery, places=14)

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

    def test_polygon___new__(self):
        """Tests whether the __new__ method works correctly."""
        polygon = Polygon.__new__(Polygon)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(polygon.verts_num, 3)

    def test_is_convex_meth(self):
        p1 = Polygon((0, 0), (0, 1), (1, 1), (1, 0))
        p2 = Polygon((0, 10), (5, 5), (10, 10), (10, 0), (0, 0))

        with self.assertRaises(TypeError):
            p1.is_convex(1)
        with self.assertRaises(TypeError):
            p1.is_convex("1")
        with self.assertRaises(TypeError):
            p1.is_convex([1])
        with self.assertRaises(TypeError):
            p1.is_convex((1,))
        with self.assertRaises(TypeError):
            p1.is_convex(object())

        self.assertTrue(p1.is_convex())
        self.assertFalse(p2.is_convex())

    def test_collidecircle_argtype(self):
        """Tests if the function correctly handles incorrect types as parameters"""

        invalid_types = (
            True,
            False,
            None,
            [],
            "1",
            (1,),
            1,
            0,
            -1,
            1.23,
            Polygon((0, 0), (0, 1), (1, 1), (1, 0)),
            Line(10, 10, 4, 4),
            Rect(10, 10, 4, 4),
            Vector2(10, 10),
        )

        p = Polygon((0, 0), (0, 1), (1, 1), (1, 0))

        for value in invalid_types:
            with self.assertRaises(TypeError):
                p.collidecircle(value)
            with self.assertRaises(TypeError):
                p.collidecircle(value, True)
            with self.assertRaises(TypeError):
                p.collidecircle(value, False)

    def test_collidecircle_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        p = Polygon((0, 0), (0, 1), (1, 1), (1, 0))

        circle = Circle(10, 10, 4)
        invalid_args = [
            (circle, circle),
            (circle, circle, circle),
            (circle, circle, circle, circle),
            (circle, circle, circle, circle, circle),
        ]

        with self.assertRaises(TypeError):
            p.collidecircle()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                p.collidecircle(*arg)
            with self.assertRaises(TypeError):
                p.collidecircle(*arg, True)
            with self.assertRaises(TypeError):
                p.collidecircle(*arg, False)

    def test_collidecircle_return_type(self):
        """Tests if the function returns the correct type"""
        p = Polygon((0, 0), (0, 1), (1, 1), (1, 0))

        circle_val = [10, 10, 4]

        items = [
            Circle(circle_val),
            circle_val,
            tuple(circle_val),
        ]

        for item in items:
            self.assertIsInstance(p.collidecircle(item), bool)
            self.assertIsInstance(p.collidecircle(item, True), bool)
            self.assertIsInstance(p.collidecircle(item, False), bool)

        self.assertIsInstance(p.collidecircle(*circle_val), bool)
        self.assertIsInstance(p.collidecircle(*circle_val, True), bool)
        self.assertIsInstance(p.collidecircle(*circle_val, False), bool)

    def test_collidecircle(self):
        """Ensures that the collidecircle method correctly determines if a polygon
        is colliding with the circle"""
        epsilon = 0.00000000000001

        c = Circle(0, 0, 15)

        p1 = Polygon([(-5, 0), (5, 0), (0, 5)])
        p2 = Polygon([(100, 150), (200, 225), (150, 200)])
        p3 = Polygon([(0, 0), (50, 50), (50, -50), (0, -50)])
        p4 = regular_polygon(4, c.center, 100)
        p5 = regular_polygon(3, (c.x + c.r - 5, c.y), 5)
        p6 = regular_polygon(3, (c.x + c.r - 5, c.y), 5 - epsilon)

        # circle contains polygon
        self.assertTrue(p1.collidecircle(c))
        self.assertTrue(p1.collidecircle(c), False)

        # non colliding
        self.assertFalse(p2.collidecircle(c))
        self.assertFalse(p2.collidecircle(c), False)

        # intersecting polygon
        self.assertTrue(p3.collidecircle(c))
        self.assertTrue(p3.collidecircle(c), False)

        # polygon contains circle
        self.assertTrue(p4.collidecircle(c))
        self.assertTrue(p4.collidecircle(c), False)

        # circle contains polygon, barely touching
        self.assertTrue(p5.collidecircle(c))
        self.assertTrue(p5.collidecircle(c), False)

        # circle contains polygon, barely not touching
        self.assertTrue(p6.collidecircle(c))
        self.assertTrue(p6.collidecircle(c), False)

        # --- Edge only ---

        # circle contains polygon
        self.assertFalse(p1.collidecircle(c, True))

        # non colliding
        self.assertFalse(p2.collidecircle(c, True))

        # intersecting polygon
        self.assertTrue(p3.collidecircle(c, True))

        # polygon contains circle
        self.assertFalse(p4.collidecircle(c, True))

        # circle contains polygon, barely touching
        self.assertTrue(p5.collidecircle(c, True))

        # circle contains polygon, barely not touching
        self.assertFalse(p6.collidecircle(c, True))

    def test_collidepolygon_invalid_only_edges_param(self):
        """Tests if the function correctly handles incorrect types as only_edges parameter"""
        c = Circle(10, 10, 4)
        poly = Polygon((-5, 0), (5, 0), (0, 5))

        invalid_types = (
            None,
            [],
            "1",
            (1,),
            1,
            0,
            -1,
            1.23,
            (1, 2, 3),
            Circle(10, 10, 4),
            Line(10, 10, 4, 4),
            Rect(10, 10, 4, 4),
            Vector3(10, 10, 4),
            Vector2(10, 10),
        )

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.collidecircle(c, value)

    def test_collidecircle_no_invalidation(self):
        """Ensures that the function doesn't modify the polygon or the circle"""
        c = Circle(10, 10, 4)
        poly = Polygon((-5, 0), (5, 0), (0, 5))

        c_copy = c.copy()
        poly_copy = poly.copy()

        poly.collidecircle(c)

        self.assertEqual(c.x, c_copy.x)
        self.assertEqual(c.y, c_copy.y)
        self.assertEqual(c.r, c_copy.r)

        self.assertEqual(poly.vertices, poly_copy.vertices)
        self.assertEqual(poly.verts_num, poly_copy.verts_num)
        self.assertEqual(poly.centerx, poly_copy.centerx)
        self.assertEqual(poly.centery, poly_copy.centery)

    def test_scale_ip(self):
        """Tests whether the scale_ip method works correctly."""
        poly = Polygon(_some_vertices.copy())

        scales = [0.5, 1.0, 2.0, 0.1, 10, 100, 1000, 0.12, 0.001, 0.000000001]

        for scale in scales:
            newpoly = poly.copy()
            data = (
                newpoly.center,
                newpoly.verts_num,
                _scale_polygon(
                    _some_vertices.copy(), 3, newpoly.centerx, newpoly.centery, scale
                ),
            )
            newpoly.scale_ip(scale)
            self.assertEqual(data[0], newpoly.center)
            self.assertEqual(data[1], newpoly.verts_num)
            self.assertEqual(data[2], newpoly.vertices)

    def test_scale_ip_inplace(self):
        """Ensures that scaling the polygon by 1.0 will not change its position."""
        poly = Polygon(_some_vertices.copy())
        vertices = _some_vertices.copy()
        center_x = poly.centerx
        center_y = poly.centery

        poly.scale_ip(1.0)

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.centerx, center_x)
        self.assertEqual(poly.centery, center_y)

    def test_scale_ip_return_type(self):
        """Tests whether the scale_ip method returns the correct type."""
        poly = Polygon(_some_vertices.copy())

        self.assertEqual(type(poly.scale_ip(1.32)), type(None))

    def test_scale_ip_invalid_args(self):
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
                poly.scale_ip(value)

    def test_scale_ip_argnum(self):
        """Tests whether the function can handle invalid parameter number correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.scale_ip(*arg)

    def test_scale(self):
        """Tests whether the scale method works correctly."""
        poly = Polygon(_some_vertices.copy())

        scales = [0.5, 1.0, 2.0, 0.1, 10, 100, 1000, 0.12, 0.001, 0.000000001]

        for scale in scales:
            new_poly = poly.copy()
            data = (
                new_poly.center,
                new_poly.verts_num,
                _scale_polygon(
                    _some_vertices.copy(), 3, new_poly.centerx, new_poly.centery, scale
                ),
            )
            new_poly = poly.scale(scale)
            self.assertEqual(data[0], new_poly.center)
            self.assertEqual(data[1], new_poly.verts_num)
            self.assertEqual(data[2], new_poly.vertices)

    def test_scale_return_type(self):
        """Tests whether the scale method returns the correct type."""
        poly = Polygon(_some_vertices.copy())

        scales = [0.5, 1.0, 2.0, 0.1, 10]

        for scale_val in scales:
            self.assertIsInstance(poly.scale(scale_val), Polygon)

        class TestPolygon(Polygon):
            pass

        poly2 = TestPolygon(_some_vertices.copy())

        for scale_val in scales:
            self.assertIsInstance(poly2.scale(scale_val), TestPolygon)

    def test_scale_invalid_args(self):
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
                poly.scale(value)

    def test_scale_argnum(self):
        """Tests whether the function can handle invalid parameter number correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.scale(*arg)

    def test_collideline_argtype(self):
        """Tests if the function correctly handles incorrect types as parameters"""

        invalid_types = (
            True,
            False,
            None,
            [],
            "1",
            (1,),
            1,
            0,
            -1,
            1.23,
            (1, 2, 3),
            Circle(10, 10, 4),
            # Rect(10, 10, 4, 4),
            Vector3(10, 10, 4),
            Vector2(10, 10),
            Polygon((0, 0), (0, 1), (1, 1), (1, 0)),
        )

        p = Polygon((0, 0), (0, 1), (1, 1), (1, 0))

        for value in invalid_types:
            with self.assertRaises(TypeError):
                p.collideline(value)
            with self.assertRaises(TypeError):
                p.collideline(value, True)
            with self.assertRaises(TypeError):
                p.collideline(value, False)

    def test_collideline_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        l = Line(0, 0, 1, 1)

        p = Polygon((-5, 0), (5, 0), (0, 5))
        invalid_args = [
            (l, l),
            (l, l, l),
            (l, l, l, l),
        ]

        with self.assertRaises(TypeError):
            p.collideline()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                p.collideline(*arg)
            with self.assertRaises(TypeError):
                p.collideline(*arg, True)
            with self.assertRaises(TypeError):
                p.collideline(*arg, False)

    def test_collideline_return_type(self):
        """Tests if the function returns the correct type"""
        p = Polygon((-5, 0), (5, 0), (0, 5))

        items = [
            Line(0, 0, 1, 1),
            [0, 0, 1, 1],
            (0, 0, 1, 1),
            [(0, 0), (1, 1)],
            ((0, 0), (1, 1)),
        ]

        for item in items:
            self.assertIsInstance(p.collideline(item), bool)
            self.assertIsInstance(p.collideline(item, True), bool)
            self.assertIsInstance(p.collideline(item, False), bool)
        for item in items[1:]:
            self.assertIsInstance(p.collideline(*item), bool)
            self.assertIsInstance(p.collideline(*item, True), bool)
            self.assertIsInstance(p.collideline(*item, False), bool)

    def test_collideline_no_invalidation(self):
        """Ensures that the function doesn't modify the polygon or the circle"""
        l = Line((0, 0), (1, 1))
        poly = Polygon((-5, 0), (5, 0), (0, 5))

        l_copy = l.copy()
        poly_copy = poly.copy()

        poly.collideline(l)

        self.assertEqual(l.a, l_copy.a)
        self.assertEqual(l.b, l_copy.b)

        self.assertEqual(poly.vertices, poly_copy.vertices)
        self.assertEqual(poly.verts_num, poly_copy.verts_num)
        self.assertEqual(poly.centerx, poly_copy.centerx)
        self.assertEqual(poly.centery, poly_copy.centery)

    def test_collideline_invalid_only_edges_param(self):
        """Tests if the function correctly handles incorrect types as only_edges parameter"""
        l = Line(0, 0, 1, 1)
        poly = Polygon((-5, 0), (5, 0), (0, 5))

        invalid_types = (
            None,
            [],
            "1",
            (1,),
            1,
            0,
            -1,
            1.23,
            (1, 2, 3),
            Circle(10, 10, 4),
            Line(10, 10, 4, 4),
            Rect(10, 10, 4, 4),
            Vector3(10, 10, 4),
            Vector2(10, 10),
        )

        for value in invalid_types:
            with self.assertRaises(TypeError):
                poly.collideline(l, value)

    def test_collidepolygon(self):
        """Ensures that the collidepolygon method correctly determines if a Polygon
        is colliding with the Line"""

        l = Line(0, 0, 10, 10)
        p1 = regular_polygon(4, l.center, 100)
        p2 = Polygon((100, 100), (150, 150), (150, 100))
        p3 = regular_polygon(4, l.a, 10)
        p4 = Polygon((5, 5), (5, 10), (0, 10), (2.5, 2.5))
        p5 = Polygon((0, 0), (0, 10), (-5, 10), (-5, 0))

        # line inside polygon
        self.assertTrue(l.collidepolygon(p1))

        # line outside polygon
        self.assertFalse(l.collidepolygon(p2))

        # line intersects polygon edge
        self.assertTrue(l.collidepolygon(p3))

        # line intersects polygon vertex
        self.assertTrue(l.collidepolygon(p4))

        # line touches polygon vertex
        self.assertTrue(l.collidepolygon(p5))

        # --- Edge only ---

        # line inside polygon
        self.assertFalse(l.collidepolygon(p1, True))

        # line outside polygon
        self.assertFalse(l.collidepolygon(p2, True))

        # line intersects polygon edge
        self.assertTrue(l.collidepolygon(p3, True))

        # line intersects polygon vertex
        self.assertTrue(l.collidepolygon(p4, True))

        # line touches polygon vertex
        self.assertTrue(l.collidepolygon(p5, True))

    def test_flip_argnum(self):
        """Tests whether the function can handle invalid parameter number correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 0, 1, 0), (1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 1)]

        with self.assertRaises(TypeError):
            poly.flip()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.flip(*arg)

    def test_flip_return_type(self):
        """Tests whether the flip method returns the correct type."""
        poly = Polygon(_some_vertices.copy())

        self.assertIsInstance(poly.flip(True), Polygon)
        self.assertIsInstance(poly.flip(True, False), Polygon)
        self.assertIsInstance(poly.flip(True, False, (10, 233)), Polygon)
        self.assertIsInstance(poly.flip(True, False, (-10, -233)), Polygon)

    def test_flip_ip_return_type(self):
        """Tests whether the flip_ip method returns the correct type."""
        poly = Polygon(_some_vertices.copy())

        self.assertIsInstance(poly.flip_ip(True), type(None))
        self.assertIsInstance(poly.flip_ip(True, False), type(None))
        self.assertIsInstance(poly.flip_ip(True, False, (10, 233)), type(None))
        self.assertIsInstance(poly.flip_ip(True, False, (-10, -233)), type(None))

    def test_flip_ip_argnum(self):
        """Tests whether the function can handle invalid parameter number correctly."""
        poly = Polygon(_some_vertices.copy())

        invalid_args = [(1, 0, 1, 0), (1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 1)]

        with self.assertRaises(TypeError):
            poly.flip_ip()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                poly.flip_ip(*arg)

    def assert_vertices_equal(self, vertices1, vertices2, eps=1e-12):
        self.assertEqual(len(vertices1), len(vertices2))

        for v1, v2 in zip(vertices1, vertices2):
            self.assertAlmostEqual(v1[0], v2[0], delta=eps)
            self.assertAlmostEqual(v1[1], v2[1], delta=eps)

    def test_flip(self):
        """Tests whether the flip method works correctly."""
        poly = Polygon(_some_vertices.copy())

        # x-axis
        flipped_vertices = _flip_polygon(poly, True, False)
        self.assert_vertices_equal(poly.flip(True).vertices, flipped_vertices)
        self.assert_vertices_equal(poly.flip(True, False).vertices, flipped_vertices)

        flipped_vertices = _flip_polygon(poly, True, False, (10, 233))
        self.assert_vertices_equal(
            poly.flip(True, False, (10, 233)).vertices, flipped_vertices
        )

        # y-axis
        flipped_vertices = _flip_polygon(poly, False, True)
        self.assert_vertices_equal(poly.flip(False, True).vertices, flipped_vertices)

        flipped_vertices = _flip_polygon(poly, False, True, (10, 233))
        self.assert_vertices_equal(
            poly.flip(False, True, (10, 233)).vertices, flipped_vertices
        )

        # both axes
        flipped_vertices = _flip_polygon(poly, True, True)
        self.assert_vertices_equal(poly.flip(True, True).vertices, flipped_vertices)

        flipped_vertices = _flip_polygon(poly, True, True, (10, 233))
        self.assert_vertices_equal(
            poly.flip(True, True, (10, 233)).vertices, flipped_vertices
        )
        flipped_vertices = _flip_polygon(poly, True, True, (-10, -233))
        self.assert_vertices_equal(
            poly.flip(True, True, (-10, -233)).vertices, flipped_vertices
        )

    def test_flip_ip(self):
        """Tests whether the flip_ip method works correctly."""
        poly = Polygon(_some_vertices.copy())

        # x-axis
        flipped_vertices = _flip_polygon(poly, True, False)
        poly.flip_ip(True)
        self.assert_vertices_equal(poly.vertices, flipped_vertices)

        poly = Polygon(_some_vertices.copy())
        flipped_vertices = _flip_polygon(poly, True, False, (10, 233))
        poly.flip_ip(True, False, (10, 233))
        self.assert_vertices_equal(poly.vertices, flipped_vertices)

        # y-axis
        poly = Polygon(_some_vertices.copy())
        flipped_vertices = _flip_polygon(poly, False, True)
        poly.flip_ip(False, True)
        self.assert_vertices_equal(poly.vertices, flipped_vertices)

        poly = Polygon(_some_vertices.copy())
        flipped_vertices = _flip_polygon(poly, False, True, (10, 233))
        poly.flip_ip(False, True, (10, 233))
        self.assert_vertices_equal(poly.vertices, flipped_vertices)

        # both axes
        poly = Polygon(_some_vertices.copy())
        flipped_vertices = _flip_polygon(poly, True, True)
        poly.flip_ip(True, True)
        self.assert_vertices_equal(poly.vertices, flipped_vertices)

        poly = Polygon(_some_vertices.copy())
        flipped_vertices = _flip_polygon(poly, True, True, (10, 233))
        poly.flip_ip(True, True, (10, 233))
        self.assert_vertices_equal(poly.vertices, flipped_vertices)

        poly = Polygon(_some_vertices.copy())
        flipped_vertices = _flip_polygon(poly, True, True, (-10, -233))
        poly.flip_ip(True, True, (-10, -233))
        self.assert_vertices_equal(poly.vertices, flipped_vertices)


if __name__ == "__main__":
    unittest.main()
