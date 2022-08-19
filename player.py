import pygame
from settings import *
from flask import Flask, render_template, request, redirect
import pymysql

#carsales = Flask(__name__)

def connection():
    s = '' #Digitar o server(host) name
    d = 'game'
    u = '' #Digitar login user
    p = '' #Digitar o password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn

class Player(pygame.sprite.Sprite):
    def __init__(self, pos,groups, obstacle_sprites): # posição e sprite group a qual pertence
        super().__init__(groups)

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT roupa FROM Player where name = 'Kor'")

        self.image = pygame.image.load(f'imagens/jogador/{cursor.fetchone()[0]}/sprite_00.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26) # Faz com que se retire -13 superior e inferior da colisão
        self.direction = pygame.math.Vector2()
        self.speed = 5
        #self.walk_sand = pygame.mixer.Sound("sounds/sand_step2.mp3")

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0: # verifica se o vetor tem qualquer comprimento a mais
            # se mover na diagonal faz com que a velocidade dobre, dobrando o vetor
            self.direction = self.direction.normalize() # logo é necessário normalizar, fazendo ficar 1 vetor

        #self.rect.center += self.direction * speed
        #self.rect.x += self.direction.x * speed
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        # self.rect.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                #if sprite.rect.colliderect(self.rect):
                if sprite.hitbox.colliderect(self.hitbox): # checando o retangulo do sprite com o retangulo do player
                    if self.direction.x > 0:
                        #self.rect.right = sprite.rect.left
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)