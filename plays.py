import random
import sys
import pygame
import os

FPS = 30
small_grow_tile = []
long_grow_tile = []
MI_LIST = ['Wood', 'Pumpkin', 'Pumpkin_Seeds', 'Tomato', 'Tomato_Seeds', 'Pepper', 'Pepper_Seeds',
           'Baklajan', 'Baklajan_Seeds', 'Wheat', 'Wheat_Seeds']


def load_image(name, road, colorkey=None):
    # Функция-Загрузчик Изображений
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
    # Класс Спрайта Тайлов Отображающий Их На Поле
    def __init__(self, tile, pos_x, pos_y):
        self.tile = tile.split(';')
        self.x, self.y = pos_x, pos_y
        if self.tile[0] == 'Grass':
            super().__init__(game.all_sprites, game.tile_group, game.map_tile_group, game.g_group)
            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
        elif self.tile[0] == 'Water':
            super().__init__(game.all_sprites, game.tile_group, game.d_group, game.map_tile_group)
            self.image = load_image(f'Water_{self.tile[2] + self.tile[1]}.png', 'Sprites/Water')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
        elif self.tile[0] == 'Stump':
            super().__init__(game.all_sprites, game.tile_group,
                             game.d_mask_group, game.map_tile_group)
            self.image = load_image(f'Stump_mask.png', 'Sprites/Wood')
            self.mask = pygame.mask.from_surface(self.image)
            self.image = load_image(f'Stump.png', 'Sprites/Wood')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
            self.hp = 5
        elif self.tile[0] == 'Tree':
            super().__init__(game.all_sprites, game.tile_group,
                             game.d_mask_group, game.walked_group, game.map_tile_group)
            self.image = load_image(f'Tree_mask.png', 'Sprites/Wood')
            self.mask = pygame.mask.from_surface(self.image)
            self.image = load_image(f'TreeUp.png', 'Sprites/Wood')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 80 - 35, 25 * pos_y + 80 - 30
            self.sub = SubTile(25 * pos_x + 80 - 35, 25 * pos_y + 80 - 30, 'td')
            self.hp = 15
        elif self.tile[0] == 'Gradka':
            super().__init__(game.all_sprites, game.tile_group, game.map_tile_group, game.g_group)
            self.image = load_image(f'Gradka.png', 'Sprites/Farm')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
            long_grow_tile.append([self, int(self.tile[2])])
            self.p = 0
        elif self.tile[0] == 'Gp':
            super().__init__(game.all_sprites, game.tile_group, game.map_tile_group)
            self.image = load_image(f'Gp{self.tile[1]}.png', 'Sprites/Farm')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
            long_grow_tile.append([self, int(self.tile[2])])
            self.p = 0
        elif self.tile[0] == 'Gt':
            super().__init__(game.all_sprites, game.tile_group, game.map_tile_group)
            self.image = load_image(f'Gt{self.tile[1]}.png', 'Sprites/Farm')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
            long_grow_tile.append([self, int(self.tile[2])])
            self.p = 0
        elif self.tile[0] == 'Gpe':
            super().__init__(game.all_sprites, game.tile_group, game.map_tile_group)
            self.image = load_image(f'Gpe{self.tile[1]}.png', 'Sprites/Farm')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
            long_grow_tile.append([self, int(self.tile[2])])
            self.p = 0
        elif self.tile[0] == 'Gb':
            super().__init__(game.all_sprites, game.tile_group, game.map_tile_group)
            self.image = load_image(f'Gb{self.tile[1]}.png', 'Sprites/Farm')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
            long_grow_tile.append([self, int(self.tile[2])])
            self.p = 0
        elif self.tile[0] == 'Gw':
            super().__init__(game.all_sprites, game.tile_group, game.map_tile_group)
            self.image = load_image(f'Gw{self.tile[1]}.png', 'Sprites/Farm')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 25 * pos_x + 75, 25 * pos_y + 140
            long_grow_tile.append([self, int(self.tile[2])])
            self.p = 0

    def update(self, arg):
        if (self.tile[0] == 'Grass' or self.tile[0] == 'Zemla' or
                self.tile[0] == 'Gradka') and arg == 'us':
            self.tile[0], self.tile[1], self.tile[2] = 'Zemla', '0', '0'
            self.image = load_image('Zemla.jpg', 'Sprites')
            small_grow_tile.append([self, 6])
        elif self.tile[0] == 'Zemla' and arg == 'sge':
            self.tile[0] = 'Grass'
            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
        elif self.tile[0] == 'Gradka' and arg == 'lge':
            self.tile[0], self.tile[1], self.tile[2] = 'Grass', '0', '0'

            self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
        elif (self.tile[0] == 'Grass' or self.tile[0] == 'Zemla' or
                self.tile[0] == 'Gradka') and arg == 'uh':
            self.tile[0] = 'Gradka'
            self.p = 0
            self.tile[2] = '4'
            long_grow_tile.append([self, 4])
            self.image = load_image('Gradka.png', 'Sprites/Farm')
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
                super().__init__(game.all_sprites, game.tile_group,
                                 game.d_mask_group, game.map_tile_group)
                self.image = load_image(f'Stump_mask.png', 'Sprites/Wood')
                self.mask = pygame.mask.from_surface(self.image)
                self.image = load_image(f'Stump.png', 'Sprites/Wood')
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = x + 30,  y + 90
                self.hp = 10
                game.character.inv.add_item('Wood', 15)
        elif self.tile[0] == 'Stump' and (arg == 'ua' or arg == 'uia' or
                                          arg == 'uga' or arg == 'uira'):
            self.hp -= 1
            if self.hp < 1:
                x, y = self.rect.x, self.rect.y
                self.kill()
                super().__init__(game.all_sprites, game.tile_group, game.map_tile_group)
                self.tile[0] = 'Grass'
                self.image = load_image(f'Grass_{self.tile[2] + self.tile[1]}.jpg', 'Sprites/Grass')
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = x, y
                game.character.inv.add_item('Wood', 5)

        elif self.tile[0] == 'Water' and arg == 'ucv':
            return True
        elif self.tile[0] == 'Gradka' and arg == 'uc':
            self.p = 1
            self.image = load_image(f'Gradka_w.png', 'Sprites/Farm')
        elif self.tile[0] == 'Gradka' and arg == 'so':
            self.p = 0
            self.image = load_image('Gradka.png', 'Sprites/Farm')
        elif self.tile[0] == 'Gradka' and arg == 'ups':
            self.tile[0] = 'Gp'
            self.tile[1] = '1'
            if self.p == 0:
                self.image = load_image(f'GP1.png', 'Sprites/Farm')
            else:
                self.image = load_image(f'GP1_w.png', 'Sprites/Farm')
        elif self.tile[0] == 'Gradka' and arg == 'uts':
            self.tile[0] = 'Gt'
            self.tile[1] = '1'
            if self.p == 0:
                self.image = load_image(f'Gt1.png', 'Sprites/Farm')
            else:
                self.image = load_image(f'Gt1_w.png', 'Sprites/Farm')
        elif self.tile[0] == 'Gradka' and arg == 'upes':
            self.tile[0] = 'Gpe'
            self.tile[1] = '1'
            if self.p == 0:
                self.image = load_image(f'Gpe1.png', 'Sprites/Farm')
            else:
                self.image = load_image(f'Gpe1_w.png', 'Sprites/Farm')
        elif self.tile[0] == 'Gradka' and arg == 'ubs':
            self.tile[0] = 'Gb'
            self.tile[1] = '1'
            if self.p == 0:
                self.image = load_image(f'Gb1.png', 'Sprites/Farm')
            else:
                self.image = load_image(f'Gb1_w.png', 'Sprites/Farm')
        elif self.tile[0] == 'Gradka' and arg == 'uws':
            self.tile[0] = 'Gw'
            self.tile[1] = '1'
            if self.p == 0:
                self.image = load_image(f'Gw1.png', 'Sprites/Farm')
            else:
                self.image = load_image(f'Gw1_w.png', 'Sprites/Farm')
        elif (self.tile[0] == 'Gp' or self.tile[0] == 'Gt' or self.tile[0] == 'Gpe' or
              self.tile[0] == 'Gb' or self.tile[0] == 'Gw') and arg == 'uc':
            self.p = 1
            self.image = load_image(f'{self.tile[0] + self.tile[1]}_w.png', 'Sprites/Farm')
        elif (self.tile[0] == 'Gp' or self.tile[0] == 'Gt' or self.tile[0] == 'Gpe' or
              self.tile[0] == 'Gb' or self.tile[0] == 'Gw') and arg == 'so':
            self.p = 0
            if (self.tile[0] == 'Gp' and self.tile[1] != '5' or
                    self.tile[0] == 'Gt' and self.tile[1] != '3' or
                    self.tile[0] == 'Gpe' and self.tile[1] != '6' or
                    self.tile[0] == 'Gb' and self.tile[1] != '5' or
                    self.tile[0] == 'Gw' and self.tile[1] != '4'):
                self.tile[1] = str(int(self.tile[1]) + 1)
            self.image = load_image(f'{self.tile[0] + self.tile[1]}.png', 'Sprites/Farm')
        elif (self.tile[0] == 'Gp' or self.tile[0] == 'Gt' or self.tile[0] == 'Gpe' or
              self.tile[0] == 'Gb' or self.tile[0] == 'Gw') and arg == 'uh':
            if self.tile[0] == 'Gp' and self.tile[1] == '5':
                self.tile[0], self.tile[1], self.tile[2] = 'Gradka', '0', '4'
                if self.p == 0:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                else:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                game.character.inv.add_item('Pumpkin', 1)
            elif self.tile[0] == 'Gt' and self.tile[1] == '3':
                self.tile[0], self.tile[1], self.tile[2] = 'Gradka', '0', '4'
                if self.p == 0:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                else:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                game.character.inv.add_item('Tomato', random.randrange(1, 6))
            elif self.tile[0] == 'Gpe' and self.tile[1] == '6':
                self.tile[0], self.tile[1], self.tile[2] = 'Gradka', '0', '4'
                if self.p == 0:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                else:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                game.character.inv.add_item('Pepper', 1)
            elif self.tile[0] == 'Gb' and self.tile[1] == '5':
                self.tile[0], self.tile[1], self.tile[2] = 'Gradka', '0', '4'
                if self.p == 0:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                else:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                game.character.inv.add_item('Baklajan', 1)
            elif self.tile[0] == 'Gw' and self.tile[1] == '4':
                self.tile[0], self.tile[1], self.tile[2] = 'Gradka', '0', '4'
                if self.p == 0:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                else:
                    self.image = load_image(f'Gradka.png', 'Sprites/Farm')
                game.character.inv.add_item('Wheat', random.randrange(1, 5))
        return False


