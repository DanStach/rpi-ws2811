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
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = 1


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





def FireCustom(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, cycles):
#   CoolingRangeStart: (0-255) cooling random value, start range
#   CoolingRangeEnd: (0-255) cooling random value, end range
#   Sparking: (0-100)  chance of sparkes are added randomly controld througn a % value, 100= 100% and 0 = 0%
#   SparkingRangeStart: (0- number of pixels) spark position random value, start range
#   SparkingRangeEnd: (0- number of pixels) spark position random value, end range
#   SpeedDelay: (0-...) slow down the effect by injecting a delay in Sec. 0=no delay, .05=50msec, 2=2sec
#
# FireCustom: makes the strand of pixels show an effect that looks flame. This effect also
# adds more detail control of "sparks" that inject "heat" to the effect, thus changing color 
# and flame length. The spark position can also be controled via start and end range. 
# Color options include red, green, and blue.
#
# Improvements: 
#  - add choice for 3 diffrent fire effect logic.
#  - add choice to control heat values "random.randint(160,255)"
#  - add choice for flame color options include red, green, and blue.

    # intialize heat array, same size of as the strip of pixels
    heat = []
    for i in range(num_pixels):
        heat.append(0)

    # 
    for loop in range(cycles):
        cooldown = 0
        
        # Step 1.  Cool down every cell a little
        for i in range(num_pixels):
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
            heat[y] = random.randint(160,255)

        # Step 4.  Convert heat to LED colors
        for j in range(num_pixels):
            t192 = round((int(heat[j])/255.0)*191)

            # calculate ramp up from
            heatramp = t192 & 63 # 0..63  0x3f=63
            heatramp <<= 2 # scale up to 0..252

            # figure out which third of the spectrum we're in:
            if t192 > 0x80: # hottest 128 = 0x80
                pixels[j] = (255, 255, int(heatramp))
            elif t192 > 0x40: # middle 64 = 0x40
                pixels[j] = (255, int(heatramp), 0)
            else: # coolest
                pixels[j] = (int(heatramp), 0, 0)

        pixels.show()
        time.sleep(SpeedDelay)


def FireCustomMirror(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, cycles):
#   CoolingRangeStart: (0-255) cooling random value, start range
#   CoolingRangeEnd: (0-255) cooling random value, end range
#   Sparking: (0-100)  chance of sparkes are added randomly controld througn a % value, 100= 100% and 0 = 0%
#   SparkingRangeStart: (0- number of pixels) spark position random value, start range
#   SparkingRangeEnd: (0- number of pixels) spark position random value, end range
#   SpeedDelay: (0-...) slow down the effect by injecting a delay in Sec. 0=no delay, .05=50msec, 2=2sec
#
# FireCustomMirror: makes the strand of pixels show an effect that looks flame. This is simular to FireCustom, 
# however it mirrors the effect on top and bottom  (rather than using just from bottom). The intent is to
# have a fire effect that could be used 144 pixel strip for a lanyard id. 
#
# Improvements: 
#  - add choice for 3 diffrent fire effect logic.
#  - add choice to control heat values "random.randint(160,255)"
#  - add choice for flame color options include red, green, and blue.

    # intialize heat array, same size of as the strip of pixels
    heat = []
    halfNumPixel = int( num_pixels/2) # note that this will round down
    for i in range(halfNumPixel):
        heat.append(0)

    # 
    for loop in range(cycles):
        cooldown = 0
        
        # Step 1.  Cool down every cell a little
        for i in range(halfNumPixel):
            cooldown = random.randint(CoolingRangeStart, CoolingRangeEnd)
            if cooldown > heat[i]:
                heat[i]=0
            else: 
                heat[i]=heat[i]-cooldown
        
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(halfNumPixel - 1, 2, -1):
            heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
            
        # Step 3.  Randomly ignite new 'sparks' near the bottom
        if random.randint(0,100) < Sparking:
            
            # randomly pick the position of the spark
            y = random.randint(SparkingRangeStart,SparkingRangeEnd)
            # different fire effects 
            heat[y] = random.randint(160,255)

        # Step 4.  Convert heat to LED colors
        for j in range(halfNumPixel):
            t192 = round((int(heat[j])/255.0)*191)

            # calculate ramp up from
            heatramp = t192 & 63 # 0..63  0x3f=63
            heatramp <<= 2 # scale up to 0..252

            # figure out which third of the spectrum we're in for color:
            if t192 > 0x80: # hottest 128 = 0x80
                colortemp = (255, 255, int(heatramp))
            elif t192 > 0x40: # middle 64 = 0x40
                colortemp = (255, int(heatramp), 0)
            else: # coolest
                colortemp = (int(heatramp), 0, 0)
            
            pixels[j] = colortemp
            pixels[num_pixels-1-j] = colortemp


        pixels.show()
        time.sleep(SpeedDelay)


