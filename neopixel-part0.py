### Sample python code for NeoPixels on Raspberry Pi
### this code is random suggestion from my family, friends, and other examples on the web
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
num_pixels = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = 1


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



### makes the strand of pixels show Fire
# Fire(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount)
#CoolingRangeStart = 0-255
#CoolingRangeEnd = 0-255
#Sparking = 0-100  (0= 0% sparkes randomly added, 100= 100% sparks randomly added)
#SparkingRangeStart = 0-255 
#SparkingRangeEnd = 0-255
#FireColor = 0-2 (0=red, 1=blue , 2=green)
#FireEffect = 0-2 (these are differnet ways of adding sparks to the strip)
def FireCustom(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount):
     heat = []
     for i in range(num_pixels):
        heat.append(0)
     for l in range(LoopCount):
        cooldown = 0
        
        # Step 1.  Cool down every cell a little
        for i in range(num_pixels):
            # for 50 leds and cooling 50
            # cooldown = random.randint(0, 12)
            # cooldown = random.randint(0, ((Cooling * 10) / num_pixels) + 2)
            cooldown = random.randint(CoolingRangeStart, CoolingRangeEnd)
            if cooldown > heat[i]:
                heat[i]=0
            else: 
                heat[i]=heat[i]-cooldown
        
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(num_pixels - 1, 2, -1):
            heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
            
        # Step 3.  Randomly ignite new 'sparks' near the bottom
        if random.randint(0,100) < Sparking:
            
            # randomly pick the position of the spark
            y = random.randint(SparkingRangeStart,SparkingRangeEnd)
            # different fire effects 
            if FireEffect == 0:
                heat[y] = random.randint(int(heat[y]),255)
            elif FireEffect == 1:
                heat[y] = heat[y] + random.randint(160,255)
            else:
                heat[y] = random.randint(160,255)

        # Step 4.  Convert heat to LED colors
        for j in range(num_pixels):
            t192 = round((int(heat[j])/255.0)*191)

            # calculate ramp up from
            heatramp = t192 & 63 # 0..63  0x3f=63
            heatramp <<= 2 # scale up to 0..252
            # figure out which third of the spectrum we're in:
            if FireColor == 2: #green flame
                if t192 > 0x80: # hottest 128 = 0x80
                    pixels[j] = (int(heatramp),255, 255)
                elif t192 > 0x40: # middle 64 = 0x40
                    pixels[j] = (0, 255, int(heatramp))
                else: # coolest
                    pixels[j] = (0, int(heatramp), 0)
            elif FireColor == 1: #blue flame
                if t192 > 0x80: # hottest 128 = 0x80
                    pixels[j] = (255, int(heatramp), 255)
                elif t192 > 0x40: # middle 64 = 0x40
                    pixels[j] = (int(heatramp), 0, 255)
                else: # coolest
                    pixels[j] = (0, 0, int(heatramp))
            else: #FireColor == 0: #red flame
                if t192 > 0x80: # hottest 128 = 0x80
                    pixels[j] = (255, 255, int(heatramp))
                elif t192 > 0x40: # middle 64 = 0x40
                    pixels[j] = (255, int(heatramp), 0)
                else: # coolest
                    pixels[j] = (int(heatramp), 0, 0)

        pixels.show()
        time.sleep(SpeedDelay)

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

    time.sleep(SpeedDelay)

def Sparkle(red, green, blue, Count, SpeedDelay):

    for i in range(Count):    
        Pixel = random.randint(0,num_pixels-1)
        pixels[Pixel] = (red,green,blue)
        pixels.show()
        time.sleep(SpeedDelay)
        pixels[Pixel] = (0,0,0)

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


def HalloweenEyes(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause):
    pixels.fill((0,0,0))
    r = 0
    g = 0
    b = 0

    # define eye1 and eye2 location
    StartPoint  = random.randint( 0, num_pixels - (2*EyeWidth) - EyeSpace )
    Start2ndEye = StartPoint + EyeWidth + EyeSpace

    #  set color of eyes for given location
    for i in range(EyeWidth):
        pixels[StartPoint + i] = (red, green, blue)
        pixels[Start2ndEye + i] = (red, green, blue)
    pixels.show()

    # if user wants fading, then fadeout pixel color
    if Fade == True:
        for j in range(Steps, -1, -1):
            r = (j/Steps)*red
            g = (j/Steps)*green
            b = (j/Steps)*blue

            for i in range(EyeWidth):
                pixels[StartPoint + i] = ((int(r), int(g), int(b)))
                pixels[Start2ndEye + i] = ((int(r), int(g), int(b)))

            pixels.show()
            time.sleep(FadeDelay)
    
    # Set all pixels to black
    pixels.fill((0,0,0))

    # pause before changing eye location
    time.sleep(EndPause)





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
    


    # makes the strand of pixels show Fire
    # Fire(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount)
    #CoolingRangeStart = 0-255
    #CoolingRangeEnd = 0-255
    #Sparking = 0-100  (0= 0% sparkes randomly added, 100= 100% sparks randomly added)
    #SparkingRangeStart = 0-255 
    #SparkingRangeEnd = 0-255
    #FireColor = 0-2 (0=red, 1=blue , 2=green)
    #FireEffect = 0-2
    FireCustom(0, 12, 25, 0, 10, 0.02, 0, 2, 500) # red fire
    time.sleep(wait_time)

    
    # makes the strand of pixels show 
    # meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay)
    meteorRain(255, 255, 255, 10, 64, True, 1, 0.030)
    time.sleep(wait_time)

    

    # makes the strand of pixels show SnowSparkle (random)
    # SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay)
    # SnowSparkle(16, 16, 16, 100, 0.020, random.randint(100,1000)/1000)
    SnowSparkle(16, 16, 16, 100, 0.1, 0.3)

    # makes the strand of pixels show Sparkle (white)
    # Sparkle(red, green, blue, Count, SpeedDelay)
    Sparkle(255, 255, 255, 100, 0)

    # makes the strand of pixels show TwinkleRandom
    # TwinkleRandom( Count, SpeedDelay, OnlyOne) 
    TwinkleRandom(20, 0.1, False)


    # fade in/out a single color (red / green / blue / white)
    # FadeInOut(red, green, blue, delay)
    FadeInOut(255, 0, 0, 0.01)
    FadeInOut(0, 255, 0, 0.01)
    FadeInOut(0, 0, 255, 0.01)
    FadeInOut(255, 255, 255, 0.01)

    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(wait_time)

    ### HALLOWEEN idea
    # shows 2 color every other pixel (purple, orange)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((128,0,128), (255,165,0) 
    time.sleep(wait_time)

    ### HALLOWEEN idea
    # make the strand of pixels show HalloweenEyes
    # HalloweenEyes(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause)
    HalloweenEyes(255, 0, 0, 1, 1, True, 10, 1, 3)
    time.sleep(wait_time)


