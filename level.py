import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *

class Level:
    def __init__(self):
        # obter display surface
        self.display_surface = pygame.display.get_surface()
        # configuração de sprite setup
        # principal propósito de um grupo: armazenar, dar draw nos sprites e armazenar os sprites
        #self.visible_sprites = pygame.sprite.Group()

        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # configuração de sprite
        self.create_map()


    def create_map(self):
        layout = {
            'boundary': import_csv_layout('mapa/mapa1_CSV._Delimitador.csv')
        }
        for style, layout in layout.items(): #style é a key do layouts e e layout é o value de layouts
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
        self.player = Player((1595, 2200), [self.visible_sprites], self.obstacle_sprites)

        # for row_index, row in enumerate(WORLD_MAP):
        #     for col_index, col in enumerate(row):
        #         x = col_index * TILESIZE
        #         y = row_index * TILESIZE
        #         if col == 'x':
        #             Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)


    def run(self):
        #self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.rect.center)

class YsortCameraGroup(pygame.sprite.Group): # Ysort significa sortear as coordenadas
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        print(self.half_width)
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 100)

        # criando o chão
        self.floor_surf = pygame.image.load('mapa/mapa1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))


    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset  #adiciona-se o offset a tudo para que a câmera acompanhe o jogador
            self.display_surface.blit(sprite.image, offset_pos)
