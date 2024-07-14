import os
import sys
import random
import time

import pygame


pygame.init()
size = width, height = 550, 500
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
balls_sprites = pygame.sprite.Group()
tank_sprites = pygame.sprite.Group()
brick_sprites = pygame.sprite.Group()
player_balls = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
base_sprite = pygame.sprite.Group()

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
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Ball(pygame.sprite.Sprite):
    def __init__(self, dir, x, y):
        super().__init__(all_sprites)
        # self.add(balls_sprites)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(x, y, 2 * self.radius, 2 * self.radius)
        self.rect.x = x
        self.rect.y = y
        self.dir = dir
        self.vx = 10 #if dir == 'hor' else 0
        self.vy = 10 #if dir == 'ver' else 0

    def update(self):
        if self.dir == 0:
            self.rect = self.rect.move(0, 20 * self.vy / self.fps)
        if self.dir == 3:
            self.rect = self.rect.move(0, -20 * self.vy / self.fps)
        if self.dir == 1:
            self.rect = self.rect.move(-20 * self.vx / self.fps, 0)
        if self.dir == 2:
            self.rect = self.rect.move(20 * self.vx / self.fps, 0)
        self.clock.tick(self.fps)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, player_sprites):
            self.kill()
            p = None
            for player in player_sprites:
                if pygame.sprite.collide_rect(self, player):
                    p = player
            p.kill()
        if pygame.sprite.spritecollideany(self, brick_sprites):
            self.kill()
            br = None
            for brick in brick_sprites:
                if pygame.sprite.collide_rect(self, brick):
                    br = brick
            br.kill()
        if pygame.sprite.spritecollideany(self, base_sprite):
            self.kill()
            br = None
            for base in base_sprite:
                if pygame.sprite.collide_rect(self, base):
                    br = base
            br.kill()
        # if pygame.sprite.collide_rect(self, base_sprite):
        #     self.kill()
            
            # saved_sprites = list(all_sprites.sprites())
            # print(saved_sprites)
            # all_sprites.empty()
            # all_sprites.add(t)
            # for sp in saved_sprites:
            #     all_sprites.add(sp)
            # for el in all_sprites:
            #     if t == el:
            #         print(1)


class BallPlayer(pygame.sprite.Sprite):
    def __init__(self, dir, x, y):
        super().__init__(all_sprites)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("yellow"),
                           (self.radius, self.radius), self.radius)
        self.rect = pygame.Rect(x, y, 2 * self.radius, 2 * self.radius)
        self.rect.x = x
        self.rect.y = y
        self.dir = dir
        self.vx = 10 #if dir == 'hor' else 0
        self.vy = 10 #if dir == 'ver' else 0

    def update(self):
        if self.dir == 0:
            self.rect = self.rect.move(0, 20 * self.vy / self.fps)
        if self.dir == 3:
            self.rect = self.rect.move(0, -20 * self.vy / self.fps)
        if self.dir == 1:
            self.rect = self.rect.move(-20 * self.vx / self.fps, 0)
        if self.dir == 2:
            self.rect = self.rect.move(20 * self.vx / self.fps, 0)
        self.clock.tick(self.fps)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, tank_sprites):
            self.kill()
            t = None
            for tank in tank_sprites:
                if pygame.sprite.collide_rect(self, tank):
                    t = tank
            t.kill()
        if pygame.sprite.spritecollideany(self, base_sprite):
            self.kill()
        if pygame.sprite.spritecollideany(self, brick_sprites):
            self.kill()
            br = None
            for brick in brick_sprites:
                if pygame.sprite.collide_rect(self, brick):
                    br = brick
            t = Tile('empty', br.rect.x, br.rect.y)
            br.kill()
            saved_sprites = list(all_sprites.sprites())
            # print(saved_sprites)
            all_sprites.empty()
            all_sprites.add(t)
            for sp in saved_sprites:
                all_sprites.add(sp)
            # for el in all_sprites:
            #     if t == el:
            #         print(1)


