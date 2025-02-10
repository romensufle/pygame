import os
import sys

import random
import pygame_ui_toolkit

import pygame
from pygame.time import Clock

pygame.init()
pygame.display.set_caption('Joe HATES zombies')
size = width, height = 500, 620
screen_rect = (0, 0, width, height)
cowboy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
zombi_sprites = pygame.sprite.Group()
drum_sprites = pygame.sprite.Group()
buttons_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
broken_wall_sprites = pygame.sprite.Group()
field_sprites = pygame.sprite.Group()


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


class Start_Screen:
    def __init__(self):
        self.flag = True

    def fla(self):
        self.flag = False

    def start_screen(self):
        zast = pygame.display.set_mode((960, 540))
        fon = pygame.transform.scale(load_image('fon.png'), (960, 540))
        zast.blit(fon, (0, 0))

        btn1 = pygame_ui_toolkit.button.ImageButton(zast, 250, 450, 102, 102,
                                                    'data/btn1.png', on_click=lambda x: load_conditions(1))

        btn2 = pygame_ui_toolkit.button.ImageButton(zast, 450, 450, 102, 102,
                                                    'data/btn2.png', on_click=lambda x: load_conditions(2))

        btn3 = pygame_ui_toolkit.button.ImageButton(zast, 650, 450, 102, 102,
                                                    'data/btn3.png', on_click=lambda x: load_conditions(3))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                elif event.type == pygame.KEYDOWN or not self.flag:
                    return  # начинаем игру
            pygame.display.flip()
            btn1.update()
            btn2.update()
            btn3.update()


class End_Screen:
    def __init__(self):
        self.scor = 0

    def score(self, hard=1):
        self.scor += 100 * hard

    def ending(self):
        self.sc = str(self.scor)
        zast = pygame.display.set_mode((960, 540))
        fon = pygame.transform.scale(load_image('end_fon.png'), (960, 540))
        zast.blit(fon, (0, 0))
        font = pygame.font.Font(None, 36)
        text_coord = 313
        string_rendered = font.render(self.sc, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 409
        zast.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    start = Start_Screen
                    start.start_screen()
                    return  # начинаем игру

            pygame.display.flip()


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
    start = Start_Screen()
    start.fla()
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

    def update(self, *args, **kwargs):
        if pygame.sprite.groupcollide(cowboy_sprites, broken_wall_sprites, False, True):
            wall = Wall(wall_sprites, 'wall', self.rect.x // 100 + 1)



class Wall(pygame.sprite.Sprite):  # класс стены
    def __init__(self, group, w_gr, n):
        super().__init__(group)
        self.n = n

        self.image = load_image(f'walls/{w_gr}{n}.png')

        self.rect = self.image.get_rect().move((0 + 100 * (n - 1), 0))

    def broke(self, *args, **kwargs):
        pass


class Broken_Wall(pygame.sprite.Sprite):
    def __init__(self, group, w_gr, n):
        super().__init__(group)
        self.image = load_image(f'walls/{w_gr}{n}.png')

        self.rect = self.image.get_rect().move((0 + 100 * (n - 1), 0))

        print('work', n)


class Field(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(field_sprites)
        self.image = load_image('field.png')

        self.rect = self.image.get_rect().move((0, 130))


class Bullet(pygame.sprite.Sprite):  # класс пули
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(zombi_sprites)
        self.pos = 20
        self.n = random.randint(0, 4)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(self.pos + 100 * self.n, 620)

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
        if pygame.sprite.groupcollide(wall_sprites, zombi_sprites, True, True):
            wall = Broken_Wall(broken_wall_sprites, 'br_wall', self.n + 1)
        if pygame.sprite.groupcollide(broken_wall_sprites, zombi_sprites, False, False):
            end.ending()

    def realrealdead(self):  # зомби умирает
        end.score()
        #  звук смерти
        #  плюс очки


end = End_Screen()
start = Start_Screen()
start.start_screen()
screen = pygame.display.set_mode(size)
Joe = Cowboy(cowboy_sprites)
Field()
for n in range(5):
    wall = Wall(wall_sprites, 'wall', n + 1)

shot = Reload()
clock = Clock()
bullet_spid = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_spid, 3)  # скорость полёта пули

zombi_speed = pygame.USEREVENT + 2
pygame.time.set_timer(zombi_speed, int(50))  # скорость передвижения зомби / con[0]

zombi_spawn = pygame.USEREVENT + 3
pygame.time.set_timer(zombi_spawn, int(5000))  # скорость появления зомби / con[1]

running = True
re = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            cowboy_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and Joe.rect.left >= 100:
            Joe.rect.left -= 100
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and Joe.rect.right <= 400:
            Joe.rect.right += 100
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not re:  # выстрел
            pos = (Joe.rect.bottomleft[0] + 40, Joe.rect.bottomleft[1])
            bul = Bullet(bullet_sprites, pos)
            shot.shoot()
            if shot.drum <= 0:
                re = True
                drum = Drum(load_image("reload_drum.png"), 6, 2, 400, 400)
                k = 0
            # звук выстрела
        if event.type == bullet_spid:
            bullet_sprites.update()
        if event.type == zombi_speed:
            zombi_sprites.update()
        if event.type == zombi_spawn:
            Zombo = AnimatedSprite(load_image("zombi.png"), 4, 2)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q and re and k == 0:
            k = 1
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and re and k == 1:
            k = 2
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and re and k == 2:
            k = 3
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and re and k == 3:
            k = 4
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t and re and k == 4:
            k = 5
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_y and re and k == 5:
            k = 6
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1 and re and k == 6:
            k = 7
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2 and re and k == 7:
            k = 8
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3 and re and k == 8:
            k = 9
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_4 and re and k == 9:
            k = 10
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_5 and re and k == 10:
            k = 11
            drum_sprites.update()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_6 and re and k == 11:
            shot.drum = 6
            re = False
            drum.kill()

    screen.fill('#FFFFFF')

    wall_sprites.draw(screen)
    broken_wall_sprites.draw(screen)
    field_sprites.draw(screen)
    cowboy_sprites.draw(screen)
    bullet_sprites.draw(screen)
    zombi_sprites.draw(screen)
    drum_sprites.draw(screen)
    pygame.display.flip()
end.ending()
