### Sample python code for NeoPixels on Raspberry Pi
### this code is ported from Arduino NeoPixels effects in C++, from https://github.com/zatamite/Neopixel-heartbeat
### orginal code: https://github.com/zatamite/Neopixel-heartbeat/blob/master/neoheart/neoheart.ino


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



    # makes the strand of pixels show random_levels
    # pancake(level, delay)
    pixels.fill((0, 0, 0))
    time.sleep(wait_time)


  // all pixels show the same color:
  redo =random(255);
  greeno = random(255);
  blueo = random (255);
      strip.setPixelColor(0, redo, greeno, blueo);
      strip.setPixelColor(1, redo, greeno, blueo);
      strip.setPixelColor(2, redo, greeno, blueo);
      
      strip.show();
      delay (20);
      
   int x = 3;
   for (int ii = 1 ; ii <252 ; ii = ii = ii + x){
     strip.setBrightness(ii);
     strip.show();              
     delay(5);
    }
    
    x = 3;
   for (int ii = 252 ; ii > 3 ; ii = ii - x){
     strip.setBrightness(ii);
     strip.show();              
     delay(3);
     }
   delay(10);
   
   x = 6;
  for (int ii = 1 ; ii <255 ; ii = ii = ii + x){
     strip.setBrightness(ii);
     strip.show();              
     delay(2);  
     }
   x = 6;
   for (int ii = 255 ; ii > 1 ; ii = ii - x){
     strip.setBrightness(ii);
     strip.show();              
     delay(3);
   }
  delay (50); 


