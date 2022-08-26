import unittest

from pygame import Vector2

from geometry import Polygon

p1 = (12.0, 12.0)
p2 = (32.0, 43.0)
p3 = (22.0, 4.0)
p4 = (332.0, 64.0)


class PolygonTypeTest(unittest.TestCase):
    def dest_Construction_invalid_type(self):
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
                p = Polygon(value)

    def dest_Construction_invalid_arguments_number(self):
        """Checks whether passing the wrong number of arguments to the constructor
        raises the appropriate errors
        """

        arguments = (([p1, p2, p3], [p1, p4, p3]),)  # two args

        # No args
        with self.assertRaises(TypeError):
            p = Polygon()

        for arg_seq in arguments:
            with self.assertRaises(TypeError):
                p = Polygon(*arg_seq)

    def dest_construction_invalid_polygon(self):
        """Checks whether the constructor works correctly with invalid polygons"""
        invalid_polygons = (
            [p1],  # 1
            [p1, p2],  # 2
        )

        for polygon in invalid_polygons:
            with self.assertRaises(TypeError):
                p = Polygon(polygon)

    def test_construction_TUP(self):
        """Checks whether the constructor works correctly with tuples"""
        p = Polygon((p1, p2, p3, p4))

        self.assertEqual(p.vertices, [p1, p2, p3, p4])
        print("==========================")

    def dest_construction_LIST(self):
        """Checks whether the constructor works correctly with lists"""
        p = Polygon([p1, p2, p3, p4])

        self.assertEqual(p.vertices, [p1, p2, p3, p4])
        print("==========================")

    def dest_construction_args(self):
        """Checks whether the constructor works correctly with n arguments"""
        p = Polygon(p1, p2, p3, p4)
        self.assertEqual(p.vertices, [p1, p2, p3, p4])

    def dest_construction_frompolygon(self):
        """Checks whether the constructor works correctly with another polygon"""
        po = Polygon([p1, p2, p3, p4])
        p = Polygon(po)

        self.assertEqual(p.vertices, [p1, p2, p3, p4])
        self.assertEqual(p.vertices, po.vertices)


if __name__ == "__main__":
    unittest.main()
