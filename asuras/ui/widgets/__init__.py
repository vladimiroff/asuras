from pygame import sprite

class Widget(sprite.Sprite):

    def __init__(self, position=(0, 0), size=(0, 0)):
        self.position = position
        self.size = size

    def update(self, *sprites):
        pass

