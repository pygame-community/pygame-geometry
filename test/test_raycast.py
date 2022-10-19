import unittest

from geometry import raycast, Circle, Line
from pygame import Rect


class RaycastTest(unittest.TestCase):
    def test_raycast_endpoint(self):
        with self.assertRaises(TypeError):
            for x in ["1", 1, (0, 0, 0), [0, 0, 0], []]:
                raycast(x, (0, 0), [])

            for x in ["1", 1, (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), x, [])

            for x in ["1", 1, (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), (0, 0), x)

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
            result = raycast(x[0], x[1], collisions)
            self.assertEqual(result, x[2])

    def test_raycast_angle(self):
        with self.assertRaises(TypeError):
            for x in ["1", 1, (0, 0, 0), [0, 0, 0], []]:
                raycast(x, 4, 5, [])

            for x in [(0, 0), (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), x, 5, [])

            for x in [(0, 0), (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), 4, x, [])

            for x in ["1", 1, (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), 4, 5, x)

        colliders = [
            Line(785.0, 360.0, 59.0, 582.0),
            Line(253.0, 59.0, 743.0, 617.0),
            Line(49.0, 493.0, 278.0, 254.0),
            Line(40.0, 35.0, 727.0, 422.0),
            Line(86.0, 510.0, 770.0, 137.0),
            Line(108.0, 252.0, 664.0, 763.0),
            Line(429.0, 33.0, 274.0, 669.0),
            Line(619.0, 372.0, 242.0, 215.0),
            Line(499.0, 212.0, 33.0, 558.0),
            Line(434.0, 167.0, 650.0, 659.0),
            Line(437.0, 713.0, 113.0, 437.0),
            Line(476.0, 599.0, 486.0, 611.0),
            Line(242.0, 507.0, 775.0, 529.0),
            Line(734.0, 559.0, 116.0, 220.0),
            Line(515.0, 694.0, 755.0, 393.0),
            Circle((285.0, 343.0), 14.0),
            Circle((546.0, 478.0), 36.0),
            Circle((51.0, 462.0), 38.0),
            Circle((139.0, 782.0), 15.0),
            Circle((593.0, 218.0), 38.0),
            Circle((621.0, 317.0), 40.0),
            Circle((325.0, 104.0), 38.0),
            Circle((378.0, 567.0), 17.0),
            Circle((271.0, 549.0), 33.0),
            Circle((442.0, 336.0), 35.0),
            Circle((444.0, 61.0), 8.0),
            Circle((515.0, 244.0), 27.0),
            Circle((376.0, 763.0), 14.0),
            Circle((585.0, 269.0), 6.0),
            Circle((423.0, 216.0), 37.0),
            Rect(776, 4, 11, 23),
            Rect(129, 153, 44, 20),
            Rect(491, 142, 41, 24),
            Rect(484, 613, 18, 21),
            Rect(588, 50, 42, 43),
            Rect(300, 174, 20, 42),
            Rect(183, 83, 17, 7),
            Rect(566, 38, 14, 36),
            Rect(302, 176, 27, 35),
            Rect(336, 658, 33, 16),
            Rect(664, 293, 30, 24),
            Rect(162, 667, 41, 23),
            Rect(189, 71, 43, 13),
            Rect(574, 243, 5, 6),
            Rect(423, 470, 33, 47),
        ]
        origin_pos = (485, 420)
        self.assertEqual(
            raycast(origin_pos, 0.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 0.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 1.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 1.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 2.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 2.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 51.99999999999999, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 59.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 59.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 60.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 68.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 68.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 69.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 69.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 70.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 70.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 71.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 71.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 72.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 72.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 96.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 97.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 97.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 97.99999999999999, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 98.50000000000001, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 99.00000000000001, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 99.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 100.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 100.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 101.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 101.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 102.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 102.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 114.99999999999999, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 115.50000000000001, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 116.00000000000001, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 116.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 117.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 117.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 118.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 118.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 119.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 119.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 120.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 120.49999999999999, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 121.00000000000001, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 121.50000000000001, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 122.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 122.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 123.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 123.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 124.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 124.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 143.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 143.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 144.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 144.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 145.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 145.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 146.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 146.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 147.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 147.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 148.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 148.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 149.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 149.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 150.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 150.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 151.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 151.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 152.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 152.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 153.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 153.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 154.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 154.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 155.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 155.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 156.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 156.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 157.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 157.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 158.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 158.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 159.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 159.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 160.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 160.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 161.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 161.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 162.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 162.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 163.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 163.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 164.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 164.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 165.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 165.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 166.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 166.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 167.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 167.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 168.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 168.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 169.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 169.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 170.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 170.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 171.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 171.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 172.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 172.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 173.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 173.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 174.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 174.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 175.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 175.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 176.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 176.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 177.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 177.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 178.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 178.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 179.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 179.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 180.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 180.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 181.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 181.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 182.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 182.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 183.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 183.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 184.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 184.49999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 184.99999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 185.49999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 186.00000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 186.50000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 187.00000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 187.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 188.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 188.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 189.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 189.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 190.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 190.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 191.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 191.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 192.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 192.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 193.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 193.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 194.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 194.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 195.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 195.49999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 195.99999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 196.49999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 197.00000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 197.50000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 198.00000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 198.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 199.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 199.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 200.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 200.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 201.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 201.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 202.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 202.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 203.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 203.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 204.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 204.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 205.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 205.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 206.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 206.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 206.99999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 207.49999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 207.99999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 208.50000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 209.00000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 209.50000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 210.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 210.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 211.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 211.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 212.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 212.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 213.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 213.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 214.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 214.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 215.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 225.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 225.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 226.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 226.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 227.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 227.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 228.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 228.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 229.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 229.49999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 229.99999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 230.49999999999997, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 231.00000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 231.50000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 232.00000000000003, 150, colliders),
            (480.60176991150445, 420.0),
        )
        self.assertEqual(
            raycast(origin_pos, 232.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 233.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 233.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 234.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 234.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 235.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 296.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 297.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 297.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 298.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 298.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 301.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 302.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 302.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 303.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 303.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 304.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 304.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 305.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 305.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 306.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 306.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 307.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 307.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 308.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 308.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 309.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 309.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 310.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 310.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 311.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 311.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 312.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 312.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 313.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 313.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 314.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 314.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 315.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 315.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 316.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 316.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 317.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 317.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 318.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 318.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 319.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 319.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 320.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 320.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 321.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 325.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 325.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 326.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 326.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 327.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 327.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 328.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 328.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 329.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 329.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 330.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 330.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 331.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 331.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 332.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 332.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 333.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 333.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 334.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 334.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 335.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 335.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 336.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 357.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 358.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 358.5, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 359.0, 150, colliders), (480.60176991150445, 420.0)
        )
        self.assertEqual(
            raycast(origin_pos, 359.5, 150, colliders), (480.60176991150445, 420.0)
        )
