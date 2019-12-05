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
ccyan = (0, 255, 255)
cpurple = (160, 32, 240)
corange = (255, 165, 0)
cwhite = (255, 255, 255)
cblk = (0, 0, 0)

cltred = (127, 0, 0)
cltblue = (0, 0, 127)
cltgreen = (0, 30, 0)
cltyellow = (127, 127, 0)
cltcyan = (0, 127, 127)
cltpurple = (127, 0, 127)
cltorange = (127, 82, 0)
cltwhite = (127, 127, 127)

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
        
def colorTransition(color1, color2, percent):
    r1 = color1[0]
    g1 = color1[1]
    b1 = color1[2]

    r2 = color2[0]
    g2 = color2[1]
    b2 = color2[2]

    rdelta = color2[0] - color1[0]
    gdelta = color2[1] - color1[1]
    bdelta = color2[2] - color1[2]

    r = int((1-percent)*rdelta) + r1
    g = int((1-percent)*gdelta) + g1
    b = int((1-percent)*bdelta) + b1
    return (int(r), int(g), int(b))

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

def RotateObject(coloreObj, delay, cycles, isDirrectionForward):
    totalColorObj = len(coloreObj)
    for c in range(cycles): #for each cycle change index number
        index = c % num_pixels
        if(isDirrectionForward):
            for loop in range(num_pixels): # re-write pixels on strand
                pos = (index - loop) % totalColorObj
                pixels[loop] = coloreObj[pos]
        else:
            for loop in range(num_pixels): # re-write pixels on strand
                pos = (index + loop) % totalColorObj
                pixels[loop] = coloreObj[pos]



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
                
                
def theaterChaseDotCollectionMiddle(sectionCount, dotColor, delay, cycles):
    pixels.fill((0, 0, 0)) # inital fill black
    pixels.show()
    sectionCountHalf= int(sectionCount/2+1)
    sectionEnd = sectionCountHalf-1
    for c in range(cycles):

        for i in range(int(sectionCountHalf)): 
            for q in range(0, int(num_pixels), int(sectionCount)):
                if i+q < num_pixels:
                    pixels[i+q] = dotColor 
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    if i > 1:
                        pixels[i+q-1] = (0,0,0)
                        
                if sectionCount-i+q < num_pixels:    
                    pixels[sectionCount-i+q] = dotColor
                if sectionCount-i+q+1 < num_pixels and sectionCount-i+q+1 >= 0:
                    if i < num_pixels:
                        pixels[sectionCount-i+q+1] = (0,0,0)
        
            pixels.show()

            if sectionEnd < 0: # fill last dots, and reset
                pixels.fill(dotColor) # fill dots
                pixels.show()
                time.sleep(delay)
                
                pixels.fill((0, 0, 0)) # inital fill black
                pixels.show()
                time.sleep(delay)
                sectionCountHalf= int(sectionCount/2+1)
                sectionEnd = sectionCountHalf-1
                
            if i >=  sectionEnd:
                sectionEnd -=1
                time.sleep(delay)
                break
            else:
                time.sleep(delay)
        
def theaterChaseGroupCustom(colorobj, colorspace, darkspace, SpeedDelay, cycles):
    colorObjCount = len(colorobj)
    n = colorspace + darkspace
    for j in range(cycles):
        for k in range(colorObjCount):

            for q in range(n):
                for i in range(0, num_pixels, n):
                    for index in range(0, colorspace, 1):
                        if i+q+index < num_pixels:
                            pixels[i+q+index] = colorobj[k]
                
                pixels.show()
                time.sleep(SpeedDelay)
                pixels.fill((0, 0, 0))
                
                for i in range(0, num_pixels, n):
                    for index in range(0, colorObjCount, 1):
                        if i+q+index < num_pixels:
                            pixels[i+q+index] = (0,0,0)        


def PatternRunningLightsFade(mainColor, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles):

    stripPattern = []
    position = 0
    # make pixels for main effect
    if isDirrectionForward == True:
        start = mainLength
        end = 0
        increment  = -1
    else:
        start = 0
        end = mainLength
        increment  = 1
        
    for m in range (start, end, increment):
        level = int(m/mainLength*128)
        stripColor = brightnessRGB(mainColor[0], mainColor[1], mainColor[2], level)
        stripPattern.append(stripColor)
    position = position + mainLength

    # make pixels for space
    for i in range(spaceLength):
        stripPattern.append(spaceColor)
    
    return stripPattern
 
