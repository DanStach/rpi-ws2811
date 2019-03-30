### Sample python code for NeoPixels on Raspberry Pi
### this code is ported from Arduino NeoPixels effects in C++, from tweaking4all
### orginal code: https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/#LEDStripEffectFire

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
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = 1


def colorAll2Color(c1, c2):
    for i in range(num_pixels):
        if(i % 2 == 0): # even
            pixels[i] = c1
        else: # odd   
            pixels[i] = c2
    pixels.show()


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


def rainbow_cycle(delay, cycles):
    for j in range(255 * cycles):
        for i in range(num_pixels):
            # " // "  this divides and returns the integer value of the quotient. 
            # It dumps the digits after the decimal
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(delay)


def RGBLoop(delay):
    for j in range(3):
        # Fade IN
        for k in range(256):
            if j == 0:
                pixels.fill((k, 0, 0))
            elif j == 1:
                pixels.fill((0, k, 0))
            elif j == 2:
                pixels.fill((0, 0, k))
            pixels.show()
            time.sleep(delay)

        # Fade OUT
        for k in range(256):
            if j == 2:
                pixels.fill((k, 0, 0))
            elif j == 1:
                pixels.fill((0, k, 0))
            elif j == 0:
                pixels.fill((0, 0, k))
            pixels.show()
            time.sleep(delay)
    
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

def Strobe(red, green, blue, StrobeCount, FlashDelay, EndPause):
    for j in range(StrobeCount):
        pixels.fill((red,green,blue))
        pixels.show()
        time.sleep(FlashDelay)
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(FlashDelay)
 
    time.sleep(EndPause)


    
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


def CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
  
    for i in range(num_pixels - EyeSize - 1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i+j] = (red, green, blue)

        pixels[i+EyeSize+1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
  
    time.sleep(ReturnDelay)
    time.sleep(10)
    
    for i in range(num_pixels - EyeSize - 2, -1, -1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i+j] = (red, green, blue)

        pixels[i+EyeSize+1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)

    time.sleep(ReturnDelay)
    time.sleep(10)

def NewKITT(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)

def CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    for i in range(int((num_pixels - EyeSize)/2), -1, -1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue)
        
        pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
        pixels[num_pixels - i - j] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[num_pixels - i - j] = (red, green, blue)

        pixels[num_pixels - i - EyeSize - 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)

    time.sleep(ReturnDelay)

def OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):

    for i in range(int(((num_pixels - EyeSize)/2)+1)):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue) 
        
        pixels[i + EyeSize +1] = (int(red/10), int(green/10), int(blue/10))
        pixels[num_pixels - i-1] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[num_pixels - i - j] = (red, green, blue)
        
        pixels[num_pixels - i - EyeSize - 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
  
    time.sleep(ReturnDelay)


def LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    for i in range(num_pixels - EyeSize - 2):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue)

        pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
    
    time.sleep(ReturnDelay)


def RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    for i in range(num_pixels - EyeSize - 2, 0, -1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue)

        pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
  
    time.sleep(ReturnDelay)


def Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne):
    pixels.fill((0,0,0))
  
    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (red, green, blue)
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill((0,0,0))

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


def RunningLights(red, green, blue, WaveDelay):
    Position = 0
    
    for j in range(num_pixels*2):
        Position = Position + 1
        
        for i in range(num_pixels):
            # sine wave, 3 offset waves make a rainbow!
            # float level = sin(i+Position) * 127 + 128;
            # setPixel(i,level,0,0);
            # float level = sin(i+Position) * 127 + 128;
            level = math.sin(i + Position) * 127 + 128
            r = int((level/255)*red)
            g = int((level/255)*green)
            b = int((level/255)*blue)
            pixels[i] = (r,g,b)

        pixels.show()
        time.sleep(WaveDelay)


def colorWipe(red, green, blue, SpeedDelay):
    for i in range(num_pixels):
        pixels[i] = (red, green, blue)
        pixels.show()
        time.sleep(SpeedDelay)


