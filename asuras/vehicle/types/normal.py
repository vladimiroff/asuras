from pygame import image

from libs.vec2d import Vec2d
from vehicle import Vehicle

class NormalVehicle(Vehicle):
    DEFAULTS = {
        'weight': 1200,
        'inventory': 16,
        'dimenstions': (40, 70),
        'slots': {
            'motions': {
                'front': 2,
                'back': 2,
            },
            'engines': {
                'front': 2,
                'back': 2,
            },
            'shields': ['front', 'back', 'left', 'right'],
            'addons': 8,
            'generators': 1,
        },
    }
    top_speed = 50
    speed = 0
    weight = 0.4
    acceleration = 1
    rotation = 0

    def __init__(self, position, *groups):
        super(__class__, self).__init__(position, *groups)
        self.image = image.load('resources/tank.png')
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.points = [Vec2d(-7, -32),
                       Vec2d(-20, -23),
                       Vec2d(-20, -13),
                       Vec2d(-15, -8),
                       Vec2d(-15, 8),
                       Vec2d(-20, 13),
                       Vec2d(-20, 23),
                       Vec2d(-7, 32),
                       Vec2d(7, 32),
                       Vec2d(20, 23),
                       Vec2d(20, 13),
                       Vec2d(15, 8),
                       Vec2d(15, -8),
                       Vec2d(20, -13),
                       Vec2d(20, -23),
                       Vec2d(7, -32),]
