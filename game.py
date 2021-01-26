import PCF8591 as ADC
import pgzrun
from random import *
import math
import os
import sys

def restartp():
    os.execl(sys.executable, sys.executable, *sys.argv)

game_over = False
end = False
finish_choose = False
HEIGHT = 788
WIDTH = 1024
#music.play("bgm")
restart = Actor("restart")
restart.pos = WIDTH/2, 200
house = Actor("house")
house.pos = 75,75
bombox = Actor("bombox")
bombox.pos = WIDTH-75, HEIGHT-75
def setup():
    ADC.setup(0x48)                    # Setup PCF8591
    global state

class Alien(Actor):
    def __init__(self, code):
        self.code = str(code)
        Actor.__init__(self,"p"+self.code+"/p"+self.code+"_stand")
        self.blood = 5
        self.pos = house.pos
        self.ishurt = False

    def hurt(self):
        self.ishurt = True
        self.nohurt = True
        self.image = "p"+self.code+"/p"+self.code+"_hurt"
        self.blood-=1
        sounds.eep.play()
        self.home()
        clock.schedule_unique(self.recovery, 1.0)
        print(self.blood)

    def recovery(self):
        self.ishurt = False
        self.image = "p"+self.code+"/p"+self.code+"_stand"
    def home(self):
        self.pos = house.pos




class Bomb(Actor):
    def __init__(self):
        Actor.__init__(self,"bomb")
        self.home()
    def move(self):
        self.left+=(alien.pos[0]-self.left+randint(-700,700))/64
        self.top+=(alien.pos[1]-self.top+randint(-700,700))/64

    def nearalien(self):
        if math.sqrt((self.left-alien.left)**2+(self.top-alien.top)**2) <=150:
            return True


    def home(self):
        self.left = bombox.left+randint(-100,100)
        self.top = bombox.top+randint(-100,100)



alien1 = Actor('p1/p1_front')
alien2 = Actor('p2/p2_front')
alien3 = Actor('p3/p3_front')

alien1.pos = 200, 394
alien2.pos = 500, 394
alien3.pos = 800, 394
bomb1 = Bomb()
bomb2 = Bomb()
bomb3 = Bomb()
bomb4 = Bomb()
def angle(x, y):
    if x - 125 < 15 and x - 125 > -15 and y - 125 < 15 and y - 125 > -15:
        return "home"
    if y == 125:
        y = 127     # there are a little error with my device.=
    x -= 127
    y -= 127

    return [x/8,y/8]

def draw():
    screen.clear()
    screen.blit("background.jpg", (0,0))
    house.draw()
    bombox.draw()
    if finish_choose == False:
        alien1.draw()
        alien2.draw()
        alien3.draw()
        screen.draw.text("choose your alien!", (200, 100), color=(255,0,0), fontsize=100)


    if end:
        alien.pos = WIDTH/2, HEIGHT/2
        alien.image = "p"+alien.code+"/p"+alien.code+"_hurt"
        alien.draw()
        restart.draw()

    elif finish_choose:
        alien.draw()
        bomb1.draw()
        bomb2.draw()
        bomb3.draw()
        bomb4.draw()
        for x in range(alien.blood):
            x+=1



def update():
    global game_over
    global end
    a = angle(ADC.read(0), ADC.read(1))
    if finish_choose and not end:
        if alien.blood<=0:
            game_over = True
        if a!="home" and not alien.ishurt:
            if alien.top<=0:
                alien.top+=20
            if alien.top+alien.height>=HEIGHT:
                alien.top-=20
            if alien.left<=0:
                alien.left+=20
            if (alien.left+alien.width)>=WIDTH:
                alien.left-=20
            alien.top+=a[0]
            alien.left+=a[1]
        if alien.ishurt==False:
            bomb1.move()
            bomb2.move()
            bomb3.move()
            bomb4.move()
            if bomb1.nearalien() or bomb2.nearalien() or bomb3.nearalien() or bomb4.nearalien():
                alien.hurt()
                bomb1.home()
                bomb2.home()
                bomb3.home()
                bomb4.home()
    if game_over and not end:
        end = True
        sounds.you_lose.play()
        clock.schedule_unique(play_game_over, 2.0)

        #exit()
def play_game_over():
    sounds.game_over.play()

def on_mouse_down(pos):
    global alien
    global finish_choose
    if end:
        if restart.collidepoint(pos):
            restartp()
    if not finish_choose:
        if alien1.collidepoint(pos):
            alien = Alien(1)
            finish_choose = True
            sounds.go.play()


        if alien2.collidepoint(pos):
            alien = Alien(2)
            finish_choose = True
            sounds.go.play()

        if alien3.collidepoint(pos):
            alien = Alien(3)
            finish_choose = True
            sounds.go.play()




setup()
pgzrun.go()