import os
import time

temp_sensor1_id = '28-3ce1d4438ff7'
temp_sensor2_id = '28-3ce1d4432b6f'
temp_sensor3_id = '28-3ce1d44312b4'


class TempSensor():
    def __init__(self, serial):
        self.temp_sensor = f'/sys/bus/w1/devices/{serial}/w1_slave'

    def temp(self):
        with open(self.temp_sensor, 'r') as tmpfile:
            last_line = tmpfile.readlines()[-1]
            temp = float(last_line.split('=')[-1]) / 1000            
        return temp



ts1 = TempSensor(temp_sensor1_id)
ts2 = TempSensor(temp_sensor2_id)
ts3 = TempSensor(temp_sensor3_id)

if __name__ == '__main__':
    while True:
        t1 = ts1.temp()
        t2 = ts2.temp()
        t3 = ts3.temp()
        print(f'T1: {t1:.2f} C. T2: {t2:.2f} C. T3: {t3:.2f} C.')        

        time.sleep(1)
