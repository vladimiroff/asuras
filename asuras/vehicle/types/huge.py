from . import Vehicle

class Huge(Vehicle):
    DEFAULTS = {
        'weight': 4800,
        'inventory': 80,
        'dimenstions': (60, 120),
        'slots': {
            'motions': {
                'front': 2,
                'middle': 2,
                'back': 4,
            },
            'engines': {
                'front': 2,
                'middle': 2,
                'back': 4,
            },
            'shields': [
                'front',
                'back',
                'front-left',
                'front-right',
                'back-left',
                'back-right'
            ],
            'addons': 12,
            'generators': 2,
        },
    }