class SubTile(pygame.sprite.Sprite):
    # Вспомогательный Класс-Тайл редко необходимый при отрисовке сложных обьектов
    def __init__(self, x, y, arg):
        if arg == 'td':
            super().__init__(game.all_sprites, game.tile_group)
            self.image = load_image('TreeDown.png', 'Sprites/Wood')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y


def load_map(file):
    # Функция-Зашрузчик обрабатывающая текстовые файлы и превращающая их в экземпляры тайлов
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
    # Спомогательная Функция-Обработчик текстовых карт
    for i in range(len(map_level[0])):
        for j in range(len(map_level[0][i])):
            Tile(map_level[0][i][j], j, i)


class Item(pygame.sprite.Sprite):
    # Спрайт Предметов в инвенторе
    def __init__(self, item_name, pos, *args):
        super().__init__(game.all_sprites, game.menu_group)
        self.name, self.pos = item_name, pos
        if self.name in MI_LIST:
            self.count = int(args[0])
        if self.name == 'Can' or self.name == 'Iron_Can' or \
                self.name == 'Gold_Can' or self.name == 'Ir_Can':
            self.image = load_image(f'{item_name}_1.png', f'Sprites/Items')
            self.capasity = 0
        else:
            self.image = load_image(f'{item_name}.png', f'Sprites/Items')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 218 + 48 * self.pos, 758

    def use(self, ori, pos):
        point = MyPoint(ori, pos)
        game.camera.appply(point)
        used_tile = pygame.sprite.spritecollide(point, game.all_sprites, False)
        if used_tile:
            if len(used_tile) > 3:
                if str(type(used_tile[3])) == "<class 'plays.CellBox'>":
                    used_tile[3].update()
                    return
            if game.character.enb.enable():
                if self.name == 'None':
                    used_tile[1].update('un')
                elif self.name == 'Shovel':
                    used_tile[1].update('us')
                elif self.name == 'Axe':
                    game.character.enb.energy -= 1
                    used_tile[1].update('ua')
                elif self.name == 'Iron_Axe':
                    game.character.enb.energy -= 1
                    used_tile[1].update('uia')
                elif self.name == 'Gold_Axe':
                    game.character.enb.energy -= 1
                    used_tile[1].update('uga')
                elif self.name == 'Ir_Axe':
                    game.character.enb.energy -= 1
                    used_tile[1].update('uira')
                elif self.name == 'Hoe':
                    game.character.enb.energy -= 5
                    used_tile[1].update('uh')
                elif self.name == 'Iron_Hoe':
                    game.character.enb.energy -= 3
                    used_tile[1].update('uh')
                elif self.name == 'Gold_Hoe':
                    game.character.enb.energy -= 2
                    used_tile[1].update('uh')
                elif self.name == 'Ir_Hoe':
                    game.character.enb.energy -= 1
                    used_tile[1].update('uh')
                elif self.name == 'Can':
                    if used_tile[1].update('ucv'):
                        self.capasity = 5
                        game.character.enb.energy -= 1
                    elif self.capasity > 0:
                        self.capasity -= 1
                        used_tile[1].update('uc')
                elif self.name == 'Iron_Can':
                    if used_tile[1].update('ucv'):
                        self.capasity = 15
                        game.character.enb.energy -= 1
                    elif self.capasity > 0:
                        self.capasity -= 1
                        used_tile[1].update('uc')
                elif self.name == 'Gold_Can':
                    if used_tile[1].update('ucv'):
                        self.capasity = 30
                        game.character.enb.energy -= 1
                    elif self.capasity > 0:
                        self.capasity -= 1
                        used_tile[1].update('uc')
                elif self.name == 'Ir_Can':
                    if used_tile[1].update('ucv'):
                        self.capasity = 60
                        game.character.enb.energy -= 1
                    elif self.capasity > 0:
                        self.capasity -= 1
                        used_tile[1].update('uc')
                elif self.name == 'Pumpkin_Seeds':
                    self.count -= 1
                    game.character.enb.energy -= 1
                    used_tile[1].update('ups')
                elif self.name == 'Tomato_Seeds':
                    self.count -= 1
                    game.character.enb.energy -= 1
                    used_tile[1].update('uts')
                elif self.name == 'Pepper_Seeds':
                    self.count -= 1
                    game.character.enb.energy -= 1
                    used_tile[1].update('upes')
                elif self.name == 'Baklajan_Seeds':
                    self.count -= 1
                    game.character.enb.energy -= 1
                    used_tile[1].update('ubs')
                elif self.name == 'Wheat_Seeds':
                    self.count -= 1
                    game.character.enb.energy -= 1
                    used_tile[1].update('uws')
                if self.name == 'Can':
                    if self.capasity > 4:
                        self.image = load_image('Can_3.png', 'Sprites/Items')
                    elif self.capasity > 1:
                        self.image = load_image('Can_2.png', 'Sprites/Items')
                    else:
                        self.image = load_image('Can_1.png', 'Sprites/Items')
                elif self.name == 'Iron_Can':
                    if self.capasity > 10:
                        self.image = load_image('Iron_Can_3.png', 'Sprites/Items')
                    elif self.capasity > 5:
                        self.image = load_image('Iron_Can_2.png', 'Sprites/Items')
                    else:
                        self.image = load_image('Iron_Can_1.png', 'Sprites/Items')
                elif self.name == 'Gold_Can':
                    if self.capasity > 19:
                        self.image = load_image('Gold_Can_3.png', 'Sprites/Items')
                    elif self.capasity > 9:
                        self.image = load_image('Gold_Can_2.png', 'Sprites/Items')
                    else:
                        self.image = load_image('Gold_Can_1.png', 'Sprites/Items')
                elif self.name == 'Ir_Can':
                    if self.capasity > 39:
                        self.image = load_image('Ir_Can_3.png', 'Sprites/Items')
                    elif self.capasity > 19:
                        self.image = load_image('Ir_Can_2.png', 'Sprites/Items')
                    else:
                        self.image = load_image('Ir_Can_1.png', 'Sprites/Items')
                if self.name in MI_LIST:
                    if self.count < 1:
                        self.name = 'None'
                        self.image = self.image = load_image('None.png', 'Sprites/Items')
        point.kill()

    def c_draw(self, screen):
        if self.name in MI_LIST and self.count > 1:
            font = pygame.font.SysFont('Times New Roman', 15)
            text = font.render(str(self.count), False, (0, 0, 0))
            screen.blit(text, (self.rect.x + 25, self.rect.y + 20))


