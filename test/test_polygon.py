import unittest

from pygame import Vector2, Vector3

from geometry import Polygon

p1 = (12.0, 12.0)
p2 = (32.0, 43.0)
p3 = (22.0, 4.0)
p4 = (332.0, 64.0)
_some_vertices = [[10.0, 10.0], [20.0, 20.0], [30.0, 10.0]]


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

    def test_copy_return_type(self):
        """Checks whether the copy method returns a polygon."""
        po = Polygon([p1, p2, p3, p4])

        self.assertIsInstance(po.copy(), Polygon)
        self.assertEqual(type(po.copy()), Polygon)

    def test_copy(self):
        """Checks whether the copy method works correctly."""
        po = Polygon([p1, p2, p3, p4])
        po_2 = po.copy()

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, po.vertices)

    def test_center_x(self):
        """Makes sure changing center x component does change the positions of vertices properly."""
        vertices = _some_vertices.copy()
        poly = Polygon(vertices)
        poly_c_x = poly.c_x
        poly.c_x = 100.0
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
        for vertex in vertices:
            vertex[0] += 200.0 - poly_center[0]
            vertex[1] += 200.0 - poly_center[1]

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(poly.vertices, vertices)
        self.assertEqual(poly.c_x, 200.0)
        self.assertEqual(poly.c_y, 200.0)

    def test_center__invalid_value(self):
        """Ensures the function can handle the polygon center component by invalid data types."""
        poly = Polygon(_some_vertices.copy())
        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                poly.center = value

    def test_center__del(self):
        """Ensures that center component cannot be deleted."""
        poly = Polygon(_some_vertices.copy())
        with self.assertRaises(AttributeError):
            del poly.center

    def test_move(self):
        """Checks whether polygon moved correctly."""
        poly = Polygon(_some_vertices.copy())
        center_x = poly.c_x
        center_y = poly.c_y

        new_poly = poly.move(10.0, 10.0)
        vertices = _some_vertices.copy()
        
        for vertex in vertices:
            vertex[0] += 10.0
            vertex[1] += 10.0

        vertices = [tuple(vertex) for vertex in vertices]
        self.assertEqual(vertices, new_poly.vertices)
        self.assertEqual(new_poly.c_x, center_x + 10.0)
        self.assertEqual(new_poly.c_y, center_y + 10.0)

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
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Polygon(_some_vertices.copy()))

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

if __name__ == "__main__":
    unittest.main()