class Tank(pygame.sprite.Sprite):
    imgD = load_image('enemy_blue_down.png')
    imgU = load_image('enemy_blue_up.png')
    imgL = load_image('enemy_blue_left.png')
    imgR = load_image('enemy_blue_right.png')
    def __init__(self, x, y):
        super().__init__(all_sprites, tank_sprites)

        self.image = Tank.imgD
        self.rect = self.image.get_rect()
        self.dir = 0
        self.fps = 60
        self.rrandi = random.randint(30, 80)
        self.clock = pygame.time.Clock()
        self.vx = random.randint(2, 6)
        self.vy = self.vx
        self.num = 0
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def update(self):
        self.num += 1
        if self.num % self.rrandi == 0:
            self.dir = random.randrange(100) % 4
        if self.num % 80 == 0:
            Ball(self.dir, self.rect.x + 10, self.rect.y + 10)
        if self.dir == 0:
            self.image = self.imgD
            self.rect = self.rect.move(0, 20 * self.vy / self.fps)
        elif self.dir == 3:
            self.image = self.imgU
            self.rect = self.rect.move(0, -20 * self.vy / self.fps)
        elif self.dir == 1:
            self.image = self.imgL
            self.rect = self.rect.move(-20 * self.vx / self.fps, 0)
        elif self.dir == 2:
            self.image = self.imgR
            self.rect = self.rect.move(20 * self.vx / self.fps, 0)
        self.clock.tick(self.fps)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.dir == 0:
                self.dir = 3
                self.rect = self.rect.move(0, -20 * self.vy / self.fps)
            else:
                self.dir = 0
                self.rect = self.rect.move(0, 20 * self.vy / self.fps)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            if self.dir == 2:
                self.dir = 1
                self.rect = self.rect.move(-20 * self.vy / self.fps, 0)
            else:
                self.dir = 2
                self.rect = self.rect.move(20 * self.vy / self.fps, 0)
        if pygame.sprite.spritecollideany(self, brick_sprites):
            if self.dir == 0:
                self.dir = 3
                self.rect = self.rect.move(0, -10 * self.vy / self.fps)
            elif self.dir == 3:
                self.dir = 0
                self.rect = self.rect.move(0, 10 * self.vy / self.fps)
            elif self.dir == 2:
                self.dir = 1
                self.rect = self.rect.move(-10 * self.vy / self.fps, 0)
            else:
                self.dir = 2
                self.rect = self.rect.move(10 * self.vy / self.fps, 0)
        if pygame.sprite.spritecollideany(self, base_sprite):
            if self.dir == 0:
                self.dir = 3
                self.rect = self.rect.move(0, -10 * self.vy / self.fps)
            elif self.dir == 3:
                self.dir = 0
                self.rect = self.rect.move(0, 10 * self.vy / self.fps)
            elif self.dir == 2:
                self.dir = 1
                self.rect = self.rect.move(-10 * self.vy / self.fps, 0)
            else:
                self.dir = 2
                self.rect = self.rect.move(10 * self.vy / self.fps, 0)
        # if pygame.sprite.spritecollideany(self, tank_sprites):
        #     for collis_sprite in tank_sprites:
        #         if collis_sprite != self:
        #
        #             if self.dir == 1:
        #                 collis_sprite.dir = 1
        #                 collis_sprite.rect = collis_sprite.rect.move(20 * collis_sprite.vx / collis_sprite.fps, 0)
        #                 self.dir = 2
        #                 self.rect = self.rect.move(-20 * self.vx / self.fps, 0)
        #             elif self.dir == 2:
        #                 collis_sprite.dir = 2
        #                 collis_sprite.rect = collis_sprite.rect.move(-20 * collis_sprite.vx / collis_sprite.fps, 0)
        #                 self.dir = 1
        #                 self.rect = self.rect.move(20 * self.vx / self.fps, 0)


class Player(pygame.sprite.Sprite):
    imgD = load_image('player_tank_down.png', 'white')
    imgU = load_image('player_tank_up.png', 'white')
    imgL = load_image('player_tank_left.png', 'white')
    imgR = load_image('player_tank_right.png', 'white')

    def __init__(self, x, y):
        super().__init__(all_sprites, player_sprites)
        self.image = Tank.imgD
        self.rect = self.image.get_rect()
        self.dir = 3
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.vx = 3
        self.vy = self.vx
        self.num = 0
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dir = 1
                self.rect.x -= 10
            elif event.key == pygame.K_RIGHT:
                self.dir = 2
                self.rect.x += 10
            elif event.key == pygame.K_UP:
                self.dir = 3
                self.rect.y -= 10
            elif event.key == pygame.K_DOWN:
                self.dir = 0
                self.rect.y += 10
            elif event.key == pygame.K_SPACE:
                BallPlayer(self.dir, self.rect.x + 10, self.rect.y + 10)

    def update(self):
        if self.dir == 0:
            self.image = self.imgD
            # self.rect = self.rect.move(0, 20 * self.vy / self.fps)
        elif self.dir == 3:
            self.image = self.imgU
            # self.rect = self.rect.move(0, -20 * self.vy / self.fps)
        elif self.dir == 1:
            self.image = self.imgL
            # self.rect = self.rect.move(-20 * self.vx / self.fps, 0)
        elif self.dir == 2:
            self.image = self.imgR
            # self.rect = self.rect.move(20 * self.vx / self.fps, 0)
        self.clock.tick(self.fps)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.dir == 0:
                self.rect = self.rect.move(0, -20 * self.vy / self.fps)
            else:
                self.rect = self.rect.move(0, 20 * self.vy / self.fps)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            if self.dir == 2:
                self.rect = self.rect.move(-20 * self.vy / self.fps, 0)
            else:
                self.rect = self.rect.move(20 * self.vy / self.fps, 0)
        if pygame.sprite.spritecollideany(self, brick_sprites):
            if self.dir == 0:
                self.rect = self.rect.move(0, -20 * self.vy / self.fps)
            elif self.dir == 3:
                self.rect = self.rect.move(0, 20 * self.vy / self.fps)
            elif self.dir == 2:
                self.rect = self.rect.move(-20 * self.vy / self.fps, 0)
            else:
                self.rect = self.rect.move(20 * self.vy / self.fps, 0)
        if pygame.sprite.spritecollideany(self, base_sprite):
            if self.dir == 0:
                self.rect = self.rect.move(0, -20 * self.vy / self.fps)
            elif self.dir == 3:
                self.rect = self.rect.move(0, 20 * self.vy / self.fps)
            elif self.dir == 2:
                self.rect = self.rect.move(-20 * self.vy / self.fps, 0)
            else:
                self.rect = self.rect.move(20 * self.vy / self.fps, 0)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def update(self):
        if pygame.sprite.spritecollide(self, balls_sprites, True):
            pass
        if pygame.sprite.spritecollide(self, balls_sprites, True):
            pass

