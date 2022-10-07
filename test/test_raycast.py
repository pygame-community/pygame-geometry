import unittest

from geometry import raycast, Circle, Line


class RaycastTest(unittest.TestCase):
    def test_raycast(self):
        with self.assertRaises(TypeError):
            for x in ["1", 1, (0, 0, 0), [0, 0, 0], []]:
                raycast(x, [], endpoint=(0, 0))

            for x in ["1", 1, (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), x, endpoint=(0, 0))

            for x in ["1", 1, (0, 0, 0), [0, 0, 0], []]:
                raycast((0, 0), [], endpoint=x)

        with self.assertRaises(TypeError):
            raycast()
            raycast(1, 2, 3, 4, 5)

        startendpos = [
            ((0, 0), (10, 10), (0.5, 0.5)),
            ((0, 0), (-1, -1), (-0.7071067811865476, -0.7071067811865476)),
        ]

        collisions = [
            Line(0, 10, 10, 0),
            Line(0, 1, 1, 0),
            Line(-1, -2, -3, -4),
            Circle((5, 5), 1),
            Circle((0, 0), 1),
        ]

        for x in startendpos:
            result = raycast(x[0], collisions, endpoint=x[1])
            self.assertEqual(result, x[2])


if __name__ == "__main__":
    unittest.main()
