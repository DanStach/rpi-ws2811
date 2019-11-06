import serial
import time
import RPi.GPIO as GPIO
ChannelPin1 = 4
ChannelPin2 = 17
ChannelPin3 = 27
ChannelPin4 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ChannelPin1,GPIO.OUT)
GPIO.setup(ChannelPin2,GPIO.OUT)
GPIO.setup(ChannelPin3,GPIO.OUT)
GPIO.setup(ChannelPin4,GPIO.OUT)

print("init all off")
GPIO.output(ChannelPin1,GPIO.HIGH)
GPIO.output(ChannelPin2,GPIO.HIGH)
GPIO.output(ChannelPin3,GPIO.HIGH)
GPIO.output(ChannelPin4,GPIO.HIGH)
time.sleep(3)


print("LED on")
GPIO.output(ChannelPin1,GPIO.LOW)
time.sleep(3)
print("LED off")
GPIO.output(ChannelPin1,GPIO.HIGH)
time.sleep(2)

print("LED on")
GPIO.output(ChannelPin2,GPIO.LOW)
time.sleep(3)
print("LED off")
GPIO.output(ChannelPin2,GPIO.HIGH)
time.sleep(2)

print("LED on")
GPIO.output(ChannelPin3,GPIO.LOW)
time.sleep(3)
print("LED off")
GPIO.output(ChannelPin3,GPIO.HIGH)
time.sleep(2)

print("LED on")
GPIO.output(ChannelPin4,GPIO.LOW)
time.sleep(3)
print("LED off")
GPIO.output(ChannelPin4,GPIO.HIGH)
time.sleep(2)

GPIO.cleanup()