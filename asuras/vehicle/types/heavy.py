from . import Vehicle

class HeavyVehicle(Vehicle):
    DEFAULTS = {
        'weight': 3400,
        'inventory': 30,
        'dimenstions': (60, 80),
        'slots': {
            'motions': 6,
            'engines': 6,
            'shields': 4,
            'addons': 12,
            'generators': 2,
            'weapons': 1,
        },
    }
