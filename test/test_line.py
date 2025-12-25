import math
import unittest
from math import sqrt

from pygame import Vector2, Vector3, Rect

from geometry import Circle, Line, Polygon, regular_polygon

E_T = "Expected True, "
E_F = "Expected False, "


def _distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_points_between(line, n_pts):
    dx = (line.xb - line.xa) / (n_pts + 1)
    dy = (line.yb - line.ya) / (n_pts + 1)

    return [(line.xa + i * dx, line.ya + i * dy) for i in range(n_pts + 2)]


def float_range(a, b, step):
    result = []
    current_value = a
    while current_value < b:
        result.append(current_value)
        current_value += step
    return result


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

        # Test xa
        for value in invalid_types:
            with self.assertRaises(TypeError):
                Line(value, 0, 1, 2)
        # Test ya
        for value in invalid_types:
            with self.assertRaises(TypeError):
                Line(0, value, 1, 2)
        # Test xb
        for value in invalid_types:
            with self.assertRaises(TypeError):
                Line(0, 0, value, 2)
        # Test yb
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

        self.assertEqual(line.xa, 1.0)
        self.assertEqual(line.ya, 2.0)
        self.assertEqual(line.xb, 3.0)
        self.assertEqual(line.yb, 4.0)

    def testConstructionTUP_X1Y1X2Y2_float(self):
        line = Line((1.0, 2.0, 3.0, 4.0))

        self.assertEqual(line.xa, 1.0)
        self.assertEqual(line.ya, 2.0)
        self.assertEqual(line.xb, 3.0)
        self.assertEqual(line.yb, 4.0)

    def testConstructionX1Y1X2Y2_int(self):
        line = Line(1, 2, 3, 4)

        self.assertEqual(line.xa, 1.0)
        self.assertEqual(line.ya, 2.0)
        self.assertEqual(line.xb, 3.0)
        self.assertEqual(line.yb, 4.0)

    def testConstructionTUP_X1Y1X2Y2_int(self):
        line = Line((1, 2, 3, 4))

        self.assertEqual(line.xa, 1.0)
        self.assertEqual(line.ya, 2.0)
        self.assertEqual(line.xb, 3.0)
        self.assertEqual(line.yb, 4.0)

    def testConstruction_class_with_line_attrib(self):
        class_ = self.ClassWithLineAttrib(Line(1.1, 2.2, 3.3, 4.4))

        line = Line(class_)

        self.assertEqual(line.xa, 1.1)
        self.assertEqual(line.ya, 2.2)
        self.assertEqual(line.xb, 3.3)
        self.assertEqual(line.yb, 4.4)

    def testConstruction_class_with_line_property(self):
        class_ = self.ClassWithLineProperty(Line(1.1, 2.2, 3.3, 4.4))

        line = Line(class_)

        self.assertEqual(line.xa, 1.1)
        self.assertEqual(line.ya, 2.2)
        self.assertEqual(line.xb, 3.3)
        self.assertEqual(line.yb, 4.4)

    def testConstruction_class_with_line_function(self):
        class_ = self.ClassWithLineFunction(Line(1.1, 2.2, 3.3, 4.4))

        line = Line(class_)

        self.assertEqual(line.xa, 1.1)
        self.assertEqual(line.ya, 2.2)
        self.assertEqual(line.xb, 3.3)
        self.assertEqual(line.yb, 4.4)

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
        """a full test for the xa attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(1, expected_y1, expected_x2, expected_y2)

        line.xa = expected_x1

        self.assertEqual(line.xa, expected_x1)
        self.assertEqual(line.ya, expected_y1)
        self.assertEqual(line.xb, expected_x2)
        self.assertEqual(line.yb, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.xa = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.xa

    def test_attrib_y1(self):
        """a full test for the ya attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(expected_x1, 1, expected_x2, expected_y2)

        line.ya = expected_y1

        self.assertEqual(line.xa, expected_x1)
        self.assertEqual(line.ya, expected_y1)
        self.assertEqual(line.xb, expected_x2)
        self.assertEqual(line.yb, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.ya = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.ya

    def test_attrib_x2(self):
        """a full test for the ya attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(expected_x1, expected_y1, 1, expected_y2)

        line.xb = expected_x2

        self.assertEqual(line.xa, expected_x1)
        self.assertEqual(line.ya, expected_y1)
        self.assertEqual(line.xb, expected_x2)
        self.assertEqual(line.yb, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.xb = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.xb

    def test_attrib_y2(self):
        """a full test for the ya attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        line = Line(expected_x1, expected_y1, expected_x2, 1)

        line.yb = expected_y2

        self.assertEqual(line.xa, expected_x1)
        self.assertEqual(line.ya, expected_y1)
        self.assertEqual(line.xb, expected_x2)
        self.assertEqual(line.yb, expected_y2)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.yb = value

        line = Line(0, 0, 1, 0)

        with self.assertRaises(AttributeError):
            del line.yb

    def test_attrib_a(self):
        """a full test for the ya attribute"""
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
        """a full test for the ya attribute"""
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

    def test_attrib_angle(self):
        """a full test for the angle attribute"""
        expected_angle = -83.93394864782331
        line = Line(300.0, 400.0, 400.0, 1341.0)
        self.assertEqual(line.angle, expected_angle)

        expected_angle = 16.17215901578255
        line = Line(300.0, 400.0, 400.0, 371.0)
        self.assertEqual(line.angle, expected_angle)

        expected_angle = -35.53767779197438
        line = Line(45.0, 32.0, 94.0, 67.0)
        self.assertEqual(line.angle, expected_angle)

        expected_angle = -53.88065915052025
        line = Line(544.0, 235.0, 382.0, 13.0)
        self.assertEqual(line.angle, expected_angle)

    def test_attrib_length(self):
        """a full test for the length attribute"""
        expected_length = 3.0
        line = Line(1, 4, 4, 4)
        self.assertEqual(line.length, expected_length)

        line.xa = 2
        expected_length = 2.0
        self.assertEqual(line.length, expected_length)

        line.xa = 2.7
        expected_length = 1.2999999999999998
        self.assertEqual(line.length, expected_length)

        line.ya = 2
        expected_length = 2.3853720883753127
        self.assertEqual(line.length, expected_length)

        line.ya = 2.7
        expected_length = 1.8384776310850233
        self.assertEqual(line.length, expected_length)

        line.xb = 2
        expected_length = 1.4764823060233399
        self.assertEqual(line.length, expected_length)

        line.xb = 2.7
        expected_length = 1.2999999999999998
        self.assertEqual(line.length, expected_length)

        line.yb = 2
        expected_length = 0.7000000000000002
        self.assertEqual(line.length, expected_length)

        line.yb = 2.7
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

    def test_attrib_center(self):
        """a full test for the center attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        expected_a = expected_x1, expected_y1
        expected_b = expected_x2, expected_y2
        expected_center = (expected_x1 + expected_x2) / 2, (
            expected_y1 + expected_y2
        ) / 2
        line = Line(expected_a, expected_b)

        self.assertEqual(line.center, expected_center)

        line.center = expected_center[0] - 1, expected_center[1] + 1.321

        self.assertEqual(
            line.center, (expected_center[0] - 1, expected_center[1] + 1.321)
        )

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3], 1, 1.2):
            with self.assertRaises(TypeError):
                line.center = value

        with self.assertRaises(AttributeError):
            del line.center

    def test_attrib_centerx(self):
        """a full test for the centerx attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        expected_a = expected_x1, expected_y1
        expected_b = expected_x2, expected_y2
        expected_center = (expected_x1 + expected_x2) / 2, (
            expected_y1 + expected_y2
        ) / 2
        line = Line(expected_a, expected_b)

        self.assertEqual(line.centerx, expected_center[0])

        line.centerx = expected_center[0] - 1

        self.assertEqual(line.centerx, expected_center[0] - 1)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.centerx = value

        with self.assertRaises(AttributeError):
            del line.centerx

    def test_attrib_centery(self):
        """a full test for the centery attribute"""
        expected_x1 = 10.0
        expected_y1 = 2.0
        expected_x2 = 5.0
        expected_y2 = 6.0
        expected_a = expected_x1, expected_y1
        expected_b = expected_x2, expected_y2
        expected_center = (expected_x1 + expected_x2) / 2, (
            expected_y1 + expected_y2
        ) / 2
        line = Line(expected_a, expected_b)

        self.assertEqual(line.centery, expected_center[1])

        line.centery = expected_center[1] - 1.321

        self.assertEqual(line.centery, expected_center[1] - 1.321)

        line = Line(0, 0, 1, 0)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                line.centery = value

        with self.assertRaises(AttributeError):
            del line.centery

    def test_collide_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1)

        l = Line(10, 10, 60, 60)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                l.collide(value)

    def test_collide_argnum(self):
        l = Line(10, 10, 4, 4)
        args = [tuple(range(x)) for x in range(2, 4)]

        # no params
        with self.assertRaises(TypeError):
            l.collide()

        # too many params
        for arg in args:
            with self.assertRaises(TypeError):
                l.collide(*arg)

    def test_collide(self):
        """Ensures the collide function correctly registers collisions with circles, lines, rects and points"""
        l = Line(10, 10, 200, 200)

        # line
        l2 = Line(400, 300, 10, 100)
        l3 = Line(400, 300, 10, 200)

        self.assertTrue(l.collide(l2), E_T + "lines should collide here")
        self.assertFalse(l.collide(l3), E_F + "lines should not collide here")

        # circle
        c = Circle(10, 10, 10)
        c2 = Circle(50, 10, 10)
        self.assertTrue(l.collide(c), E_T + "circle should collide here")
        self.assertFalse(l.collide(c2), E_F + "circle should not collide here")

        # rect
        r = Rect(10, 10, 10, 10)
        r2 = Rect(50, 10, 10, 10)
        self.assertTrue(l.collide(r), E_T + "rect should collide here")
        self.assertFalse(l.collide(r2), E_F + "rect should not collide here")

        # point
        p = (11, 11)
        p2 = (60, 80)
        self.assertTrue(c.collide(p), E_T + "point should collide here")
        self.assertFalse(c.collide(p2), E_F + "point should not collide here")

        # polygon
        l4 = Line(0, 0, 10, 10)
        po1 = regular_polygon(4, l4.center, 100)
        po2 = Polygon((100, 100), (150, 150), (150, 100))
        po3 = regular_polygon(4, l4.a, 10)
        po4 = Polygon((5, 5), (5, 10), (0, 10), (2.5, 2.5))
        po5 = Polygon((0, 0), (0, 10), (-5, 10), (-5, 0))

        self.assertTrue(l4.collide(po1))
        self.assertFalse(l4.collide(po2))
        self.assertTrue(l4.collide(po3))
        self.assertTrue(l4.collide(po4))
        self.assertTrue(l4.collide(po5))

    def test_meth_copy(self):
        line = Line(1, 2, 3, 4)
        # check 1 arg passed
        with self.assertRaises(TypeError):
            line.copy(10)

        line_2 = line.copy()
        self.assertEqual(line.xa, line_2.xa)
        self.assertEqual(line.yb, line_2.yb)
        self.assertEqual(line.xb, line_2.xb)
        self.assertEqual(line.yb, line_2.yb)

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

        self.assertEqual(ret.xa, 2.1)
        self.assertEqual(ret.ya, 4.2)
        self.assertEqual(ret.xb, 4.3)
        self.assertEqual(ret.yb, 6.4)

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

        self.assertEqual(line.xa, 2.1)
        self.assertEqual(line.ya, 4.2)
        self.assertEqual(line.xb, 4.3)
        self.assertEqual(line.yb, 6.4)

        with self.assertRaises(TypeError):
            line.move_ip()

        with self.assertRaises(TypeError):
            line.move_ip(1)

        with self.assertRaises(TypeError):
            line.move_ip(1, 2, 3)

        with self.assertRaises(TypeError):
            line.move_ip("1", "2")

    def test_meth_scale(self):
        line = Line(0, 0, 10, 0).scale(2, 0)
        self.assertEqual(line.length, 20)
        line = Line(0, 0, 20, 0).scale(2.1, 0)
        self.assertEqual(line.length, 42)
        line = Line(0, 0, 10, 0).scale(4, 0)
        self.assertEqual(line.length, 40)
        line = Line(0, 0, 10, 0).scale(3, 0)
        self.assertEqual(line.length, 30)
        line = Line(10, 10, 20, 20).scale(2, 0)
        self.assertEqual(line.length, 28.284271247461902)
        line = Line(10, 10, 20, 20).scale(2, 0.5)
        self.assertEqual(line.length, 28.284271247461902)
        line = Line(10, 10, 20, 20).scale(2, 1)
        self.assertEqual(line.length, 28.284271247461902)

        with self.assertRaises(ValueError):
            line = line.scale(0, 0.5)

        with self.assertRaises(ValueError):
            line = line.scale(2, -0.1)

        with self.assertRaises(ValueError):
            line = line.scale(-2, -0.5)

        with self.assertRaises(ValueError):
            line = line.scale(17, 1.1)

        with self.assertRaises(ValueError):
            line = line.scale(17, 10.0)

    def test_meth_scale_ip(self):
        line = Line(0, 0, 10, 0)
        line.scale_ip(2, 0)
        self.assertEqual(line.length, 20)
        line = Line(0, 0, 20, 0)
        line.scale_ip(2.1, 0)
        self.assertEqual(line.length, 42)
        line = Line(0, 0, 10, 0)
        line.scale_ip(4, 0)
        self.assertEqual(line.length, 40)
        line = Line(0, 0, 10, 0)
        line.scale_ip(3, 0)
        self.assertEqual(line.length, 30)
        line = Line(10, 10, 20, 20)
        line.scale_ip(2, 0)
        self.assertEqual(line.length, 28.284271247461902)
        line = Line(10, 10, 20, 20)
        line.scale_ip(2, 0.5)
        self.assertEqual(line.length, 28.284271247461902)
        line = Line(10, 10, 20, 20)
        line.scale_ip(2, 1.0)
        self.assertEqual(line.length, 28.284271247461902)

        with self.assertRaises(ValueError):
            line.scale_ip(0, 0.5)

        with self.assertRaises(ValueError):
            line.scale_ip(2, -0.1)

        with self.assertRaises(ValueError):
            line.scale_ip(-2, -0.5)

        with self.assertRaises(ValueError):
            line.scale_ip(17, 1.1)

        with self.assertRaises(ValueError):
            line.scale_ip(17, 10.0)

    def test_meth_flip(self):
        line = Line(1.1, 2.2, 3.3, 4.4)

        ret = line.flip_ab()

        self.assertIsInstance(ret, Line)
        self.assertEqual(ret.xa, 3.3)
        self.assertEqual(ret.ya, 4.4)
        self.assertEqual(ret.xb, 1.1)
        self.assertEqual(ret.yb, 2.2)

        with self.assertRaises(TypeError):
            line.flip_ab(1)

    def test_meth_flip_ab_ip(self):
        line = Line(1.1, 2.2, 3.3, 4.4)

        line.flip_ab_ip()

        self.assertEqual(line.xa, 3.3)
        self.assertEqual(line.ya, 4.4)
        self.assertEqual(line.xb, 1.1)
        self.assertEqual(line.yb, 2.2)

        with self.assertRaises(TypeError):
            line.flip_ab_ip(1)

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

    def test_meth_as_circle(self):
        line = Line(3, 5, 7, 5)
        circle = line.as_circle()

        self.assertIsInstance(circle, Circle)
        self.assertEqual(circle.x, 5)
        self.assertEqual(circle.y, 5)
        self.assertEqual(circle.r, 2)

        with self.assertRaises(TypeError):
            line.as_circle(1)

    def test_meth_update(self):
        line = Line(0, 0, 1, 1)

        line.update(1, 2, 3, 4)
        self.assertEqual(line.xa, 1)
        self.assertEqual(line.ya, 2)
        self.assertEqual(line.xb, 3)
        self.assertEqual(line.yb, 4)

        line.update((5, 6), (7, 8))
        self.assertEqual(line.xa, 5)
        self.assertEqual(line.ya, 6)
        self.assertEqual(line.xb, 7)
        self.assertEqual(line.yb, 8)

        line.update((9, 10, 11, 12))
        self.assertEqual(line.xa, 9)
        self.assertEqual(line.ya, 10)
        self.assertEqual(line.xb, 11)
        self.assertEqual(line.yb, 12)

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
        """Checks whether the __str__ method works correctly."""
        l_str = "<Line((10.1, 10.2), (4.3, 56.4))>"
        line = Line(10.1, 10.2, 4.3, 56.4)
        self.assertEqual(str(line), l_str)
        self.assertEqual(line.__str__(), l_str)

    def test__repr__(self):
        """Checks whether the __repr__ method works correctly."""
        l_repr = "<Line((10.1, 10.2), (4.3, 56.4))>"
        line = Line(10.1, 10.2, 4.3, 56.4)
        self.assertEqual(repr(line), l_repr)
        self.assertEqual(line.__repr__(), l_repr)

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

        self.assertEqual(line.xa, 5.5)
        self.assertEqual(line.ya, 6.6)
        self.assertEqual(line.xb, 7.7)
        self.assertEqual(line.yb, 8.8)

        line[-4] = 15.5
        line[-3] = 16.6
        line[-2] = 17.7
        line[-1] = 18.8

        self.assertEqual(line.xa, 15.5)
        self.assertEqual(line.ya, 16.6)
        self.assertEqual(line.xb, 17.7)
        self.assertEqual(line.yb, 18.8)

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
        self.assertEqual(line.xa, 10.1)
        self.assertEqual(line.ya, 10.1)
        self.assertEqual(line.xb, 10.1)
        self.assertEqual(line.yb, 10.1)

        line[0:2] = 5.59
        self.assertEqual(line.xa, 5.59)
        self.assertEqual(line.ya, 5.59)
        self.assertEqual(line.xb, 10.1)
        self.assertEqual(line.yb, 10.1)

        line[0:4] = 5.595
        self.assertEqual(line.xa, 5.595)
        self.assertEqual(line.ya, 5.595)
        self.assertEqual(line.xb, 5.595)
        self.assertEqual(line.yb, 5.595)

        line[0:4] = Line(1.1, 2.2, 3.3, 4.4)
        self.assertEqual(line.xa, 1.1)
        self.assertEqual(line.ya, 2.2)
        self.assertEqual(line.xb, 3.3)
        self.assertEqual(line.yb, 4.4)

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

    def test_meth_at(self):
        invalid_types = (None, [], "1", (1,), [1, 2, 3], Vector2(1, 1))

        line = Line(0, 0, 1, 1)

        # Test xa
        for value in invalid_types:
            with self.assertRaises(TypeError):
                line.at(value)

        self.assertEqual(line.at(0.5), (0.5, 0.5))
        self.assertEqual(line.at(1), (1, 1))
        self.assertEqual(line.at(0), (0, 0))
        self.assertEqual(line.at(-1), (-1, -1))
        self.assertEqual(line.at(2), (2, 2))

        self.assertIsInstance(line.at(0.5), tuple)
        self.assertIsInstance(line.at(1), tuple)
        self.assertIsInstance(line.at(0), tuple)
        self.assertIsInstance(line.at(-1), tuple)
        self.assertIsInstance(line.at(2), tuple)

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

    def test_collidepolygon_argtype(self):
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
            Line(10, 10, 4, 4),
            Rect(10, 10, 4, 4),
            Vector3(10, 10, 4),
            Vector2(10, 10),
        )

        l = Line(0, 0, 1, 1)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                l.collidepolygon(value)
            with self.assertRaises(TypeError):
                l.collidepolygon(value, True)
            with self.assertRaises(TypeError):
                l.collidepolygon(value, False)

    def test_collidepolygon_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        l = Line(0, 0, 1, 1)

        poly = Polygon((-5, 0), (5, 0), (0, 5))
        invalid_args = [
            (poly, poly),
            (poly, poly, poly),
            (poly, poly, poly, poly),
        ]

        with self.assertRaises(TypeError):
            l.collidepolygon()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                l.collidepolygon(*arg)
            with self.assertRaises(TypeError):
                l.collidepolygon(*arg, True)
            with self.assertRaises(TypeError):
                l.collidepolygon(*arg, False)

    def test_collidepolygon_return_type(self):
        """Tests if the function returns the correct type"""
        l = Line(0, 0, 1, 1)

        vertices = [(-5, 0), (5, 0), (0, 5)]

        items = [
            Polygon(vertices),
            vertices,
            tuple(vertices),
            [list(v) for v in vertices],
        ]

        for item in items:
            self.assertIsInstance(l.collidepolygon(item), bool)
            self.assertIsInstance(l.collidepolygon(item, True), bool)
            self.assertIsInstance(l.collidepolygon(item, False), bool)

        self.assertIsInstance(l.collidepolygon(*vertices), bool)
        self.assertIsInstance(l.collidepolygon(*vertices, True), bool)
        self.assertIsInstance(l.collidepolygon(*vertices, False), bool)

    def test_collidepolygon_no_invalidation(self):
        """Ensures that the function doesn't modify the polygon or the circle"""
        l = Line((0, 0), (1, 1))
        poly = Polygon((-5, 0), (5, 0), (0, 5))

        l_copy = l.copy()
        poly_copy = poly.copy()

        l.collidepolygon(poly)

        self.assertEqual(l.a, l_copy.a)
        self.assertEqual(l.b, l_copy.b)

        self.assertEqual(poly.vertices, poly_copy.vertices)
        self.assertEqual(poly.verts_num, poly_copy.verts_num)
        self.assertEqual(poly.centerx, poly_copy.centerx)
        self.assertEqual(poly.centery, poly_copy.centery)

    def test_collidepolygon_invalid_only_edges_param(self):
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
                l.collidepolygon(poly, value)

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

    def test_meth_as_points(self):
        """Test the as_points method."""
        l = Line(0, 0, 1, 1)

        for i in range(100):
            pts = l.as_points(i)
            self.assertEqual(2 + i, len(pts))
            ex_pts = get_points_between(l, i)

            for actual_pt, expected_pt in zip(pts, ex_pts):
                self.assertIsInstance(actual_pt, tuple)
                self.assertEqual(2, len(actual_pt))
                self.assertAlmostEqual(expected_pt[0], actual_pt[0], places=14)
                self.assertAlmostEqual(expected_pt[1], actual_pt[1], places=14)

            self.assertAlmostEqual(
                sum(_distance(p1, p2) for p1, p2 in zip(pts, pts[1:])), l.length
            )

    def test_meth_as_points_argtype(self):
        l = Line(0, 0, 1, 1)
        args = [
            "string",
            None,
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
                l.as_points(value)

    def test_meth_as_points_argnum(self):
        l = Line(0, 0, 1, 1)
        args = [
            (1, 2),
            (1, 2, 3),
            (1, 2, 3, 4),
            (1, 2, 3, 4, 5),
        ]
        for value in args:
            with self.assertRaises(TypeError):
                l.as_points(*value)

    def test_meth_as_points_argvalue(self):
        l = Line(0, 0, 1, 1)
        args = [
            -1,
            -2,
            -3,
            -4,
            -5,
        ]
        for value in args:
            with self.assertRaises(ValueError):
                l.as_points(value)

    def test_meth_as_segments_argtype(self):
        l = Line(0, 0, 1, 1)
        args = [
            "string",
            None,
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
                l.as_segments(value)

    def test_meth_as_segments_argnum(self):
        l = Line(0, 0, 1, 1)
        args = [
            (1, 2),
            (1, 2, 3),
            (1, 2, 3, 4),
            (1, 2, 3, 4, 5),
        ]
        for value in args:
            with self.assertRaises(TypeError):
                l.as_segments(*value)

    def test_meth_as_segments_argvalue(self):
        l = Line(0, 0, 1, 1)
        args = [
            0,
            -1,
            -2,
            -3,
            -4,
            -5,
        ]
        for value in args:
            with self.assertRaises(ValueError):
                l.as_segments(value)

    def test_meth_rotate_ip_invalid_argnum(self):
        """Ensures that the rotate_ip method correctly deals with invalid numbers of arguments."""
        l = Line(0, 0, 1, 1)

        with self.assertRaises(TypeError):
            l.rotate_ip()

        invalid_args = [
            (1, (2, 2), 2),
            (1, (2, 2), 2, 2),
            (1, (2, 2), 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2, 2),
        ]

        for args in invalid_args:
            with self.assertRaises(TypeError):
                l.rotate_ip(*args)

    def test_meth_rotate_ip_invalid_argtype(self):
        """Ensures that the rotate_ip method correctly deals with invalid argument types."""
        l = Line(0, 0, 1, 1)

        invalid_args = [
            ("a",),  # angle str
            (None,),  # angle str
            ((1, 2)),  # angle tuple
            ([1, 2]),  # angle list
            (1, "a"),  # origin str
            (1, None),  # origin None
            (1, True),  # origin True
            (1, False),  # origin False
            (1, (1, 2, 3)),  # origin tuple
            (1, [1, 2, 3]),  # origin list
            (1, (1, "a")),  # origin str
            (1, ("a", 1)),  # origin str
            (1, (1, None)),  # origin None
            (1, (None, 1)),  # origin None
            (1, (1, (1, 2))),  # origin tuple
            (1, (1, [1, 2])),  # origin list
        ]

        for value in invalid_args:
            with self.assertRaises(TypeError):
                l.rotate_ip(*value)

    def test_meth_rotate_ip_return(self):
        """Ensures that the rotate_ip method always returns None."""
        l = Line(0, 0, 1, 1)

        for angle in float_range(-360, 360, 1):
            self.assertIsNone(l.rotate_ip(angle))
            self.assertIsInstance(l.rotate_ip(angle), type(None))

    def test_meth_rotate_invalid_argnum(self):
        """Ensures that the rotate method correctly deals with invalid numbers of arguments."""
        l = Line(0, 0, 1, 1)

        with self.assertRaises(TypeError):
            l.rotate()

        invalid_args = [
            (1, (2, 2), 2),
            (1, (2, 2), 2, 2),
            (1, (2, 2), 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2, 2),
        ]

        for args in invalid_args:
            with self.assertRaises(TypeError):
                l.rotate(*args)

    def test_meth_rotate_invalid_argtype(self):
        """Ensures that the rotate method correctly deals with invalid argument types."""
        l = Line(0, 0, 1, 1)

        invalid_args = [
            ("a",),  # angle str
            (None,),  # angle str
            ((1, 2)),  # angle tuple
            ([1, 2]),  # angle list
            (1, "a"),  # origin str
            (1, None),  # origin None
            (1, True),  # origin True
            (1, False),  # origin False
            (1, (1, 2, 3)),  # origin tuple
            (1, [1, 2, 3]),  # origin list
            (1, (1, "a")),  # origin str
            (1, ("a", 1)),  # origin str
            (1, (1, None)),  # origin None
            (1, (None, 1)),  # origin None
            (1, (1, (1, 2))),  # origin tuple
            (1, (1, [1, 2])),  # origin list
        ]

        for value in invalid_args:
            with self.assertRaises(TypeError):
                l.rotate(*value)

    def test_meth_rotate_return(self):
        """Ensures that the rotate method always returns a Line."""
        l = Line(0, 0, 1, 1)

        for angle in float_range(-360, 360, 1):
            self.assertIsInstance(l.rotate(angle), Line)

    def test_meth_rotate(self):
        """Ensures the Line.rotate() method rotates the line correctly."""

        def rotate_line(line: Line, angle, center):
            def rotate_point(x, y, rang, cx, cy):
                x -= cx
                y -= cy
                x_new = x * math.cos(rang) - y * math.sin(rang)
                y_new = x * math.sin(rang) + y * math.cos(rang)
                return x_new + cx, y_new + cy

            angle = math.radians(angle)
            x1, y1 = line.a
            x2, y2 = line.b
            cx, cy = center if center is not None else line.center
            x1, y1 = rotate_point(x1, y1, angle, cx, cy)
            x2, y2 = rotate_point(x2, y2, angle, cx, cy)
            return Line(x1, y1, x2, y2)

        def assert_approx_equal(line1, line2, eps=1e-12):
            self.assertAlmostEqual(line1.xa, line2.xa, delta=eps)
            self.assertAlmostEqual(line1.ya, line2.ya, delta=eps)
            self.assertAlmostEqual(line1.xb, line2.xb, delta=eps)
            self.assertAlmostEqual(line1.yb, line2.yb, delta=eps)

        l = Line(0, 0, 1, 1)
        angles = float_range(-360, 360, 0.5)
        centers = [(a, b) for a in range(-10, 10) for b in range(-10, 10)]
        for angle in angles:
            assert_approx_equal(l.rotate(angle), rotate_line(l, angle, None))
            for center in centers:
                assert_approx_equal(
                    l.rotate(angle, center), rotate_line(l, angle, center)
                )

    def test_meth_rotate_ip(self):
        """Ensures the Line.rotate_ip() method rotates the line correctly."""

        def rotate_line(line: Line, angle, center):
            def rotate_point(x, y, rang, cx, cy):
                x -= cx
                y -= cy
                x_new = x * math.cos(rang) - y * math.sin(rang)
                y_new = x * math.sin(rang) + y * math.cos(rang)
                return x_new + cx, y_new + cy

            angle = math.radians(angle)
            x1, y1 = line.a
            x2, y2 = line.b
            cx, cy = center if center is not None else line.center
            x1, y1 = rotate_point(x1, y1, angle, cx, cy)
            x2, y2 = rotate_point(x2, y2, angle, cx, cy)
            return Line(x1, y1, x2, y2)

        def assert_approx_equal(line1, line2, eps=1e-12):
            self.assertAlmostEqual(line1.xa, line2.xa, delta=eps)
            self.assertAlmostEqual(line1.ya, line2.ya, delta=eps)
            self.assertAlmostEqual(line1.xb, line2.xb, delta=eps)
            self.assertAlmostEqual(line1.yb, line2.yb, delta=eps)

        l = Line(0, 0, 1, 1)
        angles = float_range(-360, 360, 0.5)
        centers = [(a, b) for a in range(-10, 10) for b in range(-10, 10)]
        for angle in angles:
            new_l = l.copy()
            new_l.rotate_ip(angle)
            assert_approx_equal(new_l, rotate_line(l, angle, None))
            for center in centers:
                new_l = l.copy()
                new_l.rotate_ip(angle, center)
                assert_approx_equal(new_l, rotate_line(l, angle, center))


if __name__ == "__main__":
    unittest.main()
