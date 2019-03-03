### Sample python code for NeoPixels on Raspberry Pi
### this code is random suggestion MSU (football) effects for my sister
### orginal code: https://github.com/DanStach/rpi-ws2811
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
num_pixels = 400

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = .5


### colorAll2Color(c1, c2) allows two alternating colors to be shown
def colorAll2Color(c1, c2):
    for i in range(num_pixels):
        if(i % 2 == 0): # even
            pixels[i] = c1
        else: # odd   
            pixels[i] = c2
    pixels.show()

### wheel(pos) will convert value 0 to 255 to get a color value.
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

def FadeInOut(red, green, blue, delay):
    r = 0
    g = 0
    b = 0
      
    for k in range(256):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)
     
    for k in range(256, -1, -1):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)
        
        
def fadeToBlack(ledNo, fadeValue):
    #ctypes.c_uint32 oldColor = 0x00000000UL
    #ctypes.c_uint8 r = 0
    #ctypes.c_uint8 g = 0
    #ctypes.c_uint8 b = 0

    oldColor = pixels[ledNo]
#    r = (oldColor & 0x00ff0000) >> 16
#    g = (oldColor & 0x0000ff00) >> 8
#    b = (oldColor & 0x000000ff)
    #print(oldColor)
#    r = oldColor >> 16
#    g = (oldColor >> 8) & 0xff
#    b = oldColor & 0xff
    r = oldColor[0]
    g = oldColor[1]
    b = oldColor[2]

    if (r<=10):
        r = 0
    else:
        r = r - ( r * fadeValue / 256 )

    if (g<=10):
        g = 0
    else:
        g = g - ( g * fadeValue / 256 )

    if (b<=10):
        b = 0
    else:
        b = b - ( b * fadeValue / 256 )

    pixels[ledNo] = ( int(r), int(g), int(b) )


def meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay): 
    for loop in range(LoopCount):
        pixels.fill((0,0,0))
        
        for i in range(num_pixels*2):
            # fade brightness all LEDs one step
            for j in range(num_pixels):
                if (not meteorRandomDecay) or (random.randint(0,10) > 5):
                    fadeToBlack(j, meteorTrailDecay )      
            
            # draw meteor
            for j in range(meteorSize):
                if ( i-j < num_pixels) and (i-j >= 0): 
                    pixels[i-j] = (red, green, blue)

        pixels.show()
        time.sleep(SpeedDelay)

def TwinkleRandom(Count, SpeedDelay, OnlyOne):
    pixels.fill((0,0,0))

    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill((0,0,0))

    #time.sleep(SpeedDelay)

def SparkleNonDestructive(red, green, blue, Count, SpeedDelay):

    for i in range(Count):    
        Pixel = random.randint(0,num_pixels-1)
        preColor = pixels[Pixel] 
        pixels[Pixel] = (red,green,blue)
        pixels.show()
        time.sleep(SpeedDelay)
        pixels[Pixel] = preColor

def SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay):
    pixels.fill((red,green,blue))

    for i in range(Count):
        Pixel = random.randint(0,num_pixels-1)
        pixels[Pixel] = (255,255,255)
        pixels.show()
        time.sleep(SparkleDelay)
        pixels[Pixel] = (red,green,blue)
        pixels.show()
        time.sleep(SpeedDelay)

def candycane_custom(c1, c2, thisbright, delay, cycles):
    index = 0
    N3  = int(num_pixels/3)
    N6  = int(num_pixels/6)
    N12 = int(num_pixels/12)
    for loop in range(cycles):
        index = index + 1
        cSwap = c1
        c1 = c2
        c2 = cSwap
        for i in range(N6):
            j0 = int((index + i + num_pixels - N12) % num_pixels)
            j1 = int((j0+N6) % num_pixels)
            j2 = int((j1+N6) % num_pixels)
            j3 = int((j2+N6) % num_pixels)
            j4 = int((j3+N6) % num_pixels)
            j5 = int((j4+N6) % num_pixels)
            pixels[j0] = brightnessRGB(c1[0], c1[1], c1[2], int(thisbright*.75))
            pixels[j1] = brightnessRGB(c2[0], c2[1], c2[2], thisbright)
            pixels[j2] = brightnessRGB(c1[0], c1[1], c1[2], int(thisbright*.75))
            pixels[j3] = brightnessRGB(c2[0], c2[1], c2[2], thisbright)
            pixels[j4] = brightnessRGB(c1[0], c1[1], c1[2], int(thisbright*.75))
            pixels[j5] = brightnessRGB(c2[0], c2[1], c2[2], thisbright)

            # show pixel values 
            pixels.show()
            time.sleep(delay)


