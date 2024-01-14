import sys
import pygame
import os

FPS = 60
small_grow_tile = []


class Game:
    def __init__(self, save):
        self.save = save
        set_map(load_map(f'Saves/Save{self.save}/Map.txt'))
        with open(f'Saves/Save{self.save}/Save.txt', mode='r', encoding='utf-8') as save_file:
            data_lines = save_file.readlines()
        self.character = Character(0, f'Saves/Save{self.save}/Inv.txt')
        self.game_clock = GameClock(data_lines[2].split('; ')[0], data_lines[2].split('; ')[1])
        self.time_update = pygame.USEREVENT + 1
        pygame.time.set_timer(self.time_update, 7000)

    def next_day(self):
        pass


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
            super().__init__(all_sprites, tile_group, g_group)
            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 80, 25 * pos_y + 80
        if self.tile[0] == 'Water':
            super().__init__(all_sprites, tile_group, d_group)
            self.image = load_image(f'Water_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Water')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 80, 25 * pos_y + 80

    def update(self, arg):
        if (self.tile[0] == 'Grass' or self.tile[0] == 'Zemla' or
                self.tile[0] == 'Gradka') and arg == 'uws':
            self.tile[0] = 'Zemla'
            self.image = load_image('Zemla.jpg', 'Sprites')
            small_grow_tile.append([self, 6])
        if self.tile[0] == 'Zemla' and arg == 'sge':
            self.tile[0] = 'Grass'
            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
        if (self.tile[0] == 'Grass' or self.tile[0] == 'Zemla' or
                self.tile[0] == 'Gradka') and arg == 'uwh':
            self.tile[0] = 'Gradka'
            self.image = load_image('Gradka.jpg', 'Sprites')
            small_grow_tile.append([self, 24])


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


class Item(pygame.sprite.Sprite):
    def __init__(self, item_name, pos):
        super().__init__(all_sprites, menu_group)
        self.name, self.pos = item_name, pos
        self.image = load_image(f'{item_name}.png', f'Sprites/Items')
        self.rect = self.image.get_rect()
        if self.pos <= 5:
            self.rect.x, self.rect.y = 450 + 25 * self.pos, 55
        else:
            self.rect.x, self.rect.y = -50, -50

    def use(self, ori, pos):
        point = MyPoint(ori, pos)
        used_tile = pygame.sprite.spritecollide(point, all_sprites, False)
        if used_tile:
            if self.name == 'wood_shovel':
                used_tile[0].update('uws')
            elif self.name == 'wood_hoe':
                used_tile[0].update('uwh')
        point.kill()


class MyPoint(pygame.sprite.Sprite):
    def __init__(self, ori, pos):
        super().__init__(all_sprites, worked_group)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 1, 1))
        self.rect = self.image.get_rect()
        if ori == 'r':
            self.rect.x, self.rect.y = pos[0] + 35, pos[1] + 30
        elif ori == 'l':
            self.rect.x, self.rect.y = pos[0] - 15, pos[1] + 30
        elif ori == 'u':
            self.rect.x, self.rect.y = pos[0] + 10, pos[1] + 20
        elif ori == 'd':
            self.rect.x, self.rect.y = pos[0] + 10, pos[1] + 55


class Inventory:
    def __init__(self, file):
        self.items = []
        with open(file, mode='r', encoding='utf-8') as inventory_file:
            item_lines = list(map(str.rstrip, inventory_file.readlines()))
            for i in range(len(item_lines)):
                self.items.append(Item(item_lines[i], i))


class Hero(pygame.sprite.Sprite):
    def __init__(self, v):
        super().__init__(all_sprites, hero_group)
        self.image = pygame.Surface((20, 45), pygame.SRCALPHA, 32)
        if v == 0:
            self.image = load_image('Character_00.png', 'Sprites/Hero/Character')
        elif v == 1:
            pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 20, 45))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 400
        self.ori = 'r'

    def update(self, arg):
        if arg[0] == 'm':
            if arg[1] == 'u':
                self.ori = 'u'
                self.rect.y -= 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.y += 1
            elif arg[1] == 'l':
                self.ori = 'l'
                self.rect.x -= 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.x += 1
            elif arg[1] == 'd':
                self.ori = 'd'
                self.rect.y += 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.y -= 1
            elif arg[1] == 'r':
                self.ori = 'r'
                self.rect.x += 1
                if pygame.sprite.groupcollide(hero_group, d_group, False, False):
                    self.rect.x -= 1


class NPC(Hero):
    ...


class Character(Hero):
    def __init__(self, v, inv):
        super().__init__(v)
        self.inv = Inventory(inv)
        self.shoosed_item = 1

    def update(self, arg):
        super().update(arg)
        if arg == 'da':
            self.inv.items[self.shoosed_item - 1].use(self.ori, (self.rect.x, self.rect.y))
        elif arg == '1':
            self.shoosed_item = 1
        elif arg == '2':
            self.shoosed_item = 2
        elif arg == '3':
            self.shoosed_item = 3
        elif arg == '4':
            self.shoosed_item = 4
        elif arg == '5':
            self.shoosed_item = 5


class GameClock:
    def __init__(self, mounts, days):
        self.mounts, self.days, self.hours, self.minuts = mounts, days, 0, 0

    def time_update(self):
        self.minuts += 10
        self.hours += self.minuts // 60
        self.minuts %= 60
        for t in small_grow_tile:
            t[1] -= 1
            if t[1] == 0:
                t[0].update('sge')
                small_grow_tile.remove(t)

    def draw_time(self, screen):
        font = pygame.font.SysFont('Times New Roman', 15)
        text = font.render(f'Время: {self.hours}:{self.minuts}', False, (0, 0, 0))
        screen.blit(text, (80, 55))


class Camera:
    def __init__(self):
        self.dx, self.dy = 0, 0

    def appply(self, object):
        object.rect = object.rect.move(self.dx, self.dy)

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


pygame.init()
all_sprites = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
d_group = pygame.sprite.Group()
g_group = pygame.sprite.Group()
menu_group = pygame.sprite.Group()
worked_group = pygame.sprite.Group()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
game = Game('a')
clock = pygame.time.Clock()
running = True
camera = Camera()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            hero_group.update('da')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            hero_group.update('1')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            hero_group.update('2')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            hero_group.update('3')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            hero_group.update('4')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            hero_group.update('5')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            hero_group.update('5')
        if event.type == game.time_update:
            game.game_clock.time_update()
    if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
        hero_group.update('mu')
    if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
        hero_group.update('ml')
    if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
        hero_group.update('md')
    if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
        hero_group.update('mr')

    screen.fill('white')
    camera.update(game.character)
    camera.appply(game.character)
    for sprite in tile_group:
        camera.appply(sprite)
    tile_group.draw(screen)
    hero_group.draw(screen)
    game.game_clock.draw_time(screen)
    menu_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
