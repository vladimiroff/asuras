import math
from pygame import sprite, transform

from libs.vec2d import Vec2d
from libs.collisions import Detection

# Keys in pressed_arrows
W = 0
A = 1
S = 2
D = 3

class Obsticle:
    def __init__(self):
        self.pos = 0
        self.points = []

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
            'shields': ['front', 'back', 'left', 'right'],
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

    def collision_check(self, tilemap):
        tile_container = (self.rect.center[0]//tilemap.layers[0].tile_width,self.rect.center[1]//tilemap.layers[0].tile_height)
        tile = tilemap.layers[0][tile_container]
        obsticles = []
        for line in range(3):
            for col in range(3):
                curent_tile = tilemap.layers[1][(tile_container[0] + line - 1, tile_container[1] + col - 1)]
                if type(curent_tile) == type(tile):#Kire trqbva da opravim tazi krupla s tipa
                    if curent_tile.tile.properties['collidable']:
                        object_points = curent_tile.tile.properties['points'].split(';')
                        new_collidable_object = Obsticle() # I tova trqbva da se opravi
                        new_collidable_object.pos = Vec2d(curent_tile.topleft)
                        new_collidable_object.points = []
                        for point in object_points:
                            point_coords = point.split(',')
                            new_collidable_object.points.append(Vec2d(int(point_coords[0]), int(point_coords[1])))
                        obsticles.append(new_collidable_object)
        player = Obsticle()
        player.pos = self.rect.center
        player.points = self.points
        vehicle_colider = Detection(player, obsticles)
        vehicle_colider.line_by_line_check()
        return not vehicle_colider.collisions == []

    def update(self, pressed, time_delta, tilemap):
        if not self.collision_check(tilemap) or self.speed == 0:
            print(self.speed)
            self.movement_controls(pressed)
            self.update_position(time_delta)
        else:
            print(self.speed)
            self.speed = - (self.speed * 0.8)
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


    def attach(self, component, slot, overwrite=True):
        if component.group not in self.DEFAULTS['slots']:
            return False
        if not slot.is_empty:
            if not overwrite:
                return False
        self._slots[component.group][slot] = component
        self.recalculate()

    def detach(self, component, slot):
        self._slots[component.group][slot] = None
        self.recalculate()