class MyPoint(pygame.sprite.Sprite):
    # Вспомогательный Класс_Спрайт, необходимый для обработки действий героя
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
    # Спрайт Инвентаря
    def __init__(self, file):
        super().__init__(game.all_sprites, game.menu_group)
        self.items = []
        with open(file, mode='r', encoding='utf-8') as inventory_file:
            item_lines = list(map(str.rstrip, inventory_file.readlines()))
            for i in range(len(item_lines)):
                if item_lines[i].split()[0] in MI_LIST:
                    self.items.append(Item(item_lines[i].split()[0], i, item_lines[i].split()[1]))
                else:
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

    def add_item(self, name, *args):
        for i in range(len(self.items)):
            if self.items[i].name == name and name in MI_LIST:
                self.items[i].count += int(args[0])
                return True
        for i in range(len(self.items)):
            if self.items[i].name == 'None':
                if args:
                    self.items[i] = Item(name, i, args[0])
                else:
                    self.items[i] = Item(name, i)
                return True
        return False

    def move_item(self, p1, p2):
        self.items[p1], self.items[p2] = self.items[p2], self.items[p1]


class EnergyBar(pygame.sprite.Sprite):
    # Спрайт Столбика Энергии
    def __init__(self):
        super().__init__(game.all_sprites, game.menu_group)
        self.energy = 70
        self.image = load_image('EnergyBar4.png', 'Sprites/EnergyBar')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 940, 500

    def enable(self):
        if self.energy > 0:
            return True
        return False

    def update(self):
        if self.energy > 55:
            self.image = load_image('EnergyBar4.png', 'Sprites/EnergyBar')
        elif 15 <= self.energy < 44:
            self.image = load_image('EnergyBar3.png', 'Sprites/EnergyBar')
        elif 5 <= self.energy < 24:
            self.image = load_image('EnergyBar2.png', 'Sprites/EnergyBar')
        elif self.energy < 9:
            self.image = load_image('EnergyBar1.png', 'Sprites/EnergyBar')


