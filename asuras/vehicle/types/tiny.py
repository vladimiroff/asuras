from . import Vehicle

class Tiny(Vehicle):
    weight = 600
    inventory = 4
    dimenstions = (20, 60)
    slots = {
        'motions': {
            'front': 2,
            'back': 2,
        },
        'engines': {
            'front': 2,
            'back': 2,
        },
        'shields': ['front', 'back', 'left', 'right'],
        'addons': 2,
        'generators': 1,
    }
