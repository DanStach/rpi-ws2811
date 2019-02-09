### Sample python code for NeoPixels on Raspberry Pi
### this code is ported from Arduino NeoPixels effects in C++, from tweaking4all
### Arduino Controlled Tree - http://youtu.be/MD3-YBaFQvw
### orginal code: https://pastebin.com/Qe0Jttme


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

  
def rgb_propeller(LoopCount):
    thishue = 0
    thisbright = 255
    thissat = 255
    index= 0

    for loop in range(LoopCount):
        index = index + 1
        ghue = (thishue + 80) % 255
        bhue = (thishue + 160) % 255
        N3  = int(num_pixels/3)
        N6  = int(num_pixels/6)
        N12 = int(num_pixels/12)

        for i in range(N3):
            j0 = (index + i + num_pixels - N12) % num_pixels
            j1 = (j0+N3) % num_pixels
            j2 = (j1+N3) % num_pixels
            pixels[j0] = wheel(thishue)
            pixels[j1] = wheel(ghue)
            pixels[j2] = wheel(bhue)
            pixels.show()


def rainbow(delay, step, cycles):
    for j in range(255 * cycles):
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
            pixels[0] = (0,0,0)
        
        # show pixels 
        pixels.show()
        time.sleep(delay)

        # rotate pixel positon
        for i in range(num_pixels - 1, 0, -1):
            pixels[i] = pixels[i-1]
        
        # there is an issue with first 2 pixels are same color 
        #pixels[0] = (0,0,0)
        #pixels.show()
        #time.sleep(delay)


 
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

### FixMe: this code does not work
### i think it also has a memory leak
### i have reached out to the author (via youtube comment)
#### next step would be to step though the code on an arduino 

def loop5(delay, cycles):
    for loop in range(cycles):
        #GB = pixels.getBrightness()
        boost = 0
        #  if( GB < 65): boost += 8
        #  if( GB < 33) boost += 8
        
        N = 2
        starttheta = 0
        starttheta = starttheta + ( 100 / N )
        starthue16 = 0
        starthue16 = starthue16 + (20 / N)
    
    
        hue16 = starthue16
        theta = starttheta
        for i in range(num_pixels):
            frac = (math.sin( theta) + 32768) / 256
            frac = frac + 32
            theta = theta + 3700
            hue16 = hue16 + 2000
            hue = hue16 / 256

            ramp = frac + boost
            if( ramp < 128):
                # fade toward black
                brightness = ramp * 2
                saturation = 255
            else:
                # desaturate toward white
                brightness = 255
                saturation = 255 - ((ramp - 128) * 2)
                # saturation = 255 - dim8_video( 255 - saturation);

            pixels[i] = hsv_to_rgb( hue, saturation, brightness)
        
        # show pixel values 
        pixels.show()
        time.sleep(delay)


def twinkle( cycles )
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




    # makes the strand of pixels show twinkle
    # twinkle(cycles)
    twinkle(cycles) 
    time.sleep(wait_time)

    # makes the strand of pixels show loop5
    # loop5( delay, cycles)
    loop5(0.25, 500) 
    time.sleep(wait_time)

    ### FixMe: think random_march and matrix are the same
    # makes the strand of pixels show random_march
    # random_march( delay, cycles)
    random_march(0.25, 256) 
    time.sleep(wait_time)

    # makes the strand of pixels show matrix
    # matrix(random_percent, delay, cycles)
    matrix(10, 0.25, 500) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow_fade
    # rainbow_fade(delay, cycles):
    rainbow_fade(.02, 256) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow_loop
    # rainbow_loop(delay, step, cycles):
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(wait_time*2)
    rainbow_loop(0.01, 10, 1000) 
    time.sleep(wait_time)

    # makes the strand of pixels show rainbow
    # rainbow(delay, step, cycles):
    pixels.fill((255, 255, 0))
    pixels.show()
    time.sleep(wait_time*2)
    rainbow(0.01, 10, 2) 
    time.sleep(wait_time)

    # makes the strand of pixels show random_burst
    # rgb_propeller(LoopCount)
    pixels.fill((0, 0, 0))
    rgb_propeller(1000)
    time.sleep(wait_time)

    # makes the strand of pixels show random_burst
    # random_burst(delayStart, delayEnd , LoopCount)
    pixels.fill((0, 0, 0))
    random_burst(0.005, .2, 100)
    time.sleep(wait_time)



    #   twinkle(leds);


    #   candycane();


    #   if (!USE_LEVEL_ANIMATIONS) incrementState();
    #   adjdelay = (adjdelay < 100) ? 100 : adjdelay;
    #   demoStateCountdown -= 15;
    #   random_levels();


    #   if (!USE_LEVEL_ANIMATIONS) incrementState();
    #   rainbow();
    #   adjdelay = (adjdelay < 50) ? 50 : adjdelay;
    #   if (demoMode) demoStateCountdown -= 600;
    #   drain();
    #   pancake();



