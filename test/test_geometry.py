import unittest
import pygame
import geometry
from geometry import Line, Circle, Polygon, is_line, is_circle, is_polygon
from pygame import Rect


def _get_vertices_from_rect(rect: pygame.Rect):
    return [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom),
    ]


class TestGeometry(unittest.TestCase):
    def test_rect_to_polygon(self):
        rects_base = [
            (1, 2, 3, 4),  # normalised rect
            (-1, -2, 3, 4),  # normalised rect, negative position
            (1, 2, -3, -4),  # not normalised rect, positive position
            (-1, -2, -3, -4),  # not normalised rect, negative position
            (1, 2, 0, 0),  # zero size rect
            (1, 2, 0, 4),  # zero width rect
            (1, 2, 3, 0),  # zero height rect
            (1, 2, -3, 0),  # zero width rect, negative width
            (1, 2, 0, -4),  # zero height rect, negative height
            (-1, -2, 0, 0),  # zero size rect, negative position
            (-1, -2, 0, 4),  # zero width rect, negative position
            (-1, -2, 3, 0),  # zero height rect, negative position
            (-1, -2, -3, 0),  # zero width rect, negative width negative position
            (-1, -2, 0, -4),  # zero height rect, negative height negative position
        ]

        for rect_base in rects_base:
            rect = pygame.Rect(*rect_base)
            polygon = geometry.rect_to_polygon(rect)
            self.assertIsInstance(polygon, geometry.Polygon)
            self.assertEqual(_get_vertices_from_rect(rect), polygon.vertices)

    def test_rect_to_polygon_invalid_argnum(self):
        # Test with invalid number of arguments
        rect = pygame.Rect(1, 2, 3, 4)
        invalid_args = [
            (),
            (rect, rect),
            (rect, rect, rect),
            (rect, rect, rect, rect),
            (rect, rect, rect, rect, rect),
        ]
        for i, args in enumerate(invalid_args):
            with self.assertRaises(TypeError):
                geometry.rect_to_polygon(*args)

    def test_rect_to_polygon_invalid_arg_type(self):
        # Test with an invalid rect object
        invalid_rects = [
            "not a rect",
            1,
            1.0,
            True,
            False,
            None,
            [],
            {},
            set(),
            (1,),
            (1, 2),
            (1, 2, 3),
            (1, 2, 3, 4, 5),
            [1],
            [1, 2],
            [1, 2, 3],
            [1, 2, 3, 4, 5],
        ]
        for invalid_rect in invalid_rects:
            with self.assertRaises(TypeError):
                geometry.rect_to_polygon(invalid_rect)

    def test_is_line(self):
        """Test is_line function"""

        class TestLine(Line):
            pass

        items = [
            (Line(0, 0, 1, 1), True),
            (Circle(0, 0, 1), False),
            (Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), False),
            (Rect(0, 0, 1, 1), False),
            (TestLine(0, 0, 1, 1), False),
            (1, False),
            (1.0, False),
            (True, False),
            (False, False),
            (None, False),
            ("", False),
            ("string", False),
            ([], False),
            ([1], False),
            ((1,), False),
            ({}, False),
        ]
        for obj, expected in items:
            self.assertEqual(expected, is_line(obj))

        # Check that the function doesn't modify the line
        # =================================================
        l = Line(0, 0, 1, 1)
        start, end = l.a, l.b

        self.assertTrue(is_line(l))
        self.assertEqual(start, l.a)
        self.assertEqual(end, l.b)
        # =================================================

    def test_is_circle(self):
        """Test is_circle function"""

        class TestCircle(Circle):
            pass

        items = [
            (Line(0, 0, 1, 1), False),
            (Circle(0, 0, 1), True),
            (Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), False),
            (Rect(0, 0, 1, 1), False),
            (TestCircle(0, 0, 1), False),
            (1, False),
            (1.0, False),
            (True, False),
            (False, False),
            (None, False),
            ("", False),
            ("string", False),
            ([], False),
            ([1], False),
            ((1,), False),
            ({}, False),
        ]
        for obj, expected in items:
            self.assertEqual(expected, is_circle(obj))

        # Check that the function doesn't modify the circle
        # =================================================
        c = Circle(0, 0, 1)
        center = c.center
        radius = c.r

        self.assertTrue(is_circle(c))
        self.assertEqual(center, c.center)
        self.assertEqual(radius, c.r)
        # =================================================

    def test_area(self):
        poly = Polygon((-3, -2), (-1, 4), (6, 1), (3, 10), (-4, 9))

        self.assertEqual(60, poly.area)

        poly = Polygon((0, 0), (0, 4), (4, 4), (4, 0))

        self.assertEqual(16, poly.area)

    def test_is_polygon(self):
        """Test is_polygon function"""

        class TestPolygon(Polygon):
            pass

        items = [
            (Line(0, 0, 1, 1), False),
            (Circle(0, 0, 1), False),
            (Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), True),
            (Rect(0, 0, 1, 1), False),
            (TestPolygon([(0, 0), (1, 0), (1, 1), (0, 1)]), False),
            (1, False),
            (1.0, False),
            (True, False),
            (False, False),
            (None, False),
            ("", False),
            ("string", False),
            ([], False),
            ([1], False),
            ((1,), False),
            ({}, False),
        ]
        for obj, expected in items:
            self.assertEqual(expected, is_polygon(obj))

        # Check that the function doesn't modify the polygon
        # =================================================
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        verts = p.vertices
        verts_num = p.verts_num
        cx, cy = p.center

        self.assertTrue(is_polygon(p))
        self.assertEqual(verts, p.vertices)
        self.assertEqual(verts_num, p.verts_num)
        self.assertEqual(cx, p.centerx)
        self.assertEqual(cy, p.centery)
        # =================================================


if __name__ == "__main__":
    unittest.main()
