from vehicle.types.normal import NormalVehicle

class Player:

    def __init__(self, *sprite_groups):
        self.vehicle = NormalVehicle((320, 240), sprite_groups)
