import pygame
import numpy as np
import random
from pygame.locals import *
import datetime

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 600
FPS = 60

BLACK = (10, 10, 10)
WHITE = (240, 240, 240)

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Vampire Orchestra - Suebin Park")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Tiki Man Sunrise/ Sunset/ Nighttime
# https://steamcommunity.com/sharedfiles/filedetails/?id=844946240
bgOrange = pygame.image.load("musicbox/assets/bg1.jpeg").convert()
bgBlue = pygame.image.load("musicbox/assets/bg2.jpeg").convert()
bgYellow = pygame.image.load("musicbox/assets/bg3.jpeg").convert()
bgDark = pygame.image.load("musicbox/assets/bg4.jpeg").convert() 
bgOrange_img = pygame.transform.scale(bgOrange, (WINDOW_WIDTH, WINDOW_HEIGHT))
bgBlue_img = pygame.transform.scale(bgBlue, (WINDOW_WIDTH, WINDOW_HEIGHT))
bgYellow_img = pygame.transform.scale(bgYellow, (WINDOW_WIDTH, WINDOW_HEIGHT))
bgDark_img = pygame.transform.scale(bgDark, (WINDOW_WIDTH, WINDOW_HEIGHT))
BG_IMAGE = bgOrange_img
BG = bgOrange

vampMale_img = pygame.image.load("musicbox/assets/vampire1.png")
vampFemale_img = pygame.image.load("musicbox/assets/vampire2.png")
bat_img = pygame.image.load("musicbox/assets/bat.png")
ax_img = pygame.image.load("musicbox/assets/ax.png")

choir = pygame.mixer.Sound("musicbox/choir.mp3")

pianoKeys = random.sample(range(1, 25), 6)
def playPianoSound(keyIndex):
    sound = pygame.mixer.Sound(f"musicbox/piano/key{keyIndex:02}.mp3")
    sound.play()

drum = pygame.mixer.Sound("musicbox/music/drum.mp3")
cymbals = pygame.mixer.Sound("musicbox/music/cymbals.mp3")
harp = pygame.mixer.Sound("musicbox/music/harp.mp3")
cello = pygame.mixer.Sound("musicbox/music/cello.mp3")
instruments = [drum,cymbals,cello]

gems = []
filename = ["gem1.png", "gem2.png", "gem3.png", "gem4.png", "gem5.png", "gem6.png",
            "wand2.png", "note.png"]
for i in filename:
    gem = pygame.image.load(f"musicbox/assets/{i}") 
    gems.append(gem)

def draw_text(screen, text, size, x, y):
    font = pygame.font.Font("musicbox/neodgm.ttf", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        imageSelect = np.random.choice([vampFemale_img, vampMale_img])
        self.image = pygame.transform.scale(vampFemale_img, (100, 128))
        self.image.set_colorkey((BLACK))
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH / 2
        self.rect.bottom = WINDOW_HEIGHT - 50
        self.speedx = 0
        self.angle = 90

    def update(self):
        if self.angle >= 170:
            self.angle = 170
        elif self.angle <= 10:
            self.angle = 10
        self.speedx = 0
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_LEFT]:
            self.speedx = -5
        elif keyState[pygame.K_RIGHT]:
            self.speedx = +5
        self.rect.x += self.speedx
        if self.rect.top <= 5:
            self.rect.top = 5
        if self.rect.bottom >= WINDOW_HEIGHT - 5:
            self.rect.bottom = WINDOW_HEIGHT - 5
        if self.rect.left <= 5:
            self.rect.left = 5
        if self.rect.right >= WINDOW_WIDTH - 5:
            self.rect.right = WINDOW_WIDTH - 5

    def shoot(self, all_sprites, axes):
        ax = Ax(self.rect.centerx, self.rect.centery, self.angle)
        all_sprites.add(ax)
        axes.add(ax)

