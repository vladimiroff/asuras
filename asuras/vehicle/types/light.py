from . import Vehicle

class LightVehicle(Vehicle):
    DEFAULTS = {
        'weight': 800,
        'inventory': 9,
        'dimenstions': (40, 50),
        'slots': {
            'motions': {
                'front': 2,
                'back': 2,
            },
            'engines': {
                'front': 2,
                'back': 2,
            },
            'shields': ['front', 'back', 'left', 'right'],
            'addons': 5,
            'generators': 1,
        },
    }
