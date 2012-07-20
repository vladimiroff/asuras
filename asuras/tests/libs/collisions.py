import unittest

from libs.collisions import Detection
from libs.vec2d import Vec2d

class FormMock:
    def __init__(self):
        self.points = []
        self.rotation = 90
        self.pos = Vec2d(100, 100)

class DetectionTest(unittest.TestCase):

    def setUp(self):
        self.entity = FormMock()
        self.entity.points.append(Vec2d(10, 10))
        self.entity.points.append(Vec2d(20, 20))

        self.building = FormMock()
        self.building.points.append(Vec2d(30, 15))
        self.building.points.append(Vec2d(40, 10))

        self.detection = Detection([self.entity], [self.building])

    def test_line_collider(self):
        self.assertFalse(self.detection.line_collider(self.entity.points, self.building.points))
        self.assertTrue(self.detection.line_collider([Vec2d(10, 10), Vec2d(20, 20)], [Vec2d(10, 15), Vec2d(20, 10)]))
        self.assertFalse(self.detection.line_collider([Vec2d(20, 10), Vec2d(20, 30)], [Vec2d(30, 10), Vec2d(30, 30)]))
        self.assertTrue(self.detection.line_collider([Vec2d(10, 20), Vec2d(30, 10)], [Vec2d(20, 10), Vec2d(20, 30)]))

    def test_cartesian_equation(self):
        self.assertTrue(self.detection.cartesian_equation([Vec2d(20, 10), Vec2d(20, 30)], [Vec2d(10, 20), Vec2d(30, 10)]))
        self.assertFalse(self.detection.cartesian_equation([Vec2d(3, 7), Vec2d(4, 15)], [Vec2d(5, 19), Vec2d(6, 27)]))
