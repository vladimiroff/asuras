from . import Vehicle

class TinyVehicle(Vehicle):
    DEFAULTS = {
        'weight': 600,
        'inventory': 4,
        'dimenstions': (20, 60),
        'slots': {
            'motions': 4,
            'engines': 4,
            'shields': 4,
            'addons': 2,
            'generators': 1,
        },
    }
