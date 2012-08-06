''' Window and window layouts '''
from pygame import sprite, rect

class Cell:
    '''
    Each window has a box layout composed of cells.
    A cell has width, height and can contain not more than one (part of) widget
    '''
    weight = 90
    height = 20
    position = (0, 0)
    empty = True

    def __init__(self, position):
        self.position = position

class Layout(list):
    '''
    Implements the grid of cells
    '''
    def __init__(self, size=(0, 0)):
        for vertical_index in range(size[0]):
            self.append([])
            for horizontal_index in range(size[1]):
                self[vertical_index].append(Cell((horizontal_index, vertical_index)))

class Window(sprite.Sprite):
    '''
    Window implementation
    '''
    def __init__(self, position, size, layout_size, *groups):
       super().__init__(*groups)
       self.position = position
       self.rect = rect.Rect(position, size)
       self.layout = Layout(layout_size)

    def update(self):
        pass


