import unittest

from geometry import raycast, Circle, Line
from pygame import Rect

class RaycastTest(unittest.TestCase):
    def test_raycast_endpoint(self):
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

    def test_raycast_angle(self):
        colliders = [
            Line(34.0, 740.0, 523.0, 474.0),
            Line(320.0, 312.0, 425.0, 153.0),
            Line(334.0, 215.0, 750.0, 166.0),
            Line(354.0, 582.0, 560.0, 776.0),
            Line(610.0, 274.0, 789.0, 170.0),
            Line(352.0, 205.0, 537.0, 475.0),
            Line(242.0, 715.0, 154.0, 620.0),
            Line(211.0, 388.0, 776.0, 188.0),
            Line(161.0, 130.0, 241.0, 482.0),
            Line(634.0, 283.0, 397.0, 403.0),
            Line(72.0, 761.0, 6.0, 212.0),
            Line(109.0, 377.0, 476.0, 58.0),
            Line(747.0, 253.0, 692.0, 228.0),
            Line(338.0, 651.0, 225.0, 484.0),
            Line(179.0, 557.0, 283.0, 4.0),
            Circle((316.0, 520.0), 40.0),
            Circle((588.0, 760.0), 35.0),
            Circle((365.0, 731.0), 10.0),
            Circle((473.0, 219.0), 41.0),
            Circle((490.0, 288.0), 39.0),
            Circle((386.0, 563.0), 12.0),
            Circle((164.0, 81.0), 26.0),
            Circle((416.0, 736.0), 30.0),
            Circle((560.0, 749.0), 49.0),
            Circle((685.0, 689.0), 10.0),
            Circle((475.0, 214.0), 9.0),
            Circle((719.0, 719.0), 40.0),
            Circle((518.0, 510.0), 42.0),
            Circle((241.0, 140.0), 25.0),
            Circle((204.0, 276.0), 16.0),
            Rect(451, 345, 43, 19),
            Rect(11, 775, 45, 17),
            Rect(173, 198, 31, 27),
            Rect(48, 106, 5, 45),
            Rect(654, 689, 7, 32),
            Rect(81, 173, 24, 22),
            Rect(744, 362, 5, 46),
            Rect(592, 500, 43, 19),
            Rect(243, 189, 16, 20),
            Rect(481, 449, 18, 21),
            Rect(55, 531, 31, 7),
            Rect(46, 696, 24, 7),
            Rect(80, 490, 25, 17),
            Rect(255, 725, 23, 34),
            Rect(453, 214, 44, 10),
        ]
        origin_pos = (216, 559)
        self.assertEqual(raycast(origin_pos, colliders, angle=0.0, max=150), (66.0, 559.0))
        self.assertEqual(raycast(origin_pos, colliders, angle=0.5, max=150), (66.0057115403743, 557.6910196752439))
        self.assertEqual(raycast(origin_pos, colliders, angle=1.0, max=150), (66.0228457265413, 556.3821390344075))
        self.assertEqual(raycast(origin_pos, colliders, angle=1.5, max=150), (66.0514012536664, 555.0734577538191))
        self.assertEqual(raycast(origin_pos, colliders, angle=2.0, max=150), (66.09137594713565, 553.7650754946249))
        self.assertEqual(raycast(origin_pos, colliders, angle=2.5, max=150), (66.14276676272132, 552.4570918951996))
        self.assertEqual(raycast(origin_pos, colliders, angle=3.0, max=150), (66.20556978681392, 551.1496065635585))
        self.assertEqual(raycast(origin_pos, colliders, angle=3.5, max=150), (179.04890181227898, 556.7399740174012))
        self.assertEqual(raycast(origin_pos, colliders, angle=4.0, max=150), (179.10901549606695, 556.4203310641825))
        self.assertEqual(raycast(origin_pos, colliders, angle=4.5, max=150), (179.16900696145146, 556.1013379838206))
        self.assertEqual(raycast(origin_pos, colliders, angle=5.0, max=150), (179.22888569134042, 555.7829443527764))
        self.assertEqual(raycast(origin_pos, colliders, angle=12.5, max=150), (180.11982305121154, 551.0455562757694))
        self.assertEqual(raycast(origin_pos, colliders, angle=12.999999999999998, max=150), (180.17914846412503, 550.7301048013352))
        self.assertEqual(raycast(origin_pos, colliders, angle=13.5, max=150), (180.23851636847127, 550.4144273868787))
        self.assertEqual(raycast(origin_pos, colliders, angle=14.0, max=150), (180.2979358630369, 550.0984756513518))
        self.assertEqual(raycast(origin_pos, colliders, angle=14.500000000000002, max=150), (180.35741607816107, 549.782201045932))
        self.assertEqual(raycast(origin_pos, colliders, angle=15.0, max=150), (180.41696618137226, 549.4655548240494))
        self.assertEqual(raycast(origin_pos, colliders, angle=15.5, max=150), (180.47659538307343, 549.1484880111577))
        self.assertEqual(raycast(origin_pos, colliders, angle=16.0, max=150), (180.53631294228325, 548.8309513742054))
        self.assertEqual(raycast(origin_pos, colliders, angle=16.5, max=150), (180.5961281724412, 548.5128953907692))
        self.assertEqual(raycast(origin_pos, colliders, angle=17.0, max=150), (180.65605044728392, 548.1942702178076))
        self.assertEqual(raycast(origin_pos, colliders, angle=17.5, max=150), (180.71608920680112, 547.8750256599903))
        self.assertEqual(raycast(origin_pos, colliders, angle=18.0, max=150), (180.77625396327917, 547.5551111375636))
        self.assertEqual(raycast(origin_pos, colliders, angle=18.5, max=150), (180.83655430744076, 547.2344756537044))
        self.assertEqual(raycast(origin_pos, colliders, angle=19.0, max=150), (180.89699991468888, 546.9130677613178))
        self.assertEqual(raycast(origin_pos, colliders, angle=19.5, max=150), (180.95760055146414, 546.5908355292339))
        self.assertEqual(raycast(origin_pos, colliders, angle=20.0, max=150), (181.01836608172496, 546.2677265077509))
        self.assertEqual(raycast(origin_pos, colliders, angle=20.5, max=150), (181.079306473559, 545.9436876934795))
        self.assertEqual(raycast(origin_pos, colliders, angle=21.0, max=150), (181.14043180593637, 545.6186654934345))
        self.assertEqual(raycast(origin_pos, colliders, angle=21.5, max=150), (181.2017522756142, 545.2926056883206))
        self.assertEqual(raycast(origin_pos, colliders, angle=22.0, max=150), (181.26327820420312, 544.9654533949583))
        self.assertEqual(raycast(origin_pos, colliders, angle=22.5, max=150), (181.3250200454062, 544.637153027792))
        self.assertEqual(raycast(origin_pos, colliders, angle=23.0, max=150), (181.38698839244165, 544.3076482594207))
        self.assertEqual(raycast(origin_pos, colliders, angle=23.5, max=150), (181.44919398566105, 543.9768819800908))
        self.assertEqual(raycast(origin_pos, colliders, angle=24.0, max=150), (181.51164772037464, 543.6447962560848))
        self.assertEqual(raycast(origin_pos, colliders, angle=24.499999999999996, max=150), (181.57436065489716, 543.311332286941))
        self.assertEqual(raycast(origin_pos, colliders, angle=25.0, max=150), (181.63734401882633, 542.976430361433))
        self.assertEqual(raycast(origin_pos, colliders, angle=25.5, max=150), (181.70060922156875, 542.6400298122354))
        self.assertEqual(raycast(origin_pos, colliders, angle=25.999999999999996, max=150), (181.76416786112674, 542.3020689692011))
        self.assertEqual(raycast(origin_pos, colliders, angle=26.5, max=150), (181.8280317331617, 541.9624851111689))
        self.assertEqual(raycast(origin_pos, colliders, angle=27.0, max=150), (181.89221284034946, 541.6212144162188))
        self.assertEqual(raycast(origin_pos, colliders, angle=27.500000000000004, max=150), (181.95672340204408, 541.2781919102848))
        self.assertEqual(raycast(origin_pos, colliders, angle=34.0, max=150), (182.8313616976623, 536.6274709730073))
        self.assertEqual(raycast(origin_pos, colliders, angle=34.5, max=150), (182.90191515695446, 536.2523165211942))
        self.assertEqual(raycast(origin_pos, colliders, angle=35.0, max=150), (182.97301510638695, 535.8742562131539))
        self.assertEqual(raycast(origin_pos, colliders, angle=35.5, max=150), (183.04467887729336, 535.4931978928536))
        self.assertEqual(raycast(origin_pos, colliders, angle=36.0, max=150), (183.1169242501363, 535.1090470161022))
        self.assertEqual(raycast(origin_pos, colliders, angle=36.5, max=150), (183.18976947381103, 534.7217065479088))
        self.assertEqual(raycast(origin_pos, colliders, angle=37.0, max=150), (183.2632332858114, 534.3310768552528))
        self.assertEqual(raycast(origin_pos, colliders, angle=37.5, max=150), (183.3373349333075, 533.9370555950093))
        self.assertEqual(raycast(origin_pos, colliders, angle=38.0, max=150), (183.4120941951872, 533.5395375967449))
        self.assertEqual(raycast(origin_pos, colliders, angle=38.5, max=150), (183.4875314051176, 533.1384147400958))
        self.assertEqual(raycast(origin_pos, colliders, angle=39.0, max=150), (183.56366747568498, 532.7335758264059))
        self.assertEqual(raycast(origin_pos, colliders, angle=39.5, max=150), (183.6405239236767, 532.324906444296))
        self.assertEqual(raycast(origin_pos, colliders, angle=40.0, max=150), (183.71812289657223, 531.9122888288035))
        self.assertEqual(raycast(origin_pos, colliders, angle=40.5, max=150), (183.79648720031437, 531.495601713713))
        self.assertEqual(raycast(origin_pos, colliders, angle=41.0, max=150), (183.87564032843773, 531.0747201766725))
        self.assertEqual(raycast(origin_pos, colliders, angle=41.5, max=150), (183.95560649263504, 530.6495154766618))
        self.assertEqual(raycast(origin_pos, colliders, angle=42.0, max=150), (184.03641065484905, 530.2198548833508))
        self.assertEqual(raycast(origin_pos, colliders, angle=50.0, max=150), (185.46712038548893, 522.6123310271599))
        self.assertEqual(raycast(origin_pos, colliders, angle=50.5, max=150), (185.56691141593035, 522.0817114133703))
        self.assertEqual(raycast(origin_pos, colliders, angle=51.0, max=150), (185.66816679266577, 521.5433054197675))
        self.assertEqual(raycast(origin_pos, colliders, angle=51.5, max=150), (185.7709347536847, 520.9968565501188))
        self.assertEqual(raycast(origin_pos, colliders, angle=51.99999999999999, max=150), (185.8752654568768, 520.4420980994917))
        self.assertEqual(raycast(origin_pos, colliders, angle=52.5, max=150), (185.98121108078556, 519.8787526185153))
        self.assertEqual(raycast(origin_pos, colliders, angle=53.0, max=150), (186.08882593167976, 519.306531344049))
        self.assertEqual(raycast(origin_pos, colliders, angle=53.5, max=150), (186.19816655741175, 518.7251335937625))
        self.assertEqual(raycast(origin_pos, colliders, angle=54.0, max=150), (186.3092918685726, 518.1342461219168))
        self.assertEqual(raycast(origin_pos, colliders, angle=54.49999999999999, max=150), (186.42226326749818, 517.533542433399))
        self.assertEqual(raycast(origin_pos, colliders, angle=55.00000000000001, max=150), (186.53714478572886, 516.9226820528071))
        self.assertEqual(raycast(origin_pos, colliders, angle=55.5, max=150), (186.65400323057816, 516.3013097450988))
        self.assertEqual(raycast(origin_pos, colliders, angle=56.0, max=150), (186.77290834152586, 515.6690546840019))
        self.assertEqual(raycast(origin_pos, colliders, angle=56.5, max=150), (186.8939329572141, 515.0255295640443))
        self.assertEqual(raycast(origin_pos, colliders, angle=57.0, max=150), (187.01715319389783, 514.3703296516779))
        self.assertEqual(raycast(origin_pos, colliders, angle=57.49999999999999, max=150), (187.14264863627892, 513.7030317705553))
        self.assertEqual(raycast(origin_pos, colliders, angle=58.00000000000001, max=150), (187.27050254174088, 513.0231932155508))
        self.assertEqual(raycast(origin_pos, colliders, angle=58.5, max=150), (187.4008020590973, 512.3303505896077))
        self.assertEqual(raycast(origin_pos, colliders, angle=65.0, max=150), (189.3656764570369, 501.882508839025))
        self.assertEqual(raycast(origin_pos, colliders, angle=65.5, max=150), (189.54222959065348, 500.94372150354457))
        self.assertEqual(raycast(origin_pos, colliders, angle=66.0, max=150), (189.72321391637956, 499.98137215617396))
        self.assertEqual(raycast(origin_pos, colliders, angle=66.5, max=150), (189.90882700676735, 498.994410242862))
        self.assertEqual(raycast(origin_pos, colliders, angle=67.0, max=150), (190.0992781188274, 497.98172307969656))
        self.assertEqual(raycast(origin_pos, colliders, angle=67.5, max=150), (190.29478907594492, 496.9421311634852))
        self.assertEqual(raycast(origin_pos, colliders, angle=68.0, max=150), (190.4955952308085, 495.87438305156627))
        self.assertEqual(raycast(origin_pos, colliders, angle=68.5, max=150), (190.70194651817155, 494.77714976395316))
        self.assertEqual(raycast(origin_pos, colliders, angle=69.0, max=150), (190.91410860737997, 493.6490186549892))
        self.assertEqual(raycast(origin_pos, colliders, angle=69.5, max=150), (191.13236416587628, 492.4884866949078))
        self.assertEqual(raycast(origin_pos, colliders, angle=70.0, max=150), (191.35701424635283, 491.2939530939124))
        self.assertEqual(raycast(origin_pos, colliders, angle=70.5, max=150), (191.58837981190754, 490.0637111924531))
        self.assertEqual(raycast(origin_pos, colliders, angle=71.0, max=150), (191.8268034154932, 488.7959395310794))
        self.assertEqual(raycast(origin_pos, colliders, angle=71.5, max=150), (192.07265105218488, 487.488692001363))
        self.assertEqual(raycast(origin_pos, colliders, angle=80.0, max=150), (197.91393131941993, 456.42880750346905))
        self.assertEqual(raycast(origin_pos, colliders, angle=80.5, max=150), (198.40156587890024, 453.8359045093093))
        self.assertEqual(raycast(origin_pos, colliders, angle=81.0, max=150), (198.91295907976547, 451.11666950855476))
        self.assertEqual(raycast(origin_pos, colliders, angle=81.5, max=150), (199.44997447104467, 448.26119343761826))
        self.assertEqual(raycast(origin_pos, colliders, angle=82.0, max=150), (200.01467536023011, 445.2585050556994))
        self.assertEqual(raycast(origin_pos, colliders, angle=82.5, max=150), (200.60935232742975, 442.09642464357074))
        self.assertEqual(raycast(origin_pos, colliders, angle=83.0, max=150), (201.2365554158795, 438.76139283671756))
        self.assertEqual(raycast(origin_pos, colliders, angle=83.5, max=150), (201.8991319531242, 435.2382695184839))
        self.assertEqual(raycast(origin_pos, colliders, angle=84.0, max=150), (202.6002711864233, 431.5100964798837))
        self.assertEqual(raycast(origin_pos, colliders, angle=84.5, max=150), (203.34355720906615, 427.55781599410017))
        self.assertEqual(raycast(origin_pos, colliders, angle=85.0, max=150), (204.1330320316814, 423.35993544692485))
        self.assertEqual(raycast(origin_pos, colliders, angle=100.5, max=150), (228.84676743379237, 489.6850456764896))
        self.assertEqual(raycast(origin_pos, colliders, angle=101.0, max=150), (229.33360765260667, 490.40453520340986))
        self.assertEqual(raycast(origin_pos, colliders, angle=101.5, max=150), (229.8120486879747, 491.1116117778033))
        self.assertEqual(raycast(origin_pos, colliders, angle=102.0, max=150), (230.28237706124781, 491.8066988427291))
        self.assertEqual(raycast(origin_pos, colliders, angle=102.5, max=150), (230.74486722796163, 492.4902020094654))
        self.assertEqual(raycast(origin_pos, colliders, angle=103.0, max=150), (231.19978222226325, 493.1625100098935))
        self.assertEqual(raycast(origin_pos, colliders, angle=103.49999999999999, max=150), (231.64737426080018, 493.8239955889702))
        self.assertEqual(raycast(origin_pos, colliders, angle=103.99999999999999, max=150), (232.08788530902402, 494.47501634165496))
        self.assertEqual(raycast(origin_pos, colliders, angle=104.50000000000001, max=150), (232.52154761261858, 495.1159154982947))
        self.assertEqual(raycast(origin_pos, colliders, angle=105.0, max=150), (232.94858419654204, 495.7470226621462))
        self.assertEqual(raycast(origin_pos, colliders, angle=105.5, max=150), (233.36920933397124, 496.36865450241766))
        self.assertEqual(raycast(origin_pos, colliders, angle=106.0, max=150), (233.78362898725416, 496.981115405942))
        self.assertEqual(raycast(origin_pos, colliders, angle=106.5, max=150), (234.19204122280965, 497.584698090347))
        self.assertEqual(raycast(origin_pos, colliders, angle=107.0, max=150), (234.59463660176212, 498.17968418136525))
        self.assertEqual(raycast(origin_pos, colliders, angle=107.5, max=150), (234.99159854796036, 498.7663447567202))
        self.assertEqual(raycast(origin_pos, colliders, angle=108.0, max=150), (235.3831036949024, 499.3449408588381))
        self.assertEqual(raycast(origin_pos, colliders, angle=108.5, max=150), (235.7693222129739, 499.91572397846585))
        self.assertEqual(raycast(origin_pos, colliders, angle=108.99999999999999, max=150), (236.15041811830025, 500.47893651111633))
        self.assertEqual(raycast(origin_pos, colliders, angle=109.49999999999999, max=150), (236.52654956441668, 501.0348121881202))
        self.assertEqual(raycast(origin_pos, colliders, angle=110.00000000000001, max=150), (236.89786911787053, 501.5835764839326))
        self.assertEqual(raycast(origin_pos, colliders, angle=110.5, max=150), (237.26452401879013, 502.1254470012208))
        self.assertEqual(raycast(origin_pos, colliders, angle=111.0, max=150), (237.62665642737704, 502.6606338351501))
        self.assertEqual(raycast(origin_pos, colliders, angle=111.5, max=150), (237.98440365721285, 503.1893399181819))
        self.assertEqual(raycast(origin_pos, colliders, angle=125.0, max=150), (246.38546189711965, 515.6050631576901))
        self.assertEqual(raycast(origin_pos, colliders, angle=125.5, max=150), (246.66189901550155, 516.013602969812))
        self.assertEqual(raycast(origin_pos, colliders, angle=125.99999999999999, max=150), (246.93654607635415, 516.4194972986827))
        self.assertEqual(raycast(origin_pos, colliders, angle=126.49999999999999, max=150), (247.20946184298015, 516.8228329891831))
        self.assertEqual(raycast(origin_pos, colliders, angle=127.00000000000001, max=150), (247.4807038159662, 517.2236950200562))
        self.assertEqual(raycast(origin_pos, colliders, angle=127.5, max=150), (247.7503282858858, 517.6221665817958))
        self.assertEqual(raycast(origin_pos, colliders, angle=128.0, max=150), (248.0183903840481, 518.0183291516463))
        self.assertEqual(raycast(origin_pos, colliders, angle=128.5, max=150), (248.28494413139396, 518.4122625658654))
        self.assertEqual(raycast(origin_pos, colliders, angle=129.0, max=150), (248.55004248563662, 518.8040450893922))
        self.assertEqual(raycast(origin_pos, colliders, angle=129.5, max=150), (248.8137373867382, 519.1937534830556))
        self.assertEqual(raycast(origin_pos, colliders, angle=130.0, max=150), (249.0760798008093, 519.5814630684526))
        self.assertEqual(raycast(origin_pos, colliders, angle=130.5, max=150), (249.33711976251428, 519.9672477906184))
        self.assertEqual(raycast(origin_pos, colliders, angle=131.0, max=150), (249.59690641606068, 520.351180278603))
        self.assertEqual(raycast(origin_pos, colliders, angle=131.5, max=150), (249.8554880548482, 520.7333319040677))
        self.assertEqual(raycast(origin_pos, colliders, angle=132.0, max=150), (250.11291215984738, 521.1137728380045))
        self.assertEqual(raycast(origin_pos, colliders, angle=132.5, max=150), (250.3692254367769, 521.4925721056791))
        self.assertEqual(raycast(origin_pos, colliders, angle=133.0, max=150), (250.6244738521435, 521.8697976398935))
        self.assertEqual(raycast(origin_pos, colliders, angle=133.5, max=150), (250.8787026682068, 522.2455163326596))
        self.assertEqual(raycast(origin_pos, colliders, angle=150.5, max=150), (259.2074636844648, 534.5543932327931))
        self.assertEqual(raycast(origin_pos, colliders, angle=151.0, max=150), (259.4512006071203, 534.9146062069832))
        self.assertEqual(raycast(origin_pos, colliders, angle=151.5, max=150), (259.69531630533123, 535.2753789645161))
        self.assertEqual(raycast(origin_pos, colliders, angle=152.0, max=150), (259.9398489351948, 535.6367678953764))
        self.assertEqual(raycast(origin_pos, colliders, angle=152.5, max=150), (260.18483691050307, 535.9988297703895))
        self.assertEqual(raycast(origin_pos, colliders, angle=153.0, max=150), (260.4303189272358, 536.3616217774194))
        self.assertEqual(raycast(origin_pos, colliders, angle=182.0, max=150), (277.19446853948637, 561.1369579300374))
        self.assertEqual(raycast(origin_pos, colliders, angle=182.5, max=150), (277.56739045585795, 561.6880903197193))
        self.assertEqual(raycast(origin_pos, colliders, angle=183.0, max=150), (277.94517499175913, 562.2464090586175))
        self.assertEqual(raycast(origin_pos, colliders, angle=183.5, max=150), (278.3279765637785, 562.8121423553187))
        self.assertEqual(raycast(origin_pos, colliders, angle=184.0, max=150), (278.7159552664964, 563.3855268097778))
        self.assertEqual(raycast(origin_pos, colliders, angle=184.49999999999997, max=150), (279.1092771533745, 563.9668078284384))
        self.assertEqual(raycast(origin_pos, colliders, angle=184.99999999999997, max=150), (279.50811453407823, 564.5562400636378))
        self.assertEqual(raycast(origin_pos, colliders, angle=185.49999999999997, max=150), (279.9126462893765, 565.15408787899))
        self.assertEqual(raycast(origin_pos, colliders, angle=186.00000000000003, max=150), (280.3230582048532, 565.7606258425707))
        self.assertEqual(raycast(origin_pos, colliders, angle=186.50000000000003, max=150), (280.73954332476785, 566.3761392498782))
        self.assertEqual(raycast(origin_pos, colliders, angle=187.00000000000003, max=150), (281.1623023275072, 567.0009246787054))
        self.assertEqual(raycast(origin_pos, colliders, angle=187.5, max=150), (281.59154392419396, 567.6352905782335))
        self.assertEqual(raycast(origin_pos, colliders, angle=193.0, max=150), (286.8102040802662, 575.347823729243))
        self.assertEqual(raycast(origin_pos, colliders, angle=193.5, max=150), (287.33710955318344, 576.1265247378906))
        self.assertEqual(raycast(origin_pos, colliders, angle=194.0, max=150), (287.87417791364066, 576.9202452352034))
        self.assertEqual(raycast(origin_pos, colliders, angle=194.5, max=150), (288.421790271831, 577.7295484548299))
        self.assertEqual(raycast(origin_pos, colliders, angle=223.0, max=150), (271.5360205321234, 610.788176970256))
        self.assertEqual(raycast(origin_pos, colliders, angle=223.5, max=150), (270.92411135958537, 611.1210355385487))
        self.assertEqual(raycast(origin_pos, colliders, angle=247.5, max=150), (243.7190474061451, 625.9197001839783))
        self.assertEqual(raycast(origin_pos, colliders, angle=248.0, max=150), (243.16014731176568, 626.2237235482011))
        self.assertEqual(raycast(origin_pos, colliders, angle=248.5, max=150), (242.60012694844482, 626.528356302073))
        self.assertEqual(raycast(origin_pos, colliders, angle=249.0, max=150), (242.03889738084004, 626.8336468235103))
        self.assertEqual(raycast(origin_pos, colliders, angle=249.5, max=150), (241.47636891991513, 627.1396439004143))
        self.assertEqual(raycast(origin_pos, colliders, angle=250.0, max=150), (240.9124510643415, 627.4463967625463))
        self.assertEqual(raycast(origin_pos, colliders, angle=250.5, max=150), (240.3470524408086, 627.7539551139978))
        self.assertEqual(raycast(origin_pos, colliders, angle=251.0, max=150), (239.7800807431608, 628.062369166297))
        self.assertEqual(raycast(origin_pos, colliders, angle=251.5, max=150), (239.2114426702701, 628.3716896722049))
        self.assertEqual(raycast(origin_pos, colliders, angle=251.99999999999997, max=150), (238.64104386255443, 628.6819679602464))
        self.assertEqual(raycast(origin_pos, colliders, angle=252.49999999999997, max=150), (238.06878883704763, 628.9932559700313))
        self.assertEqual(raycast(origin_pos, colliders, angle=252.99999999999997, max=150), (237.4945809209214, 629.305606288415))
        self.assertEqual(raycast(origin_pos, colliders, angle=253.50000000000003, max=150), (236.91832218335946, 629.619072186557))
        self.assertEqual(raycast(origin_pos, colliders, angle=254.00000000000003, max=150), (236.3399133656769, 629.9337076579345))
        self.assertEqual(raycast(origin_pos, colliders, angle=254.50000000000003, max=150), (235.75925380957523, 630.2495674573681))
        self.assertEqual(raycast(origin_pos, colliders, angle=255.0, max=150), (235.1762413834193, 630.5667071411257))
        self.assertEqual(raycast(origin_pos, colliders, angle=255.5, max=150), (234.590772406415, 630.8851831081669))
        self.assertEqual(raycast(origin_pos, colliders, angle=256.0, max=150), (234.0027415705653, 631.2050526425963))
        self.assertEqual(raycast(origin_pos, colliders, angle=256.5, max=150), (233.4120418602725, 631.5263739573978))
        self.assertEqual(raycast(origin_pos, colliders, angle=278.0, max=150), (203.5220007097121, 647.7855783460461))
        self.assertEqual(raycast(origin_pos, colliders, angle=278.5, max=150), (202.66090215081795, 648.2539877870806))
        self.assertEqual(raycast(origin_pos, colliders, angle=279.0, max=150), (201.78838450842557, 648.7286088359076))
        self.assertEqual(raycast(origin_pos, colliders, angle=279.5, max=150), (200.9040835402906, 649.20963962839))
        self.assertEqual(raycast(origin_pos, colliders, angle=280.0, max=150), (200.00762145968233, 649.6972856681482))
        self.assertEqual(raycast(origin_pos, colliders, angle=280.5, max=150), (199.09860626003154, 650.1917601939297))
        self.assertEqual(raycast(origin_pos, colliders, angle=281.0, max=150), (198.17663099968783, 650.693284568677))
        self.assertEqual(raycast(origin_pos, colliders, angle=281.5, max=150), (197.24127304398093, 651.2020886918223))
        self.assertEqual(raycast(origin_pos, colliders, angle=282.0, max=150), (196.29209326156155, 651.7184114364511))
        self.assertEqual(raycast(origin_pos, colliders, angle=282.5, max=150), (195.3286351717426, 652.2425011131216))
        self.assertEqual(raycast(origin_pos, colliders, angle=283.0, max=150), (194.35042403929793, 652.7746159622633))
        self.assertEqual(raycast(origin_pos, colliders, angle=283.5, max=150), (193.3569659128754, 653.3150246772498))
        self.assertEqual(raycast(origin_pos, colliders, angle=284.0, max=150), (192.34774660286004, 653.8640069604074))
        self.assertEqual(raycast(origin_pos, colliders, angle=284.5, max=150), (191.32223059416864, 654.4218541144195))
        self.assertEqual(raycast(origin_pos, colliders, angle=285.0, max=150), (190.27985988906582, 654.9888696717965))
        self.assertEqual(raycast(origin_pos, colliders, angle=285.5, max=150), (189.22005277466724, 655.5653700653139))
        self.assertEqual(raycast(origin_pos, colliders, angle=286.0, max=150), (188.14220250932473, 656.1516853425759))
        self.assertEqual(raycast(origin_pos, colliders, angle=308.0, max=150), (161.77981846103023, 628.398667656794))
        self.assertEqual(raycast(origin_pos, colliders, angle=308.5, max=150), (161.25148876361004, 627.8283117334427))
        self.assertEqual(raycast(origin_pos, colliders, angle=309.0, max=150), (160.7245666972521, 627.2594754118062))
        self.assertEqual(raycast(origin_pos, colliders, angle=309.5, max=150), (160.1989666989777, 626.6920663227601))
        self.assertEqual(raycast(origin_pos, colliders, angle=310.0, max=150), (159.67460403643116, 626.1259929938745))
        self.assertEqual(raycast(origin_pos, colliders, angle=317.0, max=150), (106.2969447571244, 661.2997540093747))
        self.assertEqual(raycast(origin_pos, colliders, angle=322.5, max=150), (96.99699895631475, 650.3142143513081))
        self.assertEqual(raycast(origin_pos, colliders, angle=323.0, max=150), (96.20467349290608, 649.2722534728073))
        self.assertEqual(raycast(origin_pos, colliders, angle=323.5, max=150), (95.42147090741737, 648.2234180127011))
        self.assertEqual(raycast(origin_pos, colliders, angle=324.0, max=150), (94.6474508437579, 647.167787843871))
        self.assertEqual(raycast(origin_pos, colliders, angle=350.0, max=150), (68.27883704816881, 585.0472266500396))
        self.assertEqual(raycast(origin_pos, colliders, angle=350.5, max=150), (68.05715976941528, 583.7571408791016))
        self.assertEqual(raycast(origin_pos, colliders, angle=351.0, max=150), (67.84674891072936, 582.4651697560347))
        self.assertEqual(raycast(origin_pos, colliders, angle=351.5, max=150), (67.64762049571249, 581.1714116694417))
        self.assertEqual(raycast(origin_pos, colliders, angle=352.0, max=150), (67.45978968876446, 579.8759651440099))
        self.assertEqual(raycast(origin_pos, colliders, angle=352.5, max=150), (67.28327079392844, 578.5789288330077))
        self.assertEqual(raycast(origin_pos, colliders, angle=353.0, max=150), (67.11807725380172, 577.2804015107722))
        self.assertEqual(raycast(origin_pos, colliders, angle=353.5, max=150), (66.96422164851188, 575.980482065186))
        self.assertEqual(raycast(origin_pos, colliders, angle=354.5, max=150), (66.69057024492318, 573.3768628780336))
        self.assertEqual(raycast(origin_pos, colliders, angle=355.0, max=150), (66.57079528623817, 572.0733614121488))
        self.assertEqual(raycast(origin_pos, colliders, angle=355.5, max=150), (66.46239994003079, 570.7688643591769))
        self.assertEqual(raycast(origin_pos, colliders, angle=356.0, max=150), (66.36539246102635, 569.4634710616187))
        self.assertEqual(raycast(origin_pos, colliders, angle=356.5, max=150), (66.27978023671997, 568.1572809302286))
        self.assertEqual(raycast(origin_pos, colliders, angle=357.0, max=150), (66.20556978681392, 566.8503934364417))
        self.assertEqual(raycast(origin_pos, colliders, angle=357.5, max=150), (66.14276676272132, 565.5429081048003))
        self.assertEqual(raycast(origin_pos, colliders, angle=358.0, max=150), (66.09137594713565, 564.2349245053751))
        self.assertEqual(raycast(origin_pos, colliders, angle=358.5, max=150), (66.0514012536664, 562.926542246181))
        self.assertEqual(raycast(origin_pos, colliders, angle=359.0, max=150), (66.0228457265413, 561.6178609655926))
        self.assertEqual(raycast(origin_pos, colliders, angle=359.5, max=150), (66.0057115403743, 560.308980324756))

if __name__ == "__main__":
    unittest.main()
