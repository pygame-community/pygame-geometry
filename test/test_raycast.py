import unittest

from geometry import raycast, Circle, Line, multiraycast
from pygame import Rect
import math


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


class RaycastTest(unittest.TestCase):
    def test_raycast_errors(self):
        with self.assertRaises(TypeError):
            for x in ["1", 1, (0, 0, 0), [0, 0, 0], []]:
                raycast(x, (0, 0), [])

            for x in ["1", 1, (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), x, [])

            for x in ["1", 1, (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), (0, 0), x)

        with self.assertRaises(TypeError):
            raycast()
        with self.assertRaises(TypeError):
            raycast(1, 2, 3, 4, 5)

        with self.assertRaises(TypeError):
            for x in ["1", 1, (0, 0, 0), [0, 0, 0], []]:
                raycast(x, 4, 5, [])

            for x in [1, "1", (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), x, 5, [])

            for x in ["1", (0, 0, 0), [0, 0, 0], []]:
                raycast((0, 0), 4, x, [])

            for x in ["1", 1, (0, 0, 0), [0, 0, 0]]:
                raycast((0, 0), 4, 5, x)

    def test_raycast_valid(self):
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
            result = raycast(x[0], x[1], dist(x[0], x[1]), collisions)
            self.assertAlmostEqual(result[0], x[2][0])
            self.assertAlmostEqual(result[1], x[2][1])

        colliders = [
            Line(172.0, 565.0, 78.0, 170.0),
            Line(82.0, 392.0, 767.0, 531.0),
            Line(378.0, 140.0, 120.0, 180.0),
            Line(207.0, 330.0, 227.0, 78.0),
            Line(469.0, 494.0, 510.0, 206.0),
            Line(4.0, 181.0, 676.0, 728.0),
            Line(705.0, 623.0, 226.0, 678.0),
            Line(36.0, 247.0, 517.0, 111.0),
            Line(36.0, 443.0, 719.0, 797.0),
            Line(152.0, 92.0, 730.0, 159.0),
            Circle((757.0, 68.0), 6.0),
            Circle((187.0, 586.0), 29.0),
            Circle((153.0, 434.0), 26.0),
            Circle((646.0, 480.0), 30.0),
            Circle((459.0, 316.0), 40.0),
            Circle((653.0, 622.0), 23.0),
            Circle((755.0, 619.0), 32.0),
            Circle((567.0, 727.0), 22.0),
            Circle((156.0, 576.0), 18.0),
            Circle((122.0, 397.0), 41.0),
            Rect(135, 528, 35, 25),
            Rect(695, 54, 27, 29),
            Rect(118, 177, 30, 28),
            Rect(224, 591, 39, 9),
            Rect(411, 541, 10, 10),
            Rect(648, 438, 15, 38),
            Rect(78, 380, 43, 48),
            Rect(371, 693, 44, 15),
            Rect(97, 440, 6, 5),
            Rect(155, 242, 36, 25),
        ]
        origin_pos = (450, 254)
        inputs_outputs = [
            (
                raycast(origin_pos, 39.0, 150, colliders),
                (336.4504184960395, 162.04936192211773),
            ),
            (
                raycast(origin_pos, [449.223, 253.223], 150, colliders),
                (353.2884927066423, 157.28849270664585),
            ),
            (
                raycast(origin_pos, 40.0, 150, colliders),
                (339.41765292243065, 161.2103933524936),
            ),
            (
                raycast(origin_pos, [449.234, 253.234], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 43.0, 150, colliders),
                (347.9179784721458, 158.8069749018465),
            ),
            (
                raycast(origin_pos, [449.269, 253.269], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 48.0, 150, colliders),
                (360.9659971715958, 155.11772221343654),
            ),
            (
                raycast(origin_pos, [449.331, 253.331], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 58.00000000000001, 150, colliders),
                (384.1205836528338, 148.5708952665584),
            ),
            (
                raycast(origin_pos, [449.47, 253.47], 150, colliders),
                (353.288492706641, 157.2884927066462),
            ),
            (
                raycast(origin_pos, 65.0, 150, colliders),
                (398.89027848051734, 144.3948484961531),
            ),
            (
                raycast(origin_pos, [449.577, 253.577], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 67.0, 150, colliders),
                (402.98404812139125, 143.2373585353239),
            ),
            (
                raycast(origin_pos, [449.609, 253.609], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 74.0, 150, colliders),
                (417.0952492845052, 139.24749708379892),
            ),
            (
                raycast(origin_pos, [449.724, 253.724], 150, colliders),
                (353.28849270663727, 157.28849270664725),
            ),
            (
                raycast(origin_pos, 76.0, 150, colliders),
                (421.10622930878833, 138.11341541373136),
            ),
            (
                raycast(origin_pos, [449.758, 253.758], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 78.0, 150, colliders),
                (425.12596342284127, 136.97685857483077),
            ),
            (
                raycast(origin_pos, [449.792, 253.792], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 79.0, 150, colliders),
                (427.1421937346774, 136.40678098146338),
            ),
            (
                raycast(origin_pos, [449.809, 253.809], 150, colliders),
                (353.28849270665626, 157.28849270664188),
            ),
            (
                raycast(origin_pos, 81.0, 150, colliders),
                (431.1936311541855, 135.26126021420117),
            ),
            (
                raycast(origin_pos, [449.844, 253.844], 150, colliders),
                (353.28849270665876, 157.2884927066412),
            ),
            (
                raycast(origin_pos, 86.0, 150, colliders),
                (441.49333876869935, 132.34907677225962),
            ),
            (
                raycast(origin_pos, [449.93, 253.93], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 96.0, 150, colliders),
                (463.23499719152073, 128.07741316925933),
            ),
            (
                raycast(origin_pos, [450.105, 254.105], 150, colliders),
                (475.6131400333446, 279.61314003335156),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.1045284632676, 254.10452846326766)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 112.0, 150, colliders),
                (499.1920339869739, 132.24544338603334),
            ),
            (
                raycast(origin_pos, [450.375, 254.375], 150, colliders),
                (475.613140033361, 279.61314003335906),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.37460659341593, 254.3746065934159)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 117.0, 150, colliders),
                (511.3206944943643, 133.65136078048863),
            ),
            (
                raycast(origin_pos, [450.454, 254.454], 150, colliders),
                (475.61314003336037, 279.6131400333588),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.4539904997396, 254.45399049973955)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 119.0, 150, colliders),
                (516.3849427657851, 134.23839301956332),
            ),
            (
                raycast(origin_pos, [450.485, 254.485], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.4848096202463, 254.48480962024632)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 123.0, 150, colliders),
                (526.97677209494, 135.46616562346188),
            ),
            (
                raycast(origin_pos, [450.545, 254.545], 150, colliders),
                (475.61314003335985, 279.61314003335855),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.54463903501505, 254.54463903501502)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 128.0, 150, colliders),
                (541.3106446259476, 137.12770448086246),
            ),
            (
                raycast(origin_pos, [450.616, 254.616], 150, colliders),
                (475.61314003335957, 279.6131400333584),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.6156614753257, 254.61566147532565)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 154.0, 150, colliders),
                (507.1336965045504, 226.13403430949933),
            ),
            (
                raycast(origin_pos, [450.899, 254.899], 150, colliders),
                (475.61314003335593, 279.61314003335673),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.89879404629914, 254.89879404629917)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 157.0, 150, colliders),
                (506.586090947032, 229.98062944523858),
            ),
            (
                raycast(origin_pos, [450.921, 254.921], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9205048534524, 254.92050485345243)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 164.0, 150, colliders),
                (505.4293707218406, 238.1058837099978),
            ),
            (
                raycast(origin_pos, [450.961, 254.961], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.96126169593833, 254.96126169593833)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 165.0, 150, colliders),
                (505.2751680639349, 239.18906335577404),
            ),
            (
                raycast(origin_pos, [450.966, 254.966], 150, colliders),
                (475.6131400333588, 279.61314003335804),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9659258262891, 254.96592582628907)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 167.0, 150, colliders),
                (504.97346026594437, 241.30837666848842),
            ),
            (
                raycast(origin_pos, [450.974, 254.974], 150, colliders),
                (475.6131400333588, 279.61314003335804),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.97437006478526, 254.97437006478523)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 168.0, 150, colliders),
                (504.8256801407624, 242.34644193805914),
            ),
            (
                raycast(origin_pos, [450.978, 254.978], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9781476007338, 254.9781476007338)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 169.0, 150, colliders),
                (504.6797761937679, 243.3713281998741),
            ),
            (
                raycast(origin_pos, [450.982, 254.982], 150, colliders),
                (475.61314003335605, 279.6131400333568),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.98162718344764, 254.98162718344767)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 171.0, 150, colliders),
                (504.3931108301034, 245.38497758366358),
            ),
            (
                raycast(origin_pos, [450.988, 254.988], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9876883405951, 254.98768834059513)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 173.0, 150, colliders),
                (504.1125401519366, 247.35581551810367),
            ),
            (
                raycast(origin_pos, [450.993, 254.993], 150, colliders),
                (475.61314003335605, 279.6131400333568),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9925461516413, 254.99254615164133)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 176.0, 150, colliders),
                (503.70125506993276, 250.2448424355943),
            ),
            (
                raycast(origin_pos, [450.998, 254.998], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9975640502598, 254.99756405025983)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 181.0, 150, colliders),
                (503.0348791055966, 254.92572725824834),
            ),
            (
                raycast(origin_pos, [451, 255], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9998476951564, 254.9998476951564)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 202.0, 150, colliders),
                (500.2749699287308, 274.3124063542811),
            ),
            (
                raycast(origin_pos, [450.927, 254.927], 150, colliders),
                (475.61314003335883, 279.6131400333581),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.9271838545668, 254.92718385456678)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 209.00000000000003, 150, colliders),
                (499.27803572613476, 281.3152612408094),
            ),
            (
                raycast(origin_pos, [450.875, 254.875], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.8746197071394, 254.8746197071394)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 211.0, 150, colliders),
                (498.977197124062, 283.4284689821987),
            ),
            (
                raycast(origin_pos, [450.857, 254.857], 150, colliders),
                (475.6131400333559, 279.6131400333567),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.8571673007021, 254.85716730070212)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 212.0, 150, colliders),
                (498.82347238399785, 284.5082915465517),
            ),
            (
                raycast(origin_pos, [450.848, 254.848], 150, colliders),
                (475.613140033359, 279.61314003335815),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.84804809615645, 254.84804809615642)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 215.0, 150, colliders),
                (498.3472958940303, 287.85314103705537),
            ),
            (
                raycast(origin_pos, [450.819, 254.819], 150, colliders),
                (475.61314003335906, 279.61314003335815),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.819152044289, 254.81915204428898)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 217.0, 150, colliders),
                (498.01569675961673, 290.1824227617168),
            ),
            (
                raycast(origin_pos, [450.799, 254.799], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.7986355100473, 254.7986355100473)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 218.99999999999997, 150, colliders),
                (497.6710628873723, 292.6032655716291),
            ),
            (
                raycast(origin_pos, [450.777, 254.777], 150, colliders),
                (475.6131400333591, 279.6131400333582),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.777145961457, 254.77714596145697)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 222.0, 150, colliders),
                (497.12594435293033, 296.4323908867334),
            ),
            (
                raycast(origin_pos, [450.743, 254.743], 150, colliders),
                (475.6131400333556, 279.61314003335656),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.7431448254774, 254.7431448254774)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 234.0, 150, colliders),
                (466.4992528074344, 276.7092732654359),
            ),
            (
                raycast(origin_pos, [450.588, 254.588], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.58778525229246, 254.58778525229246)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 239.0, 150, colliders),
                (463.36228749359526, 276.2385809128595),
            ),
            (
                raycast(origin_pos, [450.515, 254.515], 150, colliders),
                (475.61314003336, 279.6131400333586),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.5150380749101, 254.51503807491005)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 240.99999999999997, 150, colliders),
                (462.2689659676487, 276.133800513438),
            ),
            (
                raycast(origin_pos, [450.485, 254.485], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.4848096202463, 254.48480962024632)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 244.0, 150, colliders),
                (460.74877065653595, 276.03824576935045),
            ),
            (
                raycast(origin_pos, [450.438, 254.438], 150, colliders),
                (475.61314003335434, 279.613140033356),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.43837114678905, 254.43837114678908)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 258.0, 150, colliders),
                (454.7249426735983, 276.22910756777037),
            ),
            (
                raycast(origin_pos, [450.208, 254.208], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.20791169081775, 254.20791169081775)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 259.0, 150, colliders),
                (454.32954917500115, 276.273599595593),
            ),
            (
                raycast(origin_pos, [450.191, 254.191], 150, colliders),
                (475.61314003335036, 279.6131400333542),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.1908089953765, 254.19080899537656)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 263.0, 150, colliders),
                (452.76136368285364, 276.48950244678787),
            ),
            (
                raycast(origin_pos, [450.122, 254.122], 150, colliders),
                (475.6131400333574, 279.6131400333574),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.12186934340514, 254.12186934340514)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 267.0, 150, colliders),
                (451.1932835357393, 276.7692062526561),
            ),
            (
                raycast(origin_pos, [450.052, 254.052], 150, colliders),
                (475.61314003333183, 279.6131400333457),
            ),
            (
                raycast(
                    Line((450.0, 254.0, 450.0523359562429, 254.05233595624296)),
                    colliders,
                ),
                (450.0, 254.0),
            ),
            (
                raycast(origin_pos, 273.0, 150, colliders),
                (448.77741449446876, 277.3283211434763),
            ),
            (
                raycast(origin_pos, [449.948, 253.948], 150, colliders),
                (353.288492706686, 157.28849270663346),
            ),
            (
                raycast(origin_pos, 274.0, 150, colliders),
                (448.3608566155532, 277.4408424878709),
            ),
            (
                raycast(origin_pos, [449.93, 253.93], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 277.0, 150, colliders),
                (447.0754196641382, 277.81879541170053),
            ),
            (
                raycast(origin_pos, [449.878, 253.878], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 284.0, 150, colliders),
                (443.76285503038054, 279.0158221238487),
            ),
            (
                raycast(origin_pos, [449.758, 253.758], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
            (
                raycast(origin_pos, 287.0, 150, colliders),
                (442.13359845075234, 279.7298401054043),
            ),
            (
                raycast(origin_pos, [449.708, 253.708], 150, colliders),
                (353.2884927066524, 157.28849270664298),
            ),
            (
                raycast(origin_pos, 294.0, 150, colliders),
                (437.37921716509874, 282.34674236264726),
            ),
            (
                raycast(origin_pos, [449.593, 253.593], 150, colliders),
                (353.2884927066398, 157.28849270664654),
            ),
            (
                raycast(origin_pos, 296.0, 150, colliders),
                (435.57418465154575, 283.57730462684935),
            ),
            (
                raycast(origin_pos, [449.562, 253.562], 150, colliders),
                (353.28849270664995, 157.2884927066437),
            ),
            (raycast(origin_pos, 328.0, 150, colliders), (450.0, 254.0)),
            (
                raycast(origin_pos, [449.152, 253.152], 150, colliders),
                (353.2884927066425, 157.28849270664577),
            ),
            (raycast(origin_pos, 335.0, 150, colliders), (450.0, 254.0)),
            (
                raycast(origin_pos, [449.094, 253.094], 150, colliders),
                (353.2884927066427, 157.28849270664574),
            ),
            (raycast(origin_pos, 337.0, 150, colliders), (450.0, 254.0)),
            (
                raycast(origin_pos, [449.079, 253.079], 150, colliders),
                (353.28849270664506, 157.28849270664506),
            ),
        ]
        for (output, expected) in inputs_outputs:
            if expected is None:
                self.assertIsNone(output)
            else:
                self.assertAlmostEqual(output[0], expected[0])
                self.assertAlmostEqual(output[1], expected[1])

    def test_multiraycast_with_no_rays(self):
        """Test that multiraycast returns an empty list when no rays are given."""
        rays = []
        colliders = [Line((0, 0), (1, 0))]

        self.assertEqual([], multiraycast(rays, colliders))

    def test_multiraycast_with_no_colliders(self):
        """Test that multiraycast returns None for all rays when there are no colliders."""
        rays = [Line((0, 0), (1, 0))]
        colliders = []

        self.assertEqual(multiraycast(rays, colliders), [None])

    def test_multiraycast_with_no_colliders_and_no_rays(self):
        """Test that multiraycast returns an empty list when there are no rays."""
        rays = []
        colliders = []

        self.assertEqual(multiraycast(rays, colliders), [])

    def test_multiraycast_with_one_ray_and_one_collider(self):
        """Test that a single ray and collider returns the correct result."""
        rays = [Line((0, 0), (1, 0))]
        colliders = [Line((0, 0), (1, 0))]

        self.assertEqual(multiraycast(rays, colliders), [raycast(rays[0], colliders)])

    def test_multiraycast_with_lines(self):
        """Test that multiraycast returns the correct results for a list of lines."""
        rays = [
            Line((0, 0), (1, 0)),
            Line((0, 0), (1, 1)),
            Line((0, 0), (0, 1)),
            Line((0, 0), (-1, 1)),
            Line((0, 0), (-1, 0)),
            Line((0, 0), (-1, -1)),
            Line((0, 0), (0, -1)),
            Line((0, 0), (1, -1)),
        ]
        colliders = [
            Line((0, 1), (33, -310)),
            Line((0, 32), (331, 12)),
            Line((0, 213), (-31, 1)),
            Line((33, 0), (-22, 1)),
            Line((31, 9), (-8, 76)),
            Line((0, 99), (33, -1)),
        ]

        self.assertEqual(
            multiraycast(rays, colliders),
            [raycast(ray, colliders) for ray in rays],
        )

    def test_multiraycast_with_rects(self):
        """Test that multiraycast returns the correct results for a list of rects."""
        rays = [
            Line((0, 0), (1, 0)),
            Line((0, 0), (1, 1)),
            Line((0, 0), (0, 1)),
            Line((0, 0), (-1, 1)),
            Line((0, 0), (-1, 0)),
            Line((0, 0), (-1, -1)),
            Line((0, 0), (0, -1)),
            Line((0, 0), (1, -1)),
        ]
        colliders = [
            Rect(0, 1, 33, 310),
            Rect(0, 32, 331, 12),
            Rect(0, 213, 31, 1),
            Rect(33, 0, 22, 1),
            Rect(31, 9, 8, 76),
            Rect(0, 99, 33, 1),
        ]

        self.assertEqual(
            multiraycast(rays, colliders),
            [raycast(ray, colliders) for ray in rays],
        )

    def test_multiraycast_with_circles(self):
        """Test that multiraycast returns the correct results for a list of circles."""
        rays = [
            Line((0, 0), (1, 0)),
            Line((0, 0), (1, 1)),
            Line((0, 0), (0, 1)),
            Line((0, 0), (-1, 1)),
            Line((0, 0), (-1, 0)),
            Line((0, 0), (-1, -1)),
            Line((0, 0), (0, -1)),
            Line((0, 0), (1, -1)),
        ]
        colliders = [
            Circle(0, 1, 33),
            Circle(0, 32, 331),
            Circle(0, 213, 31),
            Circle(33, 0, 22),
            Circle(31, 9, 8),
            Circle(0, 99, 33),
        ]

        self.assertEqual(
            multiraycast(rays, colliders),
            [raycast(ray, colliders) for ray in rays],
        )

    def test_multicast_with_rays_as_tuples(self):
        """Test that multiraycast returns the correct results for a list of tuples."""
        rays = [
            ((0, 0), (1, 0)),
            ((0, 0), (1, 1)),
            ((0, 0), (0, 1)),
            ((0, 0), (-1, 1)),
            ((0, 0), (-1, 0)),
            ((0, 0), (-1, -1)),
            ((0, 0), (0, -1)),
            ((0, 0), (1, -1)),
        ]
        colliders = [
            Line((0, 1), (33, -310)),
            Line((0, 32), (331, 12)),
            Line((0, 213), (-31, 1)),
            Line((33, 0), (-22, 1)),
            Line((31, 9), (-8, 76)),
            Line((0, 99), (33, -1)),
        ]

        self.assertEqual(
            multiraycast(rays, colliders),
            [raycast(ray, colliders) for ray in rays],
        )


if __name__ == "__main__":
    unittest.main()
