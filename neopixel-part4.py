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
num_pixels = 120

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
wait_time = 1
thisbright = 255
PartyColors_p = (
    ((0x55),(0x50),(0xAB)), ((0x84),(0x00),(0x7C)), ((0xB5),(0x00),(0x4B)), ((0xE5),(0x00),(0x1B)),
    ((0xE8),(0x17),(0x00)), ((0xB8),(0x47),(0x00)), ((0xAB),(0x77),(0x00)), ((0xAB),(0xAB),(0x00)),
    ((0xAB),(0x55),(0x00)), ((0xDD),(0x22),(0x00)), ((0xF2),(0x00),(0x0E)), ((0xC2),(0x00),(0x3E)),
    ((0x8F),(0x00),(0x71)), ((0x5F),(0x00),(0xA1)), ((0x2F),(0x00),(0xD0)), ((0x00),(0x07),(0xF9))  )



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


def fadeUsingColor(colormask, delay, cycles):
    for loop in range(cycles):
        
        #get current color from colormask
        fr = colormask[0]
        fg = colormask[1]
        fb = colormask[2]
        for i in range(num_pixels):
            #get current color
            c = pixels[i]
            red = c[0]
            green = c[1]
            blue = c[2]

            # scale color
            scaled_r = (fr/256.0)*red
            scaled_g = (fg/256.0)*green
            scaled_b = (fb/256.0)*blue
            
            pixels[i] = (int(scaled_r), int(scaled_g), int(scaled_b))
            
            # show pixel
            pixels.show()
            time.sleep(delay)


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
        

def drain_gradient_RGB( startpos, startcolor, endpos, endcolor, delay ):
    endpos = endpos - 1
    
    # if the points are in the wrong order, straighten them
    if endpos > startpos :
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
    
    divisor = - pixeldistance
    # check if  divisor is 0
    if divisor == 0: #safety check to prevent divide by zero
        divisor = 1


    rdelta87 = rdistance87 / divisor
    gdelta87 = gdistance87 / divisor
    bdelta87 = bdistance87 / divisor
    
    r88 = startcolor[0]
    g88 = startcolor[1]
    b88 = startcolor[2]

    # for each pixel (from startpos to endpos)
    for i in range(startpos, endpos, -1):
        # assing color to pixel
        pixels[i] = ( int(r88), int(g88), int(b88) )
        # show new color 
        pixels.show()
        time.sleep(delay)

        # change color
        r88 = r88 + rdelta87
        g88 = g88 + gdelta87
        b88 = b88 + bdelta87
        
        

def addGlitter( chanceOfGlitter):
    if random.randint(0, 100) < chanceOfGlitter :
        index = random.randint(0, num_pixels-1)
        pixels[ index ] = (255,255,255)

def rainbowWithGlitter(initialhue, deltahue, delay, cycles):
    hue = initialhue
    for loop in range(cycles):
        # built-in FastLED rainbow, plus some random sparkly glitter
        #rainbow() #fill_rainbow( leds, NUM_LEDS, gHue, 7);
        fill_rainbow(hue, deltahue, 0)
        addGlitter(80)

        hue = hue + 1
        if hue == 256:
            hue = 0
        time.sleep(delay)

def confetti(delay, cycles):
    for loop in range(cycles):
        # random colored speckles that blink in and fade smoothly
        fadeall(10)
        pos = random.randint(0, num_pixels-1)
        hue = random.randint(0, 64)
        #pixels[pos] += CHSV( gHue + random8(64), 200, 255);
        pixels[pos] = wheel(hue)
        pixels.show()
        time.sleep(delay)

def sinelon(hue, fadescale, delay, cycles):
    for loop in range(cycles):
        # a colored dot sweeping back and forth, with fading trails
        fadeall(fadescale) 
        beatsin = (math.sin( loop/num_pixels))
        pos = (num_pixels) * (beatsin+1)/2
        
        #pixels[pos] += CHSV( gHue, 255, 192)
        pixels[int(pos)] = wheel(hue)
        pixels.show()
        time.sleep(delay)

