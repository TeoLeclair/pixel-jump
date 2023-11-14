# content from kids can code: http://kidscancode.org/blog/
# content from Mr. Cozort
# content from Sean
# content from Joeseph Matan

# GameDesign:
# Goals -make new highs score, do not lose health, reach Point to gin score
# rules- move side to side and jump, reach 0 reset health and score, hit mob lose health
# feedback -score on the screen, damage animation when touch mob,
# freedoms- run side to side and jump

# Feature Goals:
# add mob that gives points
# add easter egg when reach score of 5 you can jump to top right of corner and see game creator name and class period game was made
# randomly moving mobs
# dsipaly updating score and health amount

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math


vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    
    def new(self):
        # create a group for all sprites
        self.score = 0    #starting score
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.Coin = pg.sprite.Group() #added new new class for good and bad mobs
        self.coins_left = 10
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)
        for i in range(0,10):
            bom = Bomb(self, randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            self.all_sprites.add(bom)
            self.all_mobs.add(bom)
            # random placment of "bad" mobs
        
        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        for c in range(0,10):
            c = Coin(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            self.all_sprites.add(c)
            self.all_coins.add(c)
            self.Coin.add(c)
# random placement for "good" mobs

    


        

        self.run()  
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 0
        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.acc.y = -10
                self.player.vel.y = -10
                print("ouch")
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
        # resets player position, score, and health
        if self.player.health == 0:
            self.player.pos = vec(WIDTH/2, HEIGHT/2)
            self.player.health = 5
            self.score = 0
        if self.coins_left == 0:
            self.coins_left = 10  # resetting coin counter
            for c in range(0,10):
                c = Coin(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
                self.all_sprites.add(c)
                self.all_coins.add(c)
                self.Coin.add(c)

        pcollide  = pg.sprite.spritecollide(self.player, self.all_mobs, False)
        if pcollide:
            pcollide[0].cd.event_reset()
            print("collided....")
            if pcollide[0].tagged == False:
                print("the delta is " + str(pcollide[0].cd.delta))
                print("tagged...FALSE")
                pcollide[0].image = pg.image.load(os.path.join(img_folder, "explosive.png")).convert()
                pcollide[0].image.set_colorkey(BLACK)
                pcollide[0].tagged = True
                self.player.health -= 1
        
                
            
                    

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("health: " + str(self.player.health), 22, WHITE, WIDTH/2, HEIGHT/10) 
        self.draw_text("score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/20)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()
