import os
import time

temp_sensor1_id = '28-3ce1d44312b4'
temp_sensor2_id = '28-3ce1d4432b6f'


class TempSensor():
    def __init__(self, serial):
        self.temp_sensor = f'/sys/bus/w1/devices/{serial}/w1_slave'

    def temp(self):
        with open(self.temp_sensor, 'r') as tmpfile:
            temp = float(tmpfile.readlines()[1][-6:-1])/1000
        return temp


ts1 = TempSensor(temp_sensor1_id)
ts2 = TempSensor(temp_sensor2_id)

if __name__ == '__main__':
    while True:
        #t1 = ts1.temp()
        t2 = ts2.temp()
        #print(f'T1: {t1:.2f} C. T2: {t2:.2f} C.')
        print(f'T2: {t2:.2f} C.')

        time.sleep(1)
