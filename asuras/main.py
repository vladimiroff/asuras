#!/usr/bin/env python
import pygame

class Game:
    sprites = pygame.sprite.Group()

    def main(self, screen):
        ''' The main loop '''
        clock = pygame.time.Clock()
        # wait David to figure out how to initialize the map

        while 1:
            dt = clock.tick(45)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.sprites.update(dt)
            screen.fill((239, 237, 236))
            self.sprites.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Asuras")
    Game().main(screen)
