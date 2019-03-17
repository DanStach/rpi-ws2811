# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random
import math
import serial
import ctypes

from neopixelpart1 import *



# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)


while True:
    random.seed(num_pixels)

    ###################################################
    ###  Part1  
    ###################################################

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
    
    # makes the strand of pixels show BouncingBalls
    # BouncingColoredBalls(BallCount, colors[][3], LoopCount) 
    BouncingColoredBalls(3, ((255,0,0),(0,255,0),(0,0,255)), 1000)
    time.sleep(wait_time)
    
    # makes the strand of pixels show BouncingBalls
    # BouncingBalls(red, green, blue, BallCount, LoopCount) 
    BouncingBalls(255, 0, 0, 3, 1000) 
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
    FireCustom(0, 12, 25, 0, 10, 0.02, 1, 2, 500) # blue fire
    time.sleep(wait_time)
    FireCustom(0, 12, 25, 0, 10, 0.02, 2, 2, 500) # green fire
    time.sleep(wait_time)



    # makes the strand of pixels show Fire
    # Fire(Cooling, Sparking, SpeedDelay, LoopCount)
    Fire(55, 120,0.015, 100)
    time.sleep(wait_time)
    
    # makes the strand of pixels show 
    # meteorRain(red, green, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, LoopCount, SpeedDelay)
    meteorRain(255, 255, 255, 10, 64, True, 1, 0.030)
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChaseRainbow
    # theaterChaseRainbow(SpeedDelay)
    theaterChaseRainbow(.4)
    time.sleep(wait_time)

    # makes the strand of pixels show theaterChase
    # theaterChase(red, green, blue, cycles, SpeedDelay)
    theaterChase(255,0,0, 20, 0.4)
    time.sleep(wait_time)

    # makes the strand of pixels show colorWipe (green)
    # colorWipe(red, green, blue, SpeedDelay)
    colorWipe(0,255,0, 0.05)

    # makes the strand of pixels show RunningLights (red)
    # RunningLights(red, green, blue, WaveDelay)
    RunningLights(255,0,0, 0.05)

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

    # makes the strand of pixels show Twinkle
    # Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne)
    Twinkle(255, 0, 0, 10, 0.1, False)

    # makes the strand of pixels show NewKITT 
    # NewKITT(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    NewKITT(255, 0, 0, 4, 0.010, 0.050)
    time.sleep(wait_time)

    # makes the strand of pixels show CylonBounce
    # CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    CylonBounce(255, 0, 0, 2, 0.010, 0.050)
    time.sleep(wait_time)

    # make the strand of pixels show HalloweenEyes
    # HalloweenEyes(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause)
    HalloweenEyes(255, 0, 0, 1, 1, True, 10, 1, 3)
    time.sleep(wait_time)

    # make all pixels stobe (white)
    # Strobe(red, green, blue, StrobeCount, FlashDelay, EndPause)
    Strobe(255, 255, 255, 10, .050, 1)
    time.sleep(wait_time)


    # fade in/out a single color (red / green / blue / white)
    # FadeInOut(red, green, blue, delay)
    FadeInOut(255, 0, 0, 0.01)
    FadeInOut(0, 255, 0, 0.01)
    FadeInOut(0, 0, 255, 0.01)
    FadeInOut(255, 255, 255, 0.01)

    # loops red green blue
    # RGBLoop(delay)
    RGBLoop(0.01)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(wait_time)

    # rainbow cycle
    # rainbow cycle with 1ms delay per step, 5 cycles
    # rainbow_cycle(delay, cycles) 
    rainbow_cycle(0.001, 5) 
    time.sleep(wait_time)

    ###################################################
    ###  Part2   
    ###################################################

    # makes the strand of pixels show random_levels
    # pancake(level, delay)
    pixels.fill((0, 0, 0))
    time.sleep(wait_time)
    pancake(8, 0.5)
    time.sleep(wait_time)

    # makes the strand of pixels show drain
    # drain(level, delay)
    drain(8, 0.5)
    time.sleep(wait_time)

    # makes the strand of pixels show random_levels
    # random_levels( NUM_LEVELS, delay, cycles )
    #random_levels(12, 0, 500)
    random_levels(8, 0.1, 500)
    time.sleep(wait_time)

    # makes the strand of pixels show candycane
    # candycane(delay, cycles)
    candycane(0, 500) 
    time.sleep(wait_time)

    # makes the strand of pixels show twinkle
    # twinkle(delay, cycles)
    twinkle(0.005, 100) 
    time.sleep(wait_time)

    # makes the strand of pixels show loop5
    # loop5( delay, cycles)
    #loop5(0.25, 500) 
    #time.sleep(wait_time)

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
