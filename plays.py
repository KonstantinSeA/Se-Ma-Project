import sys
import pygame


FPS = 60


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, pos_x, pos_y):
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        tile = tile.split(';')
        if tile[0] == 'Grass':
            super().__init__(all_sprites, tile_group)
            pygame.draw.rect(self.image, pygame.Color('green'), (0, 0, 50, 50))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 50 * pos_x, 50 * pos_y
        if tile[0] == 'Water':
            super().__init__(all_sprites, tile_group, d_group)
            pygame.draw.rect(self.image, pygame.Color('blue'), (0, 0, 50, 50))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 50 * pos_x, 50 * pos_y


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
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA, 32)
        if v == 0:
            pygame.draw.rect(self.image, pygame.Color('red'), (0, 0, 40, 60))
        elif v == 1:
            pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 40, 60))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 25, 25
        self.ori = 'r'
        self.inventory = Inventory('inva.txt')

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
        elif arg == 'da':
            pass


all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
d_group = pygame.sprite.Group()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
set_map(load_map('mapa.txt'))
hero = Hero(1)
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            hero_group.update('da')
    if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
        hero_group.update('mu')
    if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
        hero_group.update('ml')
    if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
        hero_group.update('md')
    if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
        hero_group.update('mr')
    screen.fill('white')
    tile_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