def candycane_custom(c1, c2, thisbright, delay, cycles):
    N3  = int(num_pixels/3)
    N6  = int(num_pixels/6)
    N12 = int(num_pixels/12)

    for loop in range(cycles):
        cSwap = c1
        c1 = c2
        c2 = cSwap
        for i in range(N6):
            j0 = int((i + num_pixels - N12) % num_pixels)
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




def RunningLightsPreExisting(WaveDelay, cycles):
    
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    for loop in range(cycles):
        
        # change the color level on the existing colors
        for i in range(num_pixels):
            # calculate level
            level = math.sin(i + loop) * 127 + 128

            # change color level on for red, green, and blue
            r = (level/255)*stripExisting[i][0]
            g = (level/255)*stripExisting[i][1]
            b = (level/255)*stripExisting[i][2]
            pixels[i] = (int(r), int(g),int(b))

        pixels.show()
        time.sleep(WaveDelay)


def SnowSparkleExisting(Count, SparkleDelay, SpeedDelay):
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    for i in range(Count):
        index = random.randint(0,num_pixels-1)
        pixels[index] = (255,255,255)
        pixels.show()
        time.sleep(SparkleDelay)
        pixels[index] = stripExisting[index]
        pixels.show()
        time.sleep(SpeedDelay)


def HalloweenEyesExisting(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause):
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

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
    
    # Set all pixels to back
    # set color of eyes for given location
    for i in range(EyeWidth):
        pixels[StartPoint + i] = stripExisting[StartPoint + i]
        pixels[Start2ndEye + i] = stripExisting[Start2ndEye + i]
    pixels.show()

    # pause before changing eye location
    time.sleep(EndPause)


# HeartBeatExisiting - mimics a heart beat pulse, with 2 beats at different speeds. The existing colors 
# on the pixel strip are preserved, rather than a single color.
#
# HeartBeatExisiting(beat1Step, beat1FadeInDelay, beat1FadeOutDelay, beat1Delay,
#                     beat2Step, beat2FadeInDelay, beat2FadeOutDelay, beat1Delay, cycles):
# HeartBeatExisiting(3, .005, .003, 0.001, 6, .002, .003, 0.05, 10)
#
#   beat1Step: (1-255) first beat color transition step
#   beat1FadeInDelay: (0-2147483647) first beat fade in trasition speed, in seconds
#   beat1FadeOutDelay: (0-2147483647) first beat fade out trasition speed, in seconds
#   beat1Delay: (0-2147483647)  beat time delay bewteen frist and sencond beat, in seconds
#   beat2Step: (1-255) second beat color transition step
#   beat2FadeInDelay: (0-2147483647) second beat fade in trasition speed, in seconds
#   beat2FadeOutDelay: (0-2147483647) second beat fade out trasition speed, in seconds
#   beat1Delay: (0-2147483647)  beat time delay bewteen sencond and first beat, in seconds
#   cycles: (1-2147483647) number of times this effect will run
def HeartBeatExisiting(beat1Step, beat1FadeInDelay, beat1FadeOutDelay, beat1Delay, beat2Step, beat2FadeInDelay, beat2FadeOutDelay, beat2Delay, cycles):
#HeartBeatExisiting(beat1Step, beat1FadeInDelay, beat1FadeOutDelay, beat1Delay, 
#                   beat2Step, beat2FadeInDelay, beat2FadeOutDelay, beat2Delay, cycles):
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    for loop in range(cycles):               

        for ii in range(1, 252, beat1Step): #for ( ii = 1 ; ii <252 ; ii = ii = ii + x)
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat1FadeInDelay)

        for ii in range(252, 3, -beat1Step): #for (int ii = 252 ; ii > 3 ; ii = ii - x){
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat1FadeOutDelay)
            
        time.sleep(beat1Delay)
        
        for ii in range(1, 252, beat1Step): #for (int ii = 1 ; ii <255 ; ii = ii = ii + y){
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat2FadeInDelay)

        for ii in range(252, 3, -beat1Step): #for (int ii = 255 ; ii > 1 ; ii = ii - y){
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat2FadeOutDelay)
    
        time.sleep(.050) 


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


