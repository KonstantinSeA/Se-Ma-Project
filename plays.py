import sys
import pygame
import os

FPS = 60
small_grow_tile = []


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
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, pos_x, pos_y):
        self.tile = tile.split(';')
        if self.tile[0] == 'Grass':
            super().__init__(game.all_sprites, game.tile_group, game.g_group)
            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
        elif self.tile[0] == 'Water':
            super().__init__(game.all_sprites, game.tile_group, game.d_group)
            self.image = load_image(f'Water_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Water')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 80, 25 * pos_y + 80
        elif self.tile[0] == 'Stump':
            super().__init__(game.all_sprites, game.tile_group, game.d_mask_group)
            self.image = load_image(f'Stump_mask.png', 'Sprites/Wood')
            self.mask = pygame.mask.from_surface(self.image)
            self.image = load_image(f'Stump.png', 'Sprites/Wood')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.hp = 10
        elif self.tile[0] == 'Tree':
            super().__init__(game.all_sprites, game.tile_group,
                             game.d_mask_group, game.walked_group)
            self.image = load_image(f'Tree_mask.png', 'Sprites/Wood')
            self.mask = pygame.mask.from_surface(self.image)
            self.image = load_image(f'TreeUp.png', 'Sprites/Wood')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 80 - 35, 25 * pos_y + 80 - 30
            self.sub = SubTile(25 * pos_x + 80 - 35, 25 * pos_y + 80 - 30, 'td')
            self.hp = 15

    def update(self, arg):
        if (self.tile[0] == 'Grass' or self.tile[0] == 'Zemla' or
                self.tile[0] == 'Gradka') and arg == 'uws':
            self.tile[0] = 'Zemla'
            self.image = load_image('Zemla.jpg', 'Sprites')
            small_grow_tile.append([self, 6])
        elif self.tile[0] == 'Zemla' and arg == 'sge':
            self.tile[0] = 'Grass'
            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
        elif (self.tile[0] == 'Grass' or self.tile[0] == 'Zemla' or
                self.tile[0] == 'Gradka') and arg == 'uwh':
            self.tile[0] = 'Gradka'
            self.image = load_image('Gradka.jpg', 'Sprites')
            small_grow_tile.append([self, 24])
        elif self.tile[0] == 'Tree':
            if arg == 'ua':
                self.hp -= 1
            elif arg == 'uia':
                self.hp -= 2
            elif arg == 'uga':
                self.hp -= 3
            elif arg == 'uira':
                self.hp -= 5
            if self.hp < 1:
                self.sub.kill()
                x, y = self.rect.x, self.rect.y
                self.kill()
                self.tile[0] = 'Stump'
                super().__init__(game.all_sprites, game.tile_group, game.d_mask_group)
                self.image = load_image(f'Stump_mask.png', 'Sprites/Wood')
                self.mask = pygame.mask.from_surface(self.image)
                self.image = load_image(f'Stump.png', 'Sprites/Wood')
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = x + 30,  y + 90
                self.hp = 10


class SubTile(pygame.sprite.Sprite):
    def __init__(self, x, y, arg):
        if arg == 'td':
            super().__init__(game.all_sprites, game.tile_group)
            self.image = load_image('TreeDown.png', 'Sprites/Wood')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y


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
        super().__init__(game.all_sprites, game.menu_group)
        self.name, self.pos = item_name, pos
        self.image = load_image(f'{item_name}.png', f'Sprites/Items')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 218 + 48 * self.pos, 758

    def use(self, ori, pos):
        point = MyPoint(ori, pos)
        game.camera.appply(point)
        used_tile = pygame.sprite.spritecollide(point, game.all_sprites, False)
        if used_tile:
            if self.name == 'wood_shovel':
                used_tile[1].update('uws')
            elif self.name == 'wood_hoe':
                used_tile[1].update('uwh')
            elif self.name == 'Axe':
                used_tile[1].update('ua')
            elif self.name == 'Iron_Axe':
                used_tile[1].update('uia')
            elif self.name == 'Gold_Axe':
                used_tile[1].update('uga')
            elif self.name == 'Ir_Axe':
                used_tile[1].update('uira')
        point.kill()


