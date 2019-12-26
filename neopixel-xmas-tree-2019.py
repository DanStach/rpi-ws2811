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
num_pixels = 400

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = .5
wait_animate = .1
cycleFactor = 1

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

colorobj = (cgreen, cwhite, ccyan, cpurple, cyellow, cblue, cred)
xmasColorGroupAll = (cgreen, cwhite, ccyan, cyellow, cblue, cred)
xmasColorGroupDimAll = (cltgreen, cltwhite, cltcyan, cltyellow, cltblue, cltred)
xmasColorGroupRedGreen = (cred, cgreen) 
xmasColorGroupRedWhite = (cred, cwhite) 
halloweenColorGroupPurpleOrange = ((128,0,128), (250,97,35) ) 


levels = (43, 73, 103, 135, 160, 188, 213, 236, 255, 272, 286, 295, 300)
#levels = (43, 73, 103, 135, 160, 188, 213, 236, 255, 272, 286, 245, 250)

#levels = (58, 108, 149, 187, 224, 264, 292, 300)
#levels = (110, 200, 270, 300)

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
    for j in range(cycles):
        for i in range(num_pixels):
            # " // "  this divides and returns the integer value of the quotient. 
            # It dumps the digits after the decimal
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(delay)

def candycane_custom(c1, c2, thisbright, delay, cycles):
    N6  = int(num_pixels/6)
    N12 = int(num_pixels/12)

    for loop in range(cycles):
        cSwap = c1
        c1 = c2
        c2 = cSwap
        for i in range(N6):
            j0 = int(( i + num_pixels - N12) % num_pixels)
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
    pixels.fill(cblk) # inital fill black
    pixels.show()
    startPos = 0
    for c in range(cycles):

        for i in range(int(sectionCount)): 
            for q in range(0, int(num_pixels), int(sectionCount)):
                if i+q < num_pixels:
                    pixels[i+q] = dotColor
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    pixels[i+q-1] = cblk

            pixels.show()
            time.sleep(delay)


def theaterChaseDotCollection(sectionCount, dotColor, delay, cycles):
    pixels.fill(cblk) # inital fill black
    pixels.show()
    sectionEnd = sectionCount
    for c in range(cycles):

        for i in range(int(sectionCount)):
            if sectionEnd == 0:
                pixels.fill(cblk) # inital fill black
                sectionEnd = sectionCount
                
            for q in range(0, int(num_pixels), int(sectionCount)):
                if i+q < num_pixels:
                    pixels[i+q] = dotColor 
                if i+q-1 < num_pixels and i+q-1 >= 0:
                    if i > 1:
                        pixels[i+q-1] = cblk
        
            pixels.show()
            if i >=  sectionEnd-1:
                sectionEnd -=1
                break
            else:
                time.sleep(delay)
                
                
def theaterChaseDotCollectionMiddle(sectionCount, dotColor, delay, cycles):
    pixels.fill(cblk) # inital fill black
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
                        pixels[i+q-1] = cblk
                        
                if sectionCount-i+q < num_pixels:    
                    pixels[sectionCount-i+q] = dotColor
                if sectionCount-i+q+1 < num_pixels and sectionCount-i+q+1 >= 0:
                    if i < num_pixels:
                        pixels[sectionCount-i+q+1] = cblk
        
            pixels.show()

            if sectionEnd < 0: # fill last dots, and reset
                pixels.fill(dotColor) # fill dots
                pixels.show()
                time.sleep(delay)
                
                pixels.fill(cblk) # inital fill black
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
                pixels.fill(cblk)
                
                for i in range(0, num_pixels, n):
                    for index in range(0, colorObjCount, 1):
                        if i+q+index < num_pixels:
                            pixels[i+q+index] = cblk        


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

def Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne):
    pixels.fill(cblk)
  
    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (red, green, blue)
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill(cblk)

    time.sleep(SpeedDelay)


def TwinkleRandom(Count, SpeedDelay, OnlyOne):
    pixels.fill(cblk)

    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill(cblk)

    time.sleep(SpeedDelay)


