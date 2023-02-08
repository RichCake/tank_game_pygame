import os
import pprint
import sys
import time

import pygame

import random as rd
from collections import deque
import math

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_width(), screen.get_height()
clock = pygame.time.Clock()

FPS = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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

    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
            level_map_1, level_map_2 = level_map[:20], level_map[21:]
            level_map_1 = list(map(lambda x: x.split(';'), level_map_1))
            level_map_2 = list(map(lambda x: x.split(';'), level_map_2))
            return level_map_1, level_map_2
    except FileNotFoundError:
        print('файл не найден')
    return False


tile_images = {
    'grass_left_top': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_04.png'),
    'grass_top': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_05.png'),
    'grass_top_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_06.png'),
    'gray_left_top': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_07.png'),
    'gray_top': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_08.png'),
    'gray_top_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_09.png'),
    'light_grass_top': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_11.png'),
    'grass_left': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_16.png'),
    'grass': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_17.png'),
    'grass_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_18.png'),
    'gray_left': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_19.png'),
    'gray': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_20.png'),
    'gray_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_21.png'),
    'light_grass_left': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_22.png'),
    'light_grass': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_23.png'),
    'grass_bottom_left': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_28.png'),
    'grass_bottom': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_29.png'),
    'grass_bottom_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_30.png'),
    'gray_bottom': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_32.png'),
    'gray_bottom_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_33.png'),
    'light_grass_bottom': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_35.png'),
    'road_top_to_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_92.png'),
    'road_top_to_left': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_93.png'),
    'road_bottom_to_right':
        load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_101.png'),
    'road_left_to_right':
        load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_102.png'),
    'road_T_to_bottom': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_103.png'),
    'road_T_to_top': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_104.png'),
    'road_T_to_right': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_105.png'),
    'road_top_to_bottom':
        load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_113.png'),
    'road_T_to_left': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_114.png'),
    'road_left_to_bottom':
        load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/1 Tiles/Map_tile_117.png')
}
for item, key in enumerate(tile_images):
    tile_images[key] = pygame.transform.scale(tile_images[key], (128, 128))

tree_images = {
    'oak_1': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/1.png'),
    'oak_2': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/2.png'),
    'oak_3': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/3.png'),
    'birch_1': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/4.png'),
    'birch_2': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/5.png'),
    'birch_3': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/6.png'),
    'spruce_1': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/7.png'),
    'spruce_2': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/8.png'),
    'spruce_3': load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Trees/9.png'),
}
for item, key in enumerate(tree_images):
    tree_images[key] = pygame.transform.scale(tree_images[key],
                                              (tree_images[key].get_rect().w * 4, tree_images[key].get_rect().h * 4))

house_images = {
    1: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Houses/1.png'),
    2: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Houses/2.png'),
    3: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Houses/3.png'),
    4: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Houses/6.png'),
    5: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Houses/5.png'),
    # 6: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Houses/4.png'),
}
for item, key in enumerate(house_images):
    house_images[key] = pygame.transform.scale(house_images[key],
                                               (house_images[key].get_rect().w * 4, house_images[key].get_rect().h * 4))

grass_images = {
    1: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/1.png'),
    2: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/2.png'),
    3: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/3.png'),
    4: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/4.png'),
    5: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/5.png'),
    6: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/6.png'),
    7: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/7.png'),
    8: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/8.png'),
    9: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Grass/9.png'),
}
for item, key in enumerate(grass_images):
    grass_images[key] = pygame.transform.scale(grass_images[key],
                                               (grass_images[key].get_rect().w * 4, grass_images[key].get_rect().h * 4))

crystals_images = {
    1: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Crystals/1.png'),
    2: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Crystals/2.png'),
    3: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Crystals/3.png'),
    4: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Crystals/4.png'),
    5: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Crystals/5.png'),
    6: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Crystals/6.png'),
}
for item, key in enumerate(crystals_images):
    crystals_images[key] = pygame.transform.scale(crystals_images[key],
                                                  (crystals_images[key].get_rect().w * 2,
                                                   crystals_images[key].get_rect().h * 2))

