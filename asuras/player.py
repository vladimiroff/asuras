from vehicle.types.normal import NormalVehicle

class Player:

    def __init__(self, items_layer, *sprite_groups):
        self.vehicle = NormalVehicle((320, 240), items_layer, *sprite_groups)