def Sparkle(red, green, blue, Count, SpeedDelay):

    for i in range(Count):    
        Pixel = random.randint(0,num_pixels-1)
        pixels[Pixel] = (red,green,blue)
        pixels.show()
        time.sleep(SpeedDelay)
        pixels[Pixel] = cblk

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
                    pixels[i+q] = cblk



def theaterChaseRainbow(SpeedDelay):
    # cycle all 256 colors in the wheel
    for j in range(256):

        for q in range(3):
            for i in range(0, num_pixels, 3):
                # check that pixel index is not greater than number of pixels
                if i+q < num_pixels:
                    # turn every third pixel on
                    # c = Wheel( (i+j) % 255);
                    # setPixel(i+q, *c, *(c+1), *(c+2));  

                    pixels[i+q] = wheel((i+j) % 255)
                    #print("i", i , "j", j "num_pixels", num_pixels, "pixel_index", (i * 256 // num_pixels) + j)
                    #pixel_index = (i * 256 // num_pixels) + j
                    #pixels[i+q] = wheel(pixel_index & 255)

            pixels.show()
            time.sleep(SpeedDelay)
            
            for i in range(0, num_pixels, 3):
                # check that pixel index is not greater than number of pixels
                if i+q < num_pixels:
                    # turn every third pixel off
                    pixels[i+q] = cblk



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
            #print()
            #print()
            #print("rand interal" + str(((Cooling * 10) / num_pixels) + 2))
            cooldown = random.randint(0, int(((Cooling * 10) / num_pixels) + 2))
            #print("cooldown " + str(cooldown))
            #print("heat " + str(heat[i]))
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
        #print(heat)
        for j in range(num_pixels):
            #print(heat[j] )
            setPixelHeatColor(j, int(heat[j]) )

        pixels.show()
        time.sleep(SpeedDelay)

def setPixelHeatColor (Pixel, temperature):
    # Scale 'heat' down from 0-255 to 0-191
    t192 = round((temperature/255.0)*191)

    # calculate ramp up from
    heatramp = t192 & 63 # 0..63  0x3f=63
    heatramp <<= 2 # scale up to 0..252
    #print("t192=" + str(t192) + "  heatramp=" + str(heatramp))
    # figure out which third of the spectrum we're in:
    if t192 > 0x80: # hottest 128 = 0x80
        pixels[Pixel] = (255, 255, int(heatramp))
    elif t192 > 0x40: # middle 64 = 0x40
        pixels[Pixel] = (255, int(heatramp), 0)
    else: # coolest
        pixels[Pixel] = (int(heatramp), 0, 0)


def meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay): 
    for loop in range(LoopCount):
        pixels.fill(cblk)
        
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
        pixels.fill(cblk)
        


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
        pixels.fill(cblk)


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

def random_burst(delayStart, delayEnd , LoopCount):
    thisbright = 255
    for loop in range(LoopCount):
        randomIndex= random.randint(0, num_pixels-1)
        randomhue = random.randint(0, 255)
        randombright = random.randint(10, thisbright)
        
        # CHSV(rndhue, thissat, rndbright)
        #print(str(randomIndex) + " " + str(rndhue) + " " + str(rndbright))
        pixels[randomIndex] = wheelBrightLevel(randomhue, randombright)
        
        pixels.show()
        delay = random.randint(delayStart*1000, delayEnd*1000)/1000
        time.sleep(delay)

  
def rgbPropellerCustom(hue1, delay, LoopCount):
    index= 0

    hue2 = (hue1 + 80) % 255
    hue3 = (hue1 + 160) % 255
    N3  = int(num_pixels/3)
    N6  = int(num_pixels/6)
    N12 = int(num_pixels/12)

    for loop in range(LoopCount):
        index = index + 1
        cSwap = hue1
        hue1 = hue2
        hue2 = hue3
        hue3 = cSwap

        for i in range(N3):
            j0 = (index + i + num_pixels - N12) % num_pixels
            j1 = (j0+N3) % num_pixels
            j2 = (j1+N3) % num_pixels
            pixels[j0] = wheel(hue1)
            pixels[j1] = wheel(hue2)
            pixels[j2] = wheel(hue3)
            
        pixels.show()
        time.sleep(delay)


