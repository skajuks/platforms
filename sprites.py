from settings import *
import pygame as pg
from random import choice, randrange
from os import path
import time



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
    def get_bee(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        image = pg.transform.scale(image, (width * 2 + 20, height * 2 + 20))
        return image            
    def get_bee_bullet(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        image = pg.transform.scale(image, (width * 2 +5, height * 2 +5 ))
        return image
class Player(pg.sprite.Sprite):

    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
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
        self.standing_frames = [self.game.spritesheet.get_image(299,123,23,24),
                                self.game.spritesheet.get_image(287,189,23,24),
                                self.game.spritesheet.get_image(287,162,23,25),
                                self.game.spritesheet.get_image(286,216,23,26),
                                self.game.spritesheet.get_image(281,96,23,25)
        ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(274,136,23,24),
                              self.game.spritesheet.get_image(306,96,23,24),
                              self.game.spritesheet.get_image(234,207,25,24),
                              self.game.spritesheet.get_image(261,162,24,24),
                              self.game.spritesheet.get_image(248,136,24,24),
                              self.game.spritesheet.get_image(234,181,25,24)
                              ]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)                      
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)      
        self.jump_frame = self.game.spritesheet.get_image(261,216,23,28)
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
                self.image = self.game.spritesheet.get_image(261,188,24,26)
            else:  
                self.image = self.game.spritesheet.get_image(261,216,23,28) 
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom





class Platform(pg.sprite.Sprite):
    def __init__(self, game , x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_platform(0,0,380,94), self.game.spritesheet.get_platform(0,96,201,100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        #self.image = pg.transform.scale(images, (380 // 2 - 10 , 94 // 2 - 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POWERUP_FREQ:
            Powerup(self.game, self)

class Powerup(pg.sprite.Sprite):
    def __init__(self, game , plat):
        self._layer = POWERUP_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0 
        self.load_images()       
        self.plat = plat
        self.type = choice(['boost'])
        self.image = self.fan_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top

    def update(self):
        self.animate()
        self.rect.bottom = self.plat.rect.top
        if not self.game.platforms.has(self.plat):
            self.kill()

    def load_images(self):
        self.fan_frames = [self.game.spritesheet.get_image(0,238,23,8),
        self.game.spritesheet.get_image(42,238,15,8),
        self.game.spritesheet.get_image(59,238,7,8),
        self.game.spritesheet.get_image(25,238,15,8)     
        ]
        for frame in self.fan_frames:
            frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.fan_frames)
                self.image = self.fan_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.centerx = self.plat.rect.centerx
                self.rect.bottom = self.plat.rect.top 

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.current_frame = 0
        self.last_update = 0 
        self.image = self.bird_img[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH + 100
        self.vx = randrange(1, 3)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.animate()
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()       # MAKE BLUE BIRD MOB!

    def load_images(self):
        self.bird_img = [
            self.game.mob_sprites.get_image(72,58,30,23),
            self.game.mob_sprites.get_image(72,0,31,23),
            self.game.mob_sprites.get_image(38,0,32,20),
            self.game.mob_sprites.get_image(38,22,32,20),
            self.game.mob_sprites.get_image(136,56,26,28),
            self.game.mob_sprites.get_image(136,0,27,26),
            self.game.mob_sprites.get_image(136,0,27,26),
            self.game.mob_sprites.get_image(136,28,27,26)    
        ]
        for frame in self.bird_img:
            frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.bird_img)
                self.image = self.bird_img[self.current_frame]



class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        scale = randrange(50,101) /100
        self.image = pg.transform.scale(self.image,(int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500,-50)

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()

class Background(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = BACKGROUND_LAYER
        self.groups = game.all_sprites, game.backgrounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'textures')
        self.image = pg.image.load(path.join(self.img_dir, BCK)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -3200
    def update(self):
        pass    

class Bee(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.bees
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0 
        self.load_images()
        self.bullet_ratio = 0.5
        self.image = self.fly_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.vx = 3
        self.rect.y = 15  
        self.attack = False             


        #self.rect.x = self.game.WIDTH // 2

    def load_images(self):
        self.fly_frames = [
            self.game.mob_sprites.get_bee(70,83,32,29),
            self.game.mob_sprites.get_bee(36,54,34,27),
            self.game.mob_sprites.get_bee(0,83,34,27),
            self.game.mob_sprites.get_bee(36,83,32,29),
            self.game.mob_sprites.get_bee(104,25,30,31),
            self.game.mob_sprites.get_bee(72,25,30,31)
        ]
        for frame in self.fly_frames:
            frame.set_colorkey(BLACK)

        self.attack_frames = [
            self.game.mob_sprites.get_bee(70,83,32,29),
            self.game.mob_sprites.get_bee(0,54,34,27),
            self.game.mob_sprites.get_bee(0,27,36,25),
            self.game.mob_sprites.get_bee(0,0,36,25),
            self.game.mob_sprites.get_bee(0,27,36,25),
            self.game.mob_sprites.get_bee(134,89,28,32),
            self.game.mob_sprites.get_bee(104,89,28,30),
            self.game.mob_sprites.get_bee(104,58,30,29)
        ]   
        for frame in self.attack_frames:
            frame.set_colorkey(BLACK)         
    def update(self):
        self.animate()
        self.rect.x += self.vx
        #self.rect.x += self.vx
        if self.rect.right > WIDTH:
            self.vx = -3
        if self.rect.left < 0:
            self.vx = 3    
        #if self.game.player.rect.x + 30 >= self.rect.x >= self.game.player.rect.x - 30:
        if not self.bullet_ratio < randrange(0,100):
            self.attack = True
            self.shoot()
        if self.image == self.attack_frames[7]:
            self.attack = False  
        if len(self.game.bees) > 0:
           self.t1 = round(time.time(),0)
           now = pg.time.get_ticks()
           if self.game.spawnbee + 10000 < now:
               self.bee_die()
               self.game.spawnbee = now
    def bee_die(self):
        self.kill()
        self.game.bee_spawn = True
    def animate(self):
        if not self.attack:
            now = pg.time.get_ticks()
            if now - self.last_update > 250:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.fly_frames)
                    self.image = self.fly_frames[self.current_frame]
                    #self.rect = self.image.get_rect()
        if self.attack:
            now = pg.time.get_ticks()
            if now - self.last_update > 40:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
                    self.image = self.attack_frames[self.current_frame]            

    def shoot(self):
        print('TARGET')
        bullet = Bullet(self.game,self.rect.centerx, self.rect.bottom)

            
        #self.game.bullets.add(bullet)


class Bullet(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.image = self.game.mob_sprites.get_bee_bullet(0,114,8,9)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.speedy = 5

    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()        