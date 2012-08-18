"""Basic widgets and various utility functions.
"""

import pygame

from pgu.gui import events, widget
from pgu.gui.errors import PguError


def parse_color(desc):
    ''' Turns a descriptive string or a tuple into a pygame color
    Because of a bug in pygame 1.8.1 we need to explicitly define the
    alpha value otherwise it will default to transparent.
    '''
    if (is_color(desc)):
        return desc
    elif desc and desc[0] == "#":
        if len(desc) == 7:
            desc += "FF"
    return pygame.Color(desc)


def is_color(col):
    ''' Determines if the given object is a pygame-compatible color or not
    In every version of pygame (up to 1.8.1 so far) will interpret
    a tuple as a color.
    '''
    if (type(col) == tuple or type(col) == list):
        return col
    if (hasattr(pygame, "Color") and type(pygame.Color) == type):
        return (isinstance(col, pygame.Color))
    return False


class Spacer(widget.Widget):
    """An invisible space widget."""

    def __init__(self, width, height, **params):
        params.setdefault('focusable', False)
        widget.Widget.__init__(self,  width=width, height=height, **params)


class Color(widget.Widget):
    """A widget that renders as a solid block of color.

    Note the color can be changed by setting the 'value' field, and the
    widget will automatically be repainted, eg:

        c = Color()
        c.value = (255,0,0)
        c.value = (0,255,0)

    """

    value = None

    def __init__(self, value=None, **params):
        params.setdefault('focusable', False)
        if value != None:
            params['value'] = value
        widget.Widget.__init__(self, **params)

    def paint(self, s):
        if hasattr(self, 'value') and is_color(self.value):
            s.fill(self.value)

class Label(widget.Widget):
    """A text label widget."""

    def __init__(self, value="", **params):
        params.setdefault('focusable', False)
        params.setdefault('cls', 'label')
        widget.Widget.__init__(self, **params)
        self.style.check("font")
        self.value = value
        self.style.width, self.style.height = self.font.size(self.value)

    def paint(self, s):
        """Renders the label onto the given surface in the upper-left corner"""
        s.blit(self.style.font.render(self.value, 1, self.style.color), (0, 0))

    def set_text(self, txt):
        """Set the text of this label.
        Signal to the application that we need
        to resize this widget is being sent
        """
        self.value = txt
        self.chsize()

    def set_font(self, font):
        """Set the font used to render this label.

        Obsolete: use label.font instead"""
        self.font = font

    def resize(self, width=None, height=None):
        ''' Calculate the size of the rendered text '''
        (self.style.width, self.style.height) = self.font.size(self.value)
        return (self.style.width, self.style.height)

    @property
    def font(self):
        return self.style.font

    @font.setter
    def font(self, font):
        ''' Signal to the application that we need a resize is being sent '''
        self.style.font = font
        self.chsize()


class Image(widget.Widget):
    '''An image widget.
    The constructor takes a file name or a pygame surface.
    '''

    def __init__(self, value, **params):
        params.setdefault('focusable', False)
        widget.Widget.__init__(self, **params)

        if isinstance(value,  str):
            value = pygame.image.load(value)
            if (not value):
                raise PguError("Cannot load the image '%s'" % value)

        initial_width, initial_height = value.get_width(), value.get_height()
        width, height = initial_width, initial_height
        style_width, style_height = self.style.width, self.style.height

        if style_width and not style_height:
            width, height = style_width, height * style_width / width
        elif style_height and not style_width:
            width, height = width * style_height / height, style_height
        elif style_width and style_height:
            width, height = style_width, style_height

        if (initial_width, initial_height) != (width, height):
            value = pygame.transform.scale(value, (width, height))
        self.style.width, self.style.height = width, height
        self.value = value

    def paint(self, screen):
        screen.blit(self.value, (0, 0))
