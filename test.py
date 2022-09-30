from enum import Flag
from tabnanny import check
import pygame

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (1920, 1080)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

player_image = pygame.image.load("images/player.png").convert_alpha()
grass_image = pygame.image.load("images/grass.png").convert()
dirt_image = pygame.image.load("images/dirt.png").convert()
enemy_image = pygame.image.load("images/enemy.png").convert()
ENEMY_SIZE = enemy_image.get_width()

TILE_SIZE = grass_image.get_width()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = player_image
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())
        self.hit_list = []
        self.collision_types = {"top": False, "bottom": False,
                                "right": False, "left": False}
        self.movement = [0, 0]
        self.moving_right = False
        self.moving_left = False
        self.movespeed = 0.5
        self.maxspeed = 5
        self.air_timer = 0
        self.y_momentum = 0
        self.collided_with = []
        self.enemy = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = enemy_image
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())
        self.hit_list = []
        self.collision_types = {"top": False, "bottom": False,
                                "right": False, "left": False}
        self.movement = [0, 0]
        self.moving_right = False
        self.moving_left = False
        self.movespeed = 0.2
        self.maxspeed = 2

        self.y_momentum = 0
        self.air_timer = 0

        self.enemy = True

        self.collided_with = []

    def move_to_player(self, player_x):
        if player_x > self.rect.x:
            self.moving_right = True
            self.moving_left = False
        else:
            self.moving_left = True
            self.moving_right = False


player = Player(1550, 350)
enemy_coordinates = [(1350, 350), (2050, 350), (1000, 350)]

entities = []
entities.append(player)
for coordinate in enemy_coordinates:
    entities.append(Enemy(coordinate[0], coordinate[1]))


def load_map(path):
    f = open(path + ".txt", "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))

    return game_map


def check_collision(entities, tiles):
    for entity in entities:
        entity.hit_list = []

    for tile in tiles:
        for entity in entities:
            if entity.rect.colliderect(tile):
                entity.hit_list.append(tile)
    for i, entity in enumerate(entities):
        for j, entity_2 in enumerate(entities):
            if entities[i] != entity_2 and entity not in entity_2.collided_with:
                if entity.rect.colliderect(entity_2.rect):
                    entity.hit_list.append(entity_2.rect)
                    entity.collided_with.append(entity_2.rect)


def move(entities, tiles):
    for entity in entities:
        entity.rect.x += entity.movement[0]
        entity.collision_types = {"top": False, "bottom": False,
                                  "right": False, "left": False}
    check_collision(entities, tiles)
    for entity in entities:
        for tile in entity.hit_list:
            if entity.movement[0] > 0:
                entity.rect.right = tile.left
                entity.collision_types["right"] = True
            elif entity.movement[0] < 0:
                entity.rect.left = tile.right
                entity.collision_types["left"] = True

    for entity in entities:
        entity.rect.y += entity.movement[1]
    check_collision(entities, tiles)
    for entity in entities:
        for tile in entity.hit_list:
            if entity.movement[1] > 0:
                entity.rect.bottom = tile.top
                entity.collision_types["bottom"] = True
                entity.y_momentum = 0
                entity.air_timer = 0

            elif entity.movement[1] < 0:
                entity.rect.top = tile.bottom
                entity.collision_types["top"] = True
                entity.y_momentum = 0

    for i, entity in enumerate(entities):
        if entity != player:
            if entity in player.collided_with:
                entities.pop(i)


game_map = load_map("maps/map_1")

true_scroll = [0, 0]

counter_x = 0
counter_y = 0

ac_x = 0
ac_y = 0

place_char = ""


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_w:
                if player.air_timer < 6:
                    player.y_momentum = -6
                    # print(player.air_timer)

            if event.key == pygame.K_e:
                actual_lst = ""
                length = 1
                actual_counter = 0
                f = open("maps/map_1.txt", "r")
                data = f.read()
                data_split = data.split("\n")
                f.close
                lst = []
                for char in data:
                    lst.append(char)
                for row in data_split:
                    for char in row:
                        length += 1
                    break

                actual_counter = counter_x + counter_y * length
                lst[actual_counter] = place_char
                for char in lst:
                    actual_lst += char

                f = open("maps/map_1.txt", "w")
                f.write(actual_lst)
                f.close()
                game_map = load_map("maps/map_1")
            if event.key == pygame.K_i:
                counter_y -= 1
                print(counter_x, counter_y)
            if event.key == pygame.K_k:
                counter_y += 1
                print(counter_x, counter_y)
            if event.key == pygame.K_j:
                counter_x -= 1
                print(counter_x, counter_y)
            if event.key == pygame.K_l:
                counter_x += 1
                print(counter_x, counter_y)
            if event.key == pygame.K_1:
                place_char = "x"
            if event.key == pygame.K_2:
                place_char = "m"
            if event.key == pygame.K_3:
                place_char = "-"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_a:
                player.moving_left = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            '''for entity in entities:
                print(entity.hit_list)'''
            print(player.collision_types)

    true_scroll[0] += (player.rect.x - true_scroll[0] -
                       (WINDOW_SIZE[0] // 4 - 50 // 4)) / 20
    true_scroll[1] += (player.rect.y - true_scroll[1] -
                       (WINDOW_SIZE[1] // 4 - 100 // 4)) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    screen.fill(((146, 244, 255)))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == "x":
                screen.blit(dirt_image, (x * TILE_SIZE -
                                         scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == "m":
                screen.blit(grass_image, (x * TILE_SIZE -
                                          scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != "-":
                tile_rects.append(pygame.Rect(
                    x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            x += 1
        y += 1

    for entity in entities:

        if entity.enemy == True:
            entity.move_to_player(entities[0].rect.x)

        if not entity.collision_types["bottom"]:
            entity.air_timer += 1

        if entity.moving_left:
            if -entity.maxspeed < entity.movement[0]:
                if entity.movement[0] > 0:
                    entity.movement[0] = 0
                entity.movement[0] -= entity.movespeed
        if entity.moving_right:
            if entity.maxspeed > entity.movement[0]:
                if entity.movement[0] < 0:
                    entity.movement[0] = 0
                entity.movement[0] += entity.movespeed

        entity.movement[1] = 0

        entity.movement[1] += entity.y_momentum
        entity.y_momentum += 0.2
        if entity.y_momentum > 3:
            entity.y_momentum = 3

        if not entity.moving_left and not entity.moving_right:
            if entity.movement[0] > 0:
                entity.movement[0] -= entity.movespeed
            elif entity.movement[0] < 0:
                entity.movement[0] += entity.movespeed

    move(entities, tile_rects)

    for entity in entities:
        screen.blit(entity.image, (entity.rect.x -
                    scroll[0], entity.rect.y - scroll[1]))

    ac_x = counter_x * TILE_SIZE
    ac_y = counter_y * TILE_SIZE
    pygame.draw.line(screen, (0, 0, 0), (ac_x - scroll[0], ac_y - scroll[1]),
                     (player.rect.x - scroll[0], player.rect.y - scroll[1]))

    pygame.display.update()
    clock.tick(60)
