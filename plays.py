import sys
import pygame
import os

FPS = 60


def load_image(name, road, colorkey=None):
    fullname = os.path.join(road, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_it((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, pos_x, pos_y):
        self.tile = tile.split(';')
        if self.tile[0] == 'Grass':
            super().__init__(all_sprites, tile_group)
            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x, 25 * pos_y
        if self.tile[0] == 'Water':
            super().__init__(all_sprites, tile_group, d_group)
            self.image = load_image(f'Water_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Water')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x, 25 * pos_y

    def update(self, arg):
        if arg == 'step':
            if self.tile[0] == 'Grass':
                self.tile[1] = '1'
                self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
        if arg == 's_grow':
            if self.tile[0] == 'Grass':
                self.tile[1] = '0'
                self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')


def load_map(file):
    with open(file, 'r') as f:
        map_level = list(map(str.strip, f.readlines()))
    w = []
    for i in range(len(map_level)):
        map_level[i] = map_level[i].split()
        w.append(len(map_level[i]))
    w = max(w)
    h = len(map_level)
    return map_level, (w, h)


def set_map(map_level):
    for i in range(len(map_level[0])):
        for j in range(len(map_level[0][i])):
            Tile(map_level[0][i][j], j, i)


class Inventory:
    def __init__(self, file):
        ...


class Hero(pygame.sprite.Sprite):
    def __init__(self, v):
        super().__init__(all_sprites, hero_group)
        self.image = pygame.Surface((20, 45), pygame.SRCALPHA, 32)
        if v == 0:
            self.image = load_image('Character_00.png', 'Sprites/Hero/Character')
        elif v == 1:
            pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 20, 45))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 25, 25
        self.ori = 'r'

    def update(self, arg):
        if arg[0] == 'm':
            if arg[1] == 'u':
                self.rect.y -= 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.y += 1
                self.ori = 'u'
            elif arg[1] == 'l':
                self.rect.x -= 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.x += 1
                self.ori = 'l'
            elif arg[1] == 'd':
                self.rect.y += 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.y -= 1
                    self.ori = 'd'
            elif arg[1] == 'r':
                self.rect.x += 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.x -= 1
                    self.ori = 'r'


class NPC(Hero):
    ...


class Character(Hero):
    '''def __init__(self, v):
        def __init__(self, v):
            super(pygame.sprite.Sprite).__init__(all_sprites, hero_group)
            self.image = pygame.Surface((40, 60), pygame.SRCALPHA, 32)
            if v == 0:
                self.image = load_image('Character_00.png', 'Sprites/Hero/Character')
                self.rect = self.image.get_rect()
            elif v == 1:
                pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 40, 60))
                self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25, 25
            self.ori = 'r'''

    def update(self, arg):
        super().update(arg)
        if arg == 'da':
            pass


pygame.init()
all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
d_group = pygame.sprite.Group()
s_grow_event = pygame.USEREVENT + 1
pygame.time.set_timer(s_grow_event, 2500)
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
set_map(load_map('mapa.txt'))
character = Character(0)
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            hero_group.update('da')
        if event.type == s_grow_event:
            tile_group.update('s_grow')
    if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
        hero_group.update('mu')
    if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
        hero_group.update('ml')
    if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
        hero_group.update('md')
    if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
        hero_group.update('mr')
    hit_sprite = pygame.sprite.spritecollide(character, tile_group, False)
    for i in range(len(hit_sprite)):
        hit_sprite[i].update('step')

    screen.fill('white')
    tile_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
