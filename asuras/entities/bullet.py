import math
from pygame import sprite, transform, image
from libs.collisions import Detection, Obstacle
from libs.vec2d import Vec2d

class Bullet(sprite.Sprite):

    direction = Vec2d(0, 0)
    rotation = 0
    position = Vec2d(0, 0)
    points = [Vec2d(2, -2), Vec2d(2, 2)]

    def __init__(self, position, direction, type, *sprite_groups):
        super().__init__(*sprite_groups)
        self.direction = direction
        direction.length = 1
        if direction[1] < 0:
            modify = (90 - math.degrees(math.asin(direction[0]))) * 2
        else:
            modify = 0
        self.rotation = math.degrees(math.asin(direction[0])) + modify
        self.position = position

        for point in self.points:
            point.rotate(360 - self.rotation)

        base_image = image.load('resources/bomb.png')
        self.image = transform.rotate(base_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self, pressed, time_delta, tilemap):
        self.direction.length = 15
        self.position += self.direction
        self.rect.center = self.position
