import pygame, sys, math
import pygame._view
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

screenwidth = 600
screenheight = 600
potatowidth=125
potatoheight=153
backgroundwidth=765

 # set up the window
screen = pygame.display.set_mode((screenwidth, screenheight), pygame.DOUBLEBUF, 32)
pygame.display.set_caption('Crazy Potato')

WHITE = (255, 255, 255)
screen.fill(WHITE)
background = pygame.Surface((screen.get_width(), screen.get_height()), flags=pygame.SRCALPHA)
background.fill(WHITE)

background_image = pygame.image.load('background.png').convert_alpha();

class Potato(pygame.sprite.Sprite):
    normalPotato = pygame.image.load('potato1.png').convert_alpha()
    jumpingPotato = pygame.image.load('potato2.png').convert_alpha()

    soundJump = pygame.mixer.Sound('jump1.wav')

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self,
                              self.groups) 
        self.potatox = x
        self.potatoy = y
        self.lastpotatoy = y
        self.standingy = y
        self.jumpHeight = 0
        self.jumpMaxHeight = 350.0
        self.image = self.normalPotato 
        self.rect = self.image.get_rect()
        self.rect.center = (self.potatox, self.potatoy)

    def move(self, difference):
        self.jumpHeight = self.jumpHeight + difference
        self.calculatePosition()

    def calculatePosition(self):
        self.lastpotatoy = self.potatoy
        self.potatoy = self.standingy - math.sin(self.jumpHeight/self.jumpMaxHeight*math.pi)*self.jumpMaxHeight;
        self.potatoy = min(self.standingy, self.potatoy)
        self.rect.center = (self.potatox, self.potatoy)

    def getDirection(self):
        return self.lastpotatoy - self.potatoy

    def scream(self):
        self.soundJump.play()
        self.image = self.jumpingPotato

    def normal(self):
        self.image = self.normalPotato
        self.jumpHeight = 0
        self.calculatePosition()
    
    def isbottom(self):
        return self.rect.center[1] >= self.standingy

    def setStandingY(self, standingy):
        self.standingy = standingy

class Shelf(pygame.sprite.Sprite):
    shelfImage = pygame.image.load('shelf.png').convert_alpha()

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self,
                              self.groups) 
        self.image = self.shelfImage 
        self.shelfx = x 
        self.shelfy = y 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def offset(self, offset):
        self.rect.center = (self.shelfx + offset, self.shelfy)


allsprites = pygame.sprite.Group()
shelfs = pygame.sprite.Group()

Potato.groups = allsprites
Shelf.groups = allsprites, shelfs

potatohero = Potato(screenwidth/2, (screenheight-potatoheight))
potatodirection = 0
offset = 0
direction = 0

shelf1 = Shelf(screenwidth * 1.5, screenheight/2);

while True: # the main game loop
    hitshelfs = pygame.sprite.spritecollide(potatohero, shelfs, False)
    for hitself in hitshelfs:
        jumpdirection = potatohero.getDirection()
        if jumpdirection > 0:
            print "Fejbeveres"
        else:
            potatohero.setStandingY(hitself.rect.top + hitself.rect.height/2 - potatohero.rect.height/2)

    potatohero.move(potatodirection * 20)
    offset = offset + (direction*10)
    offset = min(0, offset)
    backgroundOffset = offset % (-backgroundwidth)

    if potatohero.isbottom(): 
         potatodirection = 0
         potatohero.normal()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if (event.type == KEYDOWN and event.key == K_SPACE):
            # True -> False
            # False -> True
            if potatodirection == 0:
                potatohero.scream()
                potatodirection = 1

        if (event.type == KEYDOWN and event.key == K_d):
            direction = -1

        if (event.type == KEYUP and event.key == K_d):
            direction = 0

        if (event.type == KEYDOWN and event.key == K_a):
            direction = 1

        if (event.type == KEYUP and event.key == K_a):
            direction = 0

    allsprites.clear(screen, background)
    screen.blit(background_image, [backgroundOffset, 0])
    screen.blit(background_image, [backgroundOffset+backgroundwidth, 0])
    shelf1.offset(offset)
    allsprites.draw(screen)
    pygame.display.flip()
    fpsClock.tick(FPS)