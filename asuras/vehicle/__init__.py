from pygame import sprite

class Vehicle(sprite.Sprite):
    DEFAULTS = {
        'weight': 0,
        'inventory': 0,
        'dimenstion': 0,
        'slots': {
            'motions': {
                'front': 0,
                'back': 0,
            },
            'engines': {
                'front': 0,
                'back': 0,
            },
            'shields': ['front', 'back', 'left', 'right'],
            'addons': 0,
            'generators': 0,
        },
    }
