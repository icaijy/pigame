import PCF8591 as ADC
HEIGHT = 512
WIDTH = 788
def setup():
    ADC.setup(0x48)                    # Setup PCF8591
    global state

alien = Actor('alien')
alien.pos = 100, 56

def angle(x, y):
    if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15 and ADC.read(1) - 125 < 15 and ADC.read(1) - 125 > -15:
        return "home"
    if y == 125:
        y = 127     # there are a little error with my device.
    x -= 127
    y -= 127

    return [x/64,y/64]

def draw():
    screen.clear()
    alien.draw()
def update():
    a = angle(ADC.read(0), ADC.read(1))
    if a!="home":
        alien.top+=a[0]
        alien.left+=a[1]



setup()