class Hero(pygame.sprite.Sprite):
    # Спрайт Героя также обрабатывающий действия героя
    def __init__(self, inv):
        super().__init__(game.all_sprites, game.hero_group)
        self.image = pygame.Surface((20, 45), pygame.SRCALPHA, 32)
        self.image = load_image('Character_0.png', 'Sprites/Hero')
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
                self.image = load_image('Character_2.png', 'Sprites/Hero')
                self.rect.y -= m
                self.absolute_y -= m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.y += m
                    self.absolute_y += m
            elif arg[1] == 'l':
                self.ori = 'l'
                self.image = load_image('Character_3.png', 'Sprites/Hero')
                self.rect.x -= m
                self.absolute_x -= m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.x += m
                    self.absolute_x += m
            elif arg[1] == 'd':
                self.ori = 'd'
                self.image = load_image('Character_0.png', 'Sprites/Hero')
                self.rect.y += m
                self.absolute_y += m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.y -= m
                    self.absolute_y -= m
            elif arg[1] == 'r':
                self.ori = 'r'
                self.image = load_image('Character_1.png', 'Sprites/Hero')
                self.rect.x += m
                self.absolute_x += m
                self.boots.update(self)
                if pygame.sprite.groupcollide(game.hero_boots_group, game.d_group, False, False)\
                        or mask_collide(self.boots, game.d_mask_group):
                    self.rect.x -= m
                    self.absolute_x -= m
        elif arg == 'da' and self.enb.enable():
            if 700 < self.absolute_x < 850 and 50 < self.absolute_y < 125:
                game.shop.go_shop()
            else:
                self.inv.update('da')
                self.enb.update()
        if pygame.sprite.spritecollideany(self.boots, game.home_t_group):
            game.run_type = 'home'
            self.rect.x, self.rect.y = 421, 380
        self.boots.update(self)


