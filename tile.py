import pygame
from settings import *

class Tile(pygame.sprite.Sprite): #essa classe vai adicionar a visible_sprites os sprites. Cada um com imagem e posicao
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))): # posição e sprite group a qual pertence
        super().__init__(groups)
        self.sprite_type = sprite_type # se é invisível, se é inimigo...
        self.image = surface
        if sprite_type == 'arvores':
            self.rect = self.image.get_rect(topleft=(pos[0],pos[1] - 2*TILESIZE))
            self.hitbox = self.rect.inflate(-30, -220)  # vai diminuir 5 pixels em cima e em baixo
            self.hitbox.height = 50
            print(self.hitbox.centery)
        elif sprite_type == 'grass':
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-20, -50)  # vai diminuir 5 pixels em cima e em baixo
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -20)  # vai diminuir 5 pixels em cima e em baixo
