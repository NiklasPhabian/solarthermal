#!/usr/bin/python
import RPi.GPIO as GPIO
import time, sys

flow_sensor_gpio = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(flow_sensor_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0
counting = True

def countPulse(channel):
    global count
    global counting
    if counting:
        count = count+1

GPIO.add_event_detect(flow_sensor_gpio, GPIO.FALLING, callback=countPulse)

wait_time = 2
def get_flow():
    global count
    global counting
    count = 0
    counting = True
    time.sleep(wait_time)
    counting = False
    flow = count / 7.5 / wait_time # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
    flow = flow / 60 * 1000 # flow in g/seconds
    return flow


if __name__ == '__main__':
    while True:
        try:
            flow = get_flow()
            print("The flow is: %.3f g/sec" % (flow))
            count = 0
            time.sleep(1)
        except KeyboardInterrupt:
            print('\nkeyboard interrupt!')
            GPIO.cleanup()
            sys.exit()

