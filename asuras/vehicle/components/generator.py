from . import VehicleComponent
from pygame import sprite, transform, image

class Generator(VehicleComponent):
    power = 5
    weight = 10
    compatibility = None

    def __init__(self, *groups):
        self.group = 'generators'
        super().__init__(self.group, *groups)
        # ako ima vizualizirane na generatora vurhu samata kolichka
        self.image = image.load('resources/placeholder.png')
        self.base_image = self.image
        self.rect = self.image.get_rect()

    def update(self, position, vehicle, *args):
        vehicle.power += self.power
        self.rect.center = position