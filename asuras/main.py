#!/usr/bin/env python
import ipdb
import pygame

from player import Player
from libs import tmx

class Game:
    running = True
    arrows = [
        [pygame.K_w, False],
        [pygame.K_a, False],
        [pygame.K_s, False],
        [pygame.K_d, False],
    ]

    def main(self, screen):
        ''' The main loop '''
        clock = pygame.time.Clock()
        self.tilemap = tmx.load('resources/maps/test1.tmx', screen.get_size())
        self.sprites = tmx.layers.SpriteLayer()
        self.player = Player(self.sprites)
        self.tilemap.layers.append(self.sprites)

        while self.running:
            time_delta = clock.tick(45)
            self.handle_keys()
            self.tilemap.update([arrow[1] for arrow in self.arrows], time_delta / 100, self.tilemap)
            self.tilemap.set_focus(self.player.vehicle.rect.x, self.player.vehicle.rect.y)
            screen.fill((239, 237, 236))
            self.tilemap.draw(screen)
            self.draw(screen, self.player.vehicle.draw_me)
            pygame.display.flip()

    def draw(self, screen, objects):#Debugging purpouse
        for obj in objects:
            pygame.draw.circle(screen, (255, 0, 0), (int(obj[0] - self.tilemap.viewport[0]),int(obj[1] - self.tilemap.viewport[1])), 2, 2)
        for v_points in self.player.vehicle.points:
            pygame.draw.circle(screen, (255, 0, 0), (int(v_points[0] + self.player.vehicle.rect.center[0] - self.tilemap.viewport[0]),int(v_points[1] + self.player.vehicle.rect.center[1] - self.tilemap.viewport[1])), 2, 2)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKQUOTE:
                    ipdb.set_trace()
                self.set_pressed_arrows(event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up(event.button, event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_motion(event.buttons, event.pos, event.rel)

    def set_pressed_arrows(self, key):
        for i, (arrow, is_pressed) in enumerate(self.arrows):
            if key == arrow:
                self.arrows[i][1] = not is_pressed

    def mouse_up(self, button, pos):
        pass

    def mouse_motion(self, buttons, pos, rel):
        pass

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Asuras")
    Game().main(pygame.display.set_mode((1200, 800)))
