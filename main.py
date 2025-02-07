import os
import sys

import random

import pygame
from pygame.time import Clock

pygame.init()
size = width, height = 500, 620
screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)
cowboy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
zombi_sprites = pygame.sprite.Group()
drum_sprites = pygame.sprite.Group()


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


def load_conditions(hard=1):
    sp_koef = 1
    spawn_sp_koef = 1
    xp_koef = 1
    if hard == 2:
        sp_koef = 1.25
        spawn_sp_koef = 2
        xp_koef = 2
        #  добавить сломанные стены
    elif hard == 3:
        sp_koef = 1.5
        spawn_sp_koef = 2.5
        xp_koef = 3
        #  добавить сломанные стены
    #  load_level(сюда какие стены сломаны)
    conditions = [sp_koef, spawn_sp_koef, xp_koef]
    return conditions


def load_level():
    pass


class Drum(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(drum_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(150, 120)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Cowboy(pygame.sprite.Sprite):  # класс ковбоя
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('cowboy.png')

        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):  #  класс пули
    size = (20, 20)

    def __init__(self, group, pos):
        super().__init__(group)
        self.image = load_image('bullet.png')

        self.rect = pygame.Rect(pos, Bullet.size)

    def update(self, *args, **kwargs):
        self.rect.top += 1
        if not self.rect.colliderect(screen_rect):
            self.kill()  # удаляет пулю, если она ушла за экран
        if pygame.sprite.groupcollide(bullet_sprites, zombi_sprites, True, True):
            Zombo.realrealdead()


class Reload():  # класс перезарядки
    def __init__(self):
        self.drum = 6


    def shoot(self):
        self.drum = self.drum - 1
        if self.drum <= 0:
            re = True
            while re is True:
                drum = Drum(load_image("reload_drum.png"), 6, 2, 400, 400)
                k = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.QUIT()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q and k == 0:
                        k = 1
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        k = 2
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_e and k == 2:
                        k = 3
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r and k == 3:
                        k = 4
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_t and k == 4:
                        k = 5
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_y and k == 5:
                        k = 6
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_1 and k == 6:
                        k = 7
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_2 and k == 7:
                        k = 8
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_3 and k == 8:
                        k = 9
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_4 and k == 9:
                        k = 10
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_5 and k == 10:
                        k = 11
                        drum_sprites.update()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_6 and k == 11:
                        k = 12
                    if k == 12:
                        self.drum = 6
                        pygame.QUIT()
                drum_sprites.draw(screen)
                pygame.display.flip()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(zombi_sprites)
        self.pos = 20
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(self.pos + 100 * random.randint(0, 4), 620)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):  # зомби двигается
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.rect.top -= 1

    def realrealdead(self):  # зомби умирает
        pass
        #  звук смерти
        #  плюс очки


Joe = Cowboy(cowboy_sprites)
shot = Reload()
con = load_conditions(3)
clock = pygame.time.Clock()

bullet_spid = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_spid, 10)  # скорость полёта пули

zombi_speed = pygame.USEREVENT + 2
pygame.time.set_timer(zombi_speed, int(50 / con[0]))  # скорость передвижения зомби

zombi_spawn = pygame.USEREVENT + 3
pygame.time.set_timer(zombi_spawn, int(5000 / con[1]))  # скорость появления зомби



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and Joe.rect.left >= 100:
            Joe.rect.left -= 100
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and Joe.rect.right <= 400:
            Joe.rect.right += 100
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # выстрел
            pos = (Joe.rect.bottomleft[0] + 40, Joe.rect.bottomleft[1])
            bul = Bullet(bullet_sprites, pos)
            shot.shoot()
            # звук выстрела
        if event.type == bullet_spid:
            bullet_sprites.update()
        if event.type == zombi_speed:
            zombi_sprites.update()
        if event.type == zombi_spawn:
            Zombo = AnimatedSprite(load_image("zombi.png"), 4, 2)

    screen.fill('#FFFFFF')
    cowboy_sprites.draw(screen)
    cowboy_sprites.update()
    bullet_sprites.draw(screen)
    zombi_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
#  end_screen(счёт)
