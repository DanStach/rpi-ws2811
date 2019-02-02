# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random
import math
import serial
import ctypes



# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
wait_time = 1
thisbright = 255



def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def wheelBrightLevel(pos, bright):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)

    # bight level logic
    color = brightnessRGB(r, g, b, bright)
    r = color[0]
    g = color[1]
    b = color[2]

    return color if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def brightnessRGB(red, green, blue, bright):
    r = (bright/256.0)*red
    g = (bright/256.0)*green
    b = (bright/256.0)*blue
    return (int(r), int(g), int(b))

def random_burst(delayStart, delayEnd , LoopCount):
    for loop in range(LoopCount):
        randomIndex= random.randint(0, num_pixels-1)
        rndhue = random.randint(0, 255)
        rndbright = random.randint(10, thisbright)
        
        # CHSV(rndhue, thissat, rndbright)
        print(str(randomIndex) + " " + str(rndhue) + " " + str(rndbright))
        pixels[randomIndex] = wheelBrightLevel(rndhue, rndbright)
        
        pixels.show()
        delay = random.randint(delayStart*1000, delayEnd*1000)/1000
        time.sleep(delay)





def rainbow_cycle(delay, cycles):
    for j in range(255 * cycles):
        for i in range(num_pixels):
            # " // "  this divides and returns the integer value of the quotient. 
            # It dumps the digits after the decimal
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(delay)

    


while True:
    random.seed(num_pixels)

    # make all pixels Red
    # fill(red, green, blue)
    pixels.fill((255, 0, 0)) # red
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Green
    # fill(red, green, blue)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Blue
    # fill(red, green, blue)
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(wait_time)
    
    # makes the strand of pixels show random_burst
    # random_burst(delayStart, delayEnd , LoopCount)
    pixels.fill((0, 0, 0))
    random_burst(0.1, .5, 100)
    time.sleep(wait_time)
    #random_burst();

    #rgb_propeller();

    #rainbow();

    #rainbow_fade();
    #   if ((demoMode) && !(demoStateCountdown%5)) demoStateCountdown-=2;
    #   adjdelay = (adjdelay < 30) ? 30 : adjdelay;


    #   rainbow_loop();


    #   if ((demoMode) && !(demoStateCountdown%5)) demoStateCountdown-=2;
    #   adjdelay = (adjdelay < 50) ? 50 : adjdelay;
    #   matrix();


    #   demoStateCountdown -= 2;
    #   adjdelay = (adjdelay < 120) ? 120 : adjdelay;
    #   random_march();


    #   loop5(leds);
    #   adjdelay = adjdelay/3;


    #   twinkle(leds);


    #   candycane();


    #   if (!USE_LEVEL_ANIMATIONS) incrementState();
    #   adjdelay = (adjdelay < 100) ? 100 : adjdelay;
    #   demoStateCountdown -= 15;
    #   random_levels();


    #   if (!USE_LEVEL_ANIMATIONS) incrementState();
    #   rainbow();
    #   adjdelay = (adjdelay < 50) ? 50 : adjdelay;
    #   if (demoMode) demoStateCountdown -= 600;
    #   drain();
    #   pancake();