def theaterChase(red, green, blue, cycles, SpeedDelay):
    for j in range(cycles):
        for q in range(3):
            for i in range(0, num_pixels, 3):
                if i+q < num_pixels:
                    # turn every third pixel on
                    pixels[i+q] = (red, green, blue)
            
            pixels.show()
            time.sleep(SpeedDelay)
            
            for i in range(0, num_pixels, 3):
                if i+q < num_pixels:
                    # turn every third pixel off
                    pixels[i+q] = (0,0,0)


def theaterChaseRainbow(SpeedDelay, cycles):
    # cycle all 256 colors in the wheel
    for j in range(cycles):

        for q in range(3):
            for i in range(0, num_pixels, 3):
                # check that pixel index is not greater than number of pixels
                if i+q < num_pixels:
                    # turn every third pixel on
                    pixel_index = (i * 256 // num_pixels) + j
                    pixels[i+q] = wheel(pixel_index & 255)

            
            pixels.show()
            time.sleep(SpeedDelay)
            
            for i in range(0, num_pixels, 3):
                # check that pixel index is not greater than number of pixels
                if i+q < num_pixels:
                    # turn every third pixel off
                    pixels[i+q] = (0,0,0)



### Fix Me - something is broken with the logic. the color doesn't change. and the fire effect seems small
### orginal code; https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/#LEDStripEffectFire
def Fire(Cooling, Sparking, SpeedDelay, LoopCount):
     heat = []
     for i in range(num_pixels):
        heat.append(0)
     for l in range(LoopCount):
        cooldown = 0
        
        # Step 1.  Cool down every cell a little
        for i in range(num_pixels):
            randomCooldown = ((Cooling * 10) / num_pixels) + 2
            cooldown = random.randint(0, int(randomCooldown))

            if cooldown > heat[i]:
                heat[i]=0
            else: 
                heat[i]=heat[i]-cooldown
        
        
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(num_pixels - 1, 2, -1):
            heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
            
        # Step 3.  Randomly ignite new 'sparks' near the bottom
        if random.randint(0,255) < Sparking:
            y = random.randint(0,7)
            #heat[y] = heat[y] + random.randint(160,255)
            heat[y] = random.randint(160,255)

        # Step 4.  Convert heat to LED colors
        for j in range(num_pixels):
            setPixelHeatColor(j, int(heat[j]) )

        pixels.show()
        time.sleep(SpeedDelay)

def setPixelHeatColor (Pixel, temperature):
    # Scale 'heat' down from 0-255 to 0-191
    t192 = round((temperature/255.0)*191)

    # calculate ramp up from
    heatramp = t192 & 63 # 0..63  0x3f=63
    heatramp <<= 2 # scale up to 0..252
    # figure out which third of the spectrum we're in:
    if t192 > 0x80: # hottest 128 = 0x80
        pixels[Pixel] = (255, 255, int(heatramp))
    elif t192 > 0x40: # middle 64 = 0x40
        pixels[Pixel] = (255, int(heatramp), 0)
    else: # coolest
        pixels[Pixel] = (int(heatramp), 0, 0)

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

def fadeToBlack(ledNo, fadeValue):
    oldColor = pixels[ledNo]
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


def BouncingBalls(red, green, blue, BallCount, LoopCount):
    
    ## setup 
    Gravity = -9.81
    StartHeight = 1

    Height = []
    for i in range(BallCount):
        Height.append(0)

    ImpactVelocityStart = math.sqrt( -2 * Gravity * StartHeight )

    ImpactVelocity = []
    for i in range(BallCount):
        ImpactVelocity.append(0)

    TimeSinceLastBounce = []
    for i in range(BallCount):
        TimeSinceLastBounce.append(0)

    Position = []
    for i in range(BallCount):
        Position.append(0)

    ClockTimeSinceLastBounce = []
    for i in range(BallCount):
        ClockTimeSinceLastBounce.append(0)
    
    Dampening = []
    for i in range(BallCount):
        Dampening.append(0)

    for i in range(BallCount):
        ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))

        Height[i] = StartHeight
        Position[i] = 0
        ImpactVelocity[i] = ImpactVelocityStart
        TimeSinceLastBounce[i] = 0
        Dampening[i] = 0.90 - float(i)/pow(BallCount,2)
    
    ## loop 
    for loop in range(LoopCount):
        for i in range(BallCount):
            TimeSinceLastBounce[i] =  int(round(time.time() * 1000)) - ClockTimeSinceLastBounce[i]
            Height[i] = 0.5 * Gravity * pow( TimeSinceLastBounce[i]/1000 , 2.0 ) + ImpactVelocity[i] * TimeSinceLastBounce[i]/1000
    
            if Height[i] < 0:                 
                Height[i] = 0
                ImpactVelocity[i] = Dampening[i] * ImpactVelocity[i]
                ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))
        
                if ImpactVelocity[i] < 0.01:
                    ImpactVelocity[i] = ImpactVelocityStart

            Position[i] = round( Height[i] * (num_pixels - 1) / StartHeight)
        
        for i in range(BallCount):
            pixels[Position[i]] = (red,green,blue)
        
        pixels.show()
        pixels.fill((0, 0, 0))
        


