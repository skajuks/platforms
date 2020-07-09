from settings import *
import pygame as pg
import math, random, sys, colorsys
from sprites import *
from os import path
import os


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
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()
        pg.mixer.music.fadeout(1000)

    def update(self):
        self.all_sprites.update()
        # print(pg.time.get_ticks())
        pg.display.set_caption(gameTitle)
        now = pg.time.get_ticks()
        if self.bee_spawn:
            self.spawnchance = 1
            if self.spawnchance > random.randrange(0, 1000):
                Bee(self)
                self.spawnbee = now
                self.bee_spawn = False
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            lowest = mob_hits[0]
            for hit in mob_hits:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest = hit
            if (
                self.player.rect.bottom + 5 > lowest.rect.top
                and lowest.rect.top - 5 < self.player.rect.bottom
                and self.player.rect.bottom < lowest.rect.centery
            ):
                # kinda works now
                self.player.rect.bottom = lowest.rect.top + 20
                self.player.vel.y = -40
                lowest.kill()
            else:
                if len(self.health) == 0:
                    self.playing = False
                else:
                    for x in self.health:
                        for i in self.health:
                            if i.rect.left > x.rect.left:
                                x = i
                    i.kill()
                    # self.player.healthpool -=1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    lowest.kill()
            player_currentpos = (self.player.rect.centerx, self.player.rect.centery)
            self.shockwaves.append(
                [int(player_currentpos[0]), int(player_currentpos[1]), 10, 5]
            )

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    # print(hit.rect.bottom)
                    if hit.type == "bee":
                        hit.rect.top += 2
                    if hit.type == "bee" and hit.rect.bottom >= 820:
                        hit.kill()  # print(hit.type)

                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                    print(lowest.id)
                if (
                    self.player.pos.x < lowest.rect.right + 5
                    and self.player.pos.x > lowest.rect.left - 5
                ):
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.rect.midbottom = self.player.pos
                        self.player.vel.y = 0
                        self.player.jumping = False

        for back in self.backgrounds:
            main = list(back.rect)
            first = main[1]
            if first > -60 and first < -40:
                if len(self.backgrounds) <= 1 and self.player.vel.y <= 0:
                    newBack(self, first - 1000)

        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(self.cloudr) < CLOUD_FREQ:  # controls cloud freq
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(
                    abs(self.player.vel.y / 2), 2
                )  # DIVIDE WITH LARGER NR FOR SLOWER SCROLL
            for backg in self.backgrounds:
                backg.rect.y -= round(self.player.vel.y / 4)
                self.scroll += 1
                if self.scroll == 20:
                    self.cloudr = 25
                    print(self.scroll)
            for bul in self.peabullets:
                bul.rect.y += max(abs(self.player.vel.y), 2)
            for tree in self.misc:
                tree.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.type == "moving":
                    plat.rect.x += plat.vx
                    if plat.rect.right > WIDTH:
                        plat.vx = -3
                    if plat.rect.left < 0:
                        plat.vx = 3
                if plat.rect.top >= HEIGHT:

                    plat.kill()
                    self.score += 10
                if plat.type == "bee" and plat.rect.bottom >= 820:
                    plat.kill()
            for back in self.backgrounds:
                if back.rect.top >= HEIGHT and len(self.backgrounds) > 1:
                    back.kill()

        # POWERUP TIME BAYBEEEE
        pow_hits = pg.sprite.spritecollide(
            self.player, self.powerups, True, pg.sprite.collide_mask
        )
        for pow in pow_hits:
            if pow.type == "boost":
                self.boost_sound.play()
                self.player.vel.y = -FAN_BOOST_POWER
                self.player.jumping = False
            if pow.type == "saw":
                pass
                self.playing = False
            if pow.type == "jump":
                self.jboost_sound.play()
                self.player.vel.y = -(FAN_BOOST_POWER + 30)
                self.player.jumping = False
            if pow.type == "jetpack":
                print("asdasdasdasdasdas")
                self.jetpackEvent()
            if pow.type == "health":
                if self.player.healthpool >= MAX_HEALTH:
                    pass
                else:
                    self.player.healthpool = self.player.healthpool + 1
            if pow.type == "machinegun":
                self.bee_fast_shoot = True

        bul_hits = pg.sprite.spritecollide(self.player, self.bullets, False)
        if bul_hits:
            lowest = bul_hits[0]
            for hit in bul_hits:
                if hit.rect.bottom > lowest.rect.bottom:
                    lowest = hit
            hit.kill()
            for x in self.health:
                for i in self.health:
                    if i.rect.left > x.rect.left:
                        x = i
            i.kill()
            self.player.healthpool -= 1
        if bul_hits and len(self.health) == 0:
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

        while len(self.platforms) < 8:
            pwidth = random.randrange(30, 100)
            Platform(
                self, random.randrange(0, WIDTH - pwidth), random.randrange(-75, -30), 0
            )

        if len(self.health) < self.player.healthpool:
            Health(self)
            count = -20
            for h in self.health:
                count += 40
                h.rect.left = count
        for hp in self.health:
            hp.rect.top = 20
        if self.player.healthpool == 0 or len(self.health) == 0:
            for sprite in self.all_sprites:
                sprite.kill()
            for bee in self.bees:
                bee.kill()
                self.bee_spawn = True
            self.playing = False

        if self.jetpackLaunch == True:  # while jetpack is fireing
            self.player.vel.y = -15
            self.jetpackFuel -= 5
            # if random.randint(1,20) > 10:
            self.particles.append(
                [
                    [self.player.rect.centerx + 5, self.player.rect.bottom + 20],
                    [random.randint(0, 20) / 10 - 1, 2],
                    random.randint(5, 8),
                ]
            )
            self.hue = (1.0 / 3.0) / 1000 * self.jetpackFuel
            self.fuelsize = self.jetpackFuel / 10
            self.color = self.hsv2rgb(self.hue)

            if self.jetpackFuel <= 0:
                for pow in self.jets:
                    pow.kill()
                    self.jetpackActive = False
                    self.jetpackLaunch = False

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.3
            pygame.draw.circle(
                self.MAINWINDOW,
                choice([RED, ORANGE, YORANGE, YELLOW]),
                [int(particle[0][0]), int(particle[0][1])],
                int(particle[2]),
            )
            if particle[2] <= 0:
                self.particles.remove(particle)
        for wave in self.shockwaves:
            wave[2] += 10
            wave[3] -= 1
            pg.draw.circle(
                self.MAINWINDOW,
                WHITE,
                [int(wave[0]), int(wave[1])],
                int(wave[2]),
                int(wave[3]),
            )
            pg.display.flip()
            if wave[3] <= 1.5:
                self.shockwaves.remove(wave)
        pg.display.flip()

        self.eventlist = [
            "F: " + str(self.jetpackFuel),
            "plt:" + str(len(self.platforms)),
            "bird:" + str(len(self.mobs)),
            "cld:" + str(len(self.clouds)),
            "acc:" + str(round(self.player.acc.x, 2)),
            "vel:" + str(round(self.player.vel.y, 2)),
        ]
        pea_hits = pg.sprite.spritecollide(self.player, self.peabullets, False)
        if pea_hits:
            player_currentpos = (self.player.rect.centerx, self.player.rect.centery)
            lowest = pea_hits[0]
            for pea in self.peabullets:
                if pea.rect.bottom > lowest.rect.bottom:
                    lowest = pea
            self.detect_hit_side(self.player.rect, lowest.rect)
            lowest.kill()
            self.shockwaves.append(
                [int(player_currentpos[0]), int(player_currentpos[1]), 10, 10]
            )

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
        # pg.quit()

    def detect_hit_side(self, prect1, bul1):
        if prect1.midbottom[1] < bul1.midbottom[1]:
            self.player.vel.y = -10
        if prect1.midleft[0] > bul1.midleft[0]:
            self.player.vel.x = 10
        if prect1.midright[0] < bul1.midright[0]:
            self.player.vel.x = -10

    def new(self):
        pygame.init()
        self.particles = []
        self.shockwaves = []
        self.debugon = False
        self.cloudr = 100
        self.scroll = 0
        self.fuelsize = 100
        self.mob_timer = 0
        self.score = 0
        self.jetpackActive = False
        self.jetpackLaunch = False
        self.jetpackFuel = 0
        self.bee_fast_shoot = False
        self.color = (0, 255, 0)
        self.bee_spawn = True
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.shooter_heads = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.jets = pg.sprite.Group()
        self.misc = pg.sprite.Group()
        self.peabullets = pg.sprite.Group()
        self.shooters = pg.sprite.Group()
        self.backgrounds = pg.sprite.Group()
        self.bees = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        self.health = pg.sprite.Group()
        Background(self, -200)
        Health(self)

        for plat in PLATFORM_LIST:  # SPAWN STARTING PLATS ALWAYS THE SAME
            Platform(self, *plat)
        for plat in self.platforms:
            plat.type = "static"
            plat.spawn = "start"
            if self.platforms.has(self.powerups):
                self.powerups.kill()
        print("getcwd:      ", os.getcwd())
        print("__file__:    ", __file__)
        pg.mixer.music.load(path.join(self.sound_dir, "soundtrack.wav"))
        for i in range(5):
            c = Cloud(self)
            c.rect.y += 500
        g.run()

    def jetpackEvent(self):
        for pow in self.powerups:
            if not pow.type == "jet":
                Jetpack(self)
                Fuel(self)
                self.color = (0, 255, 0)
                self.jetpackActive = True
                self.jetpackFuel = 1000
                self.fuelsize = 100

    def hsv2rgb(self, h):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, 1, 1))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN and self.jetpackActive == True:
                self.jetpackLaunch = True
            if event.type == pg.MOUSEBUTTONUP and self.jetpackActive == True:
                self.jetpackLaunch = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
                if event.key == ord("o"):
                    if self.debugon == True:
                        self.debugon = False
                    elif self.debugon == False:
                        self.debugon = True
                if event.key == ord("v"):
                    self.player.vel.y = -100
                if event.key == ord("c"):
                    self.player.vel.x = 500

    def draw(self):
        # self.bimage = pg.image.load(path.join(self.img_dir, BCK)).convert_alpha()
        self.MAINWINDOW.fill(LIGHT_BLUE)
        # self.MAINWINDOW.blit(self.bimage, [0,0])
        self.all_sprites.draw(self.MAINWINDOW)
        self.draw_rect(BLACK, WIDTH, 21, 0)
        self.draw_text(str(self.score), 20, WHITE, WIDTH // 2, 4)
        if self.clock.get_fps() >= 58:
            self.draw_text(
                str("FPS " + str(round(self.clock.get_fps(), 1))), 20, LIME, 40, 4
            )
        if self.clock.get_fps() < 58:
            self.draw_text(
                str("FPS " + str(round(self.clock.get_fps(), 1))), 20, YELLOW, 40, 4
            )
        if self.clock.get_fps() <= 30:
            self.draw_text(
                str("FPS " + str(round(self.clock.get_fps(), 1))), 20, RED, 40, 4
            )
        if self.debugon == True:
            self.draw_rect(BLACK, WIDTH, 21, HEIGHT - 21)  ## bottom rect
            self.draw_text(str(self.eventlist), 20, GREEN, WIDTH // 2, HEIGHT - 18)
        if self.jetpackActive == True:
            self.draw_rect_free(self.color, 50, self.fuelsize, 5, 105)
            self.draw_text(
                "FUEL : " + str(self.jetpackFuel), 20, self.color, 60, HEIGHT - 20
            )
        # if self.jetpackActive == True:

        # self.draw_text(str(len(self.clouds)), 20, LIGHT_BLUE, WIDTH - 170, 4)
        # self.draw_text(str(len(self.mobs)), 20, RED, WIDTH - 140, 4)
        # self.draw_text(str(round(self.player.acc.x, 2)), 20, PINK, 115, 4)
        # self.draw_text(str(round(self.player.vel.y, 2)), 20, PINK, 160, 4)
        # self.draw_text(str(len(self.backgrounds)), 20, GREEN, WIDTH - 110, 4)
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.sound_dir, "menu.ogg"))
        pg.mixer.music.play(loops=-1)
        self.MAINWINDOW.fill(VIOLET)
        self.draw_text(gameTitle, 48, WHITE, WIDTH // 2, HEIGHT // 4)
        self.draw_text(
            "Arrow keys to move, Space to jump", 22, WHITE, WIDTH // 2, HEIGHT // 2
        )
        self.draw_text("Press any key to play", 22, WHITE, WIDTH // 2, HEIGHT * 3 // 4)
        self.draw_text("High score : " + str(self.highscore), 22, WHITE, WIDTH // 2, 15)
        pg.display.flip()
        self.waitForKey()
        pg.mixer.music.fadeout(1000)

    def show_go_screen(self):
        if not self.running:
            return
        self.MAINWINDOW.fill(VIOLET)
        self.draw_text("Game Over!", 48, WHITE, WIDTH // 2, HEIGHT // 4)
        self.draw_text("Score : " + str(self.score), 22, WHITE, WIDTH // 2, HEIGHT // 2)
        self.draw_text(
            "Press any key to play again", 22, WHITE, WIDTH // 2, HEIGHT * 3 // 4
        )
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(
                "New High score! : " + str(self.score),
                22,
                WHITE,
                WIDTH // 2,
                HEIGHT / 2 + 40,
            )
            with open(path.join(self.dir, HS_SCORE), "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text(
                "High score : " + str(self.highscore),
                22,
                WHITE,
                WIDTH // 2,
                HEIGHT // 2 + 40,
            )
        pg.display.flip()
        self.waitForKey()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(path.join(self.dir, "bit5x3.TTF"), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.MAINWINDOW.blit(text_surface, text_rect)

    def draw_text2(self, text, size, color, x, y):
        font = pg.font.Font(path.join(self.dir, "bit5x3.TTF"), size)  # doesn't blit
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)

    def draw_rect(self, color, x, y, t):
        surface = pg.Surface((x, y))
        surface.fill(color)
        surface_rect = surface.get_rect()
        surface_rect.midtop = (WIDTH // 2, t)
        self.MAINWINDOW.blit(surface, surface_rect)

    def draw_rect_free(self, color, x, y, v, t):
        surface = pg.Surface((x, y))
        surface.fill(color)
        surface_rect = surface.get_rect()
        surface_rect.midtop = (v, t)
        self.MAINWINDOW.blit(surface, surface_rect)

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
        # load scoresheets
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "textures")
        with open(path.join(self.dir, HS_SCORE), "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # sprites
        self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITESHEET))
        self.mob_sprites = Spritesheet(path.join(self.img_dir, MOB_SPRITES))
        self.misc_sprites = Spritesheet(path.join(self.img_dir, MISC_SPRITES))
        self.jump_sprites = Spritesheet(path.join(self.img_dir, JUMP_SPRITES))
        # self.MAINWINDOW.fill(path.join(img_dir, 'backg.png'))

        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(
                pg.image.load(
                    path.join(self.img_dir, "cloud{}.png".format(i))
                ).convert()
            )

        # sounds
        self.sound_dir = path.join(self.dir, "sound")
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, "jump2.wav"))
        self.boost_sound = pg.mixer.Sound(path.join(self.sound_dir, "boost.wav"))
        self.shoot_sound = pg.mixer.Sound(path.join(self.sound_dir, "shoot.wav"))
        self.jboost_sound = pg.mixer.Sound(path.join(self.sound_dir, "jump_boost.wav"))


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
