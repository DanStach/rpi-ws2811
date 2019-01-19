# install process for rpi-ws2811
code need to run the xmas lights ws2811 on a raspberry pi

## Install Process

### install OS
- install raspbain os
- run in terminal:
  - sudo apt-get update
  - sudo apt-get upgrade

### install I2C
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
- tool install need, run in terminal:
  - sudo apt-get install -y python-smbus
  - sudo apt-get install -y i2c-tools
- configure options
  - sudo raspi-config
  - select "Interfacing Options" --> "I2C" --> "yes" --> "ok"
  - sudo reboot
  - <after reboot>
  - sudo i2cdetect -y 1
    - "This shows that two I2C addresses are in use – 0x40 and 0x70."

### install python
- sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
### install previous work in the repo
- sudo git clone https://github.com/DanStach/rpi-ws2811.git

