import pygame


# display mode

WIDTH = 600
HEIGHT = 800
gameTitle = "Platformer!"
# FPS

FPS = 60
FONT_NAME = "leelawadeeuisemilight"
HS_SCORE = "score.txt"
SPRITESHEET = "sprites.png"
BCK = "START.png"
MOB_SPRITES = "mobsprites.png"
MISC_SPRITES = "trees.png"
JUMP_SPRITES = "jumps.png"
# player
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.06
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 22  # 22
# powerupszzzz
MAX_HEALTH = 3
FAN_BOOST_POWER = 40
POWERUP_FREQ = 5  # 5
MOB_FREQ = 1  # 5
CLOUD_FREQ = 1
MOVE_PLAT_CHANCE = 3

PLAYER_LAYER = 5
TREE_LAYER = 6
PLATFORM_LAYER = 4
POWERUP_LAYER = 4
MOB_LAYER = 5
MISC_LAYER = 3
CLOUD_LAYER = 2
BACKGROUND_LAYER = 1
HEALTH_LAYER = 7


PLATFORM_LIST = [
    (0, HEIGHT - 60, 3),
    (WIDTH // 2 - 30, HEIGHT * 3 / 4, 3),
    (WIDTH // 2, HEIGHT - 350, 3),
    (WIDTH - 200, HEIGHT - 300, 3),
    (WIDTH // 2, HEIGHT - 700, 3),
    (WIDTH // 2, HEIGHT - 500, 3),
    (WIDTH - 356, HEIGHT - 965, 3),
    (200, HEIGHT - 800, 3),
]

# colors
LIGHT_BLUE = (183, 241, 247)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
SWAMP = (87, 128, 122)
RED = (255, 0, 0)
LIME = (0, 255, 0)
VIOLET = (94, 3, 252)
PINK = (215, 3, 252)
GREEN = (3, 252, 161)

# FIRE
ORANGE = (235, 122, 52)
YORANGE = (235, 162, 52)
