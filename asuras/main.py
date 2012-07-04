#!/usr/bin/env python
import pygame

from player import Player

class Game:
    sprites = pygame.sprite.Group()
    running = True
    pressed_arrows = [False, False, False, False]

    def main(self, screen):
        ''' The main loop '''
        clock = pygame.time.Clock()
        Player(self.sprites)
        # wait David to figure out how to initialize the map

        while self.running:
            dt = clock.tick(45)

            self.handle_keys()
            self.sprites.update(self.pressed_arrows)
            screen.fill((239, 237, 236))
            self.sprites.draw(screen)
            pygame.display.flip()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.key_down(event.key)
            elif event.type == pygame.KEYUP:
                self.key_up(event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up(event.button, event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_motion(event.buttons, event.pos, event.rel)

    def key_down(self, key):
        if key == pygame.K_w:
            self.pressed_arrows[0] = True
        if key == pygame.K_a:
            self.pressed_arrows[1] = True
        if key == pygame.K_s:
            self.pressed_arrows[2] = True
        if key == pygame.K_d:
            self.pressed_arrows[3] = True

    def key_up(self, key):
        if key == pygame.K_w:
            self.pressed_arrows[0] = False
        if key == pygame.K_a:
            self.pressed_arrows[1] = False
        if key == pygame.K_s:
            self.pressed_arrows[2] = False
        if key == pygame.K_d:
            self.pressed_arrows[3] = False

    def mouse_up(self, button, pos):
        pass

    def mouse_motion(self, buttons, pos, rel):
        pass

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Asuras")
    Game().main(screen)
