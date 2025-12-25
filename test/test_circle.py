import math
import unittest
from math import sqrt

from geometry import Circle, Line, Polygon, regular_polygon
from pygame import Rect
from pygame import Vector2, Vector3

E_T = "Expected True, "
E_F = "Expected False, "


def float_range(a, b, step):
    result = []
    current_value = a
    while current_value < b:
        result.append(current_value)
        current_value += step
    return result


class CircleTypeTest(unittest.TestCase):
    def testConstruction_invalid_type(self):
        """Checks whether passing wrong types to the constructor
        raises the appropriate errors
        """
        invalid_types = (None, [], "1", (1,), [1, 2, 3], Vector2(1, 1))

        # Test x
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle(value, 0, 1)
        # Test y
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle(0, value, 1)
        # Test r
        for value in invalid_types + (-1,):
            with self.assertRaises(TypeError):
                c = Circle(0, 0, value)

    def test2ndConstruction_invalid_type(self):
        """Checks whether passing wrong types to the 2nd constructor
        raises the appropriate errors
        """
        invalid_types = (None, [], "1", (1,), [1, 2, 3], Vector2(1, 1))

        # Test x
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle((value, 0), 1)
        # Test y
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle((0, value), 1)
        # Test r
        for value in invalid_types + (-1,):
            with self.assertRaises(TypeError):
                c = Circle((0, 0), value)

    def testConstruction_invalid_arguments_number(self):
        """Checks whether passing the wrong number of arguments to the constructor
        raises the appropriate errors
        """
        arguments = (
            (1,),  # one non vec3 non circle arg
            (1, 1, 1, 1),  # four args
        )

        for arg_seq in arguments:
            with self.assertRaises(TypeError):
                c = Circle(*arg_seq)

    def testConstructionXYR_float(self):
        c = Circle(1.0, 2.0, 3.0)

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testConstructionTUP_XYR_float(self):
        c = Circle((1.0, 2.0, 3.0))

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testConstructionXYR_int(self):
        c = Circle(1, 2, 3)

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testConstructionTUP_XYR_int(self):
        c = Circle((1, 2, 3))

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testCalculatedAttributes(self):
        """Tests whether the circle correctly calculates the r_sqr attribute on creation"""
        c = Circle(1.0, 2.0, 3.0)
        self.assertEqual(9.0, c.r_sqr)

    def test_x(self):
        """Ensures changing the x attribute moves the circle and does not change
        the circle's radius.
        """
        expected_x = 10.0
        expected_y = 2.0
        expected_radius = 5.0
        c = Circle(1, expected_y, expected_radius)

        c.x = expected_x

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

    def test_x__invalid_value(self):
        """Ensures the x attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.x = value

    def test_x__del(self):
        """Ensures the x attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.x

    def test_y(self):
        """Ensures changing the y attribute moves the circle and does not change
        the circle's radius.
        """
        expected_x = 10.0
        expected_y = 2.0
        expected_radius = 5.0
        c = Circle(expected_x, 1, expected_radius)

        c.y = expected_y

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

    def test_y__invalid_value(self):
        """Ensures the y attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.y = value

    def test_y__del(self):
        """Ensures the y attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.y

    def test_r(self):
        """Ensures changing the r attribute changes the radius without moving the circle."""
        expected_x = 10.0
        expected_y = 2.0
        expected_radius = 5.0
        c = Circle(expected_x, expected_y, 1.0)

        c.r = expected_radius

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

    def test_r__invalid_value(self):
        """Ensures the r attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.r = value

        for value in (-10.3234, -1, 0, 0.0):
            with self.assertRaises(ValueError):
                c.r = value

    def test_r__del(self):
        """Ensures the r attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.r

    def test_r_sqr(self):
        """Ensures setting the r_sqr attribute matches the r_sqr passed"""
        expected_r_sqr = 10.0
        c = Circle(1.0, 1.0, 1.0)
        c.r_sqr = expected_r_sqr

        self.assertAlmostEqual(c.r_sqr, expected_r_sqr, places=14)

    def test_r_to_r_sqr(self):
        """Ensures changing the r attribute correctly changes the r_sqr attribute."""
        expected_r_sqr = 1.0
        expected_r_sqr2 = 100.0

        c = Circle(0, 0, 23)
        c2 = Circle(0, 0, 4)

        c.r = 1
        self.assertEqual(c.r_sqr, expected_r_sqr)

        c2.r = 10
        self.assertEqual(c2.r_sqr, expected_r_sqr2)

    def test_r_sqr_to_r(self):
        """Ensures changing the r_sqr attribute correctly changes the r attribute."""
        expected_r = 2.0

        c = Circle(0, 0, 23)

        c.r_sqr = 4.0
        self.assertEqual(c.r, expected_r)

        c.r_sqr = 13.33421
        self.assertEqual(c.r, sqrt(13.33421))

    def test_r_sqr__invalid_set(self):
        """Ensures the r_sqr attribute can't be set"""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.r_sqr = value

    def test_r_sqr__del(self):
        """Ensures the r attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.r

    def test_center(self):
        """Ensures changing the center moves the circle and does not change
        the circle's radius.
        """
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.center = (expected_x, expected_y)

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

    def test_center_update(self):
        """Ensures changing the x or y value of the circle correctly updates the center."""
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.x = expected_x
        self.assertEqual(c.center, (expected_x, c.y))

        c.y = expected_y
        self.assertEqual(c.center, (c.x, expected_y))

    def test_center_invalid_value(self):
        """Ensures the center attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.center = value

    def test_center_del(self):
        """Ensures the center attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.center

    def test_top(self):
        """Ensures changing the top attribute moves the circle and does not change the circle's radius."""
        expected_radius = 5.0

        for pos in [
            (1, 0),
            (0, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]:
            c = Circle((0, 0), expected_radius)

            c.top = pos

            self.assertEqual(pos[0], c.x)
            self.assertEqual(pos[1], c.y - expected_radius)

            self.assertEqual(expected_radius, c.r)

    def test_top_update(self):
        """Ensures changing the x or y value of the circle correctly updates the top."""
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.x = expected_x
        self.assertEqual(c.top, (expected_x, c.y - expected_radius))

        c.y = expected_y
        self.assertEqual(c.top, (c.x, expected_y - expected_radius))

    def test_top_invalid_value(self):
        """Ensures the top attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3], True, False):
            with self.assertRaises(TypeError):
                c.top = value

    def test_top_del(self):
        """Ensures the top attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.top

    def test_left(self):
        """Ensures changing the left attribute moves the circle and does not change the circle's radius."""
        expected_radius = 5.0

        for pos in [
            (1, 0),
            (0, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]:
            c = Circle((0, 0), expected_radius)

            c.left = pos

            self.assertEqual(pos[0], c.x - expected_radius)
            self.assertEqual(pos[1], c.y)

            self.assertEqual(expected_radius, c.r)

    def test_left_update(self):
        """Ensures changing the x or y value of the circle correctly updates the left."""
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.x = expected_x
        self.assertEqual(c.left, (expected_x - expected_radius, c.y))

        c.y = expected_y
        self.assertEqual(c.left, (c.x - expected_radius, expected_y))

    def test_left_invalid_value(self):
        """Ensures the left attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3], True, False):
            with self.assertRaises(TypeError):
                c.left = value

    def test_left_del(self):
        """Ensures the left attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.left

    def test_right(self):
        """Ensures changing the right attribute moves the circle and does not change the circle's radius."""
        expected_radius = 5.0

        for pos in [
            (1, 0),
            (0, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]:
            c = Circle((0, 0), expected_radius)

            c.right = pos

            self.assertEqual(pos[0], c.x + expected_radius)
            self.assertEqual(pos[1], c.y)

            self.assertEqual(expected_radius, c.r)

    def test_right_update(self):
        """Ensures changing the x or y value of the circle correctly updates the right."""
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.x = expected_x
        self.assertEqual(c.right, (expected_x + expected_radius, c.y))

        c.y = expected_y
        self.assertEqual(c.right, (c.x + expected_radius, expected_y))

    def test_right_invalid_value(self):
        """Ensures the right attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3], True, False):
            with self.assertRaises(TypeError):
                c.right = value

    def test_right_del(self):
        """Ensures the right attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.right

    def test_bottom(self):
        """Ensures changing the bottom attribute moves the circle and does not change the circle's radius."""
        expected_radius = 5.0

        for pos in [
            (1, 0),
            (0, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]:
            c = Circle((0, 0), expected_radius)

            c.bottom = pos

            self.assertEqual(pos[0], c.x)
            self.assertEqual(pos[1], c.y + expected_radius)

            self.assertEqual(expected_radius, c.r)

    def test_bottom_update(self):
        """Ensures changing the x or y value of the circle correctly updates the bottom."""
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.x = expected_x
        self.assertEqual(c.bottom, (expected_x, c.y + expected_radius))

        c.y = expected_y
        self.assertEqual(c.bottom, (c.x, expected_y + expected_radius))

    def test_bottom_invalid_value(self):
        """Ensures the bottom attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3], True, False):
            with self.assertRaises(TypeError):
                c.bottom = value

    def test_bottom_del(self):
        """Ensures the bottom attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.bottom

    def test_area(self):
        """Ensures the area is calculated correctly."""
        c = Circle(0, 0, 1)

        self.assertEqual(c.area, math.pi)

    def test_area_update(self):
        """Ensures the area is updated correctly."""
        c = Circle(0, 0, 1)

        c.r = 2
        self.assertEqual(c.area, math.pi * 4)

        c.r_sqr = 100
        self.assertEqual(c.area, math.pi * (10**2))

    def test_area_invalid_value(self):
        """Ensures the area handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.area = value

        for value in (-10.3234, -1, 0, 0.0):
            with self.assertRaises(ValueError):
                c.area = value

    def test_area_del(self):
        """Ensures the area attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.area

    def test_circumference(self):
        """Ensures the circumference is calculated correctly."""
        c = Circle(0, 0, 1)

        self.assertEqual(c.circumference, math.tau)

    def test_circumference_update(self):
        """Ensures the circumference is updated correctly."""
        c = Circle(0, 0, 1)

        c.r = 2
        self.assertEqual(c.circumference, math.tau * 2)

        c.r_sqr = 100
        self.assertEqual(c.circumference, math.tau * 10)

    def test_circumference_invalid_value(self):
        """Ensures the circumference handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.circumference = value

        for value in (-10.3234, -1, 0, 0.0):
            with self.assertRaises(ValueError):
                c.circumference = value

    def test_circumference_del(self):
        """Ensures the circumference attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.circumference

    def test_diameter(self):
        """Ensures the diameter is calculated correctly."""
        c = Circle(0, 0, 1)

        self.assertEqual(c.diameter, 2.0)
        self.assertEqual(c.d, 2.0)

    def test_diameter_update(self):
        """Ensures the diameter is updated correctly."""
        c = Circle(0, 0, 1)

        c.r = 2
        self.assertEqual(c.diameter, 4.0)
        self.assertEqual(c.d, 4.0)

        c.r_sqr = 100
        self.assertEqual(c.diameter, 20.0)
        self.assertEqual(c.d, 20.0)

    def test_diameter_invalid_value(self):
        """Ensures the diameter handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.diameter = value

        for value in (-10.3234, -1, 0, 0.0):
            with self.assertRaises(ValueError):
                c.diameter = value

    def test_diameter_del(self):
        """Ensures the diameter attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.diameter

    def test__str__(self):
        """Checks whether the __str__ method works correctly."""
        c_str = "<Circle((10.3, 3.2), 4.3)>"
        circle = Circle((10.3, 3.2), 4.3)
        self.assertEqual(str(circle), c_str)
        self.assertEqual(circle.__str__(), c_str)

    def test__repr__(self):
        """Checks whether the __repr__ method works correctly."""
        c_repr = "<Circle((10.3, 3.2), 4.3)>"
        circle = Circle((10.3, 3.2), 4.3)
        self.assertEqual(repr(circle), c_repr)
        self.assertEqual(circle.__repr__(), c_repr)

    def test_copy(self):
        c = Circle(10, 10, 4)
        # check 1 arg passed
        with self.assertRaises(TypeError):
            c.copy(10)

        # check copied circle has the same attribute values
        c_2 = c.copy()
        self.assertEqual(c.x, c_2.x)
        self.assertEqual(c.y, c_2.y)
        self.assertEqual(c.r, c_2.r)
        self.assertEqual(c.r_sqr, c_2.r_sqr)

        # check c2 is not c
        self.assertIsNot(c_2, c)

    def test_bool(self):
        c = Circle(10, 10, 4)

        self.assertTrue(c, "Expected c to be True as radius is > 0")

    def test_collidecircle_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector2(1, 1), 1)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collidecircle(value)

    def test_collidecircle_argnum(self):
        c = Circle(10, 10, 4)
        # no params
        with self.assertRaises(TypeError):
            c.collidecircle()

        with self.assertRaises(TypeError):
            c.collidecircle(Circle(10, 10, 4), Circle(10, 10, 4))

    def test_collidecircle(self):
        c = Circle(0, 0, 5)
        c_same = c.copy()
        c2 = Circle(10, 0, 5)
        c3 = Circle(100, 100, 5)
        c4 = Circle(10, 0, 4.999999999999)
        c5 = Circle(0, 0, 2)

        c6 = Circle(10, 0, 7)

        # touching
        self.assertTrue(
            c.collidecircle(c2), "Expected True, circles should collide here"
        )

        # partly colliding
        self.assertTrue(
            c.collidecircle(c6), "Expected True, circles should collide here"
        )

        # self colliding
        self.assertTrue(
            c.collidecircle(c), "Expected True, circles should collide with self"
        )

        # completely colliding
        self.assertTrue(
            c.collidecircle(c_same), "Expected True, circles should collide with self"
        )

        # not touching
        self.assertFalse(
            c.collidecircle(c3), "Expected False, circles should not collide here"
        )

        # barely not touching
        self.assertFalse(
            c.collidecircle(c4), "Expected False, circles should not collide here"
        )

        # small circle inside big circle
        self.assertTrue(
            c.collidecircle(c5), "Expected True, circles should collide here"
        )

        # big circle outside small circle
        self.assertTrue(
            c5.collidecircle(c), "Expected False, circles should collide here"
        )

    def test_collideline_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1, Vector2(1, 1))

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collideline(value)

    def test_collideline_argnum(self):
        c = Circle(10, 10, 4)
        args = [tuple(range(x)) for x in range(5, 13)]

        # no params
        with self.assertRaises(TypeError):
            c.collidepoint()

        # too many params
        for arg in args:
            with self.assertRaises(TypeError):
                c.collidepoint(*arg)

    def test_collideline(self):
        c = Circle(0, 0, 5)

        l = Line(0, 0, 10, 10)
        l2 = Line(50, 0, 0, 10)

        # colliding single
        self.assertTrue(c.collideline(l), "Expected True, line should collide here")

        # not colliding single
        self.assertFalse(
            c.collideline(l2), "Expected False, line should not collide here"
        )

        # colliding 2 args
        self.assertTrue(
            c.collideline((0, 0), (10, 10)), "Expected True, line should collide here"
        )

        # not colliding 2 args
        self.assertFalse(
            c.collideline((50, 0), (0, 10)),
            "Expected False, line should not collide here",
        )

        # colliding 4 args
        self.assertTrue(
            c.collideline(0, 0, 10, 10), "Expected True, line should collide here"
        )

        # not colliding 4 args
        self.assertFalse(
            c.collideline(50, 0, 0, 10), "Expected False, line should not collide here"
        )

    def test_collidepoint_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collidepoint(value)

    def test_collidepoint_argnum(self):
        c = Circle(10, 10, 4)
        args = [tuple(range(x)) for x in range(3, 13)]

        # no params
        with self.assertRaises(TypeError):
            c.collidepoint()

        # too many params
        for arg in args:
            with self.assertRaises(TypeError):
                c.collidepoint(*arg)

    def test_collidepoint(self):
        c = Circle(0, 0, 5)

        p1 = (3, 3)
        p2 = (10, 10)

        # colliding single
        self.assertTrue(c.collidepoint(p1), "Expected True, point should collide here")

        # not colliding single
        self.assertFalse(
            c.collidepoint(p2), "Expected False, point should not collide here"
        )

        # colliding 2 args
        self.assertTrue(
            c.collidepoint(3, 3), "Expected True, point should collide here"
        )

        # not colliding 2 args
        self.assertFalse(
            c.collidepoint(10, 10), "Expected False, point should not collide here"
        )

    def test_colliderect_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.colliderect(value)

    def test_colliderect_argnum(self):
        c = Circle(10, 10, 4)
        args = [(1), (1, 1), (1, 1, 1), (1, 1, 1, 1, 1)]
        # no params
        with self.assertRaises(TypeError):
            c.colliderect()

        # invalid num
        for arg in args:
            with self.assertRaises(TypeError):
                c.colliderect(*arg)

    def test_colliderect(self):
        msgt = "Expected True, rect should collide here"
        msgf = "Expected False, rect should not collide here"
        # ====================================================
        c = Circle(0, 0, 5)

        r1 = Rect(2, 2, 4, 4)
        r2 = Rect(10, 15, 43, 24)
        r3 = Rect(0, 5, 4, 4)

        # colliding single
        self.assertTrue(c.colliderect(r1), msgt)

        # not colliding single
        self.assertFalse(c.colliderect(r2), msgf)

        # barely colliding single
        self.assertTrue(c.colliderect(r3), msgt)

        # colliding 4 args
        self.assertTrue(c.colliderect(2, 2, 4, 4), msgt)

        # not colliding 4 args
        self.assertFalse(c.colliderect(10, 15, 43, 24), msgf)

        # barely colliding single
        self.assertTrue(c.colliderect(0, 4.9999999999999, 4, 4), msgt)

    def test_collide_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collide(value)

    def test_collide_argnum(self):
        c = Circle(10, 10, 4)
        args = [tuple(range(x)) for x in range(2, 4)]

        # no params
        with self.assertRaises(TypeError):
            c.collide()

        # too many params
        for arg in args:
            with self.assertRaises(TypeError):
                c.collide(*arg)

    def test_collide(self):
        """Ensures the collide function correctly registers collisions with circles, lines, rects and points"""
        c = Circle(0, 0, 5)

        # circle
        c2 = Circle(0, 10, 15)
        c3 = Circle(100, 100, 1)
        self.assertTrue(c.collide(c2), E_T + "circles should collide here")
        self.assertFalse(c.collide(c3), E_F + "circles should not collide here")

        # line
        l = Line(0, 0, 10, 10)
        l2 = Line(50, 0, 50, 10)
        self.assertTrue(c.collide(l), E_T + "line should collide here")
        self.assertFalse(c.collide(l2), E_F + "line should not collide here")

        # rect
        r = Rect(0, 0, 10, 10)
        r2 = Rect(50, 0, 10, 10)
        self.assertTrue(c.collide(r), E_T + "rect should collide here")
        self.assertFalse(c.collide(r2), E_F + "rect should not collide here")

        # point
        p = (0, 0)
        p2 = (50, 0)
        self.assertTrue(c.collide(p), E_T + "point should collide here")
        self.assertFalse(c.collide(p2), E_F + "point should not collide here")

        # polygon
        c4 = Circle(0, 0, 15)
        po1 = Polygon([(-5, 0), (5, 0), (0, 5)])
        po2 = Polygon([(100, 150), (200, 225), (150, 200)])

        self.assertTrue(c.collide(po1), E_T + "polygon should collide here")
        self.assertFalse(c.collide(po2), E_F + "polygon should not collide here")

    def test_as_rect_invalid_args(self):
        c = Circle(0, 0, 10)

        invalid_args = [None, [], "1", (1,), Vector2(1, 1), 1]

        with self.assertRaises(TypeError):
            for arg in invalid_args:
                c.as_rect(arg)

    def test_as_rect(self):
        c = Circle(0, 0, 10)
        c2 = Circle(-10, -10, 10)

        self.assertEqual(c.as_rect(), Rect(-10, -10, 20, 20))

    def test_update(self):
        """Ensures that updating the circle position
        and dimension correctly updates position and dimension"""
        c = Circle(0, 0, 10)

        c.update(5, 5, 3)

        self.assertEqual(c.x, 5.0)
        self.assertEqual(c.y, 5.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

    def test_update_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector2(1, 1), 1, 0.2324)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.update(value)

    def test_update_argnum(self):
        c = Circle(10, 10, 4)

        # no params
        with self.assertRaises(TypeError):
            c.update()

        # too many params
        with self.assertRaises(TypeError):
            c.update(1, 1, 1, 1)

    def test_update_twice(self):
        """Ensures that updating the circle position
        and dimension correctly updates position and dimension"""
        c = Circle(0, 0, 10)

        c.update(5, 5, 3)
        c.update(0, 0, 10)

        self.assertEqual(c.x, 0.0)
        self.assertEqual(c.y, 0.0)
        self.assertEqual(c.r, 10)
        self.assertEqual(c.r_sqr, 100)

    def test_update_inplace(self):
        """Ensures that updating the circle to its position doesn't
        move the circle to another position"""
        c = Circle(0, 0, 10)
        centerx = c.x
        centery = c.y
        c_r = c.r
        c_r_sqr = c.r_sqr

        c.update(0, 0, 10)

        self.assertEqual(c.x, centerx)
        self.assertEqual(c.y, centery)
        self.assertEqual(c.r, c_r)
        self.assertEqual(c.r_sqr, c_r_sqr)

        c.update(c)

    def test_selfupdate(self):
        """Ensures that updating the circle to its position doesn't
        move the circle to another position"""
        c = Circle(0, 0, 10)
        centerx = c.x
        centery = c.y
        c_r = c.r
        c_r_sqr = c.r_sqr

        c.update(c)

        self.assertEqual(c.x, centerx)
        self.assertEqual(c.y, centery)
        self.assertEqual(c.r, c_r)
        self.assertEqual(c.r_sqr, c_r_sqr)

    def test_move_invalid_args(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Circle(3, 3, 1))

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.move(value)

    def test_move_argnum(self):
        c = Circle(10, 10, 4)

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                c.move(*arg)

    def test_move_return_type(self):
        c = Circle(10, 10, 4)

        self.assertIsInstance(c.move(1, 1), Circle)

    def test_move(self):
        """Ensures that moving the circle position correctly updates position"""
        c = Circle(0, 0, 3)

        new_c = c.move(5, 5)

        self.assertEqual(new_c.x, 5.0)
        self.assertEqual(new_c.y, 5.0)
        self.assertEqual(new_c.r, 3.0)
        self.assertEqual(new_c.r_sqr, 9.0)

        new_c = new_c.move(-5, -10)

        self.assertEqual(new_c.x, 0.0)
        self.assertEqual(new_c.y, -5.0)

    def test_move_inplace(self):
        """Ensures that moving the circle position by 0, 0 doesn't move the circle"""
        c = Circle(1, 1, 3)

        c.move(0, 0)

        self.assertEqual(c.x, 1.0)
        self.assertEqual(c.y, 1.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

    def test_move_equality(self):
        """Ensures that moving the circle by 0, 0 will
        return a circle that's equal to the original"""
        c = Circle(1, 1, 3)

        new_c = c.move(0, 0)

        self.assertEqual(new_c, c)

    def test_move_ip_invalid_args(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Circle(3, 3, 1))

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.move_ip(value)

    def test_move_ip_argnum(self):
        c = Circle(10, 10, 4)

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                c.move_ip(*arg)

    def test_move_ip(self):
        """Ensures that moving the circle position correctly updates position"""
        c = Circle(0, 0, 3)

        c.move_ip(5, 5)

        self.assertEqual(c.x, 5.0)
        self.assertEqual(c.y, 5.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

        c.move_ip(-5, -10)
        self.assertEqual(c.x, 0.0)
        self.assertEqual(c.y, -5.0)

    def test_move_ip_inplace(self):
        """Ensures that moving the circle position by 0, 0 doesn't move the circle"""
        c = Circle(1, 1, 3)

        c.move_ip(0, 0)

        self.assertEqual(c.x, 1.0)
        self.assertEqual(c.y, 1.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

    def test_move_ip_equality(self):
        """Ensures that moving the circle by 0, 0 will
        return a circle that's equal to the original"""
        c = Circle(1, 1, 3)

        c.move_ip(2, 2)

        self.assertEqual(c, Circle(3, 3, 3))

    def test_move_ip_return_type(self):
        c = Circle(10, 10, 4)

        self.assertEqual(type(c.move_ip(1, 1)), type(None))

    def test_contains_argtype(self):
        """Tests if the function correctly handles incorrect types as parameters"""

        invalid_types = (None, [], "1", (1,), 1, (1, 2, 3))

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.contains(value)

    def test_contains_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        c = Circle(10, 10, 4)

        invalid_args = [(Circle(10, 10, 4), Circle(10, 10, 4))]

        with self.assertRaises(TypeError):
            c.contains()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                c.contains(*arg)

    def test_contains_return_type(self):
        """Tests if the function returns the correct type"""
        c = Circle(10, 10, 4)

        self.assertIsInstance(c.contains(Circle(10, 10, 4)), bool)

    def test_contains_circle(self):
        """Ensures that the contains method correctly determines if a circle is
        contained within the circle"""
        c = Circle(10, 10, 4)
        c2 = Circle(10, 10, 2)
        c3 = Circle(100, 100, 5)
        c4 = Circle(16, 10, 7)

        # self
        self.assertTrue(c.contains(c))

        # contained circle
        self.assertTrue(c.contains(c2))

        # not contained circle
        self.assertFalse(c.contains(c3))

        # intersecting circle
        self.assertFalse(c.contains(c4))

    def test_contains_line(self):
        """Ensures that the contains method correctly determines if a line is
        contained within the circle"""
        c = Circle(0, 0, 15)

        l1 = Line(-5, 0, 5, 0)
        l2 = Line(100, 150, 200, 225)
        l3 = Line(0, 0, 50, 50)

        # contained line
        self.assertTrue(c.contains(l1))

        # not contained line
        self.assertFalse(c.contains(l2))

        # intersecting line
        self.assertFalse(c.contains(l3))

    def test_contains_polygon(self):
        """Ensures that the contains method correctly determines if a polygon is
        contained within the circle"""
        c = Circle(0, 0, 15)

        p1 = Polygon([(-5, 0), (5, 0), (0, 5)])
        p2 = Polygon([(100, 150), (200, 225), (150, 200)])
        p3 = Polygon([(0, 0), (50, 50), (50, -50), (0, -50)])

        # contained polygon
        self.assertTrue(c.contains(p1))

        # not contained polygon
        self.assertFalse(c.contains(p2))

        # intersecting polygon
        self.assertFalse(c.contains(p3))

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

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collidepolygon(value)
            with self.assertRaises(TypeError):
                c.collidepolygon(value, True)
            with self.assertRaises(TypeError):
                c.collidepolygon(value, False)

    def test_collidepolygon_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        c = Circle(10, 10, 4)

        poly = Polygon((-5, 0), (5, 0), (0, 5))
        invalid_args = [
            (poly, poly),
            (poly, poly, poly),
            (poly, poly, poly, poly),
        ]

        with self.assertRaises(TypeError):
            c.collidepolygon()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                c.collidepolygon(*arg)
            with self.assertRaises(TypeError):
                c.collidepolygon(*arg, True)
            with self.assertRaises(TypeError):
                c.collidepolygon(*arg, False)

    def test_collidepolygon_return_type(self):
        """Tests if the function returns the correct type"""
        c = Circle(10, 10, 4)

        vertices = [(-5, 0), (5, 0), (0, 5)]

        items = [
            Polygon(vertices),
            vertices,
            tuple(vertices),
            [list(v) for v in vertices],
        ]

        for item in items:
            self.assertIsInstance(c.collidepolygon(item), bool)
            self.assertIsInstance(c.collidepolygon(item, True), bool)
            self.assertIsInstance(c.collidepolygon(item, False), bool)

        self.assertIsInstance(c.collidepolygon(*vertices), bool)
        self.assertIsInstance(c.collidepolygon(*vertices, True), bool)
        self.assertIsInstance(c.collidepolygon(*vertices, False), bool)

    def test_collidepolygon(self):
        """Ensures that the collidepolygon method correctly determines if a polygon
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
        self.assertTrue(c.collidepolygon(p1))
        self.assertTrue(c.collidepolygon(p1, False))

        # non colliding
        self.assertFalse(c.collidepolygon(p2))
        self.assertFalse(c.collidepolygon(p2, False))

        # intersecting polygon
        self.assertTrue(c.collidepolygon(p3))
        self.assertTrue(c.collidepolygon(p3, False))

        # polygon contains circle
        self.assertTrue(c.collidepolygon(p4))
        self.assertTrue(c.collidepolygon(p4, False))

        # circle contains polygon, barely touching
        self.assertTrue(c.collidepolygon(p5))
        self.assertTrue(c.collidepolygon(p5, False))

        # circle contains polygon, barely not touching
        self.assertTrue(c.collidepolygon(p6))
        self.assertTrue(c.collidepolygon(p6, False))

        # --- Edge only ---

        # circle contains polygon
        self.assertFalse(c.collidepolygon(p1, True))

        # non colliding
        self.assertFalse(c.collidepolygon(p2, True))

        # intersecting polygon
        self.assertTrue(c.collidepolygon(p3, True))

        # polygon contains circle
        self.assertFalse(c.collidepolygon(p4, True))

        # circle contains polygon, barely touching
        self.assertTrue(c.collidepolygon(p5, True))

        # circle contains polygon, barely not touching
        self.assertFalse(c.collidepolygon(p6, True))

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
                c.collidepolygon(poly, value)

    def test_collidepolygon_no_invalidation(self):
        """Ensures that the function doesn't modify the polygon or the circle"""
        c = Circle(10, 10, 4)
        poly = Polygon((-5, 0), (5, 0), (0, 5))

        c_copy = c.copy()
        poly_copy = poly.copy()

        c.collidepolygon(poly)

        self.assertEqual(c.x, c_copy.x)
        self.assertEqual(c.y, c_copy.y)
        self.assertEqual(c.r, c_copy.r)

        self.assertEqual(poly.vertices, poly_copy.vertices)
        self.assertEqual(poly.verts_num, poly_copy.verts_num)
        self.assertEqual(poly.centerx, poly_copy.centerx)
        self.assertEqual(poly.centery, poly_copy.centery)

    def test_meth_rotate_ip_invalid_argnum(self):
        """Ensures that the rotate_ip method correctly deals with invalid numbers of arguments."""
        c = Circle(0, 0, 1)

        with self.assertRaises(TypeError):
            c.rotate_ip()

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
                c.rotate_ip(*args)

    def test_meth_rotate_ip_invalid_argtype(self):
        """Ensures that the rotate_ip method correctly deals with invalid argument types."""
        c = Circle(0, 0, 1)

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
                c.rotate_ip(*value)

    def test_meth_rotate_ip_return(self):
        """Ensures that the rotate_ip method always returns None."""
        c = Circle(0, 0, 1)

        for angle in float_range(-360, 360, 1):
            self.assertIsNone(c.rotate_ip(angle))
            self.assertIsInstance(c.rotate_ip(angle), type(None))

    def test_meth_rotate_invalid_argnum(self):
        """Ensures that the rotate method correctly deals with invalid numbers of arguments."""
        c = Circle(0, 0, 1)

        with self.assertRaises(TypeError):
            c.rotate()

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
                c.rotate(*args)

    def test_meth_rotate_invalid_argtype(self):
        """Ensures that the rotate method correctly deals with invalid argument types."""
        c = Circle(0, 0, 1)

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
                c.rotate(*value)

    def test_meth_rotate_return(self):
        """Ensures that the rotate method always returns a Line."""
        c = Circle(0, 0, 1)

        class CircleSubclass(Circle):
            pass

        cs = CircleSubclass(0, 0, 1)

        for angle in float_range(-360, 360, 1):
            self.assertIsInstance(c.rotate(angle), Circle)
            self.assertIsInstance(cs.rotate(angle), CircleSubclass)

    def test_meth_rotate(self):
        """Ensures the Circle.rotate() method rotates the Circle correctly."""

        def rotate_circle(circle: Circle, angle, center):
            def rotate_point(x, y, rang, cx, cy):
                x -= cx
                y -= cy
                x_new = x * math.cos(rang) - y * math.sin(rang)
                y_new = x * math.sin(rang) + y * math.cos(rang)
                return x_new + cx, y_new + cy

            angle = math.radians(angle)
            cx, cy = center if center is not None else circle.center
            x, y = rotate_point(circle.x, circle.y, angle, cx, cy)
            return Circle(x, y, circle.r)

        def assert_approx_equal(circle1, circle2, eps=1e-12):
            self.assertAlmostEqual(circle1.x, circle2.x, delta=eps)
            self.assertAlmostEqual(circle1.y, circle2.y, delta=eps)
            self.assertAlmostEqual(circle1.r, circle2.r, delta=eps)

        c = Circle(0, 0, 1)
        angles = float_range(-360, 360, 0.5)
        centers = [(a, b) for a in range(-10, 10) for b in range(-10, 10)]
        for angle in angles:
            assert_approx_equal(c.rotate(angle), rotate_circle(c, angle, None))
            for center in centers:
                assert_approx_equal(
                    c.rotate(angle, center), rotate_circle(c, angle, center)
                )

    def test_meth_rotate_ip(self):
        """Ensures the Circle.rotate_ip() method rotates the Circle correctly."""

        def rotate_circle(circle: Circle, angle, center):
            def rotate_point(x, y, rang, cx, cy):
                x -= cx
                y -= cy
                x_new = x * math.cos(rang) - y * math.sin(rang)
                y_new = x * math.sin(rang) + y * math.cos(rang)
                return x_new + cx, y_new + cy

            angle = math.radians(angle)
            cx, cy = center if center is not None else circle.center
            x, y = rotate_point(circle.x, circle.y, angle, cx, cy)
            circle.x = x
            circle.y = y
            return circle

        def assert_approx_equal(circle1, circle2, eps=1e-12):
            self.assertAlmostEqual(circle1.x, circle2.x, delta=eps)
            self.assertAlmostEqual(circle1.y, circle2.y, delta=eps)
            self.assertAlmostEqual(circle1.r, circle2.r, delta=eps)

        c = Circle(0, 0, 1)
        angles = float_range(-360, 360, 0.5)
        centers = [(a, b) for a in range(-10, 10) for b in range(-10, 10)]
        for angle in angles:
            c.rotate_ip(angle)
            assert_approx_equal(c, rotate_circle(c, angle, None))
            for center in centers:
                c.rotate_ip(angle, center)
                assert_approx_equal(c, rotate_circle(c, angle, center))

    def test_collidelist_argtype(self):
        """Tests if the function correctly handles incorrect types as parameters"""

        invalid_types = (None, "1", (1,), 1, (1, 2, 3), True, False)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collidelist(value)

    def test_collidelist_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        c = Circle(10, 10, 4)

        circles = [(Circle(10, 10, 4), Circle(10, 10, 4))]

        with self.assertRaises(TypeError):
            c.collidelist()

        with self.assertRaises(TypeError):
            c.collidelist(circles, 1)

    def test_collidelist_return_type(self):
        """Tests if the function returns the correct type"""
        c = Circle(10, 10, 4)

        objects = [
            Circle(10, 10, 4),
            Rect(10, 10, 4, 4),
            Line(10, 10, 4, 4),
            Polygon([(10, 10), (34, 10), (4, 43)]),
        ]

        for object in objects:
            self.assertIsInstance(c.collidelist([object]), int)

    def test_collidelist(self):
        """Ensures that the collidelist method works correctly"""
        c = Circle(10, 10, 4)

        circles = [Circle(1000, 1000, 2), Circle(5, 10, 5), Circle(16, 10, 7)]
        rects = [Rect(1000, 1000, 4, 4), Rect(1000, 200, 5, 5), Rect(5, 10, 7, 3)]
        lines = [Line(10, 10, 4, 4), Line(100, 100, 553, 553), Line(136, 110, 324, 337)]
        polygons = [
            Polygon([(100, 100), (34, 10), (4, 43)]),
            Polygon([(20, 10), (34, 10), (4, 43)]),
            Polygon([(10, 10), (34, 10), (4, 43)]),
        ]
        expected = [1, 2, 0, 2]

        for objects, expected in zip([circles, rects, lines, polygons], expected):
            self.assertEqual(c.collidelist(objects), expected)

    def test_collidelistall_argtype(self):
        """Tests if the function correctly handles incorrect types as parameters"""

        invalid_types = (None, "1", (1,), 1, (1, 2, 3), True, False)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collidelistall(value)

    def test_collidelistall_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        c = Circle(10, 10, 4)

        circles = [(Circle(10, 10, 4), Circle(10, 10, 4))]

        with self.assertRaises(TypeError):
            c.collidelistall()

        with self.assertRaises(TypeError):
            c.collidelistall(circles, 1)

    def test_collidelistall_return_type(self):
        """Tests if the function returns the correct type"""
        c = Circle(10, 10, 4)

        objects = [
            Circle(10, 10, 4),
            Rect(10, 10, 4, 4),
            Line(10, 10, 4, 4),
            Polygon([(10, 10), (34, 10), (4, 43)]),
        ]

        for object in objects:
            self.assertIsInstance(c.collidelistall([object]), list)

    def test_collidelistall(self):
        """Ensures that the collidelistall method works correctly"""
        c = Circle(10, 10, 4)

        circles = [Circle(1000, 1000, 2), Circle(5, 10, 5), Circle(16, 10, 7)]
        rects = [Rect(1000, 1000, 4, 4), Rect(1000, 200, 5, 5), Rect(5, 10, 7, 3)]
        lines = [Line(10, 10, 4, 4), Line(0, 0, 553, 553), Line(5, 5, 10, 11)]
        polygons = [
            Polygon([(100, 100), (34, 10), (4, 43)]),
            Polygon([(20, 10), (34, 10), (4, 43)]),
            Polygon([(10, 10), (34, 10), (4, 43)]),
        ]
        expected = [[1, 2], [2], [0, 1, 2], [2]]

        for objects, expected in zip([circles, rects, lines, polygons], expected):
            self.assertEqual(c.collidelistall(objects), expected)

    def test_intersect_argtype(self):
        """Tests if the function correctly handles incorrect types as parameters"""

        invalid_types = (None, "1", (1,), 1, (1, 2, 3), True, False)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.intersect(value)

    def test_intersect_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        c = Circle(10, 10, 4)

        circles = [(Circle(10, 10, 4) for _ in range(100))]
        for size in range(len(circles)):
            with self.assertRaises(TypeError):
                c.intersect(*circles[:size])

    def test_intersect_return_type(self):
        """Tests if the function returns the correct type"""
        c = Circle(10, 10, 4)

        objects = [
            Circle(10, 10, 4),
            Circle(10, 10, 400),
            Circle(10, 10, 1),
            Circle(15, 10, 10),
        ]

        for object in objects:
            self.assertIsInstance(c.intersect(object), list)

    def test_intersect(self):

        # Circle
        c = Circle(10, 10, 4)
        c2 = Circle(10, 10, 2)
        c3 = Circle(100, 100, 1)
        c3_1 = Circle(10, 10, 400)
        c4 = Circle(16, 10, 7)
        c5 = Circle(18, 10, 4)

        for circle in [c, c2, c3, c3_1]:
            self.assertEqual(c.intersect(circle), [])

        # intersecting circle
        self.assertEqual(
            [(10.25, 6.007820144332172), (10.25, 13.992179855667828)], c.intersect(c4)
        )

        # touching
        self.assertEqual([(14.0, 10.0)], c.intersect(c5))


if __name__ == "__main__":
    unittest.main()