def PatternRunningLightsFadeColorObj(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles):

    stripPattern = []
    colorObjCount = len(colorObj)
    for k in range(colorObjCount):
        mainColor = colorobj[k]
        # make pixels for main effect
        if isDirrectionForward == True:
            start = mainLength
            end = 0
            increment  = -1
        else:
            start = 0
            end = mainLength
            increment  = 1
            
        for m in range (start, end, increment):
            level = int(m/mainLength*128)
            stripColor = brightnessRGB(mainColor[0], mainColor[1], mainColor[2], level)
            stripPattern.append(stripColor)

        # make pixels for space
        for i in range(spaceLength):
            stripPattern.append(spaceColor)
    
    return stripPattern

def PatternRunningLightsWaveColorObj(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles):

    stripPattern = []
    colorObjCount = len(colorObj)
    halfLength = math.floor(mainLength/2)
    for k in range(colorObjCount):
        mainColor = colorobj[k]

        # make pixel for frist part of wave
        for m in range (0, halfLength, 1):
            level = int(m/halfLength*128)
            stripColor = brightnessRGB(mainColor[0], mainColor[1], mainColor[2], level)
            stripPattern.append(stripColor)
            
        #if odd number replace the missing pixel
        if mainLength % 2 == 1: 
            stripPattern.append(mainColor)

        # make pixel for second part of wave
        for m in range (halfLength, 0, -1):
            level = int(m/halfLength*128)
            stripColor = brightnessRGB(mainColor[0], mainColor[1], mainColor[2], level)
            stripPattern.append(stripColor)

        # make pixels for space
        for i in range(spaceLength):
            stripPattern.append(spaceColor)
    
    return stripPattern


def PatternRunningLightsWaveTrans(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles):

    stripPattern = []
    colorObjCount = len(colorObj)
    halfLength = math.floor(mainLength/2)
    for k in range(colorObjCount):
        mainColor = colorobj[k]        

        # make pixel for frist part of wave
        for m in range (0, halfLength, 1):
            level = m/halfLength
            stripColor = colorTransition(mainColor, spaceColor, level)
            stripPattern.append(stripColor)
            
        #if odd number replace the missing pixel
        if mainLength % 2 == 1: 
            stripPattern.append(mainColor)

        # make pixel for second part of wave
        for m in range (halfLength, 0, -1):
            level = m/halfLength
            stripColor = colorTransition(mainColor, spaceColor, level)
            stripPattern.append(stripColor)

        # make pixels for space
        for i in range(spaceLength):
            stripPattern.append(spaceColor)
    
    return stripPattern

def PatternRunningLightsFadeTrans(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles):

    stripPattern = []
    colorObjCount = len(colorObj)
    for k in range(colorObjCount):
        mainColor = colorobj[k]
        # make pixels for main effect
        if isDirrectionForward == True:
            start = mainLength
            end = 0
            increment  = -1
        else:
            start = 0
            end = mainLength
            increment  = 1
            
        for m in range (start, end, increment):
            level = m/mainLength
            stripColor = colorTransition(mainColor, spaceColor, level)
            stripPattern.append(stripColor)

        # make pixels for space
        for i in range(spaceLength):
            stripPattern.append(spaceColor)
    
    return stripPattern

def DotCollection(colorObj, sectionCount, spaceColor, delay, cycles):
    pixels.fill(spaceColor) # inital fill black
    pixels.show()
    collectionCount = 0
    sectionEnd = sectionCount
    
    #for c in range(cycles):
    for c in range(cycles):
        dotColor = colorObj[c%len(colorObj)]
        
        #animate dots moving
        for i in range(int(sectionCount)):
            if sectionEnd == 0:
                pixels.fill(spaceColor) # inital fill black
                sectionEnd = sectionCount
                
            for q in range(0, int(num_pixels), int(sectionCount)):
                # add dotcolor
                if i+q < num_pixels:
                    pixels[i+q] = dotColor
                
                # replace previous dot with space color
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    if i > 0:
                        pixels[i+q-1] = spaceColor
        
            pixels.show()
            if i >=  sectionEnd-1:
                sectionEnd -=1
                break
            else:
                time.sleep(delay)
                
def DotCollectionColorChange(colorObj, sectionCount, spaceColor, delay, cycles):
    pixels.fill(spaceColor) # inital fill black
    pixels.show()
    
    collectionCount = 0
    sectionEnd = sectionCount
    
    #for c in range(cycles):
    for c in range(cycles):
        dotColor = colorObj[c%len(colorObj)]
        
        #animate dots moving
        for i in range(int(sectionCount)):
            if sectionEnd == 0:
                pixels.fill(spaceColor) # inital fill black
                sectionEnd = sectionCount
                
                
            for q in range(0, int(num_pixels), int(sectionCount)):
                # add dotcolor
                if i+q < num_pixels:
                    pixels[i+q] = dotColor
                
                # replace previous dot with space color
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    if i > 0 and i <  sectionEnd:
                        pixels[i+q-1] = spaceColor
                    
            #check if at end of space section
            if i <  sectionEnd-1:
                pixels.show()
                time.sleep(delay)
        pixels.show()
        sectionEnd -=1

