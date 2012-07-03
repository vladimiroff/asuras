from pygame import sprite

class Vehicle(sprite.Sprite):
    DEFAULTS = {
        'weight': 0,
        'inventory': 0,
        'dimenstion': 0,
        'slots': {},
    }