def mask_collide(sprite, sprite_group):
    # Вспомогательная функция помогающая проверять пересечения маски с группой спрайтов
    for s in sprite_group:
        if pygame.sprite.collide_mask(sprite, s):
            return True
    return False


class HeroBoots(pygame.sprite.Sprite):
    # Вспомогательный Класс необходимый для правильной работы пересечений
    def __init__(self, hero):
        super().__init__(game.all_sprites, game.hero_boots_group)
        self.image = pygame.Surface((20, 15), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('magenta'), (0, 0, 20, 15))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = hero.rect.x, hero.rect.y + 30
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, hero):
        self.rect.x, self.rect.y = hero.rect.x, hero.rect.y + 35


class GameClock(pygame.sprite.Sprite):
    # Спрайт Времени, Обработчик времени
    def __init__(self, days):
        super().__init__(game.all_sprites, game.menu_group)
        self.days, self.hours, self.minuts = int(days), 4, 0
        self.image = load_image('Time.png', 'Sprites/Inv')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 25

    def time_update(self):
        self.minuts += 10
        self.hours += self.minuts // 60
        self.minuts %= 60
        for t in small_grow_tile:
            t[1] -= 1
            if t[1] == 0:
                t[0].update('sge')
                small_grow_tile.remove(t)
        if self.hours > 23:
            game.money.m = game.money.m // 10 * 9
            game.next_day()

    def draw_time(self, screen):
        font = pygame.font.SysFont('Times New Roman', 25)
        text = font.render(f'Время: {self.hours}:{self.minuts}', False, (0, 0, 0))
        screen.blit(text, (820, 80))
        text = font.render(f'Дней: {self.days}', False, (0, 0, 0))
        screen.blit(text, (820, 40))


class Money(pygame.sprite.Sprite):
    # Спрайт-Счетчик Монеток Также обрабатывающий их изменения
    def __init__(self, m):
        super().__init__(game.all_sprites, game.menu_group)
        self.image = load_image('Money.png', 'Sprites/Inv')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 125
        self.m = int(m)

    def print_money(self, screen):
        font = pygame.font.SysFont('Times New Roman', 25)
        text = font.render(str(self.m), False, (0, 0, 0))
        screen.blit(text, (840, 155))


