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
            Line(378.0, 729.0, 140.0, 350.0),
            Line(727.0, 53.0, 64.0, 92.0),
            Line(786.0, 678.0, 703.0, 279.0),
            Line(781.0, 79.0, 452.0, 739.0),
            Line(97.0, 310.0, 431.0, 566.0),
            Line(185.0, 726.0, 474.0, 506.0),
            Line(715.0, 661.0, 232.0, 347.0),
            Line(20.0, 759.0, 84.0, 538.0),
            Line(606.0, 614.0, 413.0, 295.0),
            Line(722.0, 20.0, 97.0, 764.0),
            Line(11.0, 772.0, 564.0, 741.0),
            Line(511.0, 246.0, 674.0, 353.0),
            Line(703.0, 669.0, 539.0, 237.0),
            Line(149.0, 211.0, 573.0, 398.0),
            Line(173.0, 130.0, 376.0, 546.0),
            Circle((499.0, 621.0), 41.0),
            Circle((616.0, 383.0), 27.0),
            Circle((227.0, 224.0), 15.0),
            Circle((178.0, 516.0), 35.0),
            Circle((140.0, 545.0), 11.0),
            Circle((38.0, 733.0), 19.0),
            Circle((326.0, 335.0), 24.0),
            Circle((412.0, 584.0), 5.0),
            Circle((710.0, 158.0), 49.0),
            Circle((520.0, 40.0), 30.0),
            Circle((271.0, 50.0), 28.0),
            Circle((455.0, 588.0), 25.0),
            Circle((154.0, 232.0), 38.0),
            Circle((263.0, 118.0), 39.0),
            Circle((272.0, 732.0), 37.0),
            Rect(541, 110, 16, 47),
            Rect(649, 110, 23, 14),
            Rect(645, 495, 6, 7),
            Rect(577, 240, 33, 30),
            Rect(60, 723, 40, 32),
            Rect(74, 388, 23, 47),
            Rect(512, 577, 47, 29),
            Rect(262, 521, 28, 23),
            Rect(762, 491, 15, 5),
            Rect(769, 434, 8, 34),
            Rect(661, 633, 40, 41),
            Rect(536, 550, 48, 46),
            Rect(623, 134, 42, 24),
            Rect(386, 426, 45, 41),
            Rect(696, 103, 39, 24),
        ]
        origin_pos = (457, 536)
        self.assertEqual(raycast(origin_pos, 0.5, 150, colliders), (434.8448936979859, 535.8066553164122))
        self.assertEqual(raycast(origin_pos, 1.5, 150, colliders), (435.3361201031828, 535.4327113401376))
        self.assertEqual(raycast(origin_pos, 3.0, 150, colliders), (436.03428855976006, 534.9012336223279))
        self.assertEqual(raycast(origin_pos, 4.0, 150, colliders), (436.4761932057342, 534.5648356219324))
        self.assertEqual(raycast(origin_pos, 5.0, 150, colliders), (436.90086796269435, 534.241553800025))
        self.assertEqual(raycast(origin_pos, 5.5, 150, colliders), (437.107133771836, 534.0845348449691))
        self.assertEqual(raycast(origin_pos, 6.0, 150, colliders), (437.3095454476466, 533.9304498322414))
        self.assertEqual(raycast(origin_pos, 8.0, 150, colliders), (438.08330147902666, 533.3414314000489))
        self.assertEqual(raycast(origin_pos, 8.5, 150, colliders), (438.2683805955462, 533.2005407231136))
        self.assertEqual(raycast(origin_pos, 9.5, 150, colliders), (438.6292927375729, 532.9257979160344))
        self.assertEqual(raycast(origin_pos, 11.0, 150, colliders), (439.1490585048952, 532.5301284737822))
        self.assertEqual(raycast(origin_pos, 12.0, 150, colliders), (439.4822506135418, 532.2764874222173))
        self.assertEqual(raycast(origin_pos, 14.500000000000002, 150, colliders), (440.2734208461178, 531.6742125046854))
        self.assertEqual(raycast(origin_pos, 15.0, 150, colliders), (440.42507908507923, 531.5587633262372))
        self.assertEqual(raycast(origin_pos, 16.0, 150, colliders), (440.72235778300967, 531.3324612032452))
        self.assertEqual(raycast(origin_pos, 17.0, 150, colliders), (441.01199480166565, 531.1119762755486))
        self.assertEqual(raycast(origin_pos, 17.5, 150, colliders), (441.15409292797995, 531.0038046915032))
        self.assertEqual(raycast(origin_pos, 19.0, 150, colliders), (441.5701558511727, 530.6870785908028))
        self.assertEqual(raycast(origin_pos, 21.0, 150, colliders), (442.10289155372703, 530.2815358414534))
        self.assertEqual(raycast(origin_pos, 25.0, 150, colliders), (443.1033952071358, 529.519906762734))
        self.assertEqual(raycast(origin_pos, 25.999999999999996, 150, colliders), (443.3417770904572, 529.3384395851191))
        self.assertEqual(raycast(origin_pos, 27.500000000000004, 150, colliders), (443.69164130390214, 529.0721069658877))
        self.assertEqual(raycast(origin_pos, 29.000000000000004, 150, colliders), (444.03298069645956, 528.8122638296848))
        self.assertEqual(raycast(origin_pos, 29.5, 150, colliders), (444.14499900753526, 528.7269903748867))
        self.assertEqual(raycast(origin_pos, 36.0, 150, colliders), (445.5341048558335, 527.6695395561129))
        self.assertEqual(raycast(origin_pos, 39.5, 150, colliders), (446.2412862419693, 527.13120078466))
        self.assertEqual(raycast(origin_pos, 42.0, 150, colliders), (446.7338028984325, 526.7562746101898))
        self.assertEqual(raycast(origin_pos, 44.5, 150, colliders), (447.21824443959036, 526.3874955823187))
        self.assertEqual(raycast(origin_pos, 45.5, 150, colliders), (447.4102121535269, 526.2413609903947))
        self.assertEqual(raycast(origin_pos, 51.99999999999999, 150, colliders), (448.64269566469187, 525.3031382483315))
        self.assertEqual(raycast(origin_pos, 52.5, 150, colliders), (448.73695191831615, 525.2313860829428))
        self.assertEqual(raycast(origin_pos, 53.0, 150, colliders), (448.8312018566675, 525.1596387250282))
        self.assertEqual(raycast(origin_pos, 58.00000000000001, 150, colliders), (449.77652162645336, 524.4400181390321))
        self.assertEqual(raycast(origin_pos, 63.50000000000001, 150, colliders), (450.83475897766755, 523.6344395325714))
        self.assertEqual(raycast(origin_pos, 66.0, 150, colliders), (451.327495398013, 523.2593460637963))
        self.assertEqual(raycast(origin_pos, 75.0, 150, colliders), (453.20349478460315, 521.8312496449388))
        self.assertEqual(raycast(origin_pos, 79.0, 150, colliders), (454.1115133558892, 521.1400244349633))
        self.assertEqual(raycast(origin_pos, 82.5, 150, colliders), (454.9587383076164, 520.4950781049287))
        self.assertEqual(raycast(origin_pos, 84.5, 150, colliders), (455.469599869257, 520.1061869507386))
        self.assertEqual(raycast(origin_pos, 86.5, 150, colliders), (456.0030551874463, 519.7000963970997))
        self.assertEqual(raycast(origin_pos, 88.0, 150, colliders), (456.4197185429283, 519.3829132199162))
        self.assertEqual(raycast(origin_pos, 88.5, 150, colliders), (456.5620294546062, 519.274579653933))
        self.assertEqual(raycast(origin_pos, 90.5, 150, colliders), (457.14986569896024, 518.8270918554629))
        self.assertEqual(raycast(origin_pos, 93.00000000000001, 150, colliders), (457.9311640291592, 518.2323318809168))
        self.assertEqual(raycast(origin_pos, 93.50000000000001, 150, colliders), (458.09431333177156, 518.1081351799663))
        self.assertEqual(raycast(origin_pos, 94.5, 150, colliders), (458.42811904517015, 517.854027024438))
        self.assertEqual(raycast(origin_pos, 98.50000000000001, 150, colliders), (459.8767421273082, 516.7512689688311))
        self.assertEqual(raycast(origin_pos, 99.00000000000001, 150, colliders), (460.07227475687137, 516.6024206003055))
        self.assertEqual(raycast(origin_pos, 100.5, 150, colliders), (460.681015134949, 516.1390196204541))
        self.assertEqual(raycast(origin_pos, 102.0, 150, colliders), (461.32593469181893, 515.6480773972313))
        self.assertEqual(raycast(origin_pos, 103.0, 150, colliders), (461.7780738428553, 515.303888424124))
        self.assertEqual(raycast(origin_pos, 103.49999999999999, 150, colliders), (462.0113256286716, 515.1263265110458))
        self.assertEqual(raycast(origin_pos, 107.0, 150, colliders), (463.7974084834036, 513.766678663153))
        self.assertEqual(raycast(origin_pos, 110.00000000000001, 150, colliders), (465.588536345172, 512.4031903254746))
        self.assertEqual(raycast(origin_pos, 111.0, 150, colliders), (466.2517746476525, 511.8983030363891))
        self.assertEqual(raycast(origin_pos, 112.5, 150, colliders), (467.320117926697, 511.08503133607843))
        self.assertEqual(raycast(origin_pos, 120.49999999999999, 150, colliders), (475.19887350168125, 505.10444364291493))
        self.assertEqual(raycast(origin_pos, 122.0, 150, colliders), (475.9859516901743, 505.6161259435088))
        self.assertEqual(raycast(origin_pos, 123.5, 150, colliders), (476.7722905383138, 506.12732759633656))
        self.assertEqual(raycast(origin_pos, 130.5, 150, colliders), (480.46392579147766, 508.52727266775156))
        self.assertEqual(raycast(origin_pos, 133.5, 150, colliders), (482.0760714801013, 509.57533425414454))
        self.assertEqual(raycast(origin_pos, 138.5, 150, colliders), (484.83809406866027, 511.3709348603713))
        self.assertEqual(raycast(origin_pos, 140.5, 150, colliders), (485.97826348537683, 512.1121630111974))
        self.assertEqual(raycast(origin_pos, 148.0, 150, colliders), (490.51185662613375, 515.0594678687495))
        self.assertEqual(raycast(origin_pos, 148.5, 150, colliders), (490.8321025673525, 515.2676608822953))
        self.assertEqual(raycast(origin_pos, 154.5, 150, colliders), (494.909238029761, 517.9182209965734))
        self.assertEqual(raycast(origin_pos, 159.5, 150, colliders), (498.7257817129663, 520.3993694779947))
        self.assertEqual(raycast(origin_pos, 160.5, 150, colliders), (499.5470704204033, 520.9332921573637))
        self.assertEqual(raycast(origin_pos, 163.5, 150, colliders), (502.15052293675916, 522.625805801537))
        self.assertEqual(raycast(origin_pos, 164.0, 150, colliders), (502.60682926243607, 522.9224521499067))
        self.assertEqual(raycast(origin_pos, 166.0, 150, colliders), (504.5041256672967, 524.1558912205614))
        self.assertEqual(raycast(origin_pos, 170.5, 150, colliders), (509.26853069799427, 527.2532477001454))
        self.assertEqual(raycast(origin_pos, 174.0, 150, colliders), (513.5760981602272, 530.0536124685535))
        self.assertEqual(raycast(origin_pos, 175.0, 150, colliders), (514.9272788514056, 530.932019791597))
        self.assertEqual(raycast(origin_pos, 176.5, 150, colliders), (517.0713371304217, 532.3258796251603))
        self.assertEqual(raycast(origin_pos, 177.0, 150, colliders), (517.8199585377303, 532.8125610369509))
        self.assertEqual(raycast(origin_pos, 180.5, 150, colliders), (523.6171865617941, 536.581359379717))
        self.assertEqual(raycast(origin_pos, 183.0, 150, colliders), (528.485716205644, 539.7464076367955))
        self.assertEqual(raycast(origin_pos, 185.49999999999997, 150, colliders), (534.1498584373055, 543.428686437503))
        self.assertEqual(raycast(origin_pos, 186.50000000000003, 150, colliders), (536.6890436161909, 545.0794196593871))
        self.assertEqual(raycast(origin_pos, 189.0, 150, colliders), (543.8925162137662, 549.762422548908))
        self.assertEqual(raycast(origin_pos, 190.0, 150, colliders), (536.3979454746479, 550.0))
        self.assertEqual(raycast(origin_pos, 192.5, 150, colliders), (536.0, 553.5138783487922))
        self.assertEqual(raycast(origin_pos, 197.00000000000003, 150, colliders), (536.0, 560.1527238352342))
        self.assertEqual(raycast(origin_pos, 198.00000000000003, 150, colliders), (536.0, 561.6686560023996))
        self.assertEqual(raycast(origin_pos, 199.0, 150, colliders), (536.0, 563.2018814498836))
        self.assertEqual(raycast(origin_pos, 200.5, 150, colliders), (536.0, 565.5368896792995))
        self.assertEqual(raycast(origin_pos, 204.0, 150, colliders), (535.721085837688, 571.0488855535742))
        self.assertEqual(raycast(origin_pos, 204.5, 150, colliders), (535.3854052977043, 571.7222872447269))
        self.assertEqual(raycast(origin_pos, 205.0, 150, colliders), (535.0499288376357, 572.3952795354421))
        self.assertEqual(raycast(origin_pos, 209.50000000000003, 150, colliders), (529.4672546659584, 577.0))
        self.assertEqual(raycast(origin_pos, 213.0, 150, colliders), (520.1344635163979, 577.0))
        self.assertEqual(raycast(origin_pos, 217.99999999999997, 150, colliders), (512.0, 578.9707094578694))
        self.assertEqual(raycast(origin_pos, 218.49999999999997, 150, colliders), (512.0, 579.7489754167304))
        self.assertEqual(raycast(origin_pos, 223.5, 150, colliders), (503.6444248875445, 580.2639064530734))
        self.assertEqual(raycast(origin_pos, 224.5, 150, colliders), (501.8776138942657, 580.1011083490575))
        self.assertEqual(raycast(origin_pos, 228.0, 150, colliders), (496.6770762737872, 580.0658574615004))
        self.assertEqual(raycast(origin_pos, 229.0, 150, colliders), (495.3872506505695, 580.1594803884893))
        self.assertEqual(raycast(origin_pos, 231.50000000000003, 150, colliders), (492.42169496483757, 580.531173690551))
        self.assertEqual(raycast(origin_pos, 233.0, 150, colliders), (490.78318729818596, 580.8318037618901))
        self.assertEqual(raycast(origin_pos, 235.5, 150, colliders), (488.22994060398366, 581.4398455437004))
        self.assertEqual(raycast(origin_pos, 236.0, 150, colliders), (487.7414564440176, 581.576083439135))
        self.assertEqual(raycast(origin_pos, 242.00000000000003, 150, colliders), (482.28833690958584, 583.5604444904525))
        self.assertEqual(raycast(origin_pos, 250.0, 150, colliders), (468.19865633699186, 566.7680554141175))
        self.assertEqual(raycast(origin_pos, 251.0, 150, colliders), (467.43780015106097, 566.3135727377175))
        self.assertEqual(raycast(origin_pos, 264.5, 150, colliders), (459.6416591191297, 563.4346789025301))
        self.assertEqual(raycast(origin_pos, 265.0, 150, colliders), (459.3962778040275, 563.3895806319799))
        self.assertEqual(raycast(origin_pos, 272.0, 150, colliders), (456.0563595169977, 563.0223278792669))
        self.assertEqual(raycast(origin_pos, 272.5, 150, colliders), (455.8205664192301, 563.0134702139006))
        self.assertEqual(raycast(origin_pos, 275.0, 150, colliders), (454.637576238284, 563.0026271577003))
        self.assertEqual(raycast(origin_pos, 275.5, 150, colliders), (454.39950116406794, 563.0072130175915))
        self.assertEqual(raycast(origin_pos, 276.5, 150, colliders), (453.92108478640023, 563.0232920111184))
        self.assertEqual(raycast(origin_pos, 278.0, 150, colliders), (453.1962404013351, 563.0651558795684))
        self.assertEqual(raycast(origin_pos, 282.5, 150, colliders), (450.94069457394755, 563.3317605115805))
        self.assertEqual(raycast(origin_pos, 287.0, 150, colliders), (448.4808283427988, 563.8649549222723))
        self.assertEqual(raycast(origin_pos, 291.0, 150, colliders), (445.9908910437321, 564.6797093539961))
        self.assertEqual(raycast(origin_pos, 292.0, 150, colliders), (445.30000024933344, 564.9585155678487))
        self.assertEqual(raycast(origin_pos, 292.5, 150, colliders), (444.9410200434404, 565.1129529595115))
        self.assertEqual(raycast(origin_pos, 293.5, 150, colliders), (444.1916647487825, 565.457154370016))
        self.assertEqual(raycast(origin_pos, 294.0, 150, colliders), (443.7991542995309, 565.6495848898888))
        self.assertEqual(raycast(origin_pos, 296.0, 150, colliders), (442.0752902256903, 566.6001897847233))
        self.assertEqual(raycast(origin_pos, 302.5, 150, colliders), (376.4050587479764, 662.5087168719328))
        self.assertEqual(raycast(origin_pos, 307.0, 150, colliders), (366.72774652719283, 655.7953265070939))
        self.assertEqual(raycast(origin_pos, 307.5, 150, colliders), (365.68578564869193, 655.0030010436852))
        self.assertEqual(raycast(origin_pos, 309.0, 150, colliders), (416.65740049426057, 585.81896141687))
        self.assertEqual(raycast(origin_pos, 310.0, 150, colliders), (416.9898896343985, 583.6821927682964))
        self.assertEqual(raycast(origin_pos, 311.5, 150, colliders), (430.6771623791308, 565.7525555959804))
        self.assertEqual(raycast(origin_pos, 312.5, 150, colliders), (430.1247710427803, 565.3291658291969))
        self.assertEqual(raycast(origin_pos, 316.0, 150, colliders), (428.1757207174219, 563.8352829450898))
        self.assertEqual(raycast(origin_pos, 318.0, 150, colliders), (427.0467880161415, 562.9699932099767))
        self.assertEqual(raycast(origin_pos, 321.5, 150, colliders), (425.0337740110429, 561.427084271937))
        self.assertEqual(raycast(origin_pos, 329.5, 150, colliders), (420.16658157095145, 557.696541563364))
        self.assertEqual(raycast(origin_pos, 330.0, 150, colliders), (419.846033899076, 557.4508523298307))
        self.assertEqual(raycast(origin_pos, 332.5, 150, colliders), (418.20682188949735, 556.1944503105129))
        self.assertEqual(raycast(origin_pos, 337.5, 150, colliders), (414.71240543944253, 553.5160951871176))
        self.assertEqual(raycast(origin_pos, 340.0, 150, colliders), (414.06046286413704, 551.6287133906224))
        self.assertEqual(raycast(origin_pos, 341.5, 150, colliders), (417.01685380086155, 549.3781735771988))
        self.assertEqual(raycast(origin_pos, 352.5, 150, colliders), (429.9050057267952, 539.5671236681836))
        self.assertEqual(raycast(origin_pos, 353.0, 150, colliders), (430.2813429671906, 539.2806385716888))
        self.assertEqual(raycast(origin_pos, 355.0, 150, colliders), (431.68104487898336, 538.2151215454106))
        self.assertEqual(raycast(origin_pos, 355.5, 150, colliders), (432.0069968657103, 537.9669920053417))