class Bat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bat_img, (100, 50))
        self.image.set_colorkey((BLACK))
        self.rect = self.image.get_rect()
        self.center = self.rect.center
        self.rect.centery = np.random.randint(300, 500)
        self.rect.centerx = np.random.randint(200, 500)
        self.speed = 15
        self.speedx = self.speed * np.cos(np.random.randint(-90,90))
        self.speedy = self.speed * np.sin(np.random.randint(-90,90))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Ax(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ax_img, (50, 60))
        self.image.set_colorkey((BLACK))
        self.rect = self.image.get_rect()
        self.center = self.rect.center
        self.rotatingAngle = 0
        self.image = pygame.transform.rotate(self.image, self.rotatingAngle)
        
        self.shootingAngle = angle
        self.direction_angle = np.deg2rad(self.shootingAngle)
        self.rect.centery = y
        self.rect.centerx = x
        self.speed = -12
        self.speedx = self.speed * np.cos(self.direction_angle)
        self.speedy = self.speed * np.sin(self.direction_angle)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotatingAngle += 5
        self.image = pygame.transform.rotate(ax_img, self.rotatingAngle)
        if self.rect.bottom < 0:
            # self.kill()
            self.speedx = random.randint(-10, 10)
            self.speedy *= -1

        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx *= -1
        elif self.rect.right > WINDOW_WIDTH-self.rect.width:
            self.rect.right = WINDOW_WIDTH-self.rect.width
            self.speedx *= -1

class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y, choirP=0.03):
        pygame.sprite.Sprite.__init__(self)
        gemPossibilities = [(1-choirP)/7, (1-choirP)/7, (1-choirP)/7, (1-choirP)/7, (1-choirP)/7, (1-choirP)/7, (1-choirP)/7, choirP]
        self.imageSelect = np.random.choice(gems, p = gemPossibilities)
        self.image = pygame.transform.scale(self.imageSelect, (58,58))
        self.image.set_colorkey((BLACK))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gemIndex = None
        if self.imageSelect == gems[0]:
            self.gemIndex = 'Blue'
        elif self.imageSelect == gems[1]:
            self.gemIndex = 'Green'
        elif self.imageSelect == gems[2]:
            self.gemIndex = 'Red'
        elif self.imageSelect == gems[3]:
            self.gemIndex = 'White'
        elif self.imageSelect == gems[4]:
            self.gemIndex = 'SkyBlue'
        elif self.imageSelect == gems[5]:
            self.gemIndex = 'Magenta'
        elif self.imageSelect == gems[6]:
            self.gemIndex = 'Else'
        elif self.imageSelect == gems[7]:
            self.gemIndex = 'Choir'

    def update(self):
        pass

def start_screen():
    screen.blit(bgDark_img, bgDark.get_rect())
    draw_text(screen, "Vampire Orchestra", 70, WINDOW_WIDTH/2, WINDOW_HEIGHT*0.29)
    draw_text(screen, "1. Left/Right key to move.", 18, WINDOW_WIDTH/2, WINDOW_HEIGHT*0.5)
    draw_text(screen, "2. Space key to shoot.", 18, WINDOW_WIDTH/2, WINDOW_HEIGHT*0.5 + 25)
    draw_text(screen, "3. Up/Down key to change the shooting angle.", 18, WINDOW_WIDTH/2, WINDOW_HEIGHT*0.5 + 50)
    draw_text(screen, "<<Press any key to start>>", 28, WINDOW_WIDTH/2, WINDOW_HEIGHT*0.79)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.KEYUP:
                done = True
        pygame.display.flip()
        clock.tick(FPS)

def dance_screen():
    pygame.mixer.pause()
    choir.play(loops=-1)
    vamp1 = pygame.transform.scale(vampFemale_img, (100, 128))
    vamp1.set_colorkey((BLACK))
    vamp1_rect = vamp1.get_rect()
    vamp1_rect.centerx = WINDOW_WIDTH *0.5 - 60
    vamp1_rect.bottom = WINDOW_HEIGHT - 60

    vamp2 = pygame.transform.scale(vampMale_img, (100, 128))
    vamp2.set_colorkey((BLACK))
    vamp2_rect = vamp2.get_rect()
    vamp2_rect.centerx = WINDOW_WIDTH *0.5 + 60
    vamp2_rect.bottom = WINDOW_HEIGHT - 60

    bats = []
    bats_rect = []
    for b in range(np.random.randint(1,5)):
        bat_size = np.random.randint(30,60)
        bat = pygame.transform.scale(bat_img, (bat_size*2, bat_size))
        bat.set_colorkey((BLACK))
        bat_rect = bat.get_rect()
        bat_rect.centery = np.random.randint(WINDOW_HEIGHT*0.2, WINDOW_HEIGHT*0.7)
        bat_rect.centerx = np.random.randint(WINDOW_WIDTH*0.2, WINDOW_WIDTH*0.8)
        bats.append(bat)
        bats_rect.append(bat_rect)

    done = False
    while not done:
        screen.blit(bgDark_img, bgDark.get_rect())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    vamp1_rect.centerx -= 7
                    vamp2_rect.centerx -= 7
                    for i in range(len(bats)):
                        bats_rect[i].centerx += 7
                        bats_rect[i].centery += 7 * np.random.choice([-1,1])
                if event.key == pygame.K_RIGHT:
                    vamp1_rect.centerx += 7
                    vamp2_rect.centerx += 7
                    for i in range(len(bats)):
                        bats_rect[i].centerx -= 7
                        bats_rect[i].centery += 7 * np.random.choice([-1,1])
        screen.blit(vamp1, vamp1_rect)
        screen.blit(vamp2, vamp2_rect)
        for i in range(len(bats)):
            screen.blit(bats[i], bats_rect[i])
        draw_text(screen,
          "This lovely song is GHOST CHOIR, from Louis Zong. Press Escape Key not to dance...",
          18, WINDOW_WIDTH/2, WINDOW_HEIGHT*0.91)
        pygame.display.flip()
        clock.tick(FPS)

