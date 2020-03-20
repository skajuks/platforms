from settings import *
import pygame as pg
from random import choice


vc = pg.math.Vector2

class Spritesheet:
    #utility for images
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        image = pg.transform.scale(image, (width * 2 - 10, height * 2 - 10))
        return image
    def get_platform(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        image = pg.transform.scale(image, (width // 2 - 20, height // 2 - 20))
        return image

class Player(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.pos = vc(20, HEIGHT - 100)
        self.vel = vc(0,0)
        self.acc = vc(0,0)



    def update(self):
        self.animate()
        self.acc = vc(0,PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[ord('a')]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[ord('d')]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION  #friction
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        #wrapper
        if self.pos.x > WIDTH + self.rect.width // 2:
            self.pos.x = 0 - self.rect.width // 2
        if self.pos.x < 0 - self.rect.width // 2:
            self.pos.x = WIDTH + self.rect.width // 2

        self.rect.midbottom = self.pos

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            self.game.jump_sound.play()  

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -1:
                self.vel.y = -1
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(104,198,23,24),
                                self.game.spritesheet.get_image(103,224,23,24),
                                self.game.spritesheet.get_image(128,224,23,25),
                                self.game.spritesheet.get_image(78,224,23,26),
                                self.game.spritesheet.get_image(153,228,23,25)
        ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(79,198,23,24),
                              self.game.spritesheet.get_image(53,224,23,24),
                              self.game.spritesheet.get_image(0,198,25,24),
                              self.game.spritesheet.get_image(27,198,24,24),
                              #self.game.spritesheet.get_image(106,96,24,24),
                              self.game.spritesheet.get_image(0,224,25,24)
                              ]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)                      
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)      
        self.jump_frame = self.game.spritesheet.get_image(76,81,23,28)
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False 
        if self.walking:            # MOVEMENT ANIMATE
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:    
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:       # IDLE PLAYER ANIMATE
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            bottom = self.rect.bottom
            if self.vel.y < 0:
                self.image = self.game.spritesheet.get_image(153,198,23,28)
            else:  
                self.image = self.game.spritesheet.get_image(27,224,24,26) 
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom





class Platform(pg.sprite.Sprite):
    def __init__(self, game , x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_platform(0,0,380,94), self.game.spritesheet.get_platform(0,96,201,100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        #self.image = pg.transform.scale(images, (380 // 2 - 10 , 94 // 2 - 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y