def BouncingColoredBalls(BallCount, colors, LoopCount):
    
    ## setup 
    Gravity = -9.81
    StartHeight = 1

    Height = []
    for i in range(BallCount):
        Height.append(0)

    ImpactVelocityStart = math.sqrt( -2 * Gravity * StartHeight )

    ImpactVelocity = []
    for i in range(BallCount):
        ImpactVelocity.append(0)

    TimeSinceLastBounce = []
    for i in range(BallCount):
        TimeSinceLastBounce.append(0)

    Position = []
    for i in range(BallCount):
        Position.append(0)

    ClockTimeSinceLastBounce = []
    for i in range(BallCount):
        ClockTimeSinceLastBounce.append(0)
    
    Dampening = []
    for i in range(BallCount):
        Dampening.append(0)

    for i in range(BallCount):
        ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))

        Height[i] = StartHeight
        Position[i] = 0
        ImpactVelocity[i] = ImpactVelocityStart
        TimeSinceLastBounce[i] = 0
        Dampening[i] = 0.90 - float(i)/pow(BallCount,2)
    
    ## loop 
    for loop in range(LoopCount):
        for i in range(BallCount):
            TimeSinceLastBounce[i] =  int(round(time.time() * 1000)) - ClockTimeSinceLastBounce[i]
            Height[i] = 0.5 * Gravity * pow( TimeSinceLastBounce[i]/1000 , 2.0 ) + ImpactVelocity[i] * TimeSinceLastBounce[i]/1000
    
            if Height[i] < 0:                 
                Height[i] = 0
                ImpactVelocity[i] = Dampening[i] * ImpactVelocity[i]
                ClockTimeSinceLastBounce[i] = int(round(time.time() * 1000))
        
                if ImpactVelocity[i] < 0.01:
                    ImpactVelocity[i] = ImpactVelocityStart

            Position[i] = round( Height[i] * (num_pixels - 1) / StartHeight)
        
        for i in range(BallCount):
            pixels[Position[i]] = (colors[i][0],colors[i][1],colors[i][2])
        
        pixels.show()
        pixels.fill((0, 0, 0))

