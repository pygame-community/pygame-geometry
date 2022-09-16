import unittest

from pygame import Vector2

from geometry import Polygon

import math

p1 = (12.0, 12.0)
p2 = (32.0, 43.0)
p3 = (22.0, 4.0)
p4 = (332.0, 64.0)


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

    def test_static_normal_polygon(self):
        center = (150.5, 100.1)
        radius = 50.2
        sides = 10
        angle = 20.6

        polygon_pg = Polygon.normal_polygon(sides, center, radius, angle)
        vertices_pg = polygon_pg.vertices

        vertices = []

        for i in range(sides):
            vertices.append(
                (
                    center[0]
                    + radius * math.cos(math.radians(angle) + math.pi * 2 * i / sides),
                    center[1]
                    + radius * math.sin(math.radians(angle) + math.pi * 2 * i / sides),
                )
            )

        self.assertEqual(vertices_pg, vertices)

        invalid_types = (
            None,
            [],
            "1",
            "123",
            (1,),
            [1, 2, 3],
            [p1, p2, p3, 32],
            [p1, p2, "(1, 1)"],
        )

        for invalid_type in invalid_types:
            with self.assertRaises(TypeError):
                Polygon.normal_polygon(5, invalid_type, 5.5, 1)

        for invalid_type in invalid_types + (1, 2):
            with self.assertRaises(TypeError):
                Polygon.normal_polygon(invalid_type, (1, 2.2), 5.5, 1)

        for invalid_type in invalid_types + (1, 2):
            with self.assertRaises(TypeError):
                Polygon.normal_polygon(5, (1, 2.2), invalid_type, 1)

        for invalid_type in invalid_types + (1, 2):
            with self.assertRaises(TypeError):
                Polygon.normal_polygon(5, (1, 2.2), 5.5, invalid_type)

        with self.assertRaises(TypeError):
            Polygon.normal_polygon(1, (1, 2.2), 5.5, 1, 5)

        with self.assertRaises(TypeError):
            Polygon.normal_polygon()

        with self.assertRaises(ValueError):
         Polygon.normal_polygon(-1, center, radius, angle)

        with self.assertRaises(ValueError):
         Polygon.normal_polygon(2, center, radius, angle)

    def test_copy_return_type(self):
        """Checks whether the copy method returns a polygon"""
        po = Polygon([p1, p2, p3, p4])

        self.assertIsInstance(po.copy(), Polygon)
        self.assertEqual(type(po.copy()), Polygon)

    def test_copy(self):
        """Checks whether the copy method works correctly"""
        po = Polygon([p1, p2, p3, p4])
        po_2 = po.copy()

        self.assertEqual(po_2.vertices, [p1, p2, p3, p4])
        self.assertEqual(po_2.vertices, po.vertices)


if __name__ == "__main__":
    unittest.main()
