import unittest

from pygame import Vector2, Vector3

import geometry
from geometry import Polygon

import math

p1 = (12.0, 12.0)
p2 = (32.0, 43.0)
p3 = (22.0, 4.0)
p4 = (332.0, 64.0)
_some_vertices = [(10.0, 10.0), (20.0, 20.0), (30.0, 10.0)]


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
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Polygon(vertices))

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

    def test_remove_vertex(self):
        """Checks whether a vertex is removed correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))

        poly = Polygon(vertices)
        vertices.pop(1)
        poly.remove_vertex(1)

        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.verts_num, 3)

        poly2 = Polygon(_some_vertices.copy())
        for i in range(poly2.verts_num):
            with self.assertRaises(IndexError):
                poly2.remove_vertex(i)

    def test_remove_vertex_invalid_args(self):
        """Checks whether the function can handle invalid types correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))
        poly = Polygon(vertices)
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Polygon(vertices))

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

        poly2 = Polygon(_some_vertices.copy())
        for i in range(poly2.verts_num):
            with self.assertRaises(IndexError):
                poly2.pop_vertex(i)

    def test_pop_vertex_invalid_args(self):
        """Checks whether the function can handle invalid types correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))
        poly = Polygon(vertices)
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Polygon(vertices))

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

        self.assertEqual(poly.center, (14.736666666666666, -4.666666666666667))

    def test_remove_vertex_center(self):
        """Checks whether the center is updated correctly."""
        vertices = _some_vertices.copy()
        vertices.append((4.21, -34.0))

        poly = Polygon(vertices)
        poly.remove_vertex(1)

        self.assertEqual(poly.center, (14.736666666666666, -4.666666666666667))

        vertices = _some_vertices.copy()
        vertices.append(Vector2(4.21, -34.0))

        poly = Polygon(vertices)
        poly.remove_vertex(1)

        self.assertEqual(poly.center, (14.736666666666666, -4.666666666666667))

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

        self.assertEqual(poly.center, (2.5, 2.5))

    def test_assign_vertices_center_Vector2(self):
        """Checks whether the center is updated correctly."""
        poly = Polygon(_some_vertices.copy())
        new_vertices = [Vector2(1, 1), Vector2(2, 2), Vector2(3, 3), Vector2(4, 4)]

        poly.vertices = new_vertices

        self.assertEqual(poly.center, (2.5, 2.5))


if __name__ == "__main__":
    unittest.main()