def main():
    all_sprites = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    axes = pygame.sprite.Group()
    bats = pygame.sprite.Group()
    myVampire = Player()
    all_sprites.add(myVampire)
    for i in range(16):
        for j in range(3):
            g = Gem(60*i, 5+60*j)
            all_sprites.add(g)
            gems.add(g)

    done = False
    game_over = False
    dance_time = False
    tick = 0
    
    while not done:
        if not game_over:
            start_screen()
            game_over = True

        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_SPACE:
                    myVampire.shoot(all_sprites, axes)
                elif event.key == pygame.K_b:
                    bat = Bat()
                    all_sprites.add(bat)
                    bats.add(bat)
                    print("bat")
                elif event.key == pygame.K_UP:
                    myVampire.angle += 10
                    print(myVampire.angle)
                elif event.key == pygame.K_DOWN:
                    myVampire.angle -= 10
                    print(myVampire.angle)
                elif event.key == pygame.K_s:
                    global BG_IMAGE, BG
                    if BG_IMAGE == bgOrange_img:
                        BG_IMAGE = bgBlue_img
                        BG = bgBlue
                    elif BG_IMAGE == bgBlue_img:
                        BG_IMAGE = bgYellow_img
                        BG = bgYellow
                    elif BG_IMAGE == bgYellow_img:
                        BG_IMAGE = bgDark_img
                        BG = bgDark
                    elif BG_IMAGE == bgDark_img:
                        BG_IMAGE = bgOrange_img
                        BG = bgOrange

        current_hour = datetime.datetime.now().strftime("%H")
        current_hour = int(current_hour)
        # if current_hour >= 6 and current_hour <12:
        #     BG_IMAGE = bgYellow_img
        #     BG = bgYellow
        # elif current_hour >=12 and current_hour <18:
        #     BG_IMAGE = bgBlue_img
        #     BG = bgBlue
        # elif current_hour >=18 and current_hour <20:
        #     BG_IMAGE = bgYellow_img
        #     BG = bgYellow
        # else:
        #     BG_IMAGE = bgDark_img
        #     BG = bgDark

        all_sprites.update()

        gemHitsAxes = pygame.sprite.groupcollide(gems, axes, True, True)
        gemHitsBats = pygame.sprite.groupcollide(gems, bats, True, True)
        gemHits = {**gemHitsAxes, **gemHitsBats}

        gemsRemaining = len(gems) - len(gemHits)

        if gemsRemaining <= 20:
            for g in gems:
                g.rect.y += 60
            for i in range(16):
                g = Gem(60*i, 5)
                all_sprites.add(g)
                gems.add(g)

        for g, b in gemHits.items():
            if g.gemIndex == 'Blue':
                playPianoSound(pianoKeys[0])
            elif g.gemIndex == 'Green':
                playPianoSound(pianoKeys[1])
            elif g.gemIndex == 'Red':
                playPianoSound(pianoKeys[2])
            elif g.gemIndex == 'White':
                playPianoSound(pianoKeys[3])
            elif g.gemIndex == 'SkyBlue':
                playPianoSound(pianoKeys[4])
            elif g.gemIndex == 'Magenta':
                playPianoSound(pianoKeys[5])
            elif g.gemIndex == 'Else':
                instruments[np.random.randint(0, len(instruments))].play()
            elif g.gemIndex == 'Choir':
                print("Choir")
                if not dance_time:
                    print("!!!")
                    dance_screen()
                    dance_time = True
                    choir.stop()

        screen.fill(BLACK)
        screen.blit(BG_IMAGE, BG.get_rect())

        all_sprites.draw(screen)
        draw_text(screen,
                  "*Tip: Press 'b' key to call your awesome bat buddy!",
                  18, WINDOW_WIDTH/2, WINDOW_HEIGHT*0.91)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()