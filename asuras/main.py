#!/usr/bin/env python
import ipdb
import pygame

from player import Player
from libs import tmx

class Game:
    running = True
    wireframe_mode = False
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
        self.items = tmx.layers.SpriteLayer()
        self.projectiles = tmx.layers.SpriteLayer()
        self.player = Player(self.items, self.sprites)
        self.tilemap.layers.append(self.sprites)
        self.tilemap.layers.append(self.projectiles)

        while self.running:
            time_delta = clock.tick(45)
            self.handle_keys()
            self.tilemap.set_focus(self.player.vehicle.rect.x, self.player.vehicle.rect.y)
            self.tilemap.update([arrow[1] for arrow in self.arrows], time_delta / 100, self.tilemap)
            screen.fill((239, 237, 236))
            self.tilemap.draw(screen)
            self.items.draw(screen)
            if self.wireframe_mode:
                self.draw_wireframe(screen, self.player.vehicle.near_obstacles,
                                            self.player.vehicle.collision_points)
            pygame.display.flip()

    def draw_wireframe(self, screen, objects, collisions):
        viewport_pos = self.tilemap.viewport
        for obj in collisions:
            pygame.draw.circle(screen, (255, 0, 0),
                (int(obj[0] - self.tilemap.viewport[0]),
                 int(obj[1] - self.tilemap.viewport[1])), 2, 2)
        for v_points in self.player.vehicle.points + self.player.vehicle.pivot_points:
            pygame.draw.circle(screen, (0, 255, 0), 
                (int(v_points[0] + self.player.vehicle.rect.center[0] - self.tilemap.viewport[0]),
                 int(v_points[1] + self.player.vehicle.rect.center[1] - self.tilemap.viewport[1])), 2, 2)
        for item in objects:
            previos_point = item.points[len(item.points) - 1]
            for point in item.points:
                pygame.draw.line(screen, (0, 0, 255), item.pos + previos_point - viewport_pos,
                                                      item.pos + point - viewport_pos)
                previos_point = point

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKQUOTE:
                    ipdb.set_trace()
                if event.key == pygame.K_TAB and event.type == pygame.KEYUP:
                    self.wireframe_mode = not self.wireframe_mode
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
        self.player.vehicle.fire(self.projectiles)

    def mouse_motion(self, buttons, pos, rel):
        self.player.vehicle._slots['weapons'][0].vriable_refresh(pos, self.player.vehicle.position, self.tilemap.viewport)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Asuras")
    try:
        Game().main(pygame.display.set_mode((1000, 600)))
    except Exception as e:
            import os, sys, traceback
            print(traceback.format_exc())
            if sys.platform == 'win32':
                os.system('pause')
