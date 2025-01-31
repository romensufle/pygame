import os
import sys

import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()

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
        self.image = load_image('cowboy — копия.png')

        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('bullet.png')

        self.rect = self.image.get_rect()


Joe = Cowboy(all_sprites)
bul = Bullet(all_sprites)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            Joe.rect.left -= 50
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            Joe.rect.right += 50



    screen.fill('#000000')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()