def rainbow(delay, step, cycles):
    for j in range(cycles):
        for i in range(num_pixels):
            # " // "  this divides and returns the integer value of the quotient. 
            # It dumps the digits after the decimal
            pixel_index = (step *i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(delay)


def rainbow_loop(delay, step, cycles):
    index = 0
    thishue = 0

    for loop in range(cycles):
        index = index + 1
        thishue = thishue + step
        if index >= num_pixels:
            index = 0
        if thishue > 255:
            thishue = 0
        pixels[index] = wheel(thishue)
        pixels.show()
        time.sleep(delay)

def rainbow_fade(delay, cycles):
    thishue = 0
    for loop in range(cycles):
        thishue = thishue + 1
        if thishue > 255:
             thishue = 0

        # an other option would be to
        pixels.fill(wheel(thishue))
        pixels.show()
        time.sleep(delay)
#        for i in range(num_pixels):
#            print(wheel(thishue))
#            pixels[i] = wheel(thishue)
#            pixels.show()
#            time.sleep(delay)


def matrix(random_percent, delay, cycles):
    for loop in range(cycles):
        rand = random.randint(0, 100)

        # set first pixel
        if rand <= random_percent:
            pixels[0] = wheelBrightLevel(random.randint(0, 255), 255)
        else:
            pixels[0] = cblk
        
        # show pixels 
        pixels.show()
        time.sleep(delay)

        # rotate pixel positon
        for i in range(num_pixels - 1, 0, -1):
            pixels[i] = pixels[i-1]

 
def random_march(delay, cycles):
    for loop in range(cycles):

        for idex in range(num_pixels-1):
            ### previous logic that was not used...
            #if idex > 0: #if not last pixel
            #    r = idex - 1
            #else: # if last pixel
            #    r = num_pixels - 1

            # shift pixel value to previous pixel (pixel1 = value of pixel2,... and so on)
            pixels[idex] = pixels[idex+1]

        # change color of the last pixel
        pixels[num_pixels-1] = wheelBrightLevel(random.randint(0, 255), 255)

        # show pixel values
        pixels.show()
        time.sleep(delay)


def twinkle2(delay, cycles ):
    for loop in range(cycles):
        huebase = 0
        
        #slowly rotate huebase
        if (random.randint(0, 4) == 0): #randomly, if 0  (0-3)
            huebase = huebase -1
        
        for whichPixel in range(num_pixels):
            hue = random.randint(0, 32) + huebase
            #saturation = 255;    #richest color
            brightness = random.randint(0, 255)
        
            pixels[whichPixel] = wheelBrightLevel(hue, brightness)
            # show pixel values 
        pixels.show()
        time.sleep(delay)


def random_levels( NUM_LEVELS, delay, cycles ):
    for loop in range(cycles):

        level = random.randint(0, NUM_LEVELS)
        if (NUM_LEVELS == level):
            level = 0
        light_level_random(level, 1)
        pixels.show()
        time.sleep(delay)


def light_level_random( level,  clearall ):
    levels = levelobj
    if (clearall):
        pixels.fill(cblk) # clear all
        pixels.show()
    
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levels[level-1]
    
    for i in range(startPxl, levels[level]):
        pixels[i] = wheelBrightLevel(random.randint(0, 255), random.randint(50, 255))


def drain(level, delay):
    interrupt = False
    for pancakeLevel in range(level):

        # only needed if you ouput to a small display 
        # updateControlVars() 
        
        if (interrupt):
            return
        
        for level in range(pancakeLevel, -1, -1):
            # only needed if you ouput to a small display 
            # updateControlVars()  
            
            if (interrupt) :
                return

            clear_level(level)
            if (level >= 1) :
                light_level_random(level-1, 0)

            # show pixel values 
            pixels.show()
            time.sleep(delay)


def pancake(NUM_LEVELS, delay):
    interrupt = False
    for pancakeLevel in range(NUM_LEVELS):
        # only needed if you ouput to a small display 
        # updateControlVars()  

        if (interrupt):
            return
        
        for level in range(NUM_LEVELS-1, pancakeLevel-1, -1):
            # only needed if you ouput to a small display 
            # updateControlVars()   

            if (interrupt):
                return

            if (level < NUM_LEVELS-1):
                clear_level(level+1)
                
            light_level_random(level, 0)

            # show pixel values 
            pixels.show()
            time.sleep(delay)


def clear_level( level):
    levels = levelobj
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levels[level-1]
    for i in range(startPxl, levels[level]):
        pixels[i] = cblk  #CRGB::Black;


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


def candycane_custom(c1, c2, thisbright, delay, cycles):
    N6  = int(num_pixels/6)
    N12 = int(num_pixels/12)

    for loop in range(cycles):
        cSwap = c1
        c1 = c2
        c2 = cSwap
        for i in range(N6):
            j0 = int(( i + num_pixels - N12) % num_pixels)
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
        pixels.fill(cblk) # clear all
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
        pixels.fill(cblk) # clear all
        pixels.show()
    
    startPxl = 0
    if (level == 0):
        startPxl = 0
    else:
        startPxl = levels[level-1]
    
    for i in range(startPxl, levels[level]):
        #print("i=",i,"color=",color,"startPxl=",startPxl,"level=",level)
        pixels[i] = color


def blink(index, delay, cycles):
    for loop in range(cycles):
        # Turn the LED on, then pause
        pixels[index] = (255,0,0) #CRGB::Red
        pixels.show()
        time.sleep(delay)
        # Now turn the LED off, then pause
        pixels[index] = cblk #CRGB::Black
        pixels.show()
        time.sleep(delay)


while True:
    random.seed()

    # make all pixels black
    # fill(red, green, blue)
    print("fill black")
    pixels.fill(cblk)
    pixels.show()
    time.sleep(2)
    
    # make all pixels Red
    # fill(red, green, blue)
    print("fill red")
    pixels.fill(cred) # red
    pixels.show()
    time.sleep(wait_time+cycleFactor)

    # make all pixels Green
    # fill(red, green, blue)
    print("fill green")
    pixels.fill(cgreen)
    pixels.show()
    time.sleep(wait_time+cycleFactor)

    # make all pixels Blue
    # fill(red, green, blue)
    print("fill blue")
    pixels.fill(cblue)
    pixels.show()
    time.sleep(wait_time+cycleFactor)


    ### this code tests that the levels are correct ##### 

    print("LevelsColorsCustom  - level  test ")
    colorobj = (cwhite, cred, cgreen, cblue, cyellow, 
                cwhite, cred, cgreen, cblue, cyellow,
                cwhite, cred, cgreen, cblue, cyellow,
                cwhite, cred, cgreen, cblue, cyellow ) 
    #LevelsColorsCustom(colorobj, levels, wait_animate)
    #time.sleep(wait_time+10)

    print("colorAllColorGroup - level test c10")
    colorobj = ( cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,
                 cred,cred,cred,cred,cred,cred,cred,cred,cred,cred,
                 cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,
                 cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,
                 cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow)
    #colorAllColorGroup(colorobj)
    #time.sleep(wait_time+10)

    # shows 2 color every other pixel (red, green)
    # colorAllColorGroup(colorObject)
    print("colorAllColorGroup - red green")
    colorAllColorGroup(xmasColorGroupRedGreen)
    pixels.show()
    time.sleep(wait_time+cycleFactor)

    # shows 2 color every other pixel (purple orange)
    # colorAllColorGroup(colorObject)
    print("colorAllColorGroup red white")
    colorAllColorGroup(xmasColorGroupRedWhite)
    pixels.show()
    time.sleep(wait_time+cycleFactor)

    # shows 2 color every other pixel (purple, orange)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2))
    print("colorAllColorGroup purple orange")
    colorAllColorGroup(halloweenColorGroupPurpleOrange )
    pixels.show()
    time.sleep(wait_time+cycleFactor)

    # makes the strand of pixels show candycane_custom
    # candycane_custom(c1, c2, brightness, delay, cycles)
    pixels.fill(cred) 
    pixels.show()
    print("candycane_custom white red")
    candycane_custom(cwhite, cred, 255, wait_animate/2, 5)
    time.sleep(wait_time+cycleFactor)

    # makes the strand of pixels show candycane_custom
    # candycane_custom(c1, c2, brightness, delay, cycles)
    pixels.fill(cgreen) 
    pixels.show()
    print("candycane_custom white green")
    candycane_custom(cwhite, cgreen, 255, wait_animate/2, 5*cycleFactor)
    time.sleep(wait_time)

    # makes the strand of pixels show candycane_custom
    # candycane_custom(c1, c2, brightness, delay, cycles)
    pixels.fill(cred) 
    pixels.show()
    print("candycane_custom red green")
    candycane_custom(cred, cgreen, 255, wait_animate/2, 5*cycleFactor)
    time.sleep(wait_time)


    # makes the strand of pixels show twinkle
    # twinkle(delay, cycles)
    pixels.fill(cblk) 
    pixels.show()
    print("twinkle2")
    twinkle2(wait_animate, 100*cycleFactor) 
    time.sleep(wait_time)

# makes the strand of pixels show random_march
    # random_march( delay, cycles)
    pixels.fill(cblk) 
    pixels.show()
    print("random_march")
    random_march(wait_animate/2, 200*cycleFactor) 
    time.sleep(wait_time)

    # makes the strand of pixels show matrix
    # matrix(random_percent, delay, cycles)
    pixels.fill(cblk) 
    pixels.show()
    print("matrix")
    matrix(10, wait_animate, 200*cycleFactor) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow_fade
    # rainbow_fade(delay, cycles):
    print("rainbow_fade")
    rainbow_fade(wait_animate, 20*cycleFactor) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow_loop
    # rainbow_loop(delay, step, cycles):
    pixels.fill(cblk)
    pixels.show()
    print("rainbow_loop")
    rainbow_loop(wait_animate/4, 10, 500*cycleFactor) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow
    # rainbow(delay, step, cycles):
    pixels.show()
    time.sleep(wait_time)
    print("rainbow")
    rainbow(wait_animate/4, 10, 20*cycleFactor) 
    time.sleep(wait_time)

    # makes the strand of pixels show random_burst
    # rgbPropellerCustom(hue, SpeedDelay, LoopCount)
    pixels.fill(cblk)
    pixels.show()
    time.sleep(wait_time)
    print("rgbPropellerCustom")
    rgbPropellerCustom(0, wait_animate, 20*cycleFactor)
    time.sleep(wait_time)

    # makes the strand of pixels show random_burst
    # random_burst(delayStart, delayEnd , LoopCount)
    pixels.fill(cblk)
    pixels.show()
    print("random_burst")
    random_burst(0, wait_animate, 1000*cycleFactor)
    time.sleep(wait_time)


    # makes the strand of pixels show Fire
    # Fire(Cooling, Sparking, SpeedDelay, LoopCount)
    print("Fire")
    Fire(15, 200, wait_animate/4, 800*cycleFactor)
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChaseRainbow
    # theaterChaseRainbow(SpeedDelay)
    print("theaterChaseRainbow")
    theaterChaseRainbow(wait_animate)
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChase
    # theaterChase(red, green, blue, cycles, SpeedDelay)
    print("theaterChase")
    theaterChase(255,0,0, 200*cycleFactor, wait_animate)
    time.sleep(wait_time)

    # makes the strand of pixels show colorWipe (green)
    # colorWipe(red, green, blue, SpeedDelay)
    print("colorWipe")
    colorWipe(0,255,0, wait_animate/2)
    time.sleep(wait_time)
    colorWipe(255,0,0, wait_animate/2)
    time.sleep(wait_time)
    colorWipe(200,200,200, wait_animate/2)
    time.sleep(wait_time)

    # makes the strand of pixels show RunningLights (red)
    # RunningLights(red, green, blue, WaveDelay)
    print("RunningLights - red")
    RunningLights(255,0,0, wait_animate/2)

    # makes the strand of pixels show RunningLights (red)
    # RunningLights(red, green, blue, WaveDelay)
    print("RunningLights - green")
    RunningLights(0,255,0, wait_animate/2)

    # makes the strand of pixels show RunningLights (red)
    # RunningLights(red, green, blue, WaveDelay)
    print("RunningLights - white")
    RunningLights(255,255,255, wait_animate/2)

    # makes the strand of pixels show SnowSparkle (random)
    # SnowSparkle(red, green, blue, Count, SparkleDelay, SpeedDelay)
    # SnowSparkle(16, 16, 16, 100, 0.020, random.randint(100,1000)/1000)
    print("SnowSparkle")
    SnowSparkle(16, 16, 16, 100*cycleFactor, 0, wait_animate/2)

    # makes the strand of pixels show Sparkle (white)
    # Sparkle(red, green, blue, Count, SpeedDelay)
    print("Sparkle")
    Sparkle(255, 255, 255, 100*cycleFactor, wait_animate/2)

    # makes the strand of pixels show TwinkleRandom
    # TwinkleRandom( Count, SpeedDelay, OnlyOne)
    print("TwinkleRandom")
    TwinkleRandom(1000*cycleFactor, wait_animate/2, False)

    # makes the strand of pixels show Twinkle
    # Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne)
    print("Twinkle")
    Twinkle(255, 0, 0, 1000*cycleFactor, wait_animate/2, False)

    # fade in/out a single color (red / green / blue / white)
    # FadeInOut(red, green, blue, delay)
    print("FadeInOut")
    FadeInOut(255, 0, 0, wait_animate/4)
    FadeInOut(0, 255, 0, wait_animate/4)
    FadeInOut(255, 255, 255, wait_animate/4)

    # rainbow cycle
    # rainbow cycle with 1ms delay per step, 5 cycles
    # rainbow_cycle(delay, cycles)
    print("rainbow_cycle")
    rainbow_cycle(wait_animate/2, 20*cycleFactor) 
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
    FireCustom(0, 4, 90, 0, int(num_pixels/3), wait_animate/2, 900*cycleFactor) # red fire
    time.sleep(wait_time)

    # makes the strand of pixels show blink
    # blink(index, delay, cycles)
    print("blink - pixel 0")
    pixels.fill(cblk)
    pixels.show()
    blink(num_pixels-1, wait_animate, 100*cycleFactor)
    time.sleep(wait_time)


    # makes the strand of pixels show randomLevelsCustom2Colors
    # randomLevelsCustom2Colors( c1, c2, levelobj, clearall, delay, cycles )
    #levels = (110, 200, 270, 340, 390, 400)
    print("randomLevelsCustom2Colors")
    randomLevelsCustom2Colors(cltwhite,cltgreen, levels, True, wait_animate, 10*cycleFactor)
    time.sleep(wait_time)
    
    # makes the strand of pixels show randomLevelsCustomColors
    # randomLevelsCustomColors( colorobj levelobj, clearall, delay, cycles ):
    #levels = (110, 200, 270, 340, 390, 400)
    print("randomLevelsCustomColors")
    colorobj = ( cltwhite, cltgreen, cltred )
    randomLevelsCustomColors(colorobj, levels, 1, wait_animate, 10*cycleFactor)
    time.sleep(wait_time)

    # makes the strand of pixels show LevelsColorsCustom
    #LevelsColorsCustom( colorobj, levelobj, delay )
    #levels = (110, 200, 270, 340, 390, 400)
    print("LevelsColorsCustom")
    colorobj = ( cltwhite, cltred, cltgreen, cltblue, cltcyan)
    LevelsColorsCustom(colorobj, levels, wait_animate)
    time.sleep(wait_time*5)
    
    # shows pattern of colors on the given pixels 
    # colorAllColorGroup((red1, green1, blue1), (red2, green2, blue2), ...) 
    print("colorAllColorGroup multi")
    colorAllColorGroup(xmasColorGroupAll) 
    time.sleep(wait_time+cycleFactor)


    # shows 2 color every other pixel (red, green)
    # SnowSparkleExisting(Count, SparkleDelay, SpeedDelay)
    print("SnowSparkleExisting purple orange")
    colorAll2Color((75,0,130), (255,165,0) )
    SnowSparkleExisting(1000*cycleFactor, .1, wait_animate)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    # RunningLightsPreExisting(WaveDelay, cycles):
    print("RunningLightsPreExisting red green")
    colorAll2Color(cred, cgreen) 
    RunningLightsPreExisting(wait_animate, 1000*cycleFactor)
    time.sleep(wait_time)


    # shows 2 color every other pixel (red, green)
    # RunningLightsPreExisting(WaveDelay, cycles):
    print("RunningLightsPreExisting multi")
    colorAllColorGroup(xmasColorGroupAll) 
    RunningLightsPreExisting(wait_animate, 1000*cycleFactor)
    time.sleep(wait_time)





    #TransColors(colorObj, incrementPrecent, delay, cycles)
    print("TransColors")
    TransColors(xmasColorGroupAll, 0.01, wait_animate/10, 50*cycleFactor)
    time.sleep(wait_time)
    
    #FadeInOutColors(colorObj, spaceColor, incrementPrecent, delay, cycles)
    print("FadeInOutColors")
    FadeInOutColors(xmasColorGroupAll, cblk, 0.01, wait_animate/100, 2*cycleFactor)
    time.sleep(wait_time)
    
    # drain_section_mid(colorObj, sectionCount, spaceColor, delay, isDirrectionOutward, cycles)
    print("drain_section_mid")
    drain_section_mid(xmasColorGroupAll, 24, cblk, wait_animate*2, True, 5*cycleFactor)
    time.sleep(wait_time)

    
    # fill_section_mid(colorObj, sectionCount, spaceColor, delay, isDirrectionOutward, cycles)
    print("fill_section_mid")
    fill_section_mid(xmasColorGroupAll, 24, cblk, wait_animate*2, True, 5*cycleFactor)
    time.sleep(wait_time)
    
    # drain_section(colorObj, sectionCount, spaceColor, delay, isDirrectionForward, cycles)
    print("drain_section")
    drain_section(xmasColorGroupAll, 24, cblk, wait_animate*2, True, 5*cycleFactor)
    time.sleep(wait_time)
    
    # fill_section(colorObj, sectionCount, spaceColor, delay, isDirrectionForward, cycles)
    print("fill_section")
    fill_section(xmasColorGroupAll, 24, cblk, wait_animate*2, True, 5*cycleFactor)
    time.sleep(wait_time)
    
    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDotCollection - green")
    theaterChaseDotCollection(100, cgreen, wait_animate, 100*cycleFactor)
    time.sleep(wait_time)

    print("DotCollectionMiddleColorChange - red")
    # DotCollectionMiddleColorChange(colorObj, sectionCount, spaceColor, delay, cycles)
    colorobj = (cred, cred)
    DotCollectionMiddleColorChange(colorobj, 24, cltgreen, wait_animate, 5*cycleFactor)
    time.sleep(wait_time)


    print("DotCollection-red white")
    #DotCollection(colorObj, sectionCount, delay, cycles)
    colorobj = (cred, cred)
    DotCollection(colorobj, 48, cltwhite, wait_animate/2, 5*cycleFactor)
    time.sleep(wait_time)

    
    print("DotCollectionColorChange - xmas blk")
    #DotCollectionColorChange(colorObj, sectionCount, spaceColor, delay, cycles):
    DotCollectionColorChange(xmasColorGroupAll, 48, cblk, wait_animate*2, 1*cycleFactor)
    time.sleep(wait_time)

    print("DotCollection")
    #DotCollection(colorObj, sectionCount, delay, cycles)
    DotCollection(xmasColorGroupAll, 48, cblk, wait_animate, 1*cycleFactor)
    time.sleep(wait_time)

    # RotateObject(coloreObj, delay, cycles, dirrection)
    print("RotateObject - multicolorn c ltgrn c 7ltgrn")
    colorobj = (cgreen,cltgreen,cgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cwhite,cltgreen,cwhite,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                ccyan,cltgreen,ccyan,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cyellow,cltgreen,cyellow,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cblue,cltgreen,cblue,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,
                cred,cltgreen,cred,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen,cltgreen
                )
    RotateObject(colorobj, wait_animate, 10*cycleFactor, True)
    time.sleep(wait_time)
    
    # RotateObject(coloreObj, delay, cycles, dirrection)
    print("RotateObject - multicolorn c b c 7b")
    colorobj = (cgreen,cblk,cgreen,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cwhite,cblk,cwhite,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                ccyan,cblk,ccyan,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cyellow,cblk,cyellow,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cblue,cblk,cblue,cblk,cblk,cblk,cblk,cblk,cblk,cblk,
                cred,cblk,cred,cblk,cblk,cblk,cblk,cblk,cblk,cblk
                )
    # RotateObject(coloreObj, delay, cycles, dirrection)
    RotateObject(colorobj, wait_animate, 10*cycleFactor, True)
    time.sleep(wait_time)
    
    print("RotateObject - multicolorn c 6b")
    colorobj = (cgreen,cblk,cblk,cblk,cblk,cblk,
                cwhite,cblk,cblk,cblk,cblk,cblk,
                ccyan,cblk,cblk,cblk,cblk,cblk,
                cyellow,cblk,cblk,cblk,cblk,cblk,
                cblue,cblk,cblk,cblk,cblk,cblk,
                cred,cblk,cblk,cblk,cblk,cblk
                )
    # RotateObject(coloreObj, delay, cycles, dirrection)
    RotateObject(colorobj, .1, 100*cycleFactor, True)
    time.sleep(wait_time)
    

    print("PatternRunningLightsWaveTrans")
    # PatternRunningLightsWaveTrans(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles)
    # RotateObject(coloreObj, delay, cycles, dirrection)
    tempStrip = PatternRunningLightsWaveTrans(xmasColorGroupAll, 24, cgreen, 8, True, 1)
    RotateObject(tempStrip, wait_animate/2, 1000*cycleFactor, True)
    time.sleep(wait_time)
        
    print("PatternRunningLightsWaveColorObj")
    # PatternRunningLightsWaveColorObj(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles)
    # RotateObject(coloreObj, delay, cycles, dirrection)
    tempStrip = PatternRunningLightsWaveColorObj(xmasColorGroupAll, 24, cblk, 8, True, 5)
    RotateObject(tempStrip, wait_animate/2, 1000*cycleFactor, True)
    time.sleep(wait_time)

    print("PatternRunningLightsFadeColorObj")
    # PatternRunningLightsFadeColorObj(colorObj, mainLength, spaceColor, spaceLength, isDirrectionForward, patternCycles)
    # RotateObject(coloreObj, delay, cycles, dirrection)
    tempStrip = PatternRunningLightsFadeColorObj(xmasColorGroupAll, 15, cblk, 5, True, 0)
    RotateObject(tempStrip, wait_animate/2, 1000*cycleFactor, True)
    time.sleep(wait_time)

    print("PatternRunningLightsFade")
    # PatternRunningLightsFade(mainColor, mainLength, spaceColor, spaceLength, patternCycles)
    # RotateObject(coloreObj, delay, cycles, dirrection)
    tempStrip = PatternRunningLightsFade(cyellow, 15, cblk, 5, True, 0)
    RotateObject(tempStrip, wait_animate/2, 1000*cycleFactor, True)
    time.sleep(wait_time)

    # RotateObject(coloreObj, delay, cycles, dirrection)
    print("RotateObject - c11")
    colorobj = (cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,cgreen,
                cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,cwhite,
                ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,ccyan,
                cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,cpurple,
                cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,cyellow,
                cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,cblue,
                cred,cred,cred,cred,cred,cred,cred,cred,cred,cred
                )
    #RotateObject(colorobj, .1, 100, "forward")
    RotateObject(colorobj, wait_animate/2, 1000*cycleFactor, True)
    time.sleep(wait_time)

    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDotCollectionMiddle white")
    theaterChaseDotCollectionMiddle(40, cwhite, wait_animate, 10*cycleFactor)
    time.sleep(wait_time)
    
    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDotCollection - cltwhite")
    theaterChaseDotCollection(20, cltwhite, wait_animate, 10*cycleFactor)
    time.sleep(wait_time)
    
    # theaterChaseDotCollection(sectionCount, dotColor, delay, cycles)
    print("theaterChaseDot")
    theaterChaseDot(20, cred, wait_animate, 5*cycleFactor)
    time.sleep(wait_time)

    # fill_group(groupCount, delay, cycles)
    print("fill_group_random")
    fill_group_random(50, wait_animate, 4*cycleFactor)
    time.sleep(wait_time)
    
    # rainbow cycle
    # rainbow_cycle(delay, cycles) 
    print("rainbow_cycle")
    rainbow_cycle(wait_animate, 1*cycleFactor) 
    time.sleep(wait_time)