ruins_images = {
    1: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Ruins/1_new.png'),
    2: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Ruins/2_new.png'),
    3: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Ruins/3_new.png'),
    4: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Ruins/4_new.png'),
    5: load_image('craftpix-net-280167-free-level-map-pixel-art-assets-pack/2 Objects/Ruins/5_new.png'),
}
for item, key in enumerate(ruins_images):
    ruins_images[key] = pygame.transform.scale(ruins_images[key],
                                               (ruins_images[key].get_rect().w * 4,
                                                ruins_images[key].get_rect().h * 4))

explosion_images = {
    1: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_A.png'),
    2: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_B.png'),
    3: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_C.png'),
    4: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_D.png'),
    5: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_E.png'),
    6: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_F.png'),
    7: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_G.png'),
    8: load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Explosion_H.png'),
}
for item, key in enumerate(explosion_images):
    explosion_images[key] = pygame.transform.scale(explosion_images[key], (128, 128))

shoot_sound = pygame.mixer.Sound('data/wot_mid.mp3')
shoot_sound.set_volume(0.125)

tank_model = pygame.transform.scale(load_image('tank_model.png'), (100, 100))

hull = pygame.transform.scale(load_image('Hull_01.png'), (128, 128))
weapon = pygame.transform.scale(
    load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Weapon_Color_A_256X256/Gun_01.png'), (128, 128))
shell_image = load_image('craftpix-901177-free-2d-battle-tank-game-assets/PNG/Effects/Light_Shell.png')

tile_width = tile_height = TILE = 128
TILE_X = TILE_Y = 20

cols = rows = 20

spawn_points = []

obstacles = [[0] * 20 for i in range(20)]

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
road_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
shell_group = pygame.sprite.Group()
effects_proup = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def clear_sprites():
    all_sprites.empty()
    tiles_group.empty()
    road_group.empty()
    objects_group.empty()
    shell_group.empty()
    player_group.empty()
    effects_proup.empty()


def start_screen():
    intro_text = ["ТАНКИ", "",
                  "Правила игры:",
                  "Перемещение: W A S D",
                  "Стрельба: кнопка мыши",
                  "Поворот: движение мышкой",
                  "Задача игры: победить всех врагов. Всего 3 уровня"]

    fon = pygame.transform.scale(load_image('start_screen.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(FPS)


def win_screen(results):
    count = 0
    time_to_wait = FPS * 3
    text = [("ПОБЕДА", pygame.Color('darkgreen'), pygame.font.Font(None, 50)),
            ("", pygame.Color('black'), pygame.font.Font(None, 30)),
            ("Нажмите любую клавишу для перехода к следующему уровню", pygame.Color('black'), pygame.font.Font(None, 30))]
    fon = pygame.transform.scale(load_image('win_screen.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 50
    for line, color, font in text:
        string_rendered = font.render(line, True, color)
        intro_rect = string_rendered.get_rect()
        intro_rect.centerx = width // 2
        intro_rect.y = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 30)
    color = pygame.Color('black')
    for name, number in results.items():
        line = f'{name}: {number}'
        string_rendered = font.render(line, True, color)
        intro_rect = string_rendered.get_rect()
        intro_rect.centerx = width // 2
        intro_rect.y = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN and count >= time_to_wait:
                return False
        count += 1
        pygame.display.flip()
        clock.tick(FPS)


def defeat_screen(results):
    count = 0
    time_to_wait = FPS * 3
    text = [("ПОРАЖЕНИЕ", pygame.Color('darkred'), pygame.font.Font(None, 50)),
            ("", pygame.Color('black'), pygame.font.Font(None, 30)),
            ("Нажмите любую клавишу для новой попытки", pygame.Color('black'),
             pygame.font.Font(None, 30))]
    fon = pygame.transform.scale(load_image('defeat_screen.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 50
    for line, color, font in text:
        string_rendered = font.render(line, True, color)
        intro_rect = string_rendered.get_rect()
        intro_rect.centerx = width // 2
        intro_rect.y = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(None, 30)
    color = pygame.Color('black')
    for name, number in results.items():
        line = f'{name}: {number}'
        string_rendered = font.render(line, True, color)
        intro_rect = string_rendered.get_rect()
        intro_rect.centerx = width // 2
        intro_rect.y = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN and count >= time_to_wait:
                return False
        count += 1
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    count = 0
    time_to_wait = FPS * 3
    text = [("ВЫ ПРОШЛИ ВСЕ УРОВНИ", pygame.Color('darkgreen'), pygame.font.Font(None, 50)),
            ("", pygame.Color('black'), pygame.font.Font(None, 30)),
            ("Нажмите любую клавишу для начала игры сначала", pygame.Color('black'),
             pygame.font.Font(None, 30))]
    fon = pygame.transform.scale(load_image('end_screen.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 50
    for line, color, font in text:
        string_rendered = font.render(line, True, color)
        intro_rect = string_rendered.get_rect()
        intro_rect.centerx = width // 2
        intro_rect.y = text_coord
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN and count >= time_to_wait:
                return True
        count += 1
        pygame.display.flip()
        clock.tick(FPS)


def start_level(number_of_tanks):
    generate_level(load_level('map_midleburg'))

    tanks = generete_player_enemy(spawn_points, n=number_of_tanks)

    player, *enemys = tanks

    shells = []
    explosions = []

    camera = Camera()

    if number_of_tanks <= 2:
        running = start_screen()
    else:
        running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.velocity_y = -player.velocity
                if event.key == pygame.K_s:
                    player.velocity_y = player.velocity
                if event.key == pygame.K_d:
                    player.velocity_x = player.velocity
                if event.key == pygame.K_a:
                    player.velocity_x = -player.velocity
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity_y = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.velocity_x = 0
            elif event.type == pygame.MOUSEMOTION:
                player.rotate_weapon(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shell = player.shoot()
                if shell is not None:
                    shells.append(shell)
        for enemy in enemys:
            if 0 <= enemy.rect.x <= screen.get_width() and 0 <= enemy.rect.y <= screen.get_height() and player.groups() \
                    and enemy.groups():
                enemy.rotate_weapon((player.rect.x + 50, player.rect.y + 50))
                shell = enemy.shoot()
                if shell is not None:
                    shells.append(shell)

        for tank in tanks:
            tank.reload()
            explosion, con = tank.collision()
            if explosion:
                explosions.append(explosion)
                if con:
                    pprint.pprint(player.result)
                    if tank.__class__.__name__ == 'Tank':
                        player.result['Полученный урон'] += player.damage
                    else:
                        player.result['Нанесенный урон''Полученный урон'] += player.damage

        for shell in shells:
            shell.throw()
            explosion = shell.collision()
            if explosion:
                shell.delete()
                explosions.append(explosion)
        for explosion in explosions:
            explosion.update()

        player.rotate(player.velocity_x, player.velocity_y)
        player.move(player.velocity_x, player.velocity_y)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill((0, 180, 255))
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        road_group.draw(screen)
        objects_group.draw(screen)
        shell_group.draw(screen)
        player_group.draw(screen)
        effects_proup.draw(screen)
        for tank in tanks:
            if tank.groups():
                tank.draw_health_bar(screen)
                if tank.__class__ == Enemy:
                    tank.move_square()
        clock.tick(FPS)
        pygame.display.flip()

        killed_enemys = 0
        for enemy in enemys:
            if not enemy.groups():
                killed_enemys += 1
        if killed_enemys >= number_of_tanks - 1:
            time.sleep(1)
            running = win_screen(player.result)
            clear_sprites()
            if number_of_tanks >= 4:
                time.sleep(1)
                new_game = end_screen()
                if new_game:
                    start_level(2)
            start_level(number_of_tanks + 1)
        if not player.groups():
            time.sleep(1)
            running = defeat_screen(player.result)
            clear_sprites()
            start_level(number_of_tanks)


def generete_player_enemy(spawn_points, n=2):
    player = Tank(*spawn_points.pop(rd.randint(0, len(spawn_points) - 1)))
    enemys = [Enemy(*spawn_points.pop(rd.randint(0, len(spawn_points) - 1))) for i in range(n - 1)]
    return player, *enemys


def generate_level(level):
    level_1, level_2 = level
    for y in range(len(level_1)):
        for x in range(len(level_1[y])):
            if level_1[y][x] == 'g':
                Tile('grass', x, y)
                Grass(x, y)
            elif level_1[y][x] == 'glt':
                Tile('grass_left_top', x, y)
            elif level_1[y][x] == 'gt':
                Tile('grass_top', x, y)
            elif level_1[y][x] == 'gtr':
                Tile('grass_top_right', x, y)
            elif level_1[y][x] == 'gt':
                Tile('grass_top', x, y)
            elif level_1[y][x] == 'gtl':
                Tile('grass_left_top', x, y)
            elif level_1[y][x] == 'gl':
                Tile('grass_left', x, y)
            elif level_1[y][x] == 'gr':
                Tile('grass_right', x, y)
            elif level_1[y][x] == 'glb':
                Tile('grass_bottom_left', x, y)
            elif level_1[y][x] == 'gbr':
                Tile('grass_bottom_right', x, y)
            elif level_1[y][x] == 'gb':
                Tile('grass_bottom', x, y)
            elif level_1[y][x] == 'lg':
                Tile('light_grass', x, y)
            elif level_1[y][x] == 'lgt':
                Tile('light_grass_top', x, y)
            elif level_1[y][x] == 'lgb':
                Tile('light_grass_bottom', x, y)
            elif level_1[y][x] == 'gray':
                Tile('gray', x, y)
            elif level_1[y][x] == 'grayt':
                Tile('gray_top', x, y)
            elif level_1[y][x] == 'grayr':
                Tile('gray_right', x, y)
            elif level_1[y][x] == 'grayb':
                Tile('gray_bottom', x, y)
            elif level_1[y][x] == 'graytr':
                Tile('gray_top_right', x, y)
            elif level_1[y][x] == 'graybr':
                Tile('gray_bottom_right', x, y)
    for y in range(len(level_2)):
        for x in range(len(level_2[y])):
            if level_2[y][x] == 'rttb':
                Tile('road_top_to_bottom', x, y)
            elif level_2[y][x] == 'rttr':
                Tile('road_top_to_right', x, y)
            elif level_2[y][x] == 'rttl':
                Tile('road_top_to_left', x, y)
            elif level_2[y][x] == 'rbtr':
                Tile('road_bottom_to_right', x, y)
            elif level_2[y][x] == 'rltr':
                Tile('road_left_to_right', x, y)
            elif level_2[y][x] == 'rTtb':
                Tile('road_T_to_bottom', x, y)
            elif level_2[y][x] == 'rTtl':
                Tile('road_T_to_left', x, y)
            elif level_2[y][x] == 'rTtt':
                Tile('road_T_to_top', x, y)
            elif level_2[y][x] == 'rltb':
                Tile('road_left_to_bottom', x, y)
            elif level_2[y][x] == 'h':
                House(x, y)
                obstacles[y][x] = 1
            elif level_2[y][x] == 'crys':
                Crystal(x, y)
                obstacles[y][x] = 1
            elif level_2[y][x] == 'rns1':
                Ruin(1, x, y)
                obstacles[y][x] = 1
            elif level_2[y][x] == 'rns2':
                Ruin(2, x, y)
                obstacles[y][x] = 1
            elif level_2[y][x] == 'rns3':
                Ruin(3, x, y)
                obstacles[y][x] = 1
            elif level_2[y][x] == 'rns4':
                Ruin(4, x, y)
                obstacles[y][x] = 1
            elif level_2[y][x] == 'rns5':
                Ruin(5, x, y)
                obstacles[y][x] = 1
            elif level_2[y][x] == '@':
                spawn_points.append((x, y))
    for y in range(len(level_2)):
        for x in range(len(level_2[y])):
            if level_2[y][x] == 'to':
                Tree('oak', x, y)
            elif level_2[y][x] == 'tb':
                Tree('birch', x, y)


def blitRotate(surf, image, pos, originPos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)


def check_next_node(x, y):
    if 0 <= x < cols and 0 <= y < rows and not obstacles[y][x]:
        return True
    return False


def get_next_nodes(x, y):
    # check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not obstacles[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Ruin(pygame.sprite.Sprite):
    def __init__(self, r_type, pos_x, pos_y):
        super().__init__(objects_group, all_sprites)
        self.image = ruins_images[r_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Crystal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(objects_group, all_sprites)
        self.image = crystals_images[rd.randint(1, 6)]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class House(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(objects_group, all_sprites)
        self.image = house_images[rd.randint(1, 5)]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Grass(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = grass_images[rd.randint(1, 9)]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + rd.random() * tile_width, tile_height * pos_y + rd.random() * tile_height)


class Tree(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(objects_group, all_sprites)
        self.image = tree_images[tile_type + '_' + str(rd.randint(1, 3))]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + rd.random() * tile_width, tile_height * pos_y + rd.random() * tile_height)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super(Explosion, self).__init__(all_sprites, effects_proup)
        self.cur_frame = 1
        self.image = explosion_images[self.cur_frame]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.update()

    def update(self):
        self.image = explosion_images[self.cur_frame // 1]
        if self.cur_frame < 8:
            self.cur_frame += 1
        else:
            self.kill()


class Shell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, angle, dam, sender):
        super().__init__(shell_group, all_sprites)
        self.image = shell_image
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle + 90
        dx = dy = 180
        self.rect = self.image.get_rect().move(pos_x + math.cos(math.radians(self.angle)) * dx,
                                               pos_y + -math.sin(math.radians(self.angle)) * dy)
        self.sender = sender
        self.damage = dam
        self.velocity = 450

    def throw(self):
        self.image = pygame.transform.rotate(shell_image, self.angle - 90)
        if self.angle:
            x_vel = self.velocity * math.cos(math.radians(self.angle)) // FPS
            y_vel = -self.velocity * math.sin(math.radians(self.angle)) // FPS
            self.rect = self.rect.move(x_vel, y_vel)

    def collision(self):
        obj = pygame.sprite.spritecollide(self, objects_group, dokill=True)
        if obj:
            obj = obj[0]
            exp = Explosion(obj.rect.x, obj.rect.y)
            self.delete()
            return exp

    def delete(self):
        self.velocity = 0
        self.rect = self.rect.move(-1000, -1000)
        self.kill()


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.angle = 0
        # self.tank_screen = pygame.Surface(hull.get_size())
        # self.hull = hull
        # print(type(self.hull))
        # self.weapon = weapon
        # print(type(self.weapon))
        # self.image = weapon.blit(hull, (0, 0))
        # print(type(self.image))
        self.image = tank_model
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x, self.y = self.rect.x // tile_width, self.rect.y // tile_height
        self.pos_x, self.pos_y = self.rect.x, self.rect.y
        self.velocity = 5
        self.hp = 3150
        self.damage = 310

        self.result = {
            'Нанесенный урон': 0,
            'Полученный урон': 0
        }

        self.time_to_reload = FPS * 0.5
        self.reloading_time = self.time_to_reload

        self.velocity_x = 0
        self.velocity_y = 0

        self.i = -1

    def delete(self):
        self.velocity = 0
        self.rect = self.rect.move(-1000, -1000)
        self.kill()

    def collision(self):
        obj = pygame.sprite.spritecollide(self, objects_group, dokill=True)
        if obj:
            obj = obj[0]
            return Explosion(obj.rect.x, obj.rect.y), False
        if pygame.sprite.spritecollide(self, shell_group, True):
            self.hp -= self.damage
            # if self.__class__ == Tank:
            #     self.result['Полученный урон'] += self.damage
            if self.hp <= 0:
                self.delete()
            return Explosion(self.rect.x, self.rect.y), True
        return None, None

    def move(self, x, y):
        if 0 <= self.pos_x + x <= TILE_X * TILE and 0 <= self.pos_y + y <= TILE_Y * TILE:
            self.pos_x += x
            self.pos_y += y
            self.rect = self.rect.move(x, y)

    # def move_to_cell(self, road):
    #     x_cell, y_cell = road[self.i]
    #     print(f'x_cell, y_cell: {x_cell, y_cell}')
    #     x, y = self.get_coords()
    #     print(f'x_pos, y_pos: {self.pos_x / TILE, self.pos_y / TILE, self.pos_x // TILE, self.pos_y // TILE}')
    #     dx, dy = (x_cell - x), (y_cell - y)
    #     print(f'dx, dy: {dx, dy}')
    #     self.velocity_x = dx * self.velocity
    #     self.velocity_y = dy * self.velocity
    #     print(self.pos_x // TILE == x_cell, self.pos_y // TILE == y_cell, -self.i <= len(road))
    #     if self.pos_x // TILE == x_cell and self.pos_y // TILE == y_cell and -self.i <= len(road):
    #         self.x += dx
    #         self.x += dy
    #         self.i -= 1
    #     print()

    def get_coords(self):
        return self.x, self.y

    def rotate(self, vel_x, vel_y):
        angle = False
        if vel_x > 0 and vel_y > 0:
            angle = 225
        elif vel_x > 0 and vel_y < 0:
            angle = 315
        elif vel_x < 0 and vel_y > 0:
            angle = 135
        elif vel_x < 0 and vel_y < 0:
            angle = 45
        elif vel_x > 0:
            angle = -90
        elif vel_x < 0:
            angle = 90
        elif vel_y > 0:
            angle = 180
        elif vel_y < 0:
            angle = 0
        elif vel_x > 0 and vel_y > 0:
            angle = 45

        if angle is not False:
            self.image = pygame.transform.rotate(tank_model, angle)

    def road_to_target(self, target):
        graph = {}
        for y, row in enumerate(obstacles):
            for x, col in enumerate(row):
                if not col:
                    graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

        start = self.get_coords()
        print(start)
        goal = start
        queue = deque([start])
        visited = {start: None}

        if target and not obstacles[target[1]][target[0]]:
            queue, visited = bfs(start, target, graph)
            goal = target

        path_head, path_segment = goal, goal
        road = []
        while path_segment and path_segment in visited:
            road.append(path_segment)
            # x_node, y_node = path_segment[0], path_segment[1]
            # x_pos, y_pos = self.get_coords()[0], self.get_coords()[1]
            # dx, dy = (x_node - x_pos) * TILE, (y_node - y_pos) * TILE
            # road.append((dx, dy))
            # self.move(dx, dy)
            # print(self.get_coords())
            path_segment = visited[path_segment]
        print(road[::1])
        return road[::1]

    def rotate_weapon(self, mouse_pos, angle=0):
        w_dx, w_dy = 64, 87
        m_x, m_y = mouse_pos
        if angle == 0:
            w_x, w_y = self.rect.x + w_dx, self.rect.y + w_dy
            a = m_x - w_x
            b = m_y - w_y
            if b != 0:
                if b < 0:
                    angle = int(math.degrees(math.atan(a/b)))
                else:
                    angle = int(math.degrees(math.atan(a/b) - math.pi))
                # print(angle)
                self.angle = angle
                # print(screen, tank_model, (self.rect.x, self.rect.y), (w_dx, w_dy), angle, end='\n')
                # blitRotate(screen, tank_model, (self.rect.x, self.rect.y), (w_dx, w_dy), angle)
                self.image = pygame.transform.rotate(tank_model, angle)

    def shoot(self):
        if self.reloading_time >= self.time_to_reload:
            self.reloading_time = 0
            shoot_sound.play()
            w_x, w_y = self.rect.x, self.rect.y
            return Shell(w_x, w_y, self.angle, self.damage, self)

    def reload(self):
        if self.reloading_time <= self.time_to_reload:
            self.reloading_time += 60 // FPS

    def draw_health_bar(self, screen):
        # Get the self rect and size
        rect = self.rect
        width = rect.width // 2
        height = rect.height // 4

        # Calculate the position of the health bar
        bar_x = rect.centerx - width // 2
        bar_y = rect.y - height

        # Create a new surface with alpha channel
        health_bar = pygame.Surface((width, height), pygame.SRCALPHA)

        # Fill the surface with a transparent color
        health_bar.fill((0, 255, 0, 128))

        # Blit the health bar surface to the screen
        screen.blit(health_bar, (bar_x, bar_y))

        # Create a new surface with alpha channel for the border
        border = pygame.Surface((width + 2, height + 2), pygame.SRCALPHA)

        # Fill the surface with a transparent color
        border.fill((0, 0, 0, 128))

        # Draw the border rectangle on the border surface
        pygame.draw.rect(border, (0, 0, 0), (0, 0, width + 2, height + 2), 2)

        # Blit the border surface to the screen
        screen.blit(border, (bar_x - 1, bar_y - 1))

        # Get the font and render the text for the HP
        font = pygame.font.Font(None, height)
        text = font.render(str(self.hp), True, (0, 0, 0))

        # Center the text inside the health bar rectangle
        text_rect = text.get_rect()
        text_rect.centerx = bar_x + width / 2
        text_rect.centery = bar_y + height / 2

        # Blit the text to the screen
        screen.blit(text, text_rect)

        # Get the font and render the text for the reloading time
        font = pygame.font.Font(None, height - 10)
        rel = f"{self.reloading_time / 60:.1f}"
        if self.reloading_time >= self.time_to_reload:
            color = pygame.Color('darkgray')
        else:
            color = pygame.Color('darkred')
        text = font.render(rel, True, color)

        # Get the text rectangle and calculate the position
        text_rect = text.get_rect()
        text_x = bar_x - text_rect.width - height
        text_y = bar_y + height / 2 - text_rect.height / 2

        # Blit the text to the screen
        screen.blit(text, (text_x, text_y))


class Enemy(Tank):
    def __init__(self, pos_x, pos_y):
        super(Enemy, self).__init__(pos_x, pos_y)
        self.velocity = 2
        self.time_to_reload = FPS * 2
        self.c = True
        self.direction = "right"
        self.square_side = 500
        self.pos_x, self.pos_y = self.rect.x, self.rect.y

    def move_square(self):
        # Check the current direction
        if self.direction == "right":
            self.move(self.velocity, 0)
            if self.pos_x >= self.square_side:
                self.direction = "down"
        elif self.direction == "down":
            self.move(0, self.velocity)
            if self.pos_y >= self.square_side:
                self.direction = "left"
        elif self.direction == "left":
            self.move(-self.velocity, 0)
            if self.pos_x <= 0:
                self.direction = "up"
        elif self.direction == "up":
            self.move(0, -self.velocity)
            if self.pos_y <= 0:
                self.direction = "right"

    def move_to_cell(self, x_cell, y_cell):
        if self.c:
            # self.c = False
            print(f'x_cell, y_cell: {x_cell, y_cell}')
            x, y = self.get_coords()
            print(f'x_pos, y_pos: {self.pos_x, self.pos_y, self.pos_x // TILE, self.pos_y // TILE}')
            dx, dy = (x_cell - x), (y_cell - y)
            print(f'x, y: {x, y}')
            print(f'dx, dy: {dx, dy}')
            self.move(dx * TILE, dy * TILE)
            self.x += dx
            self.y += dy
            print()
            clock.tick(10)
        # self.velocity_x = dx * TILE
        # self.velocity_y = dy * TILE
        # if (self.c == TILE // self.velocity or (x_cell == self.pos_x // TILE and y_cell == self.pos_y // TILE)) \
        #         and -self.i <= len(road):
        # self.x += dx
        # self.x += dy
        # self.i -= 1
        # print()


if __name__ == '__main__':
    start_level(2)
