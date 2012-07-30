import math
from pygame import sprite, transform

from libs.vec2d import Vec2d
from libs.collisions import Detection
from libs.tmx.cells import Cell


# Keys in pressed_arrows
W = 0
A = 1
S = 2
D = 3


class Obstacle:
    def __init__(self):
        self.pos = 0
        self.points = []

class Vehicle(sprite.Sprite):
    DEFAULTS = {
        'weight': 0,
        'inventory': 0,
        'dimenstion': 0,
        'power_consumption': 0,
        'slots': {
            'motions': 1,
            'engines': 1,
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
    }

    top_speed = 0
    speed = 0
    weight = 0.0
    acceleration = 0
    rotation = 0
    power = 0

    def __init__(self, location, *groups):
        super(__class__, self).__init__(*groups)
        self.position = Vec2d(location[0], location[1])

        self.near_obstacles = [] # Used only for debug wireframe mode
        self.collision_points = [] # Used only for debug wireframe mode
        self.result = 0

    def collision_check(self, tilemap, direction):
        tile_container = (self.rect.center[0] // tilemap.layers[0].tile_width, self.rect.center[1] // tilemap.layers[0].tile_height)
        obstacles = []
        for line in range(3):
            for col in range(3):
                curent_tile = tilemap.layers[1][(tile_container[0] + line - 1, tile_container[1] + col - 1)]
                if type(curent_tile) is Cell:
                    if curent_tile.tile.properties['collidable']:
                        object_points = curent_tile.tile.properties['points'].split(';')
                        new_collidable_object = Obstacle() # I tova trqbva da se opravi
                        new_collidable_object.pos = Vec2d(curent_tile.topleft)
                        new_collidable_object.points = []
                        for point in object_points:
                            point_coords = point.split(',')
                            new_collidable_object.points.append(Vec2d(int(point_coords[0]), int(point_coords[1])))
                        obstacles.append(new_collidable_object)

        player = Obstacle()
        player.pos = self.position + direction
        player.points = self.points
        vehicle_colider = Detection(player, obstacles)
        vehicle_colider.line_by_line_check()

        self.near_obstacles = obstacles # Used only for debug wireframe mode

        return vehicle_colider

    def collision_reactor(self, line):
        if line[1][0] == line[0][0]:
            tangent = math.tan(math.radians(self.rotation))
        else:
            a_prime = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
            b_prime = line[0][1] - a_prime * line[0][0]
            a_second = math.tan(math.radians(self.rotation))
            tangent = (a_prime - a_second) / (1 + a_prime * a_second)
        modify = 1 + self.speed // 6
        if tangent < 0:
            self.rotation += modify
            for point in self.points:
                point.rotate(360 - modify)
        elif tangent > 0:
            self.rotation -= modify
            for point in self.points:
                point.rotate(modify)

        else:
            self.speed = - self.speed

        self.speed *= 0.85   
        self.image = transform.rotate(self.base_image, self.rotation)
        self.rect = self.image.get_rect()


    def update(self, pressed, time_delta, tilemap):
        direction = Vec2d(math.sin(math.radians(self.rotation)), math.cos(math.radians(self.rotation)))
        direction.length = self.speed

        predicted_collision_result = self.collision_check(tilemap, direction)

        collision_result = self.collision_check(tilemap, Vec2d(0,0))
        
        self.result = collision_result
        
        self.movement_controls(pressed)
        
        if predicted_collision_result.collisions and not self.speed == 0:
            self.collision_points = collision_result.collisions
            if collision_result.collisions:
                self.speed = - self.speed * time_delta * 2
            else:
                self.collision_reactor(predicted_collision_result.collision_lines[0])
            self.update_position(time_delta)
        else:
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
            for point in self.points:
                point.rotate(358)
        if pressed[D]:
            self.rotation -= 2
            for point in self.points:
                point.rotate(2)

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
            'power_consumption': self.DEFAULTS['power_consumption']
        }

        for group in self._slots.values():
            for component in group.values():
                for parameter in parameters:
                    parameters[parameter] += getattr(component, parameter, 0)

        for parameter in parameters:
            setattr(self, parameter, parameters[parameter])

    def attach(self, component, slot, overwrite=False):
        if component.group not in self._slots or slot >= self.DEFAULTS['slots'][component.group]:
            return False
        if not self._slots[component.group].get(slot, None) or overwrite:
            self._slots[component.group][slot] = component
        self.recalculate()
        return self._slots[component.group][slot]

    def detach(self, component, slot):
        self._slots[component.group][slot] = None
        self.recalculate()
