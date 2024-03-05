import enum
import random
import pygame

available_pos = [25, 200, 375, 550]
player_score = 0

current_player_pos = 3
enemy_points = 0
enemies_on_screen = 0
game_round = 0
next_round = 0

bg = pygame.image.load('resources/images/backgrounds/main_town_gates.png')
enemy = pygame.transform.scale(pygame.image.load('resources/images/sprites/enemy.png'), (150, 150))
hero = pygame.transform.scale(pygame.image.load('resources/images/sprites/hero.png'), (150, 150))
gunman = pygame.transform.scale(pygame.image.load('resources/images/sprites/gunman.png'), (150, 150))
bullet = pygame.transform.scale(pygame.image.load('resources/images/sprites/bullet.png'), (150, 150))
hero_bullet = pygame.transform.scale(pygame.image.load('resources/images/sprites/bullet.png'), (150, 150))

class Road(enum.Enum):
    TOP = 25
    TOP_CENTRAL = 200
    LOWER_CENTRAL = 375
    LOWER = 550
    UNKNOWN = -999

    @staticmethod
    def getRandomRoad():
        return Road.index(random.randint(0, 3))

    def getMyFuckingInt(self):
        return self.value

    @staticmethod
    def index(index):
        data_array = [data.value for data in Road]
        return data_array[index]


class EnemyType(enum.Enum):

    HOSTILE_GUNMAN = [gunman, 1.2, 5]
    HOSTILE_ENEMY = [enemy, 1.5, 5]

    HOSTILE_BULLET = [bullet, 6.5, 0]
    HERO_BULLET = [hero_bullet, 6.5, 0]

    NONE = [0, 0, 0]

    @staticmethod
    def index(index):
        data_array = [data.value for data in EnemyType]
        return data_array[index]

    @staticmethod
    def getRandomEnemyType():
        return EnemyType.index(random.randint(0, 1))


class LivingEnemy:
    current_pos = 1600
    current_road = Road.UNKNOWN
    type = EnemyType.NONE

    def __init__(self, type, road):
        self.current_road = road
        self.type = type

class BulletEntity:
    current_pos = 100
    current_road = Road.UNKNOWN
    type = EnemyType.HERO_BULLET

    def __init__(self, road):
        self.current_road = road

enemy_queue = []
enemy_list = []
hero_bullet_list = []

pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

window_width, window_height = screen_width - 10, screen_height - 50
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

pygame.display.set_caption("I STILL HATE PYTHON")

x = 1600
frames = 0

running = True
while running:
    frames += 1

    screen.blit(bg, (-390, -150))
    screen.blit(hero, (100, Road.index(current_player_pos)))

    if game_round == next_round:
        enemy_points = 9.5 + (game_round * 2) + ((player_score + 1) / 10)
        while enemy_points > 0:
            chosen = random.randint(0, 1)
            if chosen == 0:
                enemy_queue.append(LivingEnemy(EnemyType.HOSTILE_ENEMY, Road.getRandomRoad()))
                enemy_points -= EnemyType.HOSTILE_ENEMY.value[2]
            if chosen == 1:
                enemy_queue.append(LivingEnemy(EnemyType.HOSTILE_GUNMAN, Road.getRandomRoad()))
                enemy_points -= EnemyType.HOSTILE_GUNMAN.value[2]
        next_round += 1

    length = len(enemy_queue)
    for i in range(0, length):
        if i < 2:
            hostile = enemy_queue.pop()
            enemy_list.append(hostile)

        else:
            break

    try:
        for i in range(0, len(enemy_list)):

            hostile = enemy_list[i]
            screen.blit(hostile.type.value[0], (hostile.current_pos, hostile.current_road))
            hostile.current_pos -= hostile.type.value[1]

            if hostile.type == EnemyType.HOSTILE_GUNMAN and frames % 350 == 0:
                hostile_bullet = (LivingEnemy(EnemyType.HOSTILE_BULLET, hostile.current_road))
                hostile_bullet.current_pos = hostile.current_pos
                enemy_list.append(hostile_bullet)

            if hostile.current_pos < -150:
                del enemy_list[i]

            if -20 <= hostile.current_pos <= 220 and hostile.current_road == Road.index(current_player_pos):
                running = False
                pygame.quit()
                break
    except:
        pass

    try:
        for i in range(0, len(hero_bullet_list)):
            bullet_entity = hero_bullet_list[i]
            screen.blit(bullet_entity.type.value[0], (bullet_entity.current_pos, bullet_entity.current_road))
            bullet_entity.current_pos += bullet_entity.type.value[1]

            if bullet_entity.current_pos >= 1579:
                del hero_bullet_list[i]

            for j in range(0, len(enemy_list)):
                hostile = enemy_list[j]

                if hostile.current_pos - 20 <= bullet_entity.current_pos and bullet_entity.current_road == hostile.current_road and hostile.type != EnemyType.HOSTILE_BULLET:
                    del enemy_list[j]
                    del hero_bullet_list[i]

    except:
        pass

    if len(enemy_list) == 0:
        game_round += 1

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and current_player_pos != 0:
                current_player_pos -= 1
            elif event.key == pygame.K_DOWN and current_player_pos != 3:
                current_player_pos += 1
            elif event.key == pygame.K_SPACE:
                hero_bullet_list.append(BulletEntity(Road.index(current_player_pos)))

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
