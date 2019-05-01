# rpi-ws2811
This project has the goal completing all the coding needed use ws2811 neopixel lights using a raspberry pi, for my xmas tree. most neopixels effects are written in C++, however i was only able to use a rpi with my ws2811 using python. I am porting all the c++ examples to python. 

### Neopixel effects example sites:
- Part1: https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/ 
  - [link to converted examples](https://github.com/DanStach/rpi-ws2811/blob/master/neopixel-part1.py)
  - [link to youtube examples](https://www.youtube.com/playlist?list=PLR6vpg1z3g54VD0OQa2YCt2Ik6PuQkrXO)
- Part2: https://pastebin.com/Qe0Jttme
- Part3: https://github.com/zatamite/Neopixel-heartbeat/blob/master/neoheart/neoheart.ino
- Part4: https://github.com/FastLED/FastLED/tree/master/examples

### Install Instuctions
simple install instuctions are located on install.md

full install tutorials:
 - https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
 - https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/
 - https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
 
### Hardware Considerations
- RPI 3b 
  - SD = 16gb, Ram = 1gb,  CPU = 4× 1.2GHz
  - OS = Raspbian
  - neopixel = 50 WS2811 (powered from RPI +5v pinout)
- RPI - 0W
  - pending...
- 6.5ft tree
- 300 programmable led (WS2811)
- 2 power supplies (each 5volt/10Amp)
