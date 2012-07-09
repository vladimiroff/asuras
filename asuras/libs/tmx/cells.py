class Cell:
    '''Layers are made of Cells (or empty space).

    Cells have some basic properties:

    x, y - the cell's index in the layer
    px, py - the cell's pixel position
    left, right, top, bottom - the cell's pixel boundaries

    Additionally the cell may have other properties which are accessed using
    standard dictionary methods:

       cell['property name']

    You may assign a new value for a property to or even delete an existing
    property from the cell - this will not affect the Tile or any other Cells
    using the Cell's Tile.
    '''
    def __init__(self, x, y, px, py, tile):
        self.x, self.y = x, y
        self.px, self.py = px, py
        self.tile = tile
        self.topleft = (px, py)
        self.left = px
        self.right = px + tile.tile_width
        self.top = py
        self.bottom = py + tile.tile_height
        self.center = (px + tile.tile_width//2, py + tile.tile_height//2)
        self._added_properties = {}
        self._deleted_properties = set()
    def __repr__(self):
        return '<Cell %s,%s %d>' % (self.px, self.py, self.tile.gid)
    def __contains__(self, key):
        if key in self._deleted_properties:
            return False
        return key in self._added_properties or key in self.tile.properties
    def __getitem__(self, key):
        if key in self._deleted_properties:
            raise KeyError(key)
        if key in self._added_properties:
            return self._added_properties[key]
        if key in self.tile.properties:
            return self.tile.properties[key]
        raise KeyError(key)
    def __setitem__(self, key, value):
        self._added_properties[key] = value
    def __delitem__(self, key):
        self._deleted_properties.add(key)
    def intersects(self, other):
        '''Determine whether this Cell intersects with the other rect (which has
        .x, .y, .width and .height attributes.)
        '''
        if self.px + self.tile.tile_width < other.x:
            return False
        if other.x + other.width < self.px:
            return False
        if self.py + self.tile.tile_height < other.y:
            return False
        if other.y + other.height < self.py:
            return False
        return True

