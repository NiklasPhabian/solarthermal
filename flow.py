#!/usr/bin/python
import RPi.GPIO as GPIO
import time, sys

flow_sensor_gpio = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_sensor_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global count
count = 0

def countPulse(channel):
   global count
   if start_counter == 1:
      count = count+1

GPIO.add_event_detect(flow_sensor_gpio, GPIO.FALLING, callback=countPulse)

while True:
    try:
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        flow = (count / 7.5) # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        print("The flow is: %.3f Liter/min" % (flow))
        count = 0
        time.sleep(1)
    except KeyboardInterrupt:
        print('\nkeyboard interrupt!')
        GPIO.cleanup()
        sys.exit()