while True:
    random.seed()


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


    print("FireCustom")
    FireCustom(0, 2, 90, 0, int(num_pixels/3), 0.02, 0, 2, 300) # red fire
    FireCustom(0, 2, 90, 0, int(num_pixels/3), 0.02, 0, 2, 300) # red fire
    time.sleep(wait_time)
    FireCustom(0, 2, 90, 0, int(num_pixels/3), 0.02, 1, 2, 300) # blue fire
    time.sleep(wait_time)
    FireCustom(0, 2, 90, 0, int(num_pixels/3), 0.02, 2, 2, 300) # green fire
    time.sleep(wait_time)



    # loops red green blue
    # RGBLoop(delay)
    print("RGBLoop")
    RGBLoop(0)
    time.sleep(wait_time)

    # fade in/out a single color (red / green / blue / white)
    # FadeInOut(red, green, blue, delay)
    print("FadeInOut")
    FadeInOut(255, 0, 0, 0)
    FadeInOut(0, 255, 0, 0)
    FadeInOut(0, 0, 255, 0)
    FadeInOut(255, 255, 255, 0)

    # make all pixels stobe (white)
    # Strobe(red, green, blue, StrobeCount, FlashDelay, EndPause)
    print("Strobe")
    Strobe(255, 255, 255, 10, 0, 1)
    time.sleep(wait_time)
    Strobe(255, 255, 255, 10, 0, 1)
    time.sleep(wait_time)

    # make the strand of pixels show HalloweenEyes
    # HalloweenEyes(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause)
    print("HalloweenEyes")
    HalloweenEyes(255, 0, 0, 1, 1, True, 10, 1, 3)
    time.sleep(wait_time)
    HalloweenEyes(255, 0, 0, 1, 1, True, 10, 1, 3)
    time.sleep(wait_time)
    HalloweenEyes(255, 0, 0, 1, 1, True, 10, 1, 3)
    time.sleep(wait_time)
    HalloweenEyes(255, 0, 0, 1, 1, True, 10, 1, 3)
    time.sleep(wait_time)

    # makes the strand of pixels show CylonBounce
    # CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    print("CylonBounce")
    CylonBounce(255, 0, 0, 2, 0, 0)
    time.sleep(wait_time)

        # makes the strand of pixels show NewKITT 
    # NewKITT(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    print("NewKITT")
    NewKITT(255, 0, 0, 4, 0, 0)
    time.sleep(wait_time)

    # makes the strand of pixels show Twinkle
    # Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne)
    print("Twinkle")
    Twinkle(255, 0, 0, 10, 0.1, False)

    # makes the strand of pixels show TwinkleRandom
    # TwinkleRandom( Count, SpeedDelay, OnlyOne) 
    print("TwinkleRandom")
    TwinkleRandom(20, 0.1, False)

    # makes the strand of pixels show Sparkle (white)
    # Sparkle(red, green, blue, Count, SpeedDelay)
    print("Sparkle")
    Sparkle(255, 255, 255, 100, 0)

    # makes the strand of pixels show SnowSparkle (random)
    # SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay)
    # SnowSparkle(16, 16, 16, 100, 0.020, random.randint(100,1000)/1000)
    print("SnowSparkle")
    SnowSparkle(16, 16, 16, 100, 0.1, 0.3)

    # makes the strand of pixels show RunningLights (red)
    # RunningLights(red, green, blue, WaveDelay)
    print("RunningLights")
    RunningLights(255,0,0, 0)

    # makes the strand of pixels show colorWipe (green)
    # colorWipe(red, green, blue, SpeedDelay)
    print("colorWipe")
    colorWipe(0,255,0, 0)

    # rainbow cycle
    # rainbow cycle with 1ms delay per step, 5 cycles
    # rainbow_cycle(delay, cycles) 
    print("rainbow_cycle")
    rainbow_cycle(0, 5) 
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChase
    # theaterChase(red, green, blue, cycles, SpeedDelay)
    print("theaterChase")
    theaterChase(255,0,0, 20, 0)
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChaseRainbow
    # theaterChaseRainbow(SpeedDelay, cycles)
    print("theaterChaseRainbow")
    theaterChaseRainbow(0.1, 30)
    time.sleep(wait_time)

    # makes the strand of pixels show Fire
    # Fire(Cooling, Sparking, SpeedDelay, LoopCount)
    print("Fire")
    Fire(55, 120,0, 100)
    time.sleep(wait_time)

    # makes the strand of pixels show BouncingBalls
    # BouncingBalls(red, green, blue, BallCount, LoopCount)
    print("BouncingBalls") 
    BouncingBalls(255, 0, 0, 3, 100) 
    time.sleep(wait_time)

    # makes the strand of pixels show BouncingBalls
    # BouncingColoredBalls(BallCount, colors[][3], LoopCount) 
    print("BouncingColoredBalls")
    BouncingColoredBalls(3, ((255,0,0),(0,255,0),(0,0,255)), 1000)
    time.sleep(wait_time)
    
    # makes the strand of pixels show 
    # meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay)
    print("meteorRain")
    meteorRain(255, 255, 255, 10, 64, True, 1, 0)
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
    print("FireCustom")
    FireCustom(0, 12, 25, 0, 10, 0.02, 0, 2, 500) # red fire
    time.sleep(wait_time)
    FireCustom(0, 12, 25, 0, 10, 0.02, 1, 2, 500) # blue fire
    time.sleep(wait_time)
    FireCustom(0, 12, 25, 0, 10, 0.02, 2, 2, 500) # green fire
    time.sleep(wait_time)





    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    print("colorAll2Color")
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(wait_time)


