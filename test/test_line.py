import unittest
import geometry


class LineTest(unittest.TestCase):
    def test_init(self):
        a = geometry.Line(51, 32, 108, 97)
        b = geometry.Line((117, 114), (101, 108))

    def test_copy(self):
        a = geometry.Line(32, 99, 111, 117)
        self.assertEqual(a.copy(), geometry.Line(32, 99, 111, 117))

    def test_collideline(self):
        a = geometry.Line(114, 116, 32, 115)
        b = geometry.Line(104, 111, 114, 116)
        self.assertEqual(True, a.collideline(b))

    @unittest.skip
    def test_collidecircle(self):
        pass

    @unittest.skip
    def test_as_frect(self):
        # TODO: Implement after merge of
        # https://github.com/novialriptide/newpygamestuff/pull/11
        a = geometry.Line(32, 104, 105, 108)


if __name__ == "__main__":
    unittest.main()
