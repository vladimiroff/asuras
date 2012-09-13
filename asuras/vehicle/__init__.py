import math
from pygame import sprite, transform

from vehicle.components.weapon import Weapon
from vehicle.components.engine import Engine
from vehicle.components.generator import Generator
from libs.vec2d import Vec2d
from libs.collisions import Detection, Obstacle, collision_check
from libs.tmx import cells
from entities.bullet import Bullet


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
        'power_consumption': 0,
        'slots': {
            'motions': 1,
         #   'engines': 1,
            'shields': 4,
            'addons': 8,
            'generators': 1,
        },
    }

    _slots = {
        'motions': {},
        'engines': {},
        'shields': {},
        'addons': {},
        'generators': {},
        'weapons': {},
    }

    top_speed = 0
    speed = 0
    weight = 0.0
    acceleration = 0
    rotation = 0
    power = 0

    def __init__(self, location, items_layer, *groups):
        super().__init__(*groups)
        self.sprite_groups = groups
        self.position = Vec2d(location[0], location[1])
        self.items_layer = items_layer
        self.near_obstacles = []
        self.collision_points = []
        self.result = 0
        turret = Weapon(self.position)
        self.attach(turret, 0)
        engine = Engine(self)
        self.attach(engine, 0)
        generator = Generator()
        self.attach(generator, 0)

    def collision_reactor(self, line):
        if line[1][0] == line[0][0]:
            tangent = math.tan(math.radians(self.rotation))
        else:
            a_prime = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
            b_prime = line[0][1] - a_prime * line[0][0] # Not used for now
            a_second = math.tan(math.radians(self.rotation))
            if line[1][1] == line[0][1]:
                tangent = (a_prime - a_second) / (1 + a_prime * a_second)
            else:
                tangent = - (a_prime - a_second) / (1 + a_prime * a_second)
        modify = 1 + self.speed // 6
        if tangent < 0:
            self.rotation += modify
            self.rotate_vehicle(360 - modify)
        elif tangent > 0:
            self.rotation -= modify
            self.rotate_vehicle(modify)
        else:
            self.speed = - self.speed

        self.speed *= 0.85
        self.image = transform.rotate(self.base_image, self.rotation)
        self.rect = self.image.get_rect()


    def update(self, pressed, time_delta, tilemap):
        direction = Vec2d(math.sin(math.radians(self.rotation)), 
                            math.cos(math.radians(self.rotation)))
        direction.length = self.speed
        predicted_collision_result = collision_check(self, tilemap, direction)
        collision_result = collision_check(self, tilemap, Vec2d(0,0))
        self.result = collision_result
        self.movement_controls(pressed, tilemap)
        if predicted_collision_result.collisions and not self.speed == 0:
            self.collision_points = collision_result.collisions
            if collision_result.collisions:
                self.speed = - self.speed * time_delta * 2
            else:
                self.collision_reactor(predicted_collision_result.collision_lines[0])
            self.update_position(time_delta)
        else:
            self.update_position(time_delta)
        self.items_layer.update(Vec2d(self.rect.center[0] - tilemap.viewport[0],
                                     self.rect.center[1] - tilemap.viewport[1]), self)

    def update_position(self, time_delta):
        direction = Vec2d(math.sin(math.radians(self.rotation)),
                             math.cos(math.radians(self.rotation)))
        direction.length = self.speed * time_delta

        self.position += direction
        self.rect.center = self.position

        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

    def rotate_vehicle(self, degrees):
        for point in self.points:
            point.rotate(degrees)
        for pivot_point in self.pivot_points:
            pivot_point.rotate(degrees)

    def movement_controls(self, pressed, tilemap):
        if pressed[A]:
            self.rotation += 2
            self.rotate_vehicle(358)
            collision_result = collision_check(self, tilemap, Vec2d(0,0))
            if collision_result.collisions:
                self.rotation -= 2
                self.rotate_vehicle(2)   
        if pressed[D]:
            self.rotation -= 2
            self.rotate_vehicle(2)
            collision_result = collision_check(self, tilemap, Vec2d(0,0))
            if collision_result.collisions:
                self.rotation += 2
                self.rotate_vehicle(358)

        if pressed[W] and abs(self.speed) < self.top_speed:
            self.speed += self.acceleration
        if pressed[S] and abs(self.speed) < self.top_speed:
            self.speed -= self.acceleration

        if not pressed[W] and not pressed[S] and self.speed != 0:
            if abs(self.speed) < abs(self.acceleration):
                self.speed = 0
            else:
                self.speed -= math.copysign(self.acceleration, self.speed)
        if pressed[A] or pressed[D]:
            self.image = transform.rotate(self.base_image, self.rotation)
            self.rect = self.image.get_rect()

    def recalculate(self):
        parameters = {
            'weight': self.DEFAULTS['weight'],
            'power_generation': 0,
            'power_consumption': self.DEFAULTS.get('power_consumption', 0)
        }

        for group in self._slots.values():
            for component in group.values():
                for parameter in parameters:
                    parameters[parameter] += getattr(component, parameter, 0)

        for parameter in parameters:
            setattr(self, parameter, parameters[parameter])

    def fire(self, projectiles):
        projectile = Bullet(self.position + self.pivot_points[0], 
                            self._slots['weapons'][0].direction, 0)
        projectiles.add(projectile)

    def attach(self, component, slot, overwrite=False):
        if component.group not in self._slots or slot >= self.DEFAULTS['slots'][component.group]:
            return False
        if not self._slots[component.group].get(slot, None) or overwrite:
            self._slots[component.group][slot] = component
        self.recalculate()
        self.items_layer.add(component)
        return self._slots[component.group][slot]

    def detach(self, component, slot):
        self._slots[component.group][slot] = None
        self.recalculate()