class MyPoint(pygame.sprite.Sprite):
    def __init__(self, ori, pos):
        super().__init__(game.all_sprites, game.worked_group)
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


class Inventory(pygame.sprite.Sprite):
    def __init__(self, file):
        super().__init__(game.all_sprites, game.menu_group)
        self.items = []
        with open(file, mode='r', encoding='utf-8') as inventory_file:
            item_lines = list(map(str.rstrip, inventory_file.readlines()))
            for i in range(len(item_lines)):
                self.items.append(Item(item_lines[i], i))
        self.choosed = 1
        self.image = load_image('InvC1.png', 'Sprites/Inv')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 200, 739

    def update(self, arg):
        if arg == 'da':
            self.items[self.choosed - 1].use(game.character.ori,
                                             (game.character.rect.x, game.character.rect.y))
        elif arg == '1':
            self.image = load_image('InvC1.png', 'Sprites/Inv')
            self.choosed = 1
        elif arg == '2':
            self.image = load_image('InvC2.png', 'Sprites/Inv')
            self.choosed = 2
        elif arg == '3':
            self.image = load_image('InvC3.png', 'Sprites/Inv')
            self.choosed = 3
        elif arg == '4':
            self.image = load_image('InvC4.png', 'Sprites/Inv')
            self.choosed = 4
        elif arg == '5':
            self.image = load_image('InvC5.png', 'Sprites/Inv')
            self.choosed = 5
        elif arg == '6':
            self.image = load_image('InvC6.png', 'Sprites/Inv')
            self.choosed = 6
        elif arg == '7':
            self.image = load_image('InvC7.png', 'Sprites/Inv')
            self.choosed = 7
        elif arg == '8':
            self.image = load_image('InvC8.png', 'Sprites/Inv')
            self.choosed = 8
        elif arg == '9':
            self.image = load_image('InvC9.png', 'Sprites/Inv')
            self.choosed = 9
        elif arg == '10':
            self.image = load_image('InvC10.png', 'Sprites/Inv')
            self.choosed = 10
        elif arg == '11':
            self.image = load_image('InvC11.png', 'Sprites/Inv')
            self.choosed = 11
        elif arg == '12':
            self.image = load_image('InvC12.png', 'Sprites/Inv')
            self.choosed = 12


class EnergyBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_sprites, game.menu_group)
        self.energy = 35
        self.image = load_image('EnergyBar4.png', 'Sprites/EnergyBar')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 940, 500

    def enable(self):
        if self.energy > 0:
            return True
        return False

    def update(self):
        self.energy -= 1
        if 15 <= self.energy < 25:
            self.image = load_image('EnergyBar3.png', 'Sprites/EnergyBar')
        elif 5 <= self.energy < 15:
            self.image = load_image('EnergyBar2.png', 'Sprites/EnergyBar')
        elif self.energy < 5:
            self.image = load_image('EnergyBar1.png', 'Sprites/EnergyBar')


class Hero(pygame.sprite.Sprite):
    def __init__(self, v, inv):
        super().__init__(game.all_sprites, game.hero_group)
        self.image = pygame.Surface((20, 45), pygame.SRCALPHA, 32)
        if v == 0:
            self.image = load_image('Character_00.png', 'Sprites/Hero/Character')
        elif v == 1:
            pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 20, 45))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 400
        self.absolute_x, self.absolute_y = 500, 400
        self.ori = 'r'
        self.inv = Inventory(inv)
        self.enb = EnergyBar()
        self.boots = HeroBoots(self)

    def update(self, arg):
        if arg[0] == 'm':
            if self.enb.enable():
                m = 5
            else:
                m = 2
            if arg[1] == 'u':
                self.ori = 'u'
                self.rect.y -= m
                self.absolute_y -= m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.y += m
                    self.absolute_y += m
            elif arg[1] == 'l':
                self.ori = 'l'
                self.rect.x -= m
                self.absolute_x -= m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.x += m
                    self.absolute_x += m
            elif arg[1] == 'd':
                self.ori = 'd'
                self.rect.y += m
                self.absolute_y += m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.y -= m
                    self.absolute_y -= m
            elif arg[1] == 'r':
                self.ori = 'r'
                self.rect.x += m
                self.absolute_x += m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.x -= m
                    self.absolute_x -= m
        elif arg == 'da' and self.enb.enable():
            self.inv.update('da')
            self.enb.update()
        print(self.rect.x, self.rect.y, '----', self.absolute_x, self.absolute_y)
        if pygame.sprite.spritecollideany(self.boots, game.home_t_group):
            game.run_type = 'home'
            self.rect.x, self.rect.y = 421, 380
        self.boots.update(self)


