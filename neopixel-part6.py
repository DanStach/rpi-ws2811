### Sample python code for NeoPixels on Raspberry Pi
### this code is an improvement on the level effects from 
### Arduino NeoPixels effects in C++, from tweaking4all
### Arduino Controlled Tree - http://youtu.be/MD3-YBaFQvw
### orginal code: https://pastebin.com/Qe0Jttme


import time
import random
import math
import ctypes

import board
import neopixel
import serial

wait_time = 1

num_pixels = 144
pixel_pin = board.D18
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)


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

def hsv_to_rgb(h, s, v):
    if s == 0.0: 
        v*=255
        return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i
    p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f))))
    v*=255
    i%=6
    if i == 0: 
        return (v, t, p)
    if i == 1: 
        return (q, v, p)
    if i == 2: 
        return (p, v, t)
    if i == 3: 
        return (p, q, v)
    if i == 4: 
        return (t, p, v)
    if i == 5: 
        return (v, p, q)

def level_object_creator(levelgp):
    print(levelgp)
    levels = []
    levels.append(num_pixels)
    pixel_remaining = num_pixels
    for item in levelgp:
        level_num = pixel_remaining - item 
        if (level_num > 0):
            levels.insert(0,level_num)
        else:
            del levels[0] #remove last element from list
            break
        pixel_remaining = level_num
    print(levels)
    return(levels)

def random_levels( levelobj, delay, cycles ):
    levels = level_object_creator(levelobj)
    NUM_LEVELS = len(levels)
    for loop in range(cycles):

        level = random.randint(0, NUM_LEVELS)
        if (NUM_LEVELS == level):
            level = 0
        light_level_random(level, levels, 1)
        pixels.show()
        time.sleep(delay)

def light_level_random( level, levels,  clearall ):
    print("l=", level, " ls=", levels)
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



def drain(levelobj, delay):
    levels = level_object_creator(levelobj)
    for pancakeLevel in range(len(levels)):

        for level in range(pancakeLevel, -1, -1):
            clear_level(level, levels)
            if (level >= 1) :
                light_level_random(level-1, levels, 0)

            # show pixel values 
            pixels.show()
            time.sleep(delay)


def pancake(groupsObj, delay):
    levels = level_object_creator(groupsObj)
    NUM_LEVELS = len(levels)
    for pancakeLevel in range(NUM_LEVELS):
        
        for level in range(NUM_LEVELS-1, pancakeLevel-1, -1):
            # only needed if you ouput to a small display 
            # updateControlVars()   

            if (level < NUM_LEVELS-1):
                clear_level(level+1, levels)
                
            light_level_random(level, levels, 0)

            # show pixel values 
            pixels.show()
            time.sleep(delay)


def clear_level( level, levelobj):
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levelobj[level-1]
    for i in range(startPxl, levelobj[level]):
        pixels[i] = (0,0,0)  #CRGB::Black;



while True:
    random.seed(num_pixels)
    
    # make all pixels black
    # fill(red, green, blue)
    print("fill - blk")
    pixels.fill((0, 0, 0)) # red
    pixels.show()
    time.sleep(2)

    # make all pixels Red
    # fill(red, green, blue)
    print("fill - red")
    pixels.fill((255, 0, 0)) # red
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Green
    # fill(red, green, blue)
    print("fill - green")
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Blue
    # fill(red, green, blue)
    print("fill - blue")
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(wait_time)

    levelgroups = (5, 9, 14, 17, 19, 23, 25, 28, 30, 32, 30, 30, 43)
    level_object_creator(levelgroups)
    time.sleep(wait_time)



    # makes the strand of pixels show random_levels
    # pancake(level, delay)
    print("pancake")
    pixels.fill((0, 0, 0))
    time.sleep(wait_time)
    pancake(levelgroups, .1)
    time.sleep(wait_time)

    # makes the strand of pixels show drain
    # drain(level, delay)
    print("drain")
    #drain(8, 0.5)
    drain(levelgroups, .1)
    time.sleep(wait_time)

    # makes the strand of pixels show random_levels
    # random_levels( NUM_LEVELS, delay, cycles )
    #random_levels(12, 0, 500)
    print("random_levels")
    #random_levels(8, 0.1, 500)
    random_levels(levelgroups, 0, 50)
    time.sleep(wait_time)
