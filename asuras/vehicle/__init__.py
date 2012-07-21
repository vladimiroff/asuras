import math
from pygame import sprite, transform

from libs.vec2d import Vec2d

# Keys in pressed_arrows
W = 0
A = 1
S = 2
D = 3

class Vehicle(sprite.Sprite):
    DEFAULTS = {
        'weight': 0,
        'inventory': 0,
        'dimenstion': 0,
        'slots': {
            'motions': {
                'front': 0,
                'back': 0,
            },
            'engines': {
                'front': 0,
                'back': 0,
            },
            'shields': {
                'front': 0,
                'back': 0,
                'left': 0,
                'right': 0,
            },
            'addons': 0,
            'generators': 0,
        },
    }

    _slots = {}

    top_speed = 0
    speed = 0
    weight = 0.0
    acceleration = 0
    rotation = 0

    def __init__(self, location, *groups):
        super(__class__, self).__init__(*groups)
        self.position = Vec2d(location[0], location[1])

    def update(self, pressed, time_delta, tilemap):
        self.movement_controls(pressed)
        self.update_position(time_delta)

    def update_position(self, time_delta):
        direction = Vec2d(math.sin(math.radians(self.rotation)), math.cos(math.radians(self.rotation)))
        direction.length = self.speed * time_delta

        self.position += direction
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.rect.center = self.position

        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

    def movement_controls(self, pressed):
        if pressed[A]:
            self.rotation += 2
        if pressed[D]:
            self.rotation -= 2

        if pressed[W] and abs(self.speed) < self.top_speed:
            self.speed += self.acceleration
        if pressed[S] and abs(self.speed) < self.top_speed:
            self.speed -= self.acceleration

        if not pressed[W] and not pressed[S] and self.speed != 0:
            self.speed -= math.copysign(self.acceleration, self.speed)

        if pressed[A] or pressed[D]:
            self.image = transform.rotate(self.base_image, self.rotation)
            self.rect = self.image.get_rect()

    def recalculate(self):
        pass

    def attach(self, component, slot):
        if component.group not in self.DEFAULTS['slots']:
            return False
        if not self._slots.setdefault(component.group, {}).setdefault(slot, None):
                return False
        self._slots[component.group][slot] = component
        self.recalculate()

    def detach(self, component, slot):
        try:
            del self._slots[component.group][slot]
        except KeyError:
            pass
        self.recalculate()
