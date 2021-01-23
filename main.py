import pgzrun
import time
alien = Actor('alien')
alien.pos = 100, 56

WIDTH = 300
HEIGHT = 300

def draw():
    screen.clear()
    alien.draw()
def update():
    alien.top+=1
    alien.left+=1

def on_mouse_down(pos):
    if alien.collidepoint(pos):
        set_alien_hurt()
        clock.schedule_unique(set_alien_normal, 1.0)


def set_alien_hurt():
    alien.image = 'alien_hurt'
    sounds.eep.play()


def set_alien_normal():
    alien.image = 'alien'

pgzrun.go()