def randomLevelsCustom( levelobj, clearall, delay, cycles ):
    NUM_LEVELS = len(levelobj)
    for loop in range(cycles):

        level = random.randint(0, NUM_LEVELS)
        if (NUM_LEVELS == level):
            level = 0
        light_level_random(levelobj, level, 1)
        pixels.show()
        time.sleep(delay)

def light_level_random( levels, level, clearall ):

    if (clearall):
        pixels.fill((0, 0, 0)) # clear all
        pixels.show()
    
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levels[level-1]
    
    for i in range(startPxl, levels[level]):
        pixels[i] = wheelBrightLevel(random.randint(0, 255), random.randint(50, 255))

def randomLevelsCustom2Colors( c1, c2, levelobj, clearall, delay, cycles ):
    NUM_LEVELS = len(levelobj)
    for loop in range(cycles):
        if loop % 2 == 0:
            color = c1
        else:
            color = c2

        level = random.randint(0, NUM_LEVELS)
        if (NUM_LEVELS == level):
            level = 0
        light_level_random_color(color, levelobj, level, 1)
        pixels.show()
        time.sleep(delay)

def light_level_random_color(color, levels, level, clearall ):

    if (clearall):
        pixels.fill((0, 0, 0)) # clear all
        pixels.show()
    
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levels[level-1]
    
    for i in range(startPxl, levels[level]):
        pixels[i] = color
      

while True:
    random.seed(num_pixels)

    # make all pixels white
    # fill(red, green, blue)
    pixels.fill((255, 255, 255)) 
    pixels.show()
    time.sleep(1)

    # make all pixels Green
    # fill(red, green, blue)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1)

    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(3)

    # makes the strand of pixels show SnowSparkle (random)
    # SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay)
    # SnowSparkle(16, 16, 16, 100, 0.020, random.randint(100,1000)/1000)
    SnowSparkle(11, 102, 35, 90, 0, 0)

    # make all pixels white
    # fill(red, green, blue)
    pixels.fill((255, 255, 255)) 
    pixels.show()
    time.sleep(.1)

    # make all pixels Green
    # fill(red, green, blue)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(.1)

    # make all pixels white
    # fill(red, green, blue)
    pixels.fill((255, 255, 255)) 
    pixels.show()
    time.sleep(.1)

    # make all pixels Green
    # fill(red, green, blue)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(.1)

    # fast effect
    pixels.fill((255, 255, 255)) 
    pixels.show()
    pixels.fill((0, 255, 0)) 
    pixels.show()
    pixels.fill((255, 255, 255)) 
    pixels.show()
    pixels.fill((0, 255, 0)) 
    pixels.show()
    pixels.fill((255, 255, 255)) 
    pixels.show()
    pixels.fill((0, 255, 0)) 
    pixels.show()


    # shows 2 color every other pixel (white, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((255, 255, 255), (0, 255, 0)) 
    time.sleep(wait_time * 4)

    # makes the strand of pixels show  randomLevelsCustom
    # levels = (58, 108, 149, 187, 224, 264, 292, 309, 321, 327, 336, 348)
    levels = (110, 200, 270, 340, 390, 400)
    #random_levels(8, 0.1, 500)
    # randomLevelsCustom( levelobj, clearall, delay, cycles ):
    #randomLevelsCustom(levels, 1, 0, 50)
    #def randomLevelsCustom2Colors( c1, c2, levelobj, clearall, delay, cycles ):
    randomLevelsCustom2Colors((255,255,255),(0,255,0), levels, 1, 0, 50)
    

    # makes the strand of pixels show candycane_custom
    # candycane_custom(c1, c2, brightness, delay, cycles)
    # white and green
    pixels.fill((0, 0, 0)) 
    pixels.show()
    candycane_custom((255,255,255), (0, 255, 0), 255, 0, 5)
    time.sleep(wait_time)

    
    # makes the strand of pixels show 
    # meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay)
    #meteorRain(0, 255, 0, 10, 64, True, 1, 0)
    #time.sleep(wait_time)


    # makes the strand of pixels show SnowSparkle (random)
    # SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay)
    # SnowSparkle(16, 16, 16, 100, 0.020, random.randint(100,1000)/1000)
    SnowSparkle(11, 102, 35, 300, 0, 0)

    # makes the strand of pixels show Sparkle (white)
    # Sparkle(red, green, blue, Count, SpeedDelay)
    #SparkleNonDestructive(11, 102, 35, 50, 0)




