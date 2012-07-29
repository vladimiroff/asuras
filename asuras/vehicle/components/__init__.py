from pygame import sprite

class VehicleComponent(sprite.Sprite):
    weight = 1
    power_consumption = 0
    power_generation = 0

    def __init__(self, group, *sprite_groups):
        self.group = group
        super().__init__(*sprite_groups)
