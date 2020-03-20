import pygame


#display mode

WIDTH = 600
HEIGHT = 800
gameTitle = 'Platformer!'
#FPS

FPS = 60
FONT_NAME = 'leelawadeeuisemilight'
HS_SCORE = 'score.txt'
SPRITESHEET = 'sprites.png'
#player
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.06
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 22

PLATFORM_LIST = [(0, HEIGHT - 40),
                 (WIDTH // 2 - 30, HEIGHT *3 /4),
                 (WIDTH // 2, HEIGHT -350),
                 (WIDTH - 200, HEIGHT -300),
                 (WIDTH // 2, HEIGHT - 700),
                 (WIDTH // 2, HEIGHT - 500)


]

#colors
LIGHT_BLUE = (218, 245, 241)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)
SWAMP = (87, 128, 122)