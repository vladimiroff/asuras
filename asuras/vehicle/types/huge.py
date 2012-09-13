from . import Vehicle

class HugeVehicle(Vehicle):
    DEFAULTS = {
        'weight': 4800,
        'inventory': 80,
        'dimenstions': (60, 120),
        'slots': {
            'motions': 8,
            'engines': 8,
            'shields': 6,
            'addons': 12,
            'generators': 2,
        },
    }