def randomLevelsCustomColors( colorobj, levelobj, clearall, delay, cycles ):
    colorCount = len(colorobj)
    NUM_LEVELS = len(levelobj)

    for loop in range(cycles):
        colorIndex = loop % colorCount
        pcolor = colorobj[colorIndex]


        level = random.randint(0, NUM_LEVELS)
        if (NUM_LEVELS == level):
            level = 0
        light_level_random_color(pcolor, levelobj, level, 1)
        pixels.show()
        time.sleep(delay)

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

def LevelsCustomColors(color, levels, level, clearall ):

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



def LevelsColorsCustom( colorobj, levelobj, delay ):
    colorCount = len(colorobj)
    NUM_LEVELS = len(levelobj)

    # for each level
    for levelnum in range(NUM_LEVELS):
        # gather color info
        colorIndex = levelnum % colorCount
        pcolor = colorobj[colorIndex]

        if (NUM_LEVELS == levelnum):
            level = 0
        else:
            level = levelnum
        light_level_random_color(pcolor, levelobj, level, False)
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
        #print("i=",i,"color=",color,"startPxl=",startPxl,"level=",level)
        pixels[i] = color
        

def theaterChaseCustom(colorobj, darkspace, cycles, SpeedDelay):
    colorCount = len(colorobj)
    n = colorCount + darkspace
    for j in range(cycles):
        for q in range(n):
            for i in range(0, num_pixels, n):
                for index in range(0, colorCount, 1):
                    if i+q+index < num_pixels:
                        #print("pixel=",i+q+index, "index", index,"i",i,"q",q,"colorobj[index]",colorobj[index]) 
                        pixels[i+q+index] = colorobj[index]
            
            pixels.show()
            time.sleep(SpeedDelay)
            pixels.fill((0, 0, 0))
            
            for i in range(0, num_pixels, n):
                for index in range(0, colorCount, 1):
                    if i+q+index < num_pixels:
                        pixels[i+q+index] = (0,0,0)
        

def RotateExisting( delay, cycles):
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    for loop in range(cycles):
        pixels[0] = pixels[num_pixels - 1]

        # rotate pixel positon
        for i in range(num_pixels - 1, 0, -1):
            pixels[i] = pixels[i-1]
        
        # there is an issue with first 2 pixels are same color 
        #pixels[0] = (0,0,0)
        pixels.show()
        time.sleep(delay)

