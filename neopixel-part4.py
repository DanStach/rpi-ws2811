### Sample python code for NeoPixels on Raspberry Pi
### this code is ported from Arduino NeoPixels effects in C++
### orginal code: https://github.com/FastLED/FastLED/blob/master/examples

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

def fadeall(scale):
    for i in range(num_pixels): #for(int i = 0; i < NUM_LEDS; i++) 
        #leds[i].nscale8(250)
        
        #get current color pf pixel
        c = pixels[i]
        red = c[0]
        green = c[1]
        blue = c[2]
        
        # scale color
        #scale = 250
        r = (scale/256.0)*red
        g = (scale/256.0)*green
        b = (scale/256.0)*blue

        #change pixel
        pixels[i] = (int(r),int(g),int(b))


def brightnessRGB(red, green, blue, bright):
    r = (bright/256.0)*red
    g = (bright/256.0)*green
    b = (bright/256.0)*blue
    return (int(r), int(g), int(b))



def blink(index, delay, cycles):
    for loop in range(cycles):
        # Turn the LED on, then pause
        pixels[index] = (255,0,0) #CRGB::Red
        pixels.show()
        time.sleep(delay)
        # Now turn the LED off, then pause
        pixels[index] = (0,0,0) #CRGB::Black
        pixels.show()
        time.sleep(delay)

def Cylon(delay, cycles):
    for loop in range(cycles):
        hue = 0
        # First slide the led in one direction
        for i in range(num_pixels):
            # Set the i'th led to red 
            hue = hue + 1
            if hue == 256:
                hue = 0

            pixels[i] =  wheel(hue) #CHSV(hue++, 255, 255);
            # Show the leds
            pixels.show() 
            # now that we've shown the leds, reset the i'th led to black
            # leds[i] = CRGB::Black;
            fadeall(250)
            # Wait a little bit before we loop around and do it again
            time.sleep(delay) #delay(10);

        # Now go in the other direction.  
        for i in range(num_pixels-1,0,-1):
            # Set the i'th led to red 
            hue = hue + 1
            if hue == 256:
                hue = 0

            pixels[i] =  wheel(hue) #CHSV(hue++, 255, 255);
            # Show the leds
            pixels.show()
            # now that we've shown the leds, reset the i'th led to black
            # leds[i] = CRGB::Black;
            fadeall(250)
            # Wait a little bit before we loop around and do it again
            time.sleep(delay) #delay(10);
    

def fill_rainbow(initialhue, deltahue, delay):
    hue = initialhue
    
    for i in range(num_pixels):
        pixels[i] =  wheel(hue) 
        hue = hue + deltahue
        if hue > 255:
            hue = hue - 255
        pixels.show()
        time.sleep(delay)

def fill_gradient_RGB( startpos, startcolor, endpos, endcolor, delay ):
    endpos = endpos + 1
    
    # if the points are in the wrong order, straighten them
    if endpos < startpos :
        t = endpos
        tc = endcolor
        endcolor = startcolor
        endpos = startpos
        startpos = t
        startcolor = tc

    rdistance87 = (endcolor[0] - startcolor[0])
    gdistance87 = (endcolor[1] - startcolor[1])
    bdistance87 = (endcolor[2] - startcolor[2])

    pixeldistance = endpos - startpos
    
    divisor = pixeldistance
    # check if  divisor is 0
    if divisor == 0:
        divisor = 1

    rdelta87 = rdistance87 / divisor
    gdelta87 = gdistance87 / divisor
    bdelta87 = bdistance87 / divisor
    
    r88 = startcolor[0]
    g88 = startcolor[1]
    b88 = startcolor[2]

    # for each pixel (from startpos to endpos)
    for i in range(startpos, endpos, 1):
        # assing color to pixel
        pixels[i] = ( int(r88), int(g88), int(b88) )
        # show new color 
        pixels.show()
        time.sleep(delay)

        # change color
        r88 = r88 + rdelta87
        g88 = g88 + gdelta87
        b88 = b88 + bdelta87
        






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


    # makes the strand of pixels show fill_gradient_RGB
    # fill_gradient_RGB( startpos, startcolor, endpos, endcolor, delay )
    fill_gradient_RGB( 0, (255,255,255), 49, (0,0,0), .1 ) #white to black
    fill_gradient_RGB( 0, (255,0,0), 49, (0,255,0), .1 ) #red to green
    time.sleep(wait_time)

    # makes the strand of pixels show fill_rainbow
    # fill_rainbow(initialhue, deltahue, delay)
    fill_rainbow(0, 10, .1)
    time.sleep(wait_time)

    # makes the strand of pixels show Cylon
    # Cylon(delay, cycles)
    Cylon(.05, 100)
    time.sleep(wait_time)

    # makes the strand of pixels show blink
    # blink(index, delay, cycles)
    time.sleep(wait_time)
    blink(0, .5, 8)



