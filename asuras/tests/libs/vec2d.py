import unittest
import pickle

from libs.vec2d import Vec2d

class UnitTestVec2D(unittest.TestCase):

    def setUp(self):
        pass

    def testCreationAndAccess(self):
        v = Vec2d(111, 222)
        self.assertTrue(v.x == 111 and v.y == 222)
        v.x = 333
        v[1] = 444
        self.assertTrue(v[0] == 333 and v[1] == 444)

    def testMath(self):
        v = Vec2d(111,222)
        self.assertEqual(v + 1, Vec2d(112,223))
        self.assertTrue(v - 2 == [109,220])
        self.assertTrue(v * 3 == (333,666))
        self.assertTrue(v / 2.0 == Vec2d(55.5, 111))
        self.assertTrue(v / 2 == (55.5, 111))
        self.assertTrue(v ** Vec2d(2,3) == [12321, 10941048])
        self.assertTrue(v + [-11, 78] == Vec2d(100, 300))
        self.assertTrue(v / [10,2] == [11.1,111])

    def testReverseMath(self):
        v = Vec2d(111,222)
        self.assertTrue(1 + v == Vec2d(112,223))
        self.assertTrue(2 - v == [-109,-220])
        self.assertTrue(3 * v == (333,666))
        self.assertTrue([222,888] / v == [2,4])
        self.assertTrue([111,222] ** Vec2d(2,3) == [12321, 10941048])
        self.assertTrue([-11, 78] + v == Vec2d(100, 300))

    def testUnary(self):
        v = Vec2d(111,222)
        v = -v
        self.assertTrue(v == [-111,-222])
        v = abs(v)
        self.assertTrue(v == [111,222])

    def testLength(self):
        v = Vec2d(3,4)
        self.assertTrue(v.length == 5)
        self.assertTrue(v.get_length_sqrd() == 25)
        self.assertTrue(v.normalize_return_length() == 5)
        self.assertTrue(v.length == 1)
        v.length = 5
        self.assertTrue(v == Vec2d(3,4))
        v2 = Vec2d(10, -2)
        self.assertTrue(v.get_distance(v2) == (v - v2).get_length())

    def testAngles(self):
        v = Vec2d(0, 3)
        self.assertEqual(v.angle, 90)
        v2 = Vec2d(v)
        v.rotate(-90)
        self.assertEqual(v.get_angle_between(v2), 90)
        v2.angle -= 90
        self.assertEqual(v.length, v2.length)
        self.assertEqual(v2.angle, 0)
        self.assertEqual(v2, [3, 0])
        self.assertTrue((v - v2).length < .00001)
        self.assertEqual(v.length, v2.length)
        v2.rotate(300)
        self.assertAlmostEqual(v.get_angle_between(v2), -60)
        v2.rotate(v2.get_angle_between(v))
        self.assertAlmostEqual(v.get_angle_between(v2), 0)

    def testHighLevel(self):
        basis0 = Vec2d(5.0, 0)
        basis1 = Vec2d(0, .5)
        v = Vec2d(10, 1)
        self.assertTrue(v.convert_to_basis(basis0, basis1) == [2, 2])
        self.assertTrue(v.projection(basis0) == (10, 0))
        self.assertTrue(basis0.dot(basis1) == 0)

    def testCross(self):
        lhs = Vec2d(1, .5)
        rhs = Vec2d(4,6)
        self.assertTrue(lhs.cross(rhs) == 4)

    def testComparison(self):
        int_vec = Vec2d(3, -2)
        flt_vec = Vec2d(3.0, -2.0)
        zero_vec = Vec2d(0, 0)
        self.assertTrue(int_vec == flt_vec)
        self.assertTrue(int_vec != zero_vec)
        self.assertTrue((flt_vec == zero_vec) == False)
        self.assertTrue((flt_vec != int_vec) == False)
        self.assertTrue(int_vec == (3, -2))
        self.assertTrue(int_vec != [0, 0])
        self.assertTrue(int_vec != 5)
        self.assertTrue(int_vec != [3, -2, -5])

    def testInplace(self):
        inplace_vec = Vec2d(5, 13)
        inplace_ref = inplace_vec
        inplace_vec *= .5
        inplace_vec += .5
        inplace_vec /= (3, 6)
        inplace_vec += Vec2d(-1, -1)
        self.assertEqual(inplace_vec, inplace_ref)

    def testPickle(self):
        testvec = Vec2d(5, .3)
        testvec_str = pickle.dumps(testvec)
        loaded_vec = pickle.loads(testvec_str)
        self.assertEqual(testvec, loaded_vec)