class Camera:
    # Камера со срезанными углами
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
    # Спрайт Фоновых стенок
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
    # Визуальный Спрайт Фона
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
    # Класс Компанующий в себе составные части дома
    def __init__(self):
        self.roof = HomeRoof()
        self.wall = HomeWall()
        self.terrace = HomeTerrace()
        self.mat = HomeMat()
        self.in_fon = InHomeFon()
        self.in_border = InHomeFonBorders()
        self.in_moved = InHomeMoved()


class HomeRoof(pygame.sprite.Sprite):
    # Спрайт Крыши
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.walked_group)
        self.image = load_image(f'Home_Roof.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 355


class HomeMat(pygame.sprite.Sprite):
    # Спрайт Коврика перед дверью
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.home_t_group)
        self.image = load_image(f'Home_Mat.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 910, 507


class HomeTerrace(pygame.sprite.Sprite):
    # Спрайт Террасы
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group)
        self.image = load_image(f'Home_Terrace.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 801, 505


class HomeWall(pygame.sprite.Sprite):
    # Спрайт Стен Дома
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.d_mask_group)
        self.image = load_image(f'Home_Wall.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 355
        self.mask = pygame.mask.from_surface(self.image)


class InHomeFon(pygame.sprite.Sprite):
    # Спрайт Фона Внутри Дома
    def __init__(self):
        super().__init__(game.all_home_sprites)
        self.image = load_image(f'InHome_Fon.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 350, 139


class InHomeMoved(pygame.sprite.Sprite):
    # Спрайт Накладываемых Обьектов Внутри Дома
    def __init__(self):
        super().__init__(game.moved_home_sprites)
        self.image = load_image(f'InHome_Moved.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 350, 139


class InHomeFonBorders(pygame.sprite.Sprite):
    # Спрайт Границ Дома
    def __init__(self):
        super().__init__(game.all_home_sprites)
        self.image = load_image(f'InHome_Border.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 350, 139


class CellBox(pygame.sprite.Sprite):
    # Спрайт Ящика для Продажи Предметов, Обработчик Ящика
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.d_mask_group)
        self.image = load_image('Mask_Box.png', 'Sprites/Home')
        self.mask = pygame.mask.from_surface(self.image)
        self.image = load_image('Box.png', 'Sprites/Home')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 1020, 500
        self.m = 0

    def update(self):
        iname = game.character.inv.items[game.character.inv.choosed - 1].name
        if iname != 'None':
            if iname == 'Axe':
                self.m += 15
            elif iname == 'Iron_Axe':
                self.m += 150
            elif iname == 'Gold_Axe':
                self.m += 450
            elif iname == 'Ir_Axe':
                self.m += 900
            elif iname == 'Wood':
                self.m += 2 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Hoe':
                self.m += 15
            elif iname == 'Iron_Hoe':
                self.m += 150
            elif iname == 'Gold_Hoe':
                self.m += 450
            elif iname == 'Ir_Hoe':
                self.m += 900
            elif iname == 'Shovel':
                self.m += 45
            elif iname == 'Can':
                self.m += 15
            elif iname == 'Iron_Can':
                self.m += 150
            elif iname == 'Gold_Can':
                self.m += 450
            elif iname == 'Ir_Can':
                self.m += 900
            elif iname == 'Pumpkin':
                self.m += 45 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Pumpkin_Seeds':
                self.m += 5 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Tomato':
                self.m += 5 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Tomato_Seeds':
                self.m += 4 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Pepper':
                self.m += 150 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Pepper_Seeds':
                self.m += 6 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Baklajan':
                self.m += 90 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Baklajan_Seeds':
                self.m += 5 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Wheat':
                self.m += 8 * game.character.inv.items[game.character.inv.choosed - 1].count
            elif iname == 'Wheat_Seeds':
                self.m += 4 * game.character.inv.items[game.character.inv.choosed - 1].count
            game.character.inv.items[game.character.inv.choosed - 1].kill()
            game.character.inv.items[game.character.inv.choosed - 1] = \
                Item('None', game.character.inv.choosed - 1)


class Shop(pygame.sprite.Sprite):
    # Спрайт Магазина, Обработчик магазина
    def __init__(self):
        super().__init__(game.all_sprites, game.tile_group, game.d_group)
        self.image = load_image('Shop.png', 'Sprites/Hero')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 750, 75
        self.fon = ShopFone()

    def go_shop(self):
        game.run_type = 'shop'

    def deal(self, pos):
        if 210 < pos[0] < 250 and 215 < pos[1] < 290:
            if game.money.m > 29:
                if game.character.inv.add_item('Axe'):
                    game.money.m -= 30
        elif 260 < pos[0] < 310 and 215 < pos[1] < 290:
            if game.money.m > 29:
                if game.character.inv.add_item('Hoe'):
                    game.money.m -= 30
        elif 320 < pos[0] < 380 and 215 < pos[1] < 290:
            if game.money.m > 29:
                if game.character.inv.add_item('Can'):
                    game.money.m -= 30
        elif 390 < pos[0] < 440 and 215 < pos[1] < 290:
            if game.money.m > 299:
                if game.character.inv.add_item('Iron_Axe'):
                    game.money.m -= 300
        elif 450 < pos[0] < 490 and 215 < pos[1] < 290:
            if game.money.m > 299:
                if game.character.inv.add_item('Iron_Hoe'):
                    game.money.m -= 300
        elif 500 < pos[0] < 540 and 215 < pos[1] < 290:
            if game.money.m > 299:
                if game.character.inv.add_item('Iron_Can'):
                    game.money.m -= 300
        elif 550 < pos[0] < 590 and 215 < pos[1] < 290:
            if game.money.m > 899:
                if game.character.inv.add_item('Gold_Axe'):
                    game.money.m -= 900
        elif 600 < pos[0] < 640 and 215 < pos[1] < 290:
            if game.money.m > 899:
                if game.character.inv.add_item('Gold_Hoe'):
                    game.money.m -= 900
        elif 650 < pos[0] < 690 and 215 < pos[1] < 290:
            if game.money.m > 899:
                if game.character.inv.add_item('Gold_Can'):
                    game.money.m -= 900
        elif 210 < pos[0] < 250 and 315 < pos[1] < 390:
            if game.money.m > 1799:
                if game.character.inv.add_item('Ir_Axe'):
                    game.money.m -= 1800
        elif 260 < pos[0] < 310 and 315 < pos[1] < 390:
            if game.money.m > 1799:
                if game.character.inv.add_item('Ir_Hoe'):
                    game.money.m -= 1800
        elif 320 < pos[0] < 380 and 315 < pos[1] < 390:
            if game.money.m > 1799:
                if game.character.inv.add_item('Ir_Can'):
                    game.money.m -= 1800
        elif 390 < pos[0] < 440 and 315 < pos[1] < 390:
            if game.money.m > 89:
                if game.character.inv.add_item('Shovel'):
                    game.money.m -= 90
        elif 450 < pos[0] < 490 and 315 < pos[1] < 390:
            if game.money.m > 24:
                if game.character.inv.add_item('Baklajan_Seeds', 1):
                    game.money.m -= 25
        elif 500 < pos[0] < 540 and 315 < pos[1] < 390:
            if game.money.m > 4:
                if game.character.inv.add_item('Wheat_Seeds', 1):
                    game.money.m -= 5
        elif 550 < pos[0] < 590 and 315 < pos[1] < 390:
            if game.money.m > 3:
                if game.character.inv.add_item('Tomato_Seeds', 1):
                    game.money.m -= 4
        elif 600 < pos[0] < 640 and 315 < pos[1] < 390:
            if game.money.m > 4:
                if game.character.inv.add_item('Pumpkin_Seeds', 1):
                    game.money.m -= 5
        elif 650 < pos[0] < 690 and 315 < pos[1] < 390:
            if game.money.m > 39:
                if game.character.inv.add_item('Pepper_Seeds', 1):
                    game.money.m -= 40
        elif 730 < pos[0] < 755 and 210 < pos[1] < 240:
            game.run_type = 'farm'


class ShopFone(pygame.sprite.Sprite):
    # Спрайт Фона Магазина
    def __init__(self):
        super().__init__(game.shop_fone_group)
        self.image = load_image('ShopMenu.png', 'Sprites')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 200, 200


class Game:
    # Класс Компанующий в себе всю игру, позволяет удобно импортировать игру
    def __init__(self, save):
        self.save = save

    def next_day(self):
        # Метод Сохраняющий Прогресс и Запускающий Следующие Сутки
        self.game_clock.days += 1
        self.game_clock.hours = 4
        self.game_clock.minuts = 0
        for i in range(len(long_grow_tile)):
            if long_grow_tile[i][0].p == 1:
                long_grow_tile[i][0].update('so')
            elif long_grow_tile[i][1] < 1:
                long_grow_tile[i][0].update('lge')
                long_grow_tile[i][0].tile[2] = '0'
            else:
                long_grow_tile[i][0].tile[2] = str(int(long_grow_tile[i][0].tile[2]) - 1)
                long_grow_tile[i][1] -= 1
        for t in small_grow_tile:
            t[0].update('sge')
        old_map = load_map(f'Saves/Save{self.save}/Map.txt')[0]
        for tile in self.map_tile_group:
            old_map[tile.y][tile.x] = ';'.join(tile.tile)
        for i in range(len(old_map)):
            old_map[i] = ' '.join(old_map[i])
        with open(f'Saves/Save{self.save}/Map.txt', mode='w', encoding='utf-8') as map_file:
            map_file.writelines('\n'.join(old_map))
        with open(f'Saves/Save{self.save}/Save.txt', mode='r', encoding='utf-8') as save_file:
            old_save = save_file.readlines()
        old_save[2] = str(self.game_clock.days) + '\n'
        old_save[3] = str(self.money.m + self.cell_box.m) + '\n'
        self.money.m += self.cell_box.m
        self.cell_box.m = 0
        with open(f'Saves/Save{self.save}/Save.txt', mode='w', encoding='utf-8') as save_file:
            save_file.writelines(''.join(old_save))
        new_inv = []
        for e in self.character.inv.items:
            if e.name in MI_LIST:
                new_inv.append(e.name + ' ' + str(e.count))
            else:
                new_inv.append(e.name)
        with open(f'Saves/Save{self.save}/Inv.txt', mode='w', encoding='utf-8') as inv_file:
            inv_file.writelines('\n'.join(new_inv))
        if self.run_type == 'home':
            self.character.rect.x, self.character.rect.y = 382, 275
            self.character.enb.energy = 76
            self.character.enb.update()
        else:
            self.character.enb.energy = 36
            self.character.enb.update()

    def reset(self):
        # Метод Обнуляющий Прогресс
        with open(f'Saves/Standart/Map.txt', mode='r', encoding='utf-8') as map_file:
            standart_map = map_file.readlines()
        with open(f'Saves/Save{self.save}/Map.txt', mode='w', encoding='utf-8') as map_file:
            map_file.writelines(''.join(standart_map))
        with open(f'Saves/Standart/Inv.txt', mode='r', encoding='utf-8') as inv_file:
            standart_inv = inv_file.readlines()
        with open(f'Saves/Save{self.save}/Inv.txt', mode='w', encoding='utf-8') as inv_file:
            inv_file.writelines(''.join(standart_inv))
        with open(f'Saves/Standart/Save.txt', mode='r', encoding='utf-8') as save_file:
            standart_save = save_file.readlines()
        with open(f'Saves/Save{self.save}/Save.txt', mode='w', encoding='utf-8') as save_file:
            save_file.writelines(''.join(standart_save))

    def run(self):
        # Основной Цикл Игры
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
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        sys.exit()
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
                self.menu_group.draw(self.screen)
                for e in self.character.inv.items:
                    e.c_draw(self.screen)
                self.game_clock.draw_time(self.screen)
                self.money.print_money(self.screen)
                pygame.display.flip()
                self.clock.tick(FPS)
            elif self.run_type == 'home':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_e and \
                            586 < self.character.rect.x and 357 < self.character.rect.y:
                        self.next_day()
                if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                    self.character.ori = 'u'
                    self.character.image = load_image('Character_2.png', 'Sprites/Hero')
                    self.character.rect.y -= 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.y += 1
                if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                    self.character.ori = 'l'
                    self.character.image = load_image('Character_3.png', 'Sprites/Hero')
                    self.character.rect.x -= 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.x += 1
                if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                    self.character.ori = 'd'
                    self.character.image = load_image('Character_0.png', 'Sprites/Hero')
                    self.character.rect.y += 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.y -= 1
                if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                    self.character.ori = 'r'
                    self.character.image = load_image('Character_1.png', 'Sprites/Hero')
                    self.character.rect.x += 1
                    self.character.boots.update(self.character)
                    if pygame.sprite.collide_mask(self.character.boots, game.home.in_border):
                        self.character.rect.x -= 1
                self.screen.fill('black')
                self.all_home_sprites.draw(self.screen)
                self.hero_group.draw(self.screen)
                self.moved_home_sprites.draw(self.screen)
                if self.character.boots.rect.y > 425:
                    self.run_type = 'farm'
                    self.character.rect.x, self.character.rect.y = 645, 378
                    self.character.absolute_x, self.character.absolute_y = 910, 505
                pygame.display.flip()
                self.clock.tick(FPS)
            elif self.run_type == 'shop':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.run_type = 'farm'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.shop.deal(event.pos)
                self.screen.fill('black')
                self.shop_fone_group.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(FPS)

    def init(self):
        # Инициализация Сущностей
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.shop_fone_group = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.map_tile_group = pygame.sprite.Group()
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
        self.character = Hero(f'Saves/Save{self.save}/Inv.txt')
        self.shop = Shop()
        self.run_type = 'farm'
        self.game_clock = GameClock(data_lines[2])
        self.money = Money(data_lines[3])
        self.time_update = pygame.USEREVENT + 1
        self.home = Home()
        self.cell_box = CellBox()
        pygame.time.set_timer(self.time_update, 3500)


game = Game('a')