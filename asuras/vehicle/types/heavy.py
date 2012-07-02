from . import Vehicle

class Heavy(Vehicle):
    weight = 3400
    inventory = 30
    dimenstions = (60, 80)
    slots = {
        'motions': {
            'front': 2,
            'middle': 2,
            'back': 2,
        },
        'engines': {
            'front': 2,
            'middle': 2,
            'back': 2,
        },
        'shields': ['front', 'back', 'left', 'right'],
        'addons': 12,
        'generators': 2,
    }