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
        pg.display.set_caption(gameTitle)
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.rect.midbottom = self.player.pos
                self.player.vel.y = 0
                #Scroll window
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:            
            self.playing = False    
        while len(self.platforms) < 7:
            pwidth = random.randrange(30,100)
            p = Platform(random.randrange(0, WIDTH - pwidth),
            random.randrange(-75, -30), pwidth, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)



    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
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
        
    def draw(self):
        self.MAINWINDOW.fill(LIGHT_BLUE)
        self.all_sprites.draw(self.MAINWINDOW)
        self.draw_text(str(self.score), 22, BLACK, WIDTH // 2, 15)
        pg.display.flip()       
    def show_start_screen(self):
        self.MAINWINDOW.fill(SWAMP)
        self.draw_text(gameTitle, 48, WHITE, WIDTH // 2 , HEIGHT // 4)
        self.draw_text("Arrow keys to move, Space to jump" ,22 ,WHITE, WIDTH // 2 , HEIGHT // 2)
        self.draw_text("Press any key to play" ,22, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
        pg.display.flip()
        self.waitForKey()
    def show_go_screen(self):
        if not self.running:
            return
        self.MAINWINDOW.fill(SWAMP)
        self.draw_text("Game Over!", 48, WHITE, WIDTH // 2 , HEIGHT // 4)
        self.draw_text("Score : " + str(self.score) ,22 ,WHITE, WIDTH // 2 , HEIGHT // 2)
        self.draw_text("Press any key to play again" ,22, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
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
        pass    


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
