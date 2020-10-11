# install process for rpi-ws2811
this is the simplified install process needed to run the xmas lights ws2811 on a raspberry pi
refernce to full instuctions: https://learn.adafruit.com/neopixels-on-raspberry-pi/overview

## Hardware Install Process
Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18 NeoPixels must be connected to D10, D12, D18 or D21 to work. I prefer  D12 (pin12)
https://pinout.xyz/pinout/pin12_gpio18
 - connect neopixels to pins
    - 5V (Pin2)
    - Ground (Pin 6)
    - Data (Pin 12)
    

## Software Install Process

### install OS
- install raspbain os
- run in terminal:
  - `sudo apt-get update`
  - `sudo apt-get upgrade`

### install I2C
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
- tool install need, run in terminal:
  - `sudo apt-get install -y python-smbus`
  - `sudo apt-get install -y i2c-tools`
- configure options
  - `sudo raspi-config`
  - select Interfacing Options --> I2C--> yes --> ok
  - `sudo reboot`
  - after reboot
  - `sudo i2cdetect -y 1`
    - This shows that two I2C addresses are in use – 0x40 and 0x70.
    - i see the graph, but no in use`
  -  `ls /dev/i2c*`
     - see the responce "/dev/i2c-1"

### install SPI
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-spi
- configure options
  - `sudo raspi-config`
  - select Interfacing Options --> SPI --> yes --> ok
  - `sudo reboot`
  - after reboot
  - `ls -l /dev/spidev*`
    - you should see two 'devices' one for each SPI bus
    ```
     /dev/spidev0.0
     /dev/spidev0.1
    ```

### Enabling Second SPI
add code to file  /boot/config.txt 
- `sudo nano /boot/config.txt`
- "add to bottom of file"
```
 # Enabling Second SPI
 dtoverlay=spi1-3cs
``` 
- cntl + x
- y
- enter
- `sudo reboot`
- after reboot
- `ls -l /dev/spidev*`
    - you should see 5 devices one for each SPI bus
    ```
    /dev/spidev0.0
    /dev/spidev0.1
    /dev/spidev1.0
    /dev/spidev1.1
    /dev/spidev1.2
    ```
  
### install python and pip
- `sudo python3 -V`
- verify verion 3 (Python 3.5.3)
- `sudo apt-get install -y python3-pip`
- `sudo apt-get install build-essential libssl-dev libffi-dev python-dev`

### Install Python libraries
- `sudo pip3 install RPI.GPIO`
- `sudo pip3 install adafruit-blinka`
- `sudo pip3 install --upgrade adafruit_blinka`


- "test python and libaries are working
- `sudo nano blinkatest.py`
- add code to file
    ```python
    import board
    import digitalio
    import busio

    print("Hello blinka!")

    # Try to great a Digital input
    pin = digitalio.DigitalInOut(board.D4)
    print("Digital IO ok!")
    # Try to create an I2C device
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C ok!")
    # Try to create an SPI device
    spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
    print("SPI ok!")
    print("done!")
    ```
- cntl + x
- y
- enter
- `sudo python3 blinkatest.py`
- you should see the following
```
Hello blinka!
Digital IO ok!
I2C ok!
SPI ok!
done!
```
### install python
- `sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`
- `sudo pip3 install pyserial`
### install previous work in the repo
- `sudo apt install git`
- `sudo git clone https://github.com/DanStach/rpi-ws2811.git`

