### Sample python code for NeoPixels on Raspberry Pi
### this code is random suggestion from my family, friends, and other examples on the web. 
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
num_pixels = 144

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = .5
cred = (255, 0, 0)
cblue = (0, 0, 255)
cgreen = (0, 255, 0)
cyellow = (255, 255, 0)
cpurple = (160, 32, 240)
corange = (255, 165, 0)
cwhite = (255, 255, 255)

### colorAll2Color allows two alternating colors to be shown
#
def colorAll2Color(c1, c2):
    for i in range(num_pixels):
        if(i % 2 == 0): # even
            pixels[i] = c1
        else: # odd   
            pixels[i] = c2
    pixels.show()

# colorAllColorGroup(colorObject) allows colors to be 
# - colorObject: list of color objects. example ((255, 0, 0), (0, 255, 0))  
def colorAllColorGroup(colorObject):
    colorCount = len(colorObject)

    for i in range(num_pixels):
            colorIndex = i % colorCount
            pixels[i] = colorObject[colorIndex]

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


def rainbow_cycle(delay, cycles):
    for j in range(255 * cycles):
        for i in range(num_pixels):
            # " // "  this divides and returns the integer value of the quotient. 
            # It dumps the digits after the decimal
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
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

def fill_group_random(groupCount, delay, cycles):
    pixels.fill((255, 0, 0)) # inital fill red
    pixels.show()
    wheelPos = 0 
    for c in range(cycles):
        
        fillColor = wheel(wheelPos)
        for i in range(groupCount): 
            for q in range(0, num_pixels, groupCount):
                if i+q < num_pixels:
                    pixels[i+q] = fillColor
                    
            pixels.show()
            time.sleep(delay)
            
        wheelPos = random.randint(0, 255)
        
            
def fill_group_expand_random(groupCount, delay, cycles):
    pixels.fill((255, 0, 0)) # inital fill red
    pixels.show()
    wheelPos = 0 
    for c in range(cycles):
        
        fillColor = wheel(wheelPos)
        for i in range(int(groupCount/2+1)): 
            for q in range(0, int(num_pixels), int(groupCount)):
                if i+q < num_pixels:
                    pixels[i+q] = fillColor
                if groupCount-i+q < num_pixels:    
                    pixels[groupCount-i+q] = fillColor

            pixels.show()
            time.sleep(delay)
        random.seed()
        wheelPos = random.randint(0, 255)
        
def theaterChaseDot(sectionCount, dotColor, delay, cycles):
    pixels.fill((0, 0, 0)) # inital fill black
    pixels.show()
    startPos = 0
    for c in range(cycles):

        for i in range(int(sectionCount)): 
            for q in range(0, int(num_pixels), int(sectionCount)):
                if i+q < num_pixels:
                    pixels[i+q] = dotColor
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    pixels[i+q-1] = (0,0,0)

            pixels.show()
            time.sleep(delay)


def theaterChaseDotCollection(sectionCount, dotColor, delay, cycles):
    pixels.fill((0, 0, 0)) # inital fill black
    pixels.show()
    sectionEnd = sectionCount
    for c in range(cycles):

        for i in range(int(sectionCount)):
            if sectionEnd == 0:
                pixels.fill((0, 0, 0)) # inital fill black
                sectionEnd = sectionCount
                
            for q in range(0, int(num_pixels), int(sectionCount)):
                if i+q < num_pixels:
                    pixels[i+q] = dotColor 
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    if i > 1:
                        pixels[i+q-1] = (0,0,0)
        
            pixels.show()
            if i >=  sectionEnd-1:
                sectionEnd -=1
                break
            else:
                time.sleep(delay)
        
        
    


while True:
    random.seed()

    # make all pixels black
    # fill(red, green, blue)
    print("fill black")
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(2)
    
    # make all pixels Red
    # fill(red, green, blue)
    print("fill red")
    pixels.fill((255, 0, 0)) # red
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Green
    # fill(red, green, blue)
    print("fill green")
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Blue
    # fill(red, green, blue)
    print("fill blue")
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(wait_time)
    
    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDotCollection")
    theaterChaseDotCollection(20, cwhite, .1, 20)
    time.sleep(wait_time)
    
    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDot")
    theaterChaseDot(20, cred, .1, 5)
    time.sleep(wait_time)

    # fill_group_expand_random(groupCount, delay, cycles)
    print("fill_group_expand_random")
    fill_group_expand_random(50, .1, 40)
    time.sleep(wait_time)

    # fill_group(groupCount, delay, cycles)
    print("fill_group_random")
    fill_group_random(50, .1, 40)
    time.sleep(wait_time)
    
    # rainbow cycle
    # rainbow_cycle(delay, cycles) 
    print("rainbow_cycle")
    rainbow_cycle(0, 5) 
    time.sleep(wait_time)