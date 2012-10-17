import struct
import base64
import zlib

import pygame

from .cells import Cell

class LayerIterator:
    '''Iterates over all the cells in a layer in column,row order.  '''
    def __init__(self, layer):
        self.layer = layer
        self.i, self.j = 0, 0
    def __next__(self):
        if self.i == self.layer.width - 1:
            self.j += 1
            self.i = 0
        if self.j == self.layer.height - 1:
            raise StopIteration()
        value = self.layer[self.i, self.j]
        self.i += 1
        return value


class Layer:
    '''A 2d grid of Cells.

    Layers have some basic properties:

        width, height - the dimensions of the Layer in cells
        tile_width, tile_height - the dimensions of each cell
        px_width, px_height - the dimensions of the Layer in pixels
        tilesets - the tilesets used in this Layer (a Tilesets instance)
        properties - any properties set for this Layer
        cells - a dict of all the Cell instances for this Layer, keyed off
                (x, y) index.

    Additionally you may look up a cell using direct item access:

       layer[x, y] is layer.cells[x, y]

    Note that empty cells will be set to None instead of a Cell instance.
    '''
    def __init__(self, name, visible, map):
        self.name = name
        self.visible = visible
        self.position = (0, 0)
        # TODO get from TMX?
        self.px_width = map.px_width
        self.px_height = map.px_height
        self.tile_width = map.tile_width
        self.tile_height = map.tile_height
        self.width = map.width
        self.height = map.height
        self.tilesets = map.tilesets
        self.group = pygame.sprite.Group()
        self.properties = {}
        self.cells = {}
        self.view_x = 0
        self.view_y = 0
        self.view_w = 0
        self.view_h = 0

    def __repr__(self):
        return '<Layer "%s" at 0x%x>' % (self.name, id(self))

    def __getitem__(self, pos):
        return self.cells.get(pos)

    def __setitem__(self, pos, tile):
        x, y = pos
        px = x * self.tile_width
        py = y * self.tile_width
        self.cells[pos] = Cell(x, y, px, py, tile)

    def __iter__(self):
        return LayerIterator(self)

    @classmethod
    def fromxml(cls, tag, map):
        layer = cls(tag.attrib['name'], int(tag.attrib.get('visible', 1)), map)

        data = tag.find('data')
        if data is None:
            raise ValueError('layer %s does not contain <data>' % layer.name)

        data = data.text.strip()
        data = zlib.decompress(base64.decodebytes(data.encode()))
        data = struct.unpack('<%di' % (len(data)/4,), data)
        for i, gid in enumerate(data):
            if gid < 1:
                continue
            tile = map.tilesets[gid]
            x = i % layer.width
            y = i // layer.width
            layer.cells[x, y] = Cell(x, y, x*map.tile_width,
                                           y*map.tile_height, tile)

        return layer

    def update(self, dt, *args):
        pass

    def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
        self.view_x, self.view_y = x, y
        self.view_w, self.view_h = w, h
        x -= viewport_ox
        y -= viewport_oy
        self.position = (x, y)

    def draw(self, surface):
        '''Draw this layer, limited to the current viewport, to the Surface.
        '''
        ox, oy = self.position
        w, h = self.view_w, self.view_h
        for x in range(ox, ox+w+self.tile_width, self.tile_width):
            i = x // self.tile_width
            for y in range(oy, oy+h+self.tile_height, self.tile_height):
                j = y // self.tile_height
                if (i, j) not in self.cells:
                    continue
                cell = self.cells[i, j]
                if not 'animated' in cell.tile.properties:
                    surface.blit(cell.tile.surfaces[cell.tile.visible_surface], (cell.px-ox, cell.py-oy))
                else:
                    cell.tile.animation.draw(surface,(cell.px-ox, cell.py-oy))

    def find(self, *properties):
        '''Find all cells with the given properties set.
        '''
        r = []
        for propname in properties:
            for cell in self.cells.values():
                if cell and propname in cell:
                    r.append(cell)
        return r

    def match(self, **properties):
        '''Find all cells with the given properties set to the given values.
        '''
        r = []
        for propname in properties:
            for cell in self.cells.values():
                if propname not in cell:
                    continue
                if properties[propname] == cell[propname]:
                    r.append(cell)
        return r

    def collide(self, rect, propname):
        '''Find all cells the rect is touching that have the indicated property
        name set.
        '''
        r = []
        for cell in self.get_in_region(rect.left, rect.top,
                                       rect.right, rect.bottom):
            if not cell.intersects(rect):
                continue
            if propname in cell:
                r.append(cell)
        return r

    def get_in_region(self, x1, y1, x2, y2):
        '''Return cells (in [column][row]) that are within the map-space
        pixel bounds specified by the bottom-left (x1, y1) and top-right
        (x2, y2) corners.

        Return a list of Cell instances.
        '''
        i1 = max(0, x1 // self.tile_width)
        j1 = max(0, y1 // self.tile_height)
        i2 = min(self.width, x2 // self.tile_width + 1)
        j2 = min(self.height, y2 // self.tile_height + 1)
        return [self.cells[i, j]
            for i in range(int(i1), int(i2))
                for j in range(int(j1), int(j2))
                    if (i, j) in self.cells]

    def get_at(self, x, y):
        '''Return the cell at the nominated (x, y) coordinate.

        Return a Cell instance or None.
        '''
        i = x // self.tile_width
        j = y // self.tile_height
        return self.cells.get((i, j))

    def neighbors(self, index):
        '''Return the indexes of the valid (ie. within the map) cardinal (ie.
        North, South, East, West) neighbors of the nominated cell index.

        Returns a list of 2-tuple indexes.
        '''
        i, j = index
        n = []
        if i < self.width-1:
            n.append((i+1, j))
        if i > 0:
            n.append((i-1, j))
        if j < self.height-1:
            n.append((i, j+1))
        if j > 0:
            n.append((i, j-1))
        return n

class SpriteLayer(pygame.sprite.AbstractGroup):
    def __init__(self):
        super().__init__()
        self.visible = True
        self.view_x = 0
        self.view_y = 0
        self.view_w = 0
        self.view_h = 0
        self.position = (0, 0)

    def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
        self.view_x, self.view_y = x, y
        self.view_w, self.view_h = w, h
        x -= viewport_ox
        y -= viewport_oy
        self.position = (x, y)

    def draw(self, screen):
        ox, oy = self.position
        w, h = self.view_w, self.view_h
        for sprite in self.sprites():
            sx, sy = sprite.rect.topleft
            screen.blit(sprite.image, (sx-ox, sy-oy))

class Layers(list):
    def __init__(self):
        super().__init__()
        self.by_name = {}

    def add_named(self, layer, name):
        self.append(layer)
        self.by_name[name] = layer

    def __getitem__(self, item):
        if isinstance(item, int):
            return super().__getitem__(item)
        return self.by_name[item]

