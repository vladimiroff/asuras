import math
from pygame import sprite, transform, image
from . import VehicleComponent

from libs.vec2d import Vec2d

class Weapon(VehicleComponent):
    power_consumption = 0
    rotation = 0
    weight = 0
    projectile = None
    damage = 0
    range = 0

    def __init__(self, position, *groups):
        #import ipdb; ipdb.set_trace()
        self.group = 'weapons'
        super().__init__(self.group, *groups)
        self.image = image.load('resources/turret.png')
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def vriable_refresh(self, mouse_pos, position, screen_focus):
        direction = Vec2d(mouse_pos[0] - (position[0] - screen_focus[0]), mouse_pos[1] - (position[1] - screen_focus[1]))
        direction.length = 1
        self.rotation = math.asin(direction[1])
        self.image = transform.rotate(self.base_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self, position, *args):
        self.image = transform.rotate(self.base_image, self.rotation)
        self.rect = self.image.get_rect()
        print(position)
        self.rect.x = position[0]
        self.rect.y = position[1]
