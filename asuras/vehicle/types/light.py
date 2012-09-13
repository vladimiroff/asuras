from . import Vehicle

class LightVehicle(Vehicle):
    DEFAULTS = {
        'weight': 800,
        'inventory': 9,
        'dimenstions': (40, 50),
        'slots': {
            'motions': 4,
            'engines': 4,
            'shields': 4,
            'addons': 5,
            'generators': 1,
        },
    }
