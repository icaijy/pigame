import PCF8591 as ADC
import pgzrun
from random import *

finish_choose = False

HEIGHT = 788
WIDTH = 1024
#music.play("bgm")
def setup():
    ADC.setup(0x48)                    # Setup PCF8591
    global state

alien1 = Actor('p1/p1_front')
alien2 = Actor('p2/p2_front')
alien3 = Actor('p3/p3_front')

alien1.pos = 200, 394
alien2.pos = 500, 394
alien3.pos = 800, 394
bomb1 = Actor('bomb')
bomb1.pos = randint(200, WIDTH-200), randint(200,HEIGHT-200)

bomb2 = Actor('bomb')
bomb2.pos = randint(200, WIDTH-200), randint(200,HEIGHT-200)

bomb3 = Actor('bomb')
bomb3.pos = randint(200, WIDTH-200), randint(200,HEIGHT-200)

bomb4 = Actor('bomb')
bomb4.pos = randint(200, WIDTH-200), randint(200,HEIGHT-200)
def angle(x, y):
    if x - 125 < 15 and x - 125 > -15 and y - 125 < 15 and y - 125 > -15:
        return "home"
    if y == 125:
        y = 127     # there are a little error with my device.=
    x -= 127
    y -= 127

    return [x/16,y/16]

def draw():
    screen.clear()
    screen.blit("background.jpg", (0,0))
    if finish_choose == False:
        alien1.draw()
        alien2.draw ()
        alien3.draw()
        screen.draw.text("choose your alien!", (200, 100), color=(255,0,0), fontsize=100)

    else:
        alien.draw()
        bomb1.draw()
        bomb2.draw()
        bomb3.draw()
        bomb4.draw()



def update():
    a = angle(ADC.read(0), ADC.read(1))
    if finish_choose:
        if a!="home":
            if alien.top<=0:
                alien.top+=10
            if alien.top+alien.height>=HEIGHT:
                alien.top-=10
            if alien.left<=0:
                alien.left+=10
            if (alien.left+alien.width)>=WIDTH:
                alien.left-=10
            alien.top+=a[0]
            alien.left+=a[1]
        bomb1.left+=(alien.pos[0]-bomb1.left+randint(-700,700))/64
        bomb1.top+=(alien.pos[1]-bomb1.top)/64

        bomb2.left+=(alien.pos[0]-bomb2.left)/64
        bomb2.top+=(alien.pos[1]-bomb2.top+randint(-700,700))/64

        bomb3.left+=(alien.pos[0]-bomb3.left+randint(-700,700))/64
        bomb3.top+=(alien.pos[1]-bomb3.top)/64

        bomb4.left+=(alien.pos[0]-bomb4.left)/64
        bomb4.top+=(alien.pos[1]-bomb4.top+randint(-700,700))/64


def on_mouse_down(pos):
    global alien_code
    global alien
    global finish_choose
    if not finish_choose:
        if alien1.collidepoint(pos):
            alien = Actor("p1/p1_stand")
            finish_choose = True
            alien.pos = 512, 394
            alien_code = "1"

        if alien2.collidepoint(pos):
            alien = Actor("p2/p2_stand")
            finish_choose = True
            alien.pos = 512, 394
            alien_code = "2"

        if alien3.collidepoint(pos):
            alien = Actor("p3/p3_stand")
            alien.pos = 512, 394
            finish_choose = True
            alien_code = "3"


setup()
pgzrun.go()