tanks_coords = []

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'K':
                Tile('brick', x, y)
            elif level[y][x] == 'B':
                b = Tile('base', x, y)
                base_sprite.add(b)
            elif level[y][x] == 'T':
                Tile('empty', x, y)
                tanks_coords.append((x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = (x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'brick':
            super().__init__(brick_sprites, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollide(self, balls_sprites, True):
            print(pygame.sprite.spritecollide(self, balls_sprites, False))


# class Player(pygame.sprite.Sprite):
#     def __init__(self, pos_x, pos_y):
#         super().__init__(player_group, all_sprites)
#         self.image = player_image
#         self.rect = self.image.get_rect().move(
#             tile_width * pos_x + 15, tile_height * pos_y + 5)
def terminate():
    pygame.quit()
    sys.exit()


FPS = 50
clock = pygame.time.Clock()


def start_screen():
    intro_text = "CLICK TO START"
    font = pygame.font.Font(None, 30)
    cnt = 0
    string_rendered = font.render(intro_text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = width // 2 - 90
    intro_rect.y = height // 2 + 70

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        fon = pygame.transform.scale(load_image('fon_tanks.png'), (width, height))
        screen.blit(fon, (0, 0))
        if cnt % 10 == 0:
            string_rendered = font.render(intro_text, 1, pygame.Color('black'))
            screen.blit(string_rendered, intro_rect)
            pygame.time.wait(100)
        else:
            string_rendered = font.render(intro_text, 1, pygame.Color('white'))
            screen.blit(string_rendered, intro_rect)
            pygame.time.wait(100)
        cnt += 1

        pygame.display.flip()
        clock.tick(FPS)



def win_screen():
    wg = pygame.transform.scale(load_image('win_game.jpg'), (width, height))
    screen.blit(wg, (0, 0))
    pygame.display.flip()


def loose_screen():
    wg = pygame.transform.scale(load_image('game_over.jpg'), (width, height))
    screen.blit(wg, (0, 0))
    pygame.display.flip()


tile_images = {
    'wall': load_image('block.png'),
    'empty': load_image('black.png'),
    'grass': load_image('grass.png'),
    'brick': load_image('brick.png'),
    'base': load_image('base.png')
}
player_image = load_image('player_tank.png')
tile_width = tile_height = 50
# all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(tile_width, tile_height, width - tile_width, tile_height)
Border(tile_width, height - tile_height, width - tile_width, height - tile_height)
Border(tile_width, tile_height, tile_width, height - tile_height)
Border(width - tile_width, tile_height, width - tile_width, height - tile_height)

not_start_screen = True
start_screen()
v = 20  # пикселей в секунду
currentMap = 1
player_coords, level_x, level_y = generate_level(load_level('map0' + str(currentMap) + '.txt'))
not_start_screen = False
player = Player(player_coords[0], player_coords[1])
for el in tanks_coords:
    Tank(el[0], el[1])
running = True
cnt = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     board.get_click(event.pos)
    # в главном игровом цикле
        player.move(event)
    if not tank_sprites:
        if currentMap == 3:
            win_screen()
            time.sleep(5)
            break
        currentMap += 1
        tanks_coords = []
        tiles_group.empty()
        player_group.empty()
        player_coords, level_x, level_y = generate_level(load_level('map0' + str(currentMap) + '.txt'))
        player = Player(player_coords[0], player_coords[1])
        for el in tanks_coords:
            Tank(el[0], el[1])
    if not player_sprites:
        loose_screen()
        time.sleep(5)
        break
    if not base_sprite or not_start_screen:
        loose_screen()
        time.sleep(5)
        break
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    cnt += 1
pygame.quit()