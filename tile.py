import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, color, screen):
        super().__init__()

        self.screen = screen
        self.image = pygame.Surface([8, 8])
        self.image.set_colorkey( color)
        self.image.fill((0,0,0))
        pygame.draw.rect(self.image, color ,pygame.Rect(0, 0, 8, 8))
        self.rect = self.image.get_rect()

        # self.image = tile
        # self.image.set_colorkey(color)




