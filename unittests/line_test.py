import unittest
from math import sqrt

from pygame import Vector2, Rect

from geometry import Circle, Line


class LineTypeTest(unittest.TestCase):

    def testConstruction_invalid_type(self):
        """Checks whether passing wrong types to the constructor
         raises the appropriate errors
         """
        invalid_types = (None, [], "1", (1,), [1, 2, 3], Vector2(1, 1))

        # Test x1
        for value in invalid_types:
            with self.assertRaises(TypeError):
                Line(value, 0, 1, 2)
        # Test y1
        for value in invalid_types:
            with self.assertRaises(TypeError):
                Line(0, value, 1, 2)
        # Test x2
        for value in invalid_types + (-1, ):
            with self.assertRaises(TypeError):
                Line(0, 0, value, 2)
        # Test y2
        for value in invalid_types + (-1, ):
            with self.assertRaises(TypeError):
                Line(0, 1, 2, value)

    def testConstruction_invalid_arguments_number(self):
        """Checks whether passing the wrong number of arguments to the constructor
           raises the appropriate errors
        """
        arguments = (
            (1,),  # one non vec3 non circle arg
            (1, 1),  # two args
            (1, 1, 1),  # three args
            (1, 1, 1, 1, 1),  # five args
        )

        for arg_seq in arguments:
            with self.assertRaises(TypeError):
                Line(*arg_seq)

    def testConstructionX1Y1X2Y2_float(self):

        line = Line(1.0, 2.0, 3.0, 4.0)

        self.assertEqual(line.x1, 1.0)
        self.assertEqual(line.y1, 2.0)
        self.assertEqual(line.x2, 3.0)
        self.assertEqual(line.y2, 4.0)

    def testConstructionTUP_X1Y1X2Y2_float(self):

        line = Line((1.0, 2.0, 3.0, 4.0))

        self.assertEqual(line.x1, 1.0)
        self.assertEqual(line.y1, 2.0)
        self.assertEqual(line.x2, 3.0)
        self.assertEqual(line.y2, 4.0)

    def testConstructionX1Y1X2Y2_int(self):

        line = Line(1, 2, 3, 4)

        self.assertEqual(line.x1, 1.0)
        self.assertEqual(line.y1, 2.0)
        self.assertEqual(line.x2, 3.0)
        self.assertEqual(line.y2, 4.0)

    def testConstructionTUP_X1Y1X2Y2_int(self):

        line = Line((1, 2, 3, 4))

        self.assertEqual(line.x1, 1.0)
        self.assertEqual(line.y1, 2.0)
        self.assertEqual(line.x2, 3.0)
        self.assertEqual(line.y2, 4.0)

    def test_x1(self):
        """a full test for the x1 attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(1, expected_y1, expected_x2, expected_y2)

        line.x1 = expected_x1

        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.x1 = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.x1

    def test_y1(self):
        """a full test for the y1 attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(expected_x1, 1, expected_x2, expected_y2)

        line.y1 = expected_y1

        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.y1 = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.y1

    def test_x2(self):
        """a full test for the y1 attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(expected_x1, expected_y1, 1, expected_y2)

        line.x2 = expected_x2

        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.x2 = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.x2

    def test_y2(self):
        """a full test for the y1 attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(expected_x1, expected_y1, expected_x2, 1)

        line.y2 = expected_y2

        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.y2 = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.y2

    def test_copy(self):
        line = Line(1, 2, 3, 4)
        # check 1 arg passed
        with self.assertRaises(TypeError):
            line.copy(10)

        line_2 = line.copy()
        self.assertEqual(line.x1, line_2.x1)
        self.assertEqual(line.y2, line_2.y2)
        self.assertEqual(line.x2, line_2.x2)
        self.assertEqual(line.y2, line_2.y2)

        self.assertIsNot(line, line_2)

    def test_bool(self):
        line = Line(10, 10, 4, 56)
        line2 = Line(0, 0, 0, 0)

        self.assertTrue(line)
        self.assertFalse(line2)

    def test_raycast(self):
        A = Line(0, 0, 1, 1)
        B = Line(0, 1, 1, 0)
        point = A.raycast(B)
        self.assertEqual(point, (0.5, 0.5))

        self.assertIsNone(A.raycast(A))

    def test_collideline(self):
        A = Line(0, 0, 1, 1)
        B = Line(0, 1, 1, 0)

        self.assertTrue(A.collideline(B))
        self.assertFalse(A.collideline(A))

    def test_collidepoint(self):
        A = Line(0, 0, 1, 1)

        self.assertTrue(A.collidepoint(0, 0))
        self.assertTrue(A.collidepoint(0.5, 0.5))
        self.assertTrue(A.collidepoint(1, 1))
        self.assertFalse(A.collidepoint(-1, -1))
        self.assertFalse(A.collidepoint(0.5, 0.6))
        self.assertFalse(A.collidepoint(100, 5))

    def test_collidecircle(self):
        A = Line(0, 0, 1, 1)
        B = Circle(0, 0, 1)
        C = Circle(-1, -1, 0.5)

        self.assertTrue(A.collidecircle(B))
        self.assertFalse(A.collidecircle(C))

    def test_update(self):
        line = Line(0, 0, 1, 1)

        line.update(1, 2, 3, 4)
        self.assertEqual(line.x1, 1)
        self.assertEqual(line.y1, 2)
        self.assertEqual(line.x2, 3)
        self.assertEqual(line.y2, 4)

        line.update((5, 6), (7, 8))
        self.assertEqual(line.x1, 5)
        self.assertEqual(line.y1, 6)
        self.assertEqual(line.x2, 7)
        self.assertEqual(line.y2, 8)

        line.update((9, 10, 11, 12))
        self.assertEqual(line.x1, 9)
        self.assertEqual(line.y1, 10)
        self.assertEqual(line.x2, 11)
        self.assertEqual(line.y2, 12)


if __name__ == "__main__":
    unittest.main()
