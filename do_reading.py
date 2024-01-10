import temp
import flow
import datetime
import sqlite3

def thermal_power(t1, t2, f):
    """
    t1 in C
    t2 in C
    f in g/sec

    returns:
    power in J/s = W
    """

    cp = 4.326 # J/g/K
    power = (t1-t2) * f * cp # in J/s = W
    return power


temp_sensor1_id = '28-3ce1d4438ff7'
temp_sensor2_id = '28-3ce1d4432b6f'

ts1 = temp.TempSensor(temp_sensor1_id)
ts2 = temp.TempSensor(temp_sensor2_id)

now = datetime.datetime.now()
t1 = ts1.temp()
t2 = ts2.temp()

f = flow.get_flow() # in g/sec

power = thermal_power(t1, t2, f)

row = { 'timestamp': now,
        'temp1': round(t1, 2),
        'temp2': round(t2, 2),
        'flow': round(f, 2),
        'power': round(power, 2)}

conn = sqlite3.connect('/home/griessbaum/solarthermal/solarthermal.db')
cursor = conn.cursor()

cursor.execute('''INSERT INTO solarthermal (timestamp, temp1, temp2, flow, power)
                VALUES (:timestamp, :temp1, :temp2, :flow, :power)''',
               row)
conn.commit()
conn.close()

print(row)
