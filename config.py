import math

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

SHOUT_DISTANCE = 100
ANT_SIZE = 2
N_ANTS = 700
MIN_DISTANCE_FROM_BORDER = 10
N_TARGET_TYPES = 4  # 1 food target and 1 queen target
target_colors = [YELLOW, BLUE, RED, GREEN, MAGENTA]
queen_health_color = ORANGE
N_TARGETS = (N_TARGET_TYPES - 1) * 3
TARGET_START_SIZE = 25
TARGET_ACCELERATION = 50
ANT_SPEED = 250
ANT_SPEED_NOISE = 0.1
ANT_DIRECTION_NOISE = math.pi / 90
TARGET_HEALTH = 1000
CHANCE_TO_SHOUT = 0.003
CHANCE_TO_QUEEN = 0.0001
MARGIN_TO_QUEEN = 0.3
QUEEN_START_HEALTH = 300
QUEEN_LOSE_HEALTH_CHANCE = 1

DELETE_TARGET_MARGIN = 4  # determines when targets deletes itself (so if 4 and start target size = 40 in deletes at size 10)
ACTUAL_HEALTH = TARGET_HEALTH * (1 - 1 / DELETE_TARGET_MARGIN)

FPS = 60
HEIGHT = 900
WIDTH = 1600


def update():
    '''
    updates config.py with user inputs
    '''
    global N_ANTS, N_TARGET_TYPES, N_TARGETS, TARGET_HEALTH, MARGIN_TO_QUEEN, QUEEN_START_HEALTH
    with open('user_settings.txt') as f:
        arr = [int(i.split(':')[1][:-1]) for i in f.readlines()]
        N_ANTS = arr[0]
        N_TARGET_TYPES = arr[2]
        N_TARGETS = (N_TARGET_TYPES - 1) * arr[1]
        TARGET_HEALTH = arr[3]
        MARGIN_TO_QUEEN = arr[4] / 10
        QUEEN_START_HEALTH = arr[5]
