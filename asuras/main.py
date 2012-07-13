#!/usr/bin/env python
import pygame

from player import Player

class Game:
    sprites = pygame.sprite.Group()
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
        Player(self.sprites)
        # wait David to figure out how to initialize the map

        while self.running:
            time_delta = clock.tick(45)

            self.handle_keys()
            self.sprites.update([arrow[1] for arrow in self.arrows], time_delta / 100)
            screen.fill((239, 237, 236))
            self.sprites.draw(screen)
            pygame.display.flip()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
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
