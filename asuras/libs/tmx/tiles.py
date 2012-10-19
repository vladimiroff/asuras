import os
import sys
import glob
from xml.etree import ElementTree

import pygame

class Animation:
    ''' Visualisation of entity. '''
    def __init__(self):
        self.frames = []
        self.curframe = 0
        self.maxframe = 0
        self.timer = 0
    
    def setup(self, folder):
        ''' Goes in the given folder and takes all the framse in order to visualise them later. '''
        tempimages = glob.glob("resources/animations/" + folder + "/frame*.png")
        tempimages.sort()
        for i in range(len(tempimages)):        
            self.frames.append(pygame.image.load(tempimages[i]))
        self.maxframe = len(self.frames) - 1
 
    def draw(self, screen, pos):
        ''' Draw curent frame and move to the next one. '''
        screen.blit(self.frames[self.curframe], pos)
        
        if self.curframe == self.maxframe:
            self.curframe = 0
        else:
            if self.timer == 4:
                self.curframe += 1
                self.timer = 0
            else:
                self.timer += 1

class Tile:
    def __init__(self, gid, surface, tileset):
        self.gid = gid
        self.surface = surface
        self.tile_width = tileset.tile_width
        self.tile_height = tileset.tile_height
        self.properties = {}
        self.visible_surface = 0
        self.surfaces = [surface]
        self.health = -1

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
            if name == 'animated':
                self.animation = Animation()
                self.animation.setup(value)
            elif name == 'building':
                '''
                    building type nz dali shte se polzva no vse pak mislq che shte e nujno i go dobavqm
                '''
                self.building_type = value
            elif name == 'health':
                self.health = value

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
    def fromxml(cls, tag, firstgid=None, base_path=''):
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
                tileset.add_image(os.path.join(base_path, c.attrib['source']))
                damaged_images = glob.glob("resources/maps/DamageStates/state*.png")
                damaged_images.sort()
                for image in damaged_images:        
                    tileset.add_sub_image(pygame.image.load(image).convert_alpha())
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

    def add_sub_image(self, input_image):
        '''
            Dobavq damaged images kato izpolzva loading image algoritama
            no dobavq otdelnite damage images v strukturata na tilea
        '''
        image = input_image
        if not image:
            sys.exit("Error creating new Tileset: file %s not found" % file)
        position = 0
        for line in range(int(image.get_height()/self.tile_height)):
            for column in range(int(image.get_width()/self.tile_width)):
                pos = pygame.Rect(column*self.tile_width,
                    line*self.tile_height,
                    self.tile_width,
                    self.tile_height )
                self.tiles[position].surfaces.append(image.subsurface(pos))
                position += 1


    def get_tile(self, gid):
        return self.tiles[gid - self.firstgid]

class Tilesets(dict):
    def add(self, tileset):
        for i, tile in enumerate(tileset.tiles):
            i += tileset.firstgid
            self[i] = tile