def mask_collide(sprite, sprite_group):
    for s in sprite_group:
        if pygame.sprite.collide_mask(sprite, s):
            return True
    return False


class HeroBoots(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__(game.all_sprites, game.hero_boots_group)
        self.image = pygame.Surface((20, 15), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 20, 15))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = hero.rect.x, hero.rect.y + 30
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, hero):
        self.rect.x, self.rect.y = hero.rect.x, hero.rect.y + 30


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
        self.absolute_x, self.absolute_y = 0, 0

    def appply(self, obj):
        if 500 < self.absolute_x < 760 and 400 < self.absolute_y < 610:
            obj.rect = obj.rect.move(self.dx, self.dy)
        elif 500 < self.absolute_x < 760:
            obj.rect = obj.rect.move(self.dx, 0)
        elif 400 < self.absolute_y < 610:
            obj.rect = obj.rect.move(0, self.dy)

    def update(self, target):
        self.dx = game.width // 2 - target.rect.x - target.rect.w // 2
        self.dy = game.height // 2 - target.rect.y - target.rect.h // 2
        self.absolute_x, self.absolute_y = target.absolute_x, target.absolute_y


class FonWall(pygame.sprite.Sprite):
    def __init__(self, t):
        super().__init__(game.all_sprites, game.d_group, game.wall_group)
        if t == 'l':
            self.image = pygame.Surface((45, 1400), pygame.SRCALPHA, 32)
            pygame.draw.line(self.image, 'red', (0, 0), (0, 1400), 45)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 0, 0
        if t == 'r':
            self.image = pygame.Surface((45, 1400), pygame.SRCALPHA, 32)
            pygame.draw.line(self.image, 'red', (0, 0), (0, 1400), 45)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 1240, 0
        if t == 'u':
            self.image = pygame.Surface((1400, 125), pygame.SRCALPHA, 32)
            pygame.draw.line(self.image, 'red', (0, 0), (1400, 0), 125)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 0, 0
        if t == 'd':
            self.image = pygame.Surface((1400, 5), pygame.SRCALPHA, 32)
            pygame.draw.line(self.image, 'red', (0, 0), (1400, 0), 5)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 0, 1005
        if t == 'vu':
            self.image = pygame.Surface((600, 150), pygame.SRCALPHA, 32)
            pygame.draw.line(self.image, 'red', (0, 0), (600, 0), 150)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 800, 0


class Fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group)
        self.image = load_image(f'Farm_Fon.png', 'Sprites')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        FonWall('l')
        FonWall('r')
        FonWall('u')
        FonWall('d')
        FonWall('vu')


class Home:
    def __init__(self):
        self.roof = HomeRoof()
        self.wall = HomeWall()
        self.terrace = HomeTerrace()
        self.mat = HomeMat()
        self.in_fon = InHomeFon()
        self.in_border = InHomeFonBorders()
        self.in_moved = InHomeMoved()