def bpm(pallet, delay, cycles): 
    # colored stripes pulsing at a defined Beats-Per-Minute (BPM)
    """
    uint8_t BeatsPerMinute = 62;
    CRGBPalette16 palette = PartyColors_p;
    uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
    for( int i = 0; i < NUM_LEDS; i++) { //9948
        leds[i] = ColorFromPalette(palette, gHue+(i*2), beat-gHue+(i*10));
    """
    gHue = 0
    for loop in range(cycles):

        #beat = beatsin8( BeatsPerMinute, 64, 255)
        beatsin = (math.sin( loop/num_pixels))
        delta = (255-64) * (beatsin+1)/2
        beat = 64 + delta

        for i in  range(0, num_pixels, 1):  #for( int i = 0; i < NUM_LEDS; i++) #9948
            palColor = pallet[i % len(pallet) ]
            
            color = brightnessRGB(palColor[0], palColor[1], palColor[2], beat)
            pixels[i] = color
        pixels.show()
        time.sleep(delay)

def juggle(fadescale, delay, cycles):
    # eight colored dots, weaving in and out of sync with each other
    for loop in range(cycles):
        fadeall(fadescale)  #fadeToBlackBy( leds, NUM_LEDS, 20);
        dothue = 0
        for i in  range(0, 8, 1):  #for( int i = 0; i < 8; i++) {
            #leds[beatsin16( i+7, 0, NUM_LEDS-1 )] |= CHSV(dothue, 200, 255);
            beatsin = (math.sin( loop/num_pixels))
            index = (i+7) * (beatsin+1)/2
            pixels[int(index)] = wheel(dothue)
            dothue += 32
        pixels.show()
        time.sleep(delay)


#https://git.defproc.co.uk/red-violet-made/kites/blob/d9574021fb77de0ac7f83d4a195648ec5085083a/arduino/test/lib/FastLED/lib8tion.h
def beatsin16(  beats_per_minute, lowest = 0, highest = 65535, timebase = 0, phase_offset = 0):
    beat = beat16( beats_per_minute, timebase)
    #print("beat", beat)
    beatsin = (math.sin( beat + phase_offset) + 32768)
    #print( "beatsin", beatsin, "highest", highest, "lowest", lowest)
    rangewidth = highest - lowest
    scaledbeat = scale16( beatsin, rangewidth)
    #print(":scaledbeat", scaledbeat)
    result = lowest + scaledbeat
    return result

    """
    uint16_t beat = beat16( beats_per_minute, timebase);
    uint16_t beatsin = (sin16( beat + phase_offset) + 32768);
    uint16_t rangewidth = highest - lowest;
    uint16_t scaledbeat = scale16( beatsin, rangewidth);
    uint16_t result = lowest + scaledbeat;
    """


# beat16 generates a 16-bit 'sawtooth' wave at a given BPM
# http://fastled.io/docs/3.1/lib8tion_8h_source.html
def beat16( beats_per_minute, timebase = 0):
    # Convert simple 8-bit BPM's to full Q8.8 accum88's if needed
    #print("beats_per_minute", beats_per_minute)
    if beats_per_minute < 256:
       beats_per_minute <<= 8
    return beat88(beats_per_minute, timebase)
    """
    if( beats_per_minute < 256) beats_per_minute <<= 8;
    return beat88(beats_per_minute, timebase);
    """


# beat16 generates a 16-bit 'sawtooth' wave at a given BPM,
#        with BPM specified in Q8.8 fixed-point format; e.g.
#        for this function, 120 BPM MUST BE specified as
#        120*256 = 30720.
#        If you just want to specify "120", use beat16 or beat8.
# https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
# https://git.defproc.co.uk/red-violet-made/kites/blob/d9574021fb77de0ac7f83d4a195648ec5085083a/arduino/test/lib/FastLED/lib8tion.h
def beat88( beats_per_minute_88, timebase = 0):
    mills = int(round(time.time() * 1000))
    #print("mills", mills)
    return ((mills - timebase) * beats_per_minute_88 * 280) #>> 16
    """
    return (((GET_MILLIS()) - timebase) * beats_per_minute_88 * 280) >> 16;
    """


# http://fastled.io/docs/3.1/scale8_8h_source.html
def scale16(i , scale):
    num = 65536
    #num = 1
    return ((i * scale) / num)

    """
    #if SCALE16_C == 1
        uint16_t result;
    #if FASTLED_SCALE8_FIXED == 1
        result = ((uint32_t)(i) * (1+(uint32_t)(scale))) / 65536;
    #else
        result = ((uint32_t)(i) * (uint32_t)(scale)) / 65536;
    #endif
    """



