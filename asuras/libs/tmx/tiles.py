import sys
from xml.etree import ElementTree

import pygame

class Tile:
    def __init__(self, gid, surface, tileset):
        self.gid = gid
        self.surface = surface
        self.tile_width = tileset.tile_width
        self.tile_height = tileset.tile_height
        self.properties = {}

    @classmethod
    def from_surface(cls, surface):
        '''Create a new Tile object straight from a pygame Surface.

        Its tile_width and tile_height will be set using the Surface dimensions.
        Its gid will be 0.
        '''
        class TileSurface:
            tile_width, tile_height = surface.get_size()
        return cls(0, surface, TileSurface)

    def loadxml(self, tag):
        props = tag.find('properties')
        if props is None:
            return
        for c in props.findall('property'):
            # store additional properties.
            name = c.attrib['name']
            value = c.attrib['value']

            # TODO hax
            if value.isdigit():
                value = int(value)
            self.properties[name] = value

    def __repr__(self):
        return '<Tile %d>' % self.gid

class Tileset:
    def __init__(self, name, tile_width, tile_height, firstgid):
        self.name = name
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.firstgid = firstgid
        self.tiles = []
        self.properties = {}

    @classmethod
    def fromxml(cls, tag, firstgid=None):
        if 'source' in tag.attrib:
            firstgid = int(tag.attrib['firstgid'])
            with open(tag.attrib['source']) as f:
                tileset = ElementTree.fromstring(f.read())
            return cls.fromxml(tileset, firstgid)

        name = tag.attrib['name']
        if firstgid is None:
            firstgid = int(tag.attrib['firstgid'])
        tile_width = int(tag.attrib['tilewidth'])
        tile_height = int(tag.attrib['tileheight'])

        tileset = cls(name, tile_width, tile_height, firstgid)

        for c in tag.getchildren():
            if c.tag == "image":
                # create a tileset
                tileset.add_image(c.attrib['source'])
            elif c.tag == 'tile':
                gid = tileset.firstgid + int(c.attrib['id'])
                tileset.get_tile(gid).loadxml(c)
        return tileset

    def add_image(self, file):
        image = pygame.image.load(file).convert_alpha()
        if not image:
            sys.exit("Error creating new Tileset: file %s not found" % file)
        id = self.firstgid
        for line in range(int(image.get_height()/self.tile_height)):
            for column in range(int(image.get_width()/self.tile_width)):
                pos = pygame.Rect(column*self.tile_width,
                    line*self.tile_height,
                    self.tile_width,
                    self.tile_height )
                self.tiles.append(Tile(id, image.subsurface(pos), self))
                id += 1

    def get_tile(self, gid):
        return self.tiles[gid - self.firstgid]

class Tilesets(dict):
    def add(self, tileset):
        for i, tile in enumerate(tileset.tiles):
            i += tileset.firstgid
            self[i] = tile

