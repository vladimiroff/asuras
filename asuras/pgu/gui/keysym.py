"""
"""
import pygame
from pgu.gui import events, widget

class Keysym(widget.Widget):
    """A keysym input. This is deprecated and is scheduled to be removed from PGU."""

    _value = None

    def __init__(self,value=None,**params):
        params.setdefault('cls','keysym')
        widget.Widget.__init__(self,**params)
        self.value = value
        
        self.font = self.style.font
        w,h = self.font.size("Right Super") #"Right Shift")
        self.style.width,self.style.height = w,h
        #self.rect.w=w+self.style.padding_left+self.style.padding_right
        #self.rect.h=h+self.style.padding_top+self.style.padding_bottom
    
    def event(self,e):
        used = None
        if e.type == events.FOCUS or e.type == events.BLUR: self.repaint()
        elif e.type == events.KEYDOWN:
            if e.key != events.K_TAB:
                self.value = e.key
                self.repaint()
                self.send(events.CHANGE)
                used = True
            next(self)
        self.pcls = ""
        if self.container.myfocus is self: self.pcls = "focus"
        return used
    
    def paint(self,s):
        r = pygame.rect.Rect(0,0,self.rect.w,self.rect.h)
        #render_box(s,self.style.background,r)
        if self.value == None: return
        name = ""
        for p in pygame.key.name(self.value).split(): name += p.capitalize()+" "
        #r.x = self.style.padding_left;
        #r.y = self.style.padding_bottom;
        s.blit(self.style.font.render(name, 1, self.style.color), r)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if (val != None):
            val = int(val)
        oldval = self._value
        self._value = val
        if (oldval != val):
            self.send(events.CHANGE)
            self.repaint()