while True:
    random.seed(num_pixels)

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
    print("fill -blue")
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(wait_time)

    #fix me: not working correctly
    # makes the strand of pixels show juggle
    # juggle(fadescale, delay, cycles)
    print("juggle")
    juggle(230, 0, 100)
    
    # makes the strand of pixels show bpm
    # bpm(pallet, delay, cycles)
    print("bpm")
    bpm(PartyColors_p, 0, 50)

    # makes the strand of pixels show sinelon
    # sinelon(hue, fadescale, delay, cycles)
    print("sinelon")
    sinelon(0, 230, 0, 500)
    time.sleep(wait_time)

    # makes the strand of pixels show confetti
    # confetti(delay, cycles) 
    print("confetti")
    confetti(0.1, 1000)
    time.sleep(wait_time)

    # gradientdrain and fill example
    # fill_gradient_RGB( startpos, startcolor, endpos, endcolor, delay )
    print("fill_gradient_RGB - white-blue white-green")
    fill_gradient_RGB( 0, (255,255,255), num_pixels-1, (0,0,255), .01 ) #white to blue
    drain_gradient_RGB( num_pixels-1, (0,255,0), 0, (255,255,255), .01 ) # white to green
    time.sleep(wait_time)

    # blue and white cyclone
    # fill_gradient_RGB( startpos, startcolor, endpos, endcolor, delay )
    print("fill_gradient_RGB blue white cyclone cloud")
    cyclonewait = .05
    fill_gradient_RGB( 0, (255,255,255), num_pixels-1, (0,0,255), cyclonewait ) #white to blue
    fill_gradient_RGB( 0, (0,0,255), num_pixels-1, (255,255,255), cyclonewait ) #white to blue
    fill_gradient_RGB( 0, (255,255,255), num_pixels-1, (0,0,255), cyclonewait ) #white to blue
    fill_gradient_RGB( 0, (0,0,255), num_pixels-1, (255,255,255), cyclonewait ) #white to blue
    fill_gradient_RGB( 0, (255,255,255), num_pixels-1, (0,0,255), cyclonewait ) #white to blue
    fill_gradient_RGB( 0, (0,0,255), num_pixels-1, (255,255,255), cyclonewait ) #white to blue
    fill_gradient_RGB( 0, (255,255,255), num_pixels-1, (0,0,255), cyclonewait ) #white to blue
    fill_gradient_RGB( 0, (0,0,255), num_pixels-1, (255,255,255), cyclonewait ) #white to blue
    time.sleep(wait_time)

    # makes the strand of pixels show fadeUsingColor
    # rinbowWithGlitter(initialhue, deltahue, delay, cycles)
    print("rainbowWithGlitter")
    rainbowWithGlitter(0, 7, 0, 100)

    # makes the strand of pixels show fadeUsingColor
    # fadeUsingColor(colormask, delay, cycles)
    print("fadeUsingColor")
    fadeUsingColor((0,0,100), 0, 5)
    time.sleep(wait_time)


    # makes the strand of pixels show fill_gradient_RGB
    # fill_gradient_RGB( startpos, startcolor, endpos, endcolor, delay )
    print("fill_gradient_RGB  white-black red-green")
    fill_gradient_RGB( 0, (255,255,255), num_pixels-1, (0,0,0), .1 ) #white to black
    fill_gradient_RGB( 0, (255,0,0), num_pixels-1, (0,255,0), .1 ) #red to green
    time.sleep(wait_time)

    # makes the strand of pixels show fill_rainbow
    # fill_rainbow(initialhue, deltahue, delay)
    print("fill_rainbow")
    fill_rainbow(0, 10, .1)
    time.sleep(wait_time)

    # makes the strand of pixels show Cylon
    # Cylon(delay, cycles)
    print("Cylon")
    Cylon(.05, 100)
    time.sleep(wait_time)

    # makes the strand of pixels show blink
    # blink(index, delay, cycles)
    print("blink - pixel 0")
    time.sleep(wait_time)
    blink(0, .5, 8)



