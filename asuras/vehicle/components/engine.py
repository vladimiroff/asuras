from . import VehicleComponent
from pygame import sprite, transform, image

class Engine(VehicleComponent):
    power_consumption = 2
    top_speed = 50
    weight = 10
    torque = 0

    def __init__(self, vehicle, *groups):
        self.group = 'engines'
        super().__init__(self.group, *groups)
        vehicle.top_speed = self.top_speed
        # ako ima vizualizirane na dvigatelq vurhu samata kolichka
        self.image = image.load('resources/placeholder.png')
        self.base_image = self.image
        self.rect = self.image.get_rect()

    def update(self, position, vehicle, *args):
        vehicle.power -= self.power_consumption
        self.rect.center = position