while True:
    random.seed(num_pixels)


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
    
    # makes the strand of pixels RotateExisting
    #RotateExisting( delay, cycles)
    cloudObj = ((16,125,171),(18,142,195),(20,159,218),(29,173,234),(53,182,236)) 
    colorAllColorGroup(cloudObj)
    RotateExisting( .1, 100)
    
    # makes the strand of pixels show 
    # theaterChaseCustom(colorobj, darkspace, cycles, SpeedDelay)
    print("theaterChaseCustom")
    cobj = [(255,255,0),(0,0,255),(255,0,0)]
    theaterChaseCustom(cobj, 2, 100, 0.2)
    time.sleep(wait_time)

    # makes the strand of pixels show Fire
    # FireCustom(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, 
    #             SpeedDelay, cycles):
    #   CoolingRangeStart: (0-255) cooling random value, start range
    #   CoolingRangeEnd: (0-255) cooling random value, end range
    #   Sparking: (0-100)  chance of sparkes are added randomly controld througn a % value, 100= 100% and 0 = 0%
    #   SparkingRangeStart: (0- number of pixels) spark position random value, start range
    #   SparkingRangeEnd: (0- number of pixels) spark position random value, end range
    #   SpeedDelay: (0-...) slow down the effect by injecting a delay in Sec. 0=no delay, .05=50msec, 2=2sec
    print("FireCustomMirror")
    FireCustomMirror(0, 2, 30, 0, int(num_pixels/6), 0, 900) # red fire
    time.sleep(wait_time)


    # makes the strand of pixels show Fire
    # FireCustom(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, 
    #             SpeedDelay, cycles):
    #   CoolingRangeStart: (0-255) cooling random value, start range
    #   CoolingRangeEnd: (0-255) cooling random value, end range
    #   Sparking: (0-100)  chance of sparkes are added randomly controld througn a % value, 100= 100% and 0 = 0%
    #   SparkingRangeStart: (0- number of pixels) spark position random value, start range
    #   SparkingRangeEnd: (0- number of pixels) spark position random value, end range
    #   SpeedDelay: (0-...) slow down the effect by injecting a delay in Sec. 0=no delay, .05=50msec, 2=2sec
    print("FireCustom")
    FireCustom(0, 2, 90, 0, int(num_pixels/3), 0, 900) # red fire
    time.sleep(wait_time)

    ### this code tests that the levels are correct ##### 
    cw = (255,255,255)
    cr = (255,0,0)
    cg = (0,255,0)
    cb = (0,0,255)
    cy = (255,255,0)
    levels = (43, 73, 103, 135, 160, 188, 213, 236, 255, 272, 286, 295, 300)
    levels = (10, 20, 30, 40, 50, 60, 70, 236, 255, 272, 286, 295, 300)

    #levels = (58, 108, 149, 187, 224, 264, 292, 300)
    #levels = (110, 200, 270, 300)
    print("LevelsColorsCustom  - level  test ")
    colorobj = ( cw, cr, cg, cb, cy, cw, cr, cg, cb, cy, cw, cr, cg, cb, cy, cw, cr, cg, cb, cy ) 
    LevelsColorsCustom(colorobj, levels, .5)
    time.sleep(wait_time)

    print("colorAllColorGroup - level test")
    colorobj = ( cw,cw,cw,cw,cw,cw,cw,cw,cw,cw,
                 cr,cr,cr,cr,cr,cr,cr,cr,cr,cr,
                 cg,cg,cg,cg,cg,cg,cg,cg,cg,cg,
                 cb,cb,cb,cb,cb,cb,cb,cb,cb,cb,
                 cy,cy,cy,cy,cy,cy,cy,cy,cy,cy )
    colorAllColorGroup(colorobj)
    time.sleep(wait_time)

    # makes the strand of pixels show randomLevelsCustom2Colors
    # randomLevelsCustom2Colors( c1, c2, levelobj, clearall, delay, cycles )
    #levels = (110, 200, 270, 340, 390, 400)
    print("randomLevelsCustom2Colors")
    randomLevelsCustom2Colors((100,100,100),(0,100,0), levels, True, .2, 10)
    time.sleep(wait_time)
    
    # makes the strand of pixels show randomLevelsCustomColors
    # randomLevelsCustomColors( colorobj levelobj, clearall, delay, cycles ):
    #levels = (110, 200, 270, 340, 390, 400)
    print("randomLevelsCustomColors")
    colorobj = ( (100,100,100), (0,100,0), (100,0,0) )
    randomLevelsCustomColors(colorobj, levels, 1, .2, 10)
    time.sleep(wait_time)

    # makes the strand of pixels show LevelsColorsCustom
    #LevelsColorsCustom( colorobj, levelobj, delay )
    #levels = (110, 200, 270, 340, 390, 400)
    print("LevelsColorsCustom")
    colorobj = ( (100,100,100), (100,0,0), (0,100,0), (0,0,100),  (0,100,100) )
    LevelsColorsCustom(colorobj, levels, .5)
    time.sleep(wait_time*5)
    
    # shows pattern of colors on the given pixels 
    # colorAllColorGroup((red1, green1, blue1), (red2, green2, blue2), ...) 
    print("colorAllColorGroup multi")
    xmasColorGroup = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 255, 255)) 
    colorAllColorGroup(xmasColorGroup) 
    time.sleep(wait_time)


    # shows 2 color every other pixel (red, green)
    # SnowSparkleExisting(Count, SparkleDelay, SpeedDelay)
    print("colorAll2Color purple orange")
    colorAll2Color((75,0,130), (255,165,0) )
    SnowSparkleExisting(100, .1, .1)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    # RunningLightsPreExisting(WaveDelay, cycles):
    print("RunningLightsPreExisting red green")
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    RunningLightsPreExisting(0, 100)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    #HeartBeatExisiting(beat1Step, beat1FadeInDelay, beat1FadeOutDelay, beat1Delay, 
    #                   beat2Step, beat2FadeInDelay, beat2FadeOutDelay, beat2Delay, cycles):
    print("HeartBeatExisiting")
    HeartBeatExisiting(3, .005, .003, 0.001, 6, .002, .003, 0.05, 1)


    # makes the strand of pixels show candycane_custom
    # candycane_custom(c1, c2, brightness, delay, cycles)
    print("candycane_custom white green")
    candycane_custom((255,255,255), (0,200,0), 255, 0, 2)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    print("colorAll2Color red green")
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(wait_time)

    # sean suggests we have lightning and thunder
    #maybe strobe lightning and a fast heart beat for thunder?

    # sean suggests rain falling...

    # need to work on the rotating cloud palet

    #burnt out blub effect

    # effect for lanyard id (144 pixel strip)

    # vertical stripe effect, using groups of Pixel# to define a top to bottom stripe
    
    # fire effect using palette colors. if heat range is 0-255, then give fucntion 3 colors
    # and it can find the grandiant between the colors and give fire effect 256 color options?  

    # on tree ring levels, have every other ring rotate