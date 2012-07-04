import pdb
import math
import pygame

from libs.vec2d import Vec2d

# Keys in pressed_arrows
W = 0
A = 1
S = 2
D = 3


class Player(pygame.sprite.Sprite):
    top_speed = 5
    speed = 0
    weight = 0.4
    acceleration = 1
    rotation = 0
    position = Vec2d(320, 240)

    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('resources/tank.png')
        self.base_image = self.image
        self.rect = pygame.rect.Rect(self.position, self.image.get_size())

    def update(self, pressed):
        print(pressed)
        if pressed[A]:
            self.rotation -= 1
            self.image = pygame.transform.rotate(self.base_image, self.rotation)
        if pressed[D]:
            self.rotation += 1
            self.image = pygame.transform.rotate(self.base_image, self.rotation)
        if pressed[W] and abs(self.speed) < self.top_speed:
            self.speed += self.acceleration
        if pressed[S] and abs(self.speed) < self.top_speed:
            self.speed -= self.acceleration
        if not pressed[W] and not pressed[S] and self.speed != 0:
            self.speed -= math.copysign(self.acceleration, self.speed)

        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

        direction = Vec2d(math.cos(self.rotation), math.sin(self.rotation))
        direction.length = self.speed

        print(self.speed, self.rotation, direction, self.acceleration)
        print()
        self.position += direction
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

