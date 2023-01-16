import unittest
import pygame
import geometry


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


if __name__ == "__main__":
    unittest.main()
