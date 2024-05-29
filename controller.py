import RPi.GPIO as GPIO
import datetime

class Controller:
    
    def __init__(self, cursor=None):
        self.channel = 22
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)
        self.pump_on = None
        self.cursor = cursor

    def get_state(self):
        query = 'SELECT pump FROM solarthermal ORDER BY timestamp DESC LIMIT 1'
        self.cursor.execute(query)
        self.pump_on = bool(self.cursor.fetchone()[0])

    def get_seconds_since_on(self):
        query = 'SELECT timestamp FROM solarthermal WHERE pump=1 ORDER BY timestamp DESC LIMIT 1'
        self.cursor.execute(query)
        last_time_on = self.cursor.fetchone()[0]
        last_time_on = datetime.datetime.strptime(last_time_on, '%Y-%m-%d %H:%M:%S.%f')
        self.seconds_since_on = (datetime.datetime.now()-last_time_on).total_seconds()

    def control(self, power, t_ambient):
        if power < -10:
            print("Negative power. Turning off")
            self.turn_off()
        elif t_ambient < 5:
            print("Ambient temp below 5 C. Turning off")
            self.turn_off()
        elif self.pump_on==False and self.seconds_since_on > 60*60:
            print("Wait expired. Turning on")
            self.turn_on()
    
    def turn_off(self):
        self.pump_on = False
        GPIO.output(self.channel, GPIO.LOW)
    
    def turn_on(self):
        self.pump_on = True
        GPIO.output(self.channel, GPIO.HIGH)