def DotCollectionMiddleColorChange(colorObj, sectionCount, spaceColor, delay, cycles):
    pixels.fill(spaceColor) # inital fill black
    pixels.show()
    
    collectionCount = 0
    sectionCountDouble = sectionCount*2
    sectionEnd = sectionCount
    
    #for c in range(cycles):
    for c in range(cycles):
        dotColor = colorObj[c%len(colorObj)]
        
        #animate dots moving
        for i in range(int(sectionCount)):
            if sectionEnd == 0:
                pixels.fill(spaceColor) # inital fill black
                sectionEnd = sectionCount
                
            for q in range(0, int(num_pixels), int(sectionCountDouble)):
                # add dotcolor
                if i+q < num_pixels:
                    pixels[i+q] = dotColor
                if sectionCountDouble-i+q-1 < num_pixels:    
                    pixels[sectionCountDouble-i+q-1] = dotColor
                    
                # replace previous dot with space color
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    if i > 0 and i <  sectionEnd:
                        pixels[i+q-1] = spaceColor    
                if sectionCountDouble-i+q < num_pixels and sectionCountDouble-i+q >= 0:
                    if i < num_pixels and i <= sectionEnd-1:
                        pixels[sectionCountDouble-i+q] = spaceColor       

            #check if at end of space section
            if i <  sectionEnd-1:
                pixels.show()
                time.sleep(delay)
                
        pixels.show()
        sectionEnd -=1
        
def fill_section(colorObj, sectionCount, spaceColor, delay, isDirrectionForward, cycles):
    pixels.fill(spaceColor) # inital fill red
    pixels.show()
    
    if isDirrectionForward == True:
        start = 0
        end = sectionCount
        increment  = 1
    else:
        start = sectionCount
        end = 0
        increment  = -1
        
    for c in range(cycles):
        pixels.fill(spaceColor) # inital fill
        pixels.show()
        
        fillColor = colorObj[c%len(colorObj)]
        for i in range(start, end, increment): 
            for q in range(0, num_pixels, sectionCount):
                if i+q < num_pixels:
                    pixels[i+q] = fillColor
                    
            pixels.show()
            time.sleep(delay)

def fill_section_mid(colorObj, sectionCount, spaceColor, delay, isDirrectionOutward, cycles):
    pixels.fill(spaceColor) # inital fill red
    pixels.show()
    sectionCountDouble = sectionCount * 2
    
    if isDirrectionOutward == True:
        start = sectionCount
        end = 0
        increment  = -1
    else:
        start = 0
        end = sectionCount
        increment  = 1
        
    for c in range(cycles):
        pixels.fill(spaceColor) # inital fill
        pixels.show()
        
        fillColor = colorObj[c%len(colorObj)]
        for i in range(start, end, increment): 
            for q in range(0, num_pixels, sectionCountDouble):
                if i+q < num_pixels:
                    pixels[i+q] = fillColor
                if sectionCountDouble-i+q-1 < num_pixels:    
                    pixels[sectionCountDouble-i+q-1] = fillColor
                    
            pixels.show()
            time.sleep(delay)

def drain_section(colorObj, sectionCount, spaceColor, delay, isDirrectionForward, cycles):
    if isDirrectionForward == True:
        start = 0
        end = sectionCount
        increment  = 1
    else:
        start = sectionCount
        end = 0
        increment  = -1
            
    for c in range(cycles):
            
        fillColor = colorObj[c%len(colorObj)]
        pixels.fill(fillColor) # inital fill
        pixels.show()
        for i in range(start, end, increment): 
            for q in range(0, num_pixels, sectionCount):
                if i+q < num_pixels:
                    pixels[i+q] = spaceColor
                    
            pixels.show()
            time.sleep(delay)
        
def drain_section_mid(colorObj, sectionCount, spaceColor, delay, isDirrectionOutward, cycles):
    sectionCountDouble = sectionCount * 2
        
    if isDirrectionOutward == True:
        start = 0
        end = sectionCount
        increment  = 1
    else:
        start = sectionCount
        end = 0
        increment  = -1
            
    for c in range(cycles):
            
        fillColor = colorObj[c%len(colorObj)]
        pixels.fill(fillColor) # inital fill
        pixels.show()
        for i in range(start, end, increment): 
            for q in range(0, num_pixels, sectionCountDouble):
                if i+q < num_pixels:
                    pixels[i+q] = spaceColor
                if sectionCountDouble-i+q-1 < num_pixels:    
                    pixels[sectionCountDouble-i+q-1] = spaceColor
                    
            pixels.show()
            time.sleep(delay)
            
