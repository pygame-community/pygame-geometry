import unittest
from math import sqrt

from pygame import Vector2, Vector3

from geometry import Circle, Line


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

    def testConstruction_invalid_arguments_number(self):
        """Checks whether passing the wrong number of arguments to the constructor
        raises the appropriate errors
        """
        arguments = (
            (1,),  # one non vec3 non circle arg
            (1, 1),  # two args
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

        for value in (None, [], "1", (1,), [1, 2, 3], -1):
            with self.assertRaises(TypeError):
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

        self.assertEqual(c.r_sqr, expected_r_sqr)

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
        c2 = Circle(10, 10, 0)

        self.assertTrue(c, "Expected c to be True as radius is > 0")
        self.assertFalse(c2, "Expected c to be False as radius is != 0")

    def test_collidecircle_argtype(self):
        """tests if the function correctly handler incorrect types as parameters"""
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
            c.collidecircle(c3), "Expected True, circles should collide here"
        )

        # barely not touching
        self.assertFalse(
            c.collidecircle(c4), "Expected False, circles should not collide here"
        )

        # small circle inside big circle
        self.assertTrue(
            c.collidecircle(c5), "Expected False, circles should collide here"
        )

        # big circle outside small circle
        self.assertTrue(
            c5.collidecircle(c), "Expected False, circles should collide here"
        )

    def test_collideline_argtype(self):
        """tests if the function correctly handler incorrect types as parameters"""
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
        self.assertTrue(
            c.collideline(l), "Expected True, line should collide here"
        )

        # not colliding single
        self.assertFalse(
            c.collideline(l2), "Expected True, line should not collide here"
        )

        # colliding 2 args
        self.assertTrue(
            c.collideline((0, 0), (10, 10)), "Expected True, line should collide here"
        )

        # not colliding 2 args
        self.assertFalse(
            c.collideline((50, 0), (0, 10)),
            "Expected True, line should not collide here"
        )

        # colliding 4 args
        self.assertTrue(
            c.collideline(0, 0, 10, 10), "Expected True, line should collide here"
        )

        # not colliding 4 args
        self.assertFalse(
            c.collideline(50, 0, 0, 10), "Expected True, line should not collide here"
        )

    def test_collidepoint_argtype(self):
        """tests if the function correctly handler incorrect types as parameters"""
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
        self.assertTrue(
            c.collidepoint(p1), "Expected True, point should collide here"
        )

        # not colliding single
        self.assertFalse(
            c.collidepoint(p2), "Expected True, point should not collide here"
        )

        # colliding 2 args
        self.assertTrue(
            c.collidepoint(3, 3), "Expected True, point should collide here"
        )

        # not colliding 2 args
        self.assertFalse(
            c.collidepoint(10, 10), "Expected True, point should not collide here"
        )


if __name__ == "__main__":
    unittest.main()