class HomeRoof(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.walked_group)
        self.image = load_image(f'Home_Roof.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 355


class HomeMat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.home_t_group)
        self.image = load_image(f'Home_Mat.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 910, 507


class HomeTerrace(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group)
        self.image = load_image(f'Home_Terrace.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 801, 505


class HomeWall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.d_mask_group)
        self.image = load_image(f'Home_Wall.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 355
        self.mask = pygame.mask.from_surface(self.image)


class InHomeFon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_home_sprites)
        self.image = load_image(f'InHome_Fon.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 350, 139


class InHomeMoved(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.moved_home_sprites)
        self.image = load_image(f'InHome_Moved.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 350, 139


class InHomeFonBorders(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game.all_home_sprites)
        self.image = load_image(f'InHome_Border.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 350, 139


class Game:
    def __init__(self, save):
        self.save = save

    def next_day(self):
        pass

    def run(self):
        while self.running:
            if self.run_type == 'farm':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                        self.hero_group.update('da')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                        self.character.inv.update('1')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                        self.character.inv.update('2')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                        self.character.inv.update('3')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                        self.character.inv.update('4')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                        self.character.inv.update('5')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                        self.character.inv.update('6')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                        self.character.inv.update('7')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                        self.character.inv.update('8')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                        self.character.inv.update('9')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                        self.character.inv.update('10')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                        self.character.inv.update('11')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                        self.character.inv.update('12')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                        self.hero_group.update('5')
                    if event.type == game.time_update:
                        self.game_clock.time_update()
                if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                    self.hero_group.update('mu')
                if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                    self.hero_group.update('ml')
                if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                    self.hero_group.update('md')
                if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                    self.hero_group.update('mr')

                self.screen.fill('white')
                self.camera.update(game.character)
                self.camera.appply(game.character)
                for sprite in self.tile_group:
                    self.camera.appply(sprite)
                for sprite in self.wall_group:
                    self.camera.appply(sprite)
                self.character.boots.update(self.character)
                self.tile_group.draw(self.screen)
                self.hero_group.draw(self.screen)
                self.walked_group.draw(self.screen)
                self.game_clock.draw_time(self.screen)
                self.menu_group.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(FPS)
            elif self.run_type == 'home':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                        self.hero_group.update('da')
                if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[
                    pygame.K_w]:
                    self.character.ori = 'u'
                    self.character.rect.y -= 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.y += 1
                if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[
                    pygame.K_a]:
                    self.character.ori = 'l'
                    self.character.rect.x -= 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.x += 1
                if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[
                    pygame.K_s]:
                    self.character.ori = 'd'
                    self.character.rect.y += 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.y -= 1
                    print(self.character.boots.rect.x, self.character.boots.rect.y)
                if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[
                    pygame.K_d]:
                    self.character.ori = 'r'
                    self.character.rect.x += 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.x -= 1
                self.screen.fill('white')
                self.all_home_sprites.draw(self.screen)
                self.hero_group.draw(self.screen)
                self.moved_home_sprites.draw(self.screen)
                if self.character.boots.rect.y > 425:
                    self.run_type = 'farm'
                    self.character.rect.x, self.character.rect.y = 645, 378
                    self.character.absolute_x, self.character.absolute_y = 910, 505
                pygame.display.flip()
                self.clock.tick(FPS)


    def init(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.hero_group = pygame.sprite.Group()
        self.hero_boots_group = pygame.sprite.Group()
        self.d_group = pygame.sprite.Group()
        self.g_group = pygame.sprite.Group()
        self.menu_group = pygame.sprite.Group()
        self.worked_group = pygame.sprite.Group()
        self.fon_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.d_mask_group = pygame.sprite.Group()
        self.walked_group = pygame.sprite.Group()
        self.home_t_group = pygame.sprite.Group()
        self.all_home_sprites = pygame.sprite.Group()
        self.moved_home_sprites = pygame.sprite.Group()
        Fon()
        self.size = self.width, self.height = 1000, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = Camera()
        set_map(load_map(f'Saves/Save{self.save}/Map.txt'))
        with open(f'Saves/Save{self.save}/Save.txt', mode='r', encoding='utf-8') as save_file:
            data_lines = save_file.readlines()
        self.character = Hero(0, f'Saves/Save{self.save}/Inv.txt')
        self.run_type = 'farm'
        self.game_clock = GameClock(data_lines[2].split('; ')[0], data_lines[2].split('; ')[1])
        self.time_update = pygame.USEREVENT + 1
        self.home = Home()
        pygame.time.set_timer(self.time_update, 7000)


game = Game('a')
game.init()
game.run()
