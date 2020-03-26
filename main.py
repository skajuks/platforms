from settings import *
import pygame as pg
import math, random, sys
from sprites import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.MAINWINDOW = pg.display.set_mode((WIDTH, HEIGHT))
        
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        
        self.load_data()

    def run(self):
        pg.mixer.music.play(loops =-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()
        pg.mixer.music.fadeout(1000)    

    def update(self):
        self.all_sprites.update()
        #print(pg.time.get_ticks())
        pg.display.set_caption(gameTitle + ' ' + str(round(self.clock.get_fps(), 1)))
        now = pg.time.get_ticks()
        if self.bee_spawn:
            self.spawnchance = 1
            if self.spawnchance > random.randrange(0,1000):
                Bee(self)
                self.spawnbee = now
                self.bee_spawn = False
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            for mob in self.mobs:
                print(mob.rect.top, self.player.rect.bottom)
                if self.player.rect.bottom - 20 < mob.rect.top:     # REDO
                    #print('RANGE')
                    self.player.vel.y = -40
                                     
                    #print('asdasdasdas')
                if self.player.rect.top < mob.rect.bottom: 
                    self.playing = False   
                else:    
                    self.playing = False
            mob.kill()        
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 5 and self.player.pos.x > lowest.rect.left - 5:         
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.rect.midbottom = self.player.pos
                        self.player.vel.y = 0
                        self.player.jumping = False
                #Scroll window


        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(self.cloudr) < CLOUD_FREQ:  # controls cloud freq
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)  # DIVIDE WITH LARGER NR FOR SLOWER SCROLL
            for backg in self.backgrounds:
                backg.rect.y -= (round(self.player.vel.y / 1000, 9))
                self.scroll +=1
                if self.scroll == 20:
                    self.cloudr = 25
                    print(self.scroll)
            #for bee in self.bees:
                #bee.rect.y += max(abs(self.player.vel.y), 2)    #        
            for plat in self.platforms:
 
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.type == 'moving':
                    plat.rect.x += plat.vx
                    if plat.rect.right > WIDTH:
                        plat.vx = -3
                    if plat.rect.left < 0:
                        plat.vx = 3
                if plat.type == 'ice':
                    pass
                if plat.rect.top >= HEIGHT + 200:
                    plat.kill()
                    self.score += 10
        #POWERUP TIME BAYBEEEE
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True, pg.sprite.collide_mask)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -FAN_BOOST_POWER
                self.player.jumping = False
            if pow.type == 'saw':
                self.playing = False
            if pow.type == 'jump':
                self.jboost_sound.play()
                self.player.vel.y = -(FAN_BOOST_POWER + 30)
                self.player.jumping = False

        bul_hits = pg.sprite.spritecollide(self.player, self.bullets, False)
        if bul_hits:
            for sprite in self.all_sprites:
                sprite.kill()    
            for bee in self.bees:
                bee.kill()
                self.bee_spawn = True
            if len(self.platforms) == 0:            
                self.playing = False            
        if self.player.rect.bottom > HEIGHT:
            self.hit()    
        if len(self.platforms) == 0:            
            self.playing = False
            

        while len(self.platforms) < 10:
            pwidth = random.randrange(30,100)
            Platform(self, random.randrange(0, WIDTH - pwidth),
            random.randrange(-75, -30))


    def hit(self):
        for sprite in self.all_sprites:
            sprite.rect.y -= max(self.player.vel.y, 10)
                
            if sprite.rect.bottom < 0:
                sprite.kill()
        for back in self.backgrounds:
            back.rect.y += max(self.player.vel.y, 10)
        for bee in self.bees:
            bee.kill()
            self.bee_spawn = True   
        #pg.quit()
    def new(self):
        pygame.init()
        self.cloudr = 100
        self.scroll = 0
        self.mob_timer = 0
        self.score = 0
        self.bee_spawn = True
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.misc = pg.sprite.Group()
        self.backgrounds = pg.sprite.Group()     
        self.bees = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        
        Background(self)        
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        for plat in self.platforms:
            plat.type = 'static'
            if self.platforms.has(self.powerups):
                self.powerups.kill()    
        pg.mixer.music.load(path.join(self.sound_dir, 'soundtrack.wav'))
        for i in range(5):
            c = Cloud(self)
            c.rect.y += 500    
        g.run()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE:
                   self.player.jump()
                   
            if event.type == pg.KEYUP:
               if event.key == pg.K_SPACE:
                   self.player.jump_cut()                          
        
    def draw(self):
        #self.bimage = pg.image.load(path.join(self.img_dir, BCK)).convert_alpha()
        self.MAINWINDOW.fill(LIGHT_BLUE)
        #self.MAINWINDOW.blit(self.bimage, [0,0])
        self.all_sprites.draw(self.MAINWINDOW)
        self.draw_text(str(self.score), 22, BLACK, WIDTH // 2, 15)
        pg.display.flip()       
    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.sound_dir, 'menu.ogg'))
        pg.mixer.music.play(loops=-1)
        self.MAINWINDOW.fill(SWAMP)
        self.draw_text(gameTitle, 48, WHITE, WIDTH // 2 , HEIGHT // 4)
        self.draw_text("Arrow keys to move, Space to jump" ,22 ,WHITE, WIDTH // 2 , HEIGHT // 2)
        self.draw_text("Press any key to play" ,22, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
        self.draw_text("High score : " + str(self.highscore), 22, WHITE, WIDTH // 2, 15)
        pg.display.flip()
        self.waitForKey()
        pg.mixer.music.fadeout(1000)

    def show_go_screen(self):
        if not self.running:
            return
        self.MAINWINDOW.fill(SWAMP)
        self.draw_text("Game Over!", 48, WHITE, WIDTH // 2 , HEIGHT // 4)
        self.draw_text("Score : " + str(self.score) ,22 ,WHITE, WIDTH // 2 , HEIGHT // 2)
        self.draw_text("Press any key to play again" ,22, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New High score! : " + str(self.score), 22, WHITE, WIDTH //2 , HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_SCORE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High score : " + str(self.highscore), 22, WHITE, WIDTH // 2, HEIGHT // 2 + 40)        
        pg.display.flip()
        self.waitForKey()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name , size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.MAINWINDOW.blit(text_surface, text_rect)

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False   

    def load_data(self):
        #load scoresheets
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'textures')
        with open(path.join(self.dir, HS_SCORE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:    
                self.highscore = 0
    #sprites
        self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITESHEET))
        self.mob_sprites = Spritesheet(path.join(self.img_dir, MOB_SPRITES))
        self.misc_sprites = Spritesheet(path.join(self.img_dir, MISC_SPRITES))
        self.jump_sprites = Spritesheet(path.join(self.img_dir, JUMP_SPRITES))
        #self.MAINWINDOW.fill(path.join(img_dir, 'backg.png'))

        self.cloud_images = []
        for i in range(1,4):
            self.cloud_images.append(pg.image.load(path.join(self.img_dir, 'cloud{}.png'.format(i))).convert())

    #sounds
        self.sound_dir = path.join(self.dir, 'sound')
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, 'jump2.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.sound_dir, 'boost.wav'))
        self.shoot_sound = pg.mixer.Sound(path.join(self.sound_dir, 'shoot.wav'))
        self.jboost_sound = pg.mixer.Sound(path.join(self.sound_dir, 'jump_boost.wav'))
    

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