def FadeInOutColors(colorObj, spaceColor, incrementPrecent, delay, cycles):
    increment = int(incrementPrecent * 100)
    for c in range(cycles):
            
        fillColor = colorObj[c%len(colorObj)]
        pixels.fill(spaceColor) # inital fill
        pixels.show()
        
        for level in range(0, 100, increment):
            colorLevel = colorTransition(fillColor, spaceColor, level/100)
            pixels.fill(colorLevel) 
            pixels.show()
            time.sleep(delay)
        for level in range(100, 0, -increment):
            colorLevel = colorTransition(fillColor, spaceColor, level/100)
            pixels.fill(colorLevel) 
            pixels.show()
            time.sleep(delay)
            
def TransColors(colorObj, incrementPrecent, delay, cycles):
    increment = int(incrementPrecent * 100)
    for c in range(cycles):
            
        fillColor = colorObj[c%len(colorObj)]
        fillColor2 = colorObj[(c+1)%len(colorObj)]

        
        for level in range(0, 100, increment):
            colorLevel = colorTransition(fillColor, fillColor2, level/100)
            pixels.fill(colorLevel) 
            pixels.show()
            time.sleep(delay)
        for level in range(100, 0, -increment):
            colorLevel = colorTransition(fillColor, fillColor2, level/100)
            pixels.fill(colorLevel) 
            pixels.show()
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
    
    #TransColors(colorObj, incrementPrecent, delay, cycles)
    print("TransColors")
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    TransColors(colorobj, 0.01, .001, 20)
    time.sleep(wait_time)
    
    #FadeInOutColors(colorObj, spaceColor, incrementPrecent, delay, cycles)
    print("FadeInOutColors")
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    FadeInOutColors(colorobj, cblk, 0.01, .001, 20)
    time.sleep(wait_time)
    
    # drain_section_mid(colorObj, sectionCount, spaceColor, delay, isDirrectionOutward, cycles)
    print("drain_section_mid")
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    drain_section_mid(colorobj, 24, cblk, .1, True, 50)
    time.sleep(wait_time)

    
    # fill_section_mid(colorObj, sectionCount, spaceColor, delay, isDirrectionOutward, cycles)
    print("fill_section_mid")
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    fill_section_mid(colorobj, 24, cblk, .05, True, 50)
    time.sleep(wait_time)
    
    # drain_section(colorObj, sectionCount, spaceColor, delay, isDirrectionForward, cycles)
    print("drain_section")
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    drain_section(colorobj, 24, cblk, .05, True, 50)
    time.sleep(wait_time)
    
    # fill_section(colorObj, sectionCount, spaceColor, delay, isDirrectionForward, cycles)
    print("fill_section")
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    fill_section(colorobj, 24, cblk, .05, True, 50)
    time.sleep(wait_time)
    
    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDotCollection - green")
    theaterChaseDotCollection(48, cgreen, .1, 100)
    time.sleep(wait_time)

    print("DotCollectionMiddleColorChange - cpurple")
    # DotCollectionMiddleColorChange(colorObj, sectionCount, spaceColor, delay, cycles)
    colorobj = (cpurple, cpurple)
    DotCollectionMiddleColorChange(colorobj, 24, cltgreen, .05, 50)
    time.sleep(wait_time)

    print("DotCollectionMiddleColorChange")
    # DotCollectionMiddleColorChange(colorObj, sectionCount, spaceColor, delay, cycles)
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    DotCollectionMiddleColorChange(colorobj, 24, cblk, .05, 50)
    time.sleep(wait_time)

    print("DotCollection-green")
    #DotCollection(colorObj, sectionCount, delay, cycles)
    colorobj = (cblue,cblue)
    DotCollection(colorobj, 48, cltgreen, .05, 100)
    time.sleep(wait_time)

    
    print("DotCollectionColorChange")
    #DotCollectionColorChange(colorObj, sectionCount, spaceColor, delay, cycles):
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    DotCollectionColorChange(colorobj, 48, cblk, .05, 50)
    time.sleep(wait_time)

    print("DotCollection")
    #DotCollection(colorObj, sectionCount, delay, cycles)
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    DotCollection(colorobj, 48, cblk, .05, 100)
    time.sleep(wait_time)

    # RotateObject(coloreObj, delay, cycles, dirrection)
    print("RotateObject")
    colorobj = (cgreen,cltgreen,cgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cwhite,cltgreen,cwhite,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                ccyan,cltgreen,ccyan,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cpurple,cltgreen,cpurple,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cyellow,cltgreen,cyellow,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cblue,cltgreen,cblue,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cred,cltgreen,cred,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen
                )
    #RotateObject(colorobj, .1, 100, "forward")
    RotateObject(colorobj, .1, 100, True)
    time.sleep(wait_time)
    
    # RotateObject(coloreObj, delay, cycles, dirrection)
    print("RotateObject")
    colorobj = (cgreen,cblk,cgreen,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cwhite,cblk,cwhite,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                ccyan,cblk,ccyan,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cpurple,cblk,cpurple,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cyellow,cblk,cyellow,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cblue,cblk,cblue,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cred,cblk,cred,cblk,cblk,cblk,cblk,cblk,cblk,cblk
                )
    #RotateObject(colorobj, .1, 100, "forward")
    RotateObject(colorobj, .1, 100, True)
    time.sleep(wait_time)
    
    # RotateObject(coloreObj, delay, cycles, dirrection)
    print("RotateObject")
    colorobj = (cgreen,cblk,cblk,cblk,cblk,cblk,
                cwhite,cblk,cblk,cblk,cblk,cblk,
                ccyan,cblk,cblk,cblk,cblk,cblk,
                cpurple,cblk,cblk,cblk,cblk,cblk,
                cyellow,cblk,cblk,cblk,cblk,cblk,
                cblue,cblk,cblk,cblk,cblk,cblk,
                cred,cblk,cblk,cblk,cblk,cblk
                )
    #RotateObject(colorobj, .1, 100, "forward")
    RotateObject(colorobj, .1, 100, True)
    time.sleep(wait_time)
    
    print("PatternRunningLightsFadeTrans")
    #PatternRunningLightsWaveTrans(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles)
    colorobj = (cwhite, ccyan, cpurple, cyellow, cblue, cred)
    tempStrip = PatternRunningLightsFadeTrans(colorobj, 16, cgreen, 4, True, 5)
    RotateObject(tempStrip, .05, 100, True)
    time.sleep(wait_time)

    print("PatternRunningLightsWaveTrans")
    #PatternRunningLightsWaveTrans(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles)
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    tempStrip = PatternRunningLightsWaveTrans(colorobj, 24, cgreen, 8, True, 1)
    RotateObject(tempStrip, .05, 100, True)
    time.sleep(wait_time)
        
    print("PatternRunningLightsWaveColorObj")
    # PatternRunningLightsWaveColorObj(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles)
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    tempStrip = PatternRunningLightsWaveColorObj(colorobj, 24, (0,0,0), 8, True, 5)
    RotateObject(tempStrip, .05, 100, True)
    time.sleep(wait_time)

    print("PatternRunningLightsFadeColorObj")
    # PatternRunningLightsFadeColorObj(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles)
    colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
    tempStrip = PatternRunningLightsFadeColorObj(colorobj, 15, (0,0,0), 5, True, 0)
    RotateObject(tempStrip, .05, 100, True)
    time.sleep(wait_time)

    print("PatternRunningLightsFade")
    # PatternRunningLightsFade(mainColor, mainLength, spaceColor, spaceLength, patternCycles)
    tempStrip = PatternRunningLightsFade((255,255,0), 15, (0,0,0), 5, True, 0)
    RotateObject(tempStrip, .05, 100, True)
    time.sleep(wait_time)

    # RotateObject(coloreObj, delay, cycles, dirrection)
    print("RotateObject")
    colorobj = (cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,
                cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,
                ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,
                cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,
                cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,
                cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,
                cred,cred,cred,cred,cred,cred,cred,cred,cred,cred
                )
    #RotateObject(colorobj, .1, 100, "forward")
    RotateObject(colorobj, .05, 100, True)
    time.sleep(wait_time)
    
    # theaterChaseGroupCustom(colorobj, darkspace, SpeedDelay, cycles):
    #print("theaterChaseGroupCustom")
    #colorobj = (cwhite,cred,cgreen,cblue,cyellow,cpurple)
    #theaterChaseGroupCustom(colorobj, 5, 2, .1, 100)
    #time.sleep(wait_time)

    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDotCollectionMiddle")
    theaterChaseDotCollectionMiddle(40, cwhite, .1, 100)
    time.sleep(wait_time)
    
    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDotCollection")
    theaterChaseDotCollection(20, cwhite, .1, 100)
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