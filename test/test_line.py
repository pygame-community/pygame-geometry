import unittest
from math import sqrt

from pygame import Vector2, Rect

from geometry import Circle, Line


class LineTypeTest(unittest.TestCase):
    class ClassWithLineAttrib:
        def __init__(self, line):
            self.line = line

    class ClassWithLineProperty:
        def __init__(self, line):
            self._line = line

        @property
        def line(self):
            return self._line

    class ClassWithLineFunction:
        def __init__(self, line):
            self._line = line

        def line(self):
            return self._line

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
        for value in invalid_types:
            with self.assertRaises(TypeError):
                Line(0, 0, value, 2)
        # Test y2
        for value in invalid_types:
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

    def testConstruction_class_with_line_attrib(self):
        class_ = self.ClassWithLineAttrib(Line(1.1, 2.2, 3.3, 4.4))

        line = Line(class_)

        self.assertEqual(line.x1, 1.1)
        self.assertEqual(line.y1, 2.2)
        self.assertEqual(line.x2, 3.3)
        self.assertEqual(line.y2, 4.4)

    def testConstruction_class_with_line_property(self):
        class_ = self.ClassWithLineProperty(Line(1.1, 2.2, 3.3, 4.4))

        line = Line(class_)

        self.assertEqual(line.x1, 1.1)
        self.assertEqual(line.y1, 2.2)
        self.assertEqual(line.x2, 3.3)
        self.assertEqual(line.y2, 4.4)

    def testConstruction_class_with_line_function(self):
        class_ = self.ClassWithLineFunction(Line(1.1, 2.2, 3.3, 4.4))

        line = Line(class_)

        self.assertEqual(line.x1, 1.1)
        self.assertEqual(line.y1, 2.2)
        self.assertEqual(line.x2, 3.3)
        self.assertEqual(line.y2, 4.4)

    def testConstruction_degenerate(self):
        """Ensures that you can't create degenerate lines (lines with zero length)"""

        # 4 args
        with self.assertRaises(TypeError):
            Line(1.0, 2.0, 1.0, 2.0)
        with self.assertRaises(TypeError):
            Line(1, 2, 1, 2)

        # 1 list arg 4
        with self.assertRaises(TypeError):
            Line([1, 2, 1, 2])
        with self.assertRaises(TypeError):
            Line([1.0, 2.0, 1.0, 2.0])

        # 1 tuple arg 4
        with self.assertRaises(TypeError):
            Line((1, 2, 1, 2))
        with self.assertRaises(TypeError):
            Line((1.0, 2.0, 1.0, 2.0))

        # two tuple args
        with self.assertRaises(TypeError):
            Line((1, 2), (1, 2))
        with self.assertRaises(TypeError):
            Line((1.0, 2.0), (1.0, 2.0))

        # two list args
        with self.assertRaises(TypeError):
            Line([1, 2], [1, 2])
        with self.assertRaises(TypeError):
            Line([1.0, 2.0], [1.0, 2.0])

        # one list two tuple args
        with self.assertRaises(TypeError):
            Line([1, 2], (1, 2))
        with self.assertRaises(TypeError):
            Line((1, 2), [1, 2])
        with self.assertRaises(TypeError):
            Line([1.0, 2.0], (1.0, 2.0))
        with self.assertRaises(TypeError):
            Line((1.0, 2.0), [1.0, 2.0])

        # one list two sub-tuples arg
        with self.assertRaises(TypeError):
            Line([(1, 2), (1, 2)])
        with self.assertRaises(TypeError):
            Line([(1.0, 2.0), (1.0, 2.0)])

        # one tuple two sub-lists arg
        with self.assertRaises(TypeError):
            Line(([1, 2], [1, 2]))
        with self.assertRaises(TypeError):
            Line(([1.0, 2.0], [1.0, 2.0]))

    def test_attrib_x1(self):
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

    def test_attrib_y1(self):
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

    def test_attrib_x2(self):
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

    def test_attrib_y2(self):
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

    def test_attrib_a(self):
        """a full test for the y1 attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        expected_a = expected_x1, expected_y1
        expected_b = expected_x2, expected_y2
        line = Line((0, 1), expected_b)

        line.a = expected_a

        self.assertEqual(line.a, expected_a)
        self.assertEqual(line.b, expected_b)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3], 1):
            with self.assertRaises(TypeError):
                line.a = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.a

    def test_attrib_b(self):
        """a full test for the y1 attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        expected_a = expected_x1, expected_y1
        expected_b = expected_x2, expected_y2
        line = Line(expected_a, (0, 1))

        line.b = expected_b

        self.assertEqual(line.a, expected_a)
        self.assertEqual(line.b, expected_b)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3], 1):
            with self.assertRaises(TypeError):
                line.b = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.b

    def test_attrib_length(self):
        """a full test for the length attribute"""
        expected_length = 3.0
        line = Line(1, 4, 4, 4)
        self.assertEqual(line.length, expected_length)

        line.x1 = 2
        expected_length = 2.0
        self.assertEqual(line.length, expected_length)

        line.x1 = 2.7
        expected_length = 1.2999999999999998
        self.assertEqual(line.length, expected_length)

        line.y1 = 2
        expected_length = 2.3853720883753127
        self.assertEqual(line.length, expected_length)

        line.y1 = 2.7
        expected_length = 1.8384776310850233
        self.assertEqual(line.length, expected_length)

        line.x2 = 2
        expected_length = 1.4764823060233399
        self.assertEqual(line.length, expected_length)

        line.x2 = 2.7
        expected_length = 1.2999999999999998
        self.assertEqual(line.length, expected_length)

        line.y2 = 2
        expected_length = 0.7000000000000002
        self.assertEqual(line.length, expected_length)

        line.y2 = 2.7
        expected_length = 0.0
        self.assertEqual(line.length, expected_length)

        line1 = Line(7, 3, 2, 3)
        line2 = Line(9, 5, 4, 5)
        self.assertEqual(line1.length, line2.length)

        line = Line(7.6, 3.2, 2.1, 3.8)
        expected_length = 5.532630477449222
        self.assertEqual(line.length, expected_length)

        line = Line(-9.8, -5.2, -4.4, -5.6)
        expected_length = 5.414794548272353
        self.assertEqual(line.length, expected_length)

    def test_meth_copy(self):
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

    def test_meth_parallel(self):
        line1 = Line(0, 0, 10, 10)
        line2 = Line(1, 1, 11, 11)
        line3 = Line(1, 3, 11, 11)
        line4 = Line(0, 0, 0, 2)

        self.assertTrue(line1.is_parallel(line2))
        self.assertFalse(line1.is_parallel(line3))
        self.assertFalse(line1.is_parallel(line4))
        self.assertTrue(line1.is_parallel(line1))

    def test_meth_raycast(self):
        lineA = Line(0, 0, 10, 10)
        lineB = Line(0, 0, -1, -1)

        A = Line(0, 10, 10, 0)
        B = Line(0, 1, 1, 0)
        C = Line(-1, -2, -3, -4)
        D = Circle(5, 5, 1)
        E = Circle(0, 0, 1)

        with self.assertRaises(TypeError):
            lineA.raycast(A, B, C)

        with self.assertRaises(TypeError):
            lineA.raycast()

        with self.assertRaises(TypeError):
            lineA.raycast(lineA, "5")

        self.assertEqual(lineA.raycast([lineA, A, B, C]), (0.5, 0.5))
        self.assertEqual(
            lineA.raycast([D, E]), (0.7071067811865475, 0.7071067811865475)
        )
        self.assertEqual(lineA.raycast([lineA, lineB, A, B, C, D, E]), (0.5, 0.5))
        self.assertEqual(
            lineB.raycast([D, E]), (-0.7071067811865476, -0.7071067811865476)
        )
        self.assertEqual(
            lineB.raycast([lineA, lineB, A, B, C, D, E]),
            (-0.7071067811865476, -0.7071067811865476),
        )

    def test_meth_collideline(self):
        A = Line(0, 0, 1, 1)
        B = Line(0, 1, 1, 0)

        self.assertTrue(A.collideline(B))
        self.assertFalse(A.collideline(A))

        with self.assertRaises(TypeError):
            A.collideline()

        with self.assertRaises(TypeError):
            A.collideline(1, 5)

    def test_meth_colliderect(self):
        A = Line(0, 0, 1, 1)
        B = Rect(1, 1, 1, 1)
        C = Rect(-2, -2, 1, 1)

        self.assertTrue(A.colliderect(B))
        self.assertFalse(A.colliderect(C))

        with self.assertRaises(TypeError):
            A.colliderect()

        with self.assertRaises(TypeError):
            A.colliderect(1, 5)

    def test_meth_move(self):
        line = Line(1.1, 2.2, 3.3, 4.4)

        ret = line.move(1, 2)

        self.assertEqual(ret.x1, 2.1)
        self.assertEqual(ret.y1, 4.2)
        self.assertEqual(ret.x2, 4.3)
        self.assertEqual(ret.y2, 6.4)

        with self.assertRaises(TypeError):
            line.move()

        with self.assertRaises(TypeError):
            line.move(1)

        with self.assertRaises(TypeError):
            line.move(1, 2, 3)

        with self.assertRaises(TypeError):
            line.move("1", "2")

    def test_meth_move_ip(self):
        line = Line(1.1, 2.2, 3.3, 4.4)

        line.move_ip(1, 2)

        self.assertEqual(line.x1, 2.1)
        self.assertEqual(line.y1, 4.2)
        self.assertEqual(line.x2, 4.3)
        self.assertEqual(line.y2, 6.4)

        with self.assertRaises(TypeError):
            line.move_ip()

        with self.assertRaises(TypeError):
            line.move_ip(1)

        with self.assertRaises(TypeError):
            line.move_ip(1, 2, 3)

        with self.assertRaises(TypeError):
            line.move_ip("1", "2")

    def test_meth_collidepoint(self):
        A = Line(0, 0, 1, 1)

        self.assertTrue(A.collidepoint(0, 0))
        self.assertTrue(A.collidepoint(0.5, 0.5))
        self.assertTrue(A.collidepoint(1, 1))
        self.assertFalse(A.collidepoint(-1, -1))
        self.assertFalse(A.collidepoint(0.5, 0.6))
        self.assertFalse(A.collidepoint(100, 5))

        with self.assertRaises(TypeError):
            A.collidepoint()

        with self.assertRaises(TypeError):
            A.collidepoint(1, 2, 3)

    def test_meth_collidecircle(self):
        A = Line(0, 0, 1, 1)
        B = Circle(0, 0, 1)
        C = Circle(-1, -1, 0.5)

        self.assertTrue(A.collidecircle(B))
        self.assertFalse(A.collidecircle(C))

        with self.assertRaises(TypeError):
            A.collidecircle()

        with self.assertRaises(TypeError):
            A.collidecircle(1, 2, 3, 4)

    def test_meth_update(self):
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

        with self.assertRaises(TypeError):
            line.update()

        with self.assertRaises(TypeError):
            line.update(1, 2, 3, 4, 5)

        with self.assertRaises(TypeError):
            line.update(1, 2, 3)

    def test_meth_as_rect(self):
        line = Line(0, 0, 1, 1)

        with self.assertRaises(TypeError):
            line.as_rect(1, 2, 3, 4, 5)

        with self.assertRaises(TypeError):
            line.as_rect((1, 2, 3, 4))

        with self.assertRaises(TypeError):
            line.as_rect(1, 2, 3)

        with self.assertRaises(TypeError):
            line.as_rect(1, 2)

        rect = line.as_rect()

        self.assertIsInstance(rect, Rect)

        self.assertEqual(rect.x, 0)
        self.assertEqual(rect.y, 0)
        self.assertEqual(rect.width, 1)
        self.assertEqual(rect.height, 1)

        line = Line(0.5, 1.6, -1.2, -0.5)

        rect = line.as_rect()

        self.assertEqual(rect.x, -2)
        self.assertEqual(rect.y, -1)
        self.assertEqual(rect.width, 2)
        self.assertEqual(rect.height, 3)

    def test_bool(self):
        line = Line(10, 10, 4, 56)

        self.assertTrue(bool(line))

    def test__str__(self):
        line = Line(10.1, 10.2, 4.3, 56.4)
        self.assertEqual(str(line), "pygame.Line(10.1, 10.2, 4.3, 56.4)")

    def test__repr__(self):
        line = Line(10.1, 10.2, 4.3, 56.4)
        self.assertEqual(repr(line), "pygame.Line(10.1, 10.2, 4.3, 56.4)")

    def test_seq_length(self):
        self.assertEqual(len(Line(1, 2, 3, 4)), 4)

    def test_seq_getitem(self):
        line = Line(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(line[0], 1.1)
        self.assertEqual(line[1], 2.2)
        self.assertEqual(line[2], 3.3)
        self.assertEqual(line[3], 4.4)

        self.assertEqual(line[-4], 1.1)
        self.assertEqual(line[-3], 2.2)
        self.assertEqual(line[-2], 3.3)
        self.assertEqual(line[-1], 4.4)

        with self.assertRaises(IndexError):
            line[4]
        with self.assertRaises(IndexError):
            line[-5]

    def test_seq_setitem(self):
        line = Line(1.1, 2.2, 3.3, 4.4)
        line[0] = 5.5
        line[1] = 6.6
        line[2] = 7.7
        line[3] = 8.8

        self.assertEqual(line.x1, 5.5)
        self.assertEqual(line.y1, 6.6)
        self.assertEqual(line.x2, 7.7)
        self.assertEqual(line.y2, 8.8)

        line[-4] = 15.5
        line[-3] = 16.6
        line[-2] = 17.7
        line[-1] = 18.8

        self.assertEqual(line.x1, 15.5)
        self.assertEqual(line.y1, 16.6)
        self.assertEqual(line.x2, 17.7)
        self.assertEqual(line.y2, 18.8)

        with self.assertRaises(IndexError):
            line[4] = 1
        with self.assertRaises(IndexError):
            line[-5] = 1

        with self.assertRaises(TypeError):
            line[0] = (1, 2)
        with self.assertRaises(TypeError):
            line[0] = [1, 2]
        with self.assertRaises(TypeError):
            line[0] = {1: 2}
        with self.assertRaises(TypeError):
            line[0] = object()

        line[:] = 10.1
        self.assertEqual(line.x1, 10.1)
        self.assertEqual(line.y1, 10.1)
        self.assertEqual(line.x2, 10.1)
        self.assertEqual(line.y2, 10.1)

        line[0:2] = 5.59
        self.assertEqual(line.x1, 5.59)
        self.assertEqual(line.y1, 5.59)
        self.assertEqual(line.x2, 10.1)
        self.assertEqual(line.y2, 10.1)

        line[0:4] = 5.595
        self.assertEqual(line.x1, 5.595)
        self.assertEqual(line.y1, 5.595)
        self.assertEqual(line.x2, 5.595)
        self.assertEqual(line.y2, 5.595)

        line[0:4] = Line(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(line.x1, 1.1)
        self.assertEqual(line.y1, 2.2)
        self.assertEqual(line.x2, 3.3)
        self.assertEqual(line.y2, 4.4)

        with self.assertRaises(TypeError):
            line[0:4] = [1, 2, 3, 4, 5]
        with self.assertRaises(TypeError):
            line[0:4] = {1: 2, 3: 4}
        with self.assertRaises(TypeError):
            line[0:4] = object()

    def test_subscript(self):
        r = Line(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(r[0], 1.1)
        self.assertEqual(r[1], 2.2)
        self.assertEqual(r[2], 3.3)
        self.assertEqual(r[3], 4.4)
        self.assertEqual(r[-1], 4.4)
        self.assertEqual(r[-2], 3.3)
        self.assertEqual(r[-4], 1.1)
        self.assertRaises(IndexError, r.__getitem__, 5)
        self.assertRaises(IndexError, r.__getitem__, -5)
        self.assertEqual(r[0:2], [1.1, 2.2])
        self.assertEqual(r[0:4], [1.1, 2.2, 3.3, 4.4])
        self.assertEqual(r[0:-1], [1.1, 2.2, 3.3])
        self.assertEqual(r[:], [1.1, 2.2, 3.3, 4.4])
        self.assertEqual(r[...], [1.1, 2.2, 3.3, 4.4])
        self.assertEqual(r[0:4:2], [1.1, 3.3])
        self.assertEqual(r[0:4:3], [1.1, 4.4])
        self.assertEqual(r[3::-1], [4.4, 3.3, 2.2, 1.1])
        self.assertRaises(TypeError, r.__getitem__, None)

    def test_ass_subscript(self):
        r = Line(1, 2, 3, 4)
        r[...] = 1.1, 2.2, 3.3, 4.4
        self.assertEqual(r, [1.1, 2.2, 3.3, 4.4])
        self.assertRaises(TypeError, r.__setitem__, None, 0)
        self.assertEqual(r, [1.1, 2.2, 3.3, 4.4])
        self.assertRaises(TypeError, r.__setitem__, 0, "")
        self.assertEqual(r, [1.1, 2.2, 3.3, 4.4])
        self.assertRaises(IndexError, r.__setitem__, 4, 0)
        self.assertEqual(r, [1.1, 2.2, 3.3, 4.4])
        self.assertRaises(IndexError, r.__setitem__, -5, 0)
        self.assertEqual(r, [1.1, 2.2, 3.3, 4.4])
        r[0] = 10.1
        self.assertEqual(r, [10.1, 2.2, 3.3, 4.4])
        r[3] = 40.40
        self.assertEqual(r, [10.1, 2.2, 3.3, 40.4])
        r[-1] = 400.45
        self.assertEqual(r, [10.1, 2.2, 3.3, 400.45])
        r[-4] = 100.5
        self.assertEqual(r, [100.5, 2.2, 3.3, 400.45])
        r[1:3] = 0
        self.assertEqual(r, [100.5, 0, 0, 400.45])
        r[:] = 11.11, 12.12, 13.13, 14.14
        self.assertEqual(r, [11.11, 12.12, 13.13, 14.14])
        r[::-1] = r
        self.assertEqual(r, [14.14, 13.13, 12.12, 11.11])

    def test_slope_getter(self):
        lines = [
            [Line(2, 2, 4, 4), 1, False],
            [Line(4.6, 2.3, 1.6, 7.3), -5 / 3, True],
            [Line(2, 0, 2, 1), 0, False],
            [Line(1.2, 3.2, 4.5, 3.2), 0, False],
        ]

        for l in lines:
            if l[2]:
                self.assertAlmostEqual(l[0].slope, l[1])
            else:
                self.assertEqual(l[0].slope, l[1])

    def test_meth_perpendicular(self):
        # prepare the lines
        l = Line(0, 0, 1, 1)
        l2 = Line(1, 0, 0, 1)
        l3 = Line(-12, 0, 31, 1)
        l4 = Line(3, 3, 6, 6)

        # self perpendicular
        self.assertFalse(l.is_perpendicular(l))
        self.assertFalse(l.is_perpendicular((0, 0, 1, 1)))
        self.assertFalse(l.is_perpendicular(((0, 0), (1, 1))))
        self.assertFalse(l.is_perpendicular([0, 0, 1, 1]))
        self.assertFalse(l.is_perpendicular([(0, 0), (1, 1)]))

        # perpendicular
        self.assertTrue(l.is_perpendicular(l2))
        self.assertTrue(l.is_perpendicular((1, 0, 0, 1)))
        self.assertTrue(l.is_perpendicular(((1, 0), (0, 1))))
        self.assertTrue(l.is_perpendicular([1, 0, 0, 1]))
        self.assertTrue(l.is_perpendicular([(1, 0), (0, 1)]))

        # not perpendicular
        self.assertFalse(l.is_perpendicular(l3))
        self.assertFalse(l.is_perpendicular((-12, 0, 31, 1)))
        self.assertFalse(l.is_perpendicular(((-12, 0), (31, 1))))
        self.assertFalse(l.is_perpendicular([-12, 0, 31, 1]))
        self.assertFalse(l.is_perpendicular([(-12, 0), (31, 1)]))

        # parallel
        self.assertFalse(l.is_perpendicular(l4))
        self.assertFalse(l.is_perpendicular((3, 3, 6, 6)))
        self.assertFalse(l.is_perpendicular(((3, 3), (6, 6))))
        self.assertFalse(l.is_perpendicular([3, 3, 6, 6]))
        self.assertFalse(l.is_perpendicular([(3, 3), (6, 6)]))

    def test_meth_perpendicular_argtype(self):

        l = Line(0, 0, 1, 1)
        args = [
            1,
            1.1,
            "string",
            [1, 2, 3],
            [1, "s", 3, 4],
            (1, 2, 3),
            (1, "s", 3, 4),
            ((1, "s"), (3, 4)),
            ((1, 4), (3, "4")),
            {1: 2, 3: 4},
            object(),
        ]
        for value in args:
            with self.assertRaises(TypeError):
                l.is_perpendicular(value)


if __name__ == "__main__":
    unittest.main()
