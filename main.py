import os
import sys

import pygame
from pygame.time import Clock

pygame.init()
size = width, height = 500, 620
screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)
cowboy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Cowboy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('cowboy.png')

        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    size = (20, 20)

    def __init__(self, group, pos):
        super().__init__(group)
        self.image = load_image('bullet.png')

        self.rect = pygame.Rect(pos, Bullet.size)

    def update(self, *args, **kwargs):
        self.rect.top += 1
        if not self.rect.colliderect(screen_rect):
            self.kill()  # удаляет пулю, если она ушла за экран


Joe = Cowboy(cowboy_sprites)
clock = pygame.time.Clock()
bullet_spid = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_spid, 10)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            Joe.rect.left -= 100
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            Joe.rect.right += 100
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pos = (Joe.rect.bottomleft[0] + 40, Joe.rect.bottomleft[1])
            bul = Bullet(bullet_sprites, pos)
        if event.type == bullet_spid:
            bullet_sprites.update()

    screen.fill('#000000')
    cowboy_sprites.draw(screen)
    cowboy_sprites.update()
    bullet_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
