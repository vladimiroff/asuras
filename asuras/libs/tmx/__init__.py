# "Tiled" TMX loader/renderer and more
# Copyright 2012 Richard Jones <richard@mechanicalcat.net>
# Modified by: Kiril Vladimirov <kiril@vladimiroff.org>
# This code is placed in the Public Domain.

# TODO: support properties on more things

import os
import pygame
from xml.etree import ElementTree

from .layers import Layer, Layers
from .tiles import Tileset, Tilesets


class TileMap:
    '''A TileMap is a collection of Layers which contain gridded maps or sprites
    which are drawn constrained by a viewport.

    And breathe.

    TileMaps are loaded from TMX files which sets the .layers and .tilesets
    properties. After loading additional SpriteLayers may be added.

    A TileMap's rendering is restricted by a viewport which is defined by the
    size passed in at construction time and the focus set by set_focus() or
    force_focus().

    TileMaps have a number of properties:

        width, height - the dimensions of the tilemap in cells
        tile_width, tile_height - the dimensions of the cells in the map
        px_width, px_height - the dimensions of the tilemap in pixels
        properties - any properties set on the tilemap in the TMX file
        layers - all layers of this tilemap as a Layers instance
        tilesets - all tilesets of this tilemap as a Tilesets instance
        fx, fy - viewport focus point
        view_w, view_h - viewport size
        view_x, view_y - viewport offset (origin)
        viewport - a pygame.Rect instance giving the current viewport specification

    '''
    def __init__(self, size, origin=(0, 0)):
        self.px_width = 0
        self.px_height = 0
        self.tile_width = 0
        self.tile_height = 0
        self.width = 0
        self.height  = 0
        self.properties = {}
        self.layers = Layers()
        self.tilesets = Tilesets()
        self.fx, self.fy = 0, 0             # viewport focus point
        self.view_w, self.view_h = size     # viewport size
        self.view_x, self.view_y = origin   # viewport offset
        self.viewport = pygame.Rect(origin, size)
        self.childs_ox = 0
        self.childs_oy = 0
        self.restricted_fx = 0
        self.restricted_fy = 0

    def update(self, dt, *args):
        for layer in self.layers:
            layer.update(dt, *args)

    def draw(self, screen):
        for layer in self.layers:
            if layer.visible:
                layer.draw(screen)

    @classmethod
    def load(cls, filename, viewport):
        with open(filename) as f:
            map = ElementTree.fromstring(f.read())

        tilemap = TileMap(viewport)
        tilemap.width = int(map.attrib['width'])
        tilemap.height  = int(map.attrib['height'])
        tilemap.tile_width = int(map.attrib['tilewidth'])
        tilemap.tile_height = int(map.attrib['tileheight'])
        tilemap.px_width = tilemap.width * tilemap.tile_width
        tilemap.px_height = tilemap.height * tilemap.tile_height
        tilemap.path = os.path.abspath(os.path.dirname(filename))

        for tag in map.findall('tileset'):
            tilemap.tilesets.add(Tileset.fromxml(tag, base_path=tilemap.path))

        for tag in map.findall('layer'):
            layer = Layer.fromxml(tag, tilemap)
            tilemap.layers.add_named(layer, layer.name)

        return tilemap

    _old_focus = None
    def set_focus(self, fx, fy, force=False):
        '''Determine the viewport based on a desired focus pixel in the
        Layer space (fx, fy) and honoring any bounding restrictions of
        child layers.

        The focus will always be shifted to ensure no child layers display
        out-of-bounds data, as defined by their dimensions px_width and px_height.
        '''
        # The result is that all chilren will have their viewport set, defining
        # which of their pixels should be visible.
        fx, fy = int(fx), int(fy)
        self.fx, self.fy = fx, fy

        a = (fx, fy)

        # check for NOOP (same arg passed in)
        if not force and self._old_focus == a:
            return
        self._old_focus = a

        # get our viewport information, scaled as appropriate
        w = int(self.view_w)
        h = int(self.view_h)
        w2, h2 = w//2, h//2

        if self.px_width <= w:
            # this branch for centered view and no view jump when
            # crossing the center; both when world width <= view width
            restricted_fx = self.px_width / 2
        else:
            if (fx - w2) < 0:
                restricted_fx = w2       # hit minimum X extent
            elif (fx + w2) > self.px_width:
                restricted_fx = self.px_width - w2       # hit maximum X extent
            else:
                restricted_fx = fx
        if self.px_height <= h:
            # this branch for centered view and no view jump when
            # crossing the center; both when world height <= view height
            restricted_fy = self.px_height / 2
        else:
            if (fy - h2) < 0:
                restricted_fy = h2       # hit minimum Y extent
            elif (fy + h2) > self.px_height:
                restricted_fy = self.px_height - h2       # hit maximum Y extent
            else:
                restricted_fy = fy

        # ... and this is our focus point, center of screen
        self.restricted_fx = int(restricted_fx)
        self.restricted_fy = int(restricted_fy)

        # determine child view bounds to match that focus point
        x, y = int(restricted_fx - w2), int(restricted_fy - h2)
        self.viewport.x = x
        self.viewport.y = y

        self.childs_ox = x - self.view_x
        self.childs_oy = y - self.view_y

        for layer in self.layers:
            layer.set_view(x, y, w, h, self.view_x, self.view_y)

    def force_focus(self, fx, fy):
        '''Force the manager to focus on a point, regardless of any managed 
        layer visible boundaries.
        '''
        # This calculation takes into account the scaling of this Layer (and
        # therefore also its children).
        # The result is that all chilren will have their viewport set, defining
        # which of their pixels should be visible.
        self.fx, self.fy = map(int, (fx, fy))
        self.fx, self.fy = fx, fy

        # get our view size
        w = int(self.view_w)
        h = int(self.view_h)
        w2, h2 = w//2, h//2

        # bottom-left corner of the viewport
        x, y = fx - w2, fy - h2
        self.viewport.x = x
        self.viewport.y = y

        self.childs_ox = x - self.view_x
        self.childs_oy = y - self.view_y

        for layer in self.layers:
            layer.set_view(x, y, w, h, self.view_x, self.view_y)

    def pixel_from_screen(self, x, y):
        '''Look up the Layer-space pixel matching the screen-space pixel.
        '''
        vx, vy = self.childs_ox, self.childs_oy
        return int(vx + x), int(vy + y)

    def pixel_to_screen(self, x, y):
        '''Look up the screen-space pixel matching the Layer-space pixel.
        '''
        screen_x = x-self.childs_ox
        screen_y = y-self.childs_oy
        return int(screen_x), int(screen_y)

    def index_at(self, x, y):
        '''Return the map index at the (screen-space) pixel position.
        '''
        sx, sy = self.pixel_from_screen(x, y)
        return int(sx//self.tile_width), int(sy//self.tile_height)

def load(filename, viewport):
    return TileMap.load(filename, viewport)
