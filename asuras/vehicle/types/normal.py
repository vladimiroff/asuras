from . import Vehicle

class Normal(Vehicle):
    weight = 1200
    inventory = 16
    dimenstions = (40, 70)
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
        'addons': 8,
        'generators': 1,
    }
