import temp
import flow
import datetime
import sqlite3
import controller

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
temp_sensor3_id = '28-3ce1d44312b4'

ts1 = temp.TempSensor(temp_sensor1_id)
ts2 = temp.TempSensor(temp_sensor2_id)
ts3 = temp.TempSensor(temp_sensor3_id) # Ambient

now = datetime.datetime.now()
t1 = ts1.temp()
t2 = ts2.temp()
t3 = ts3.temp()

f = flow.get_flow() # in g/sec

power = thermal_power(t1, t2, f)

conn = sqlite3.connect('/home/griessbaum/solarthermal/solarthermal.db')
cursor = conn.cursor()

# controller will read the state it has been in for the previous step
cont = controller.Controller(cursor)
cont.control(power=power, t_ambient=t3)

row = { 'timestamp': now,
        'temp1': round(t1, 2),
        'temp2': round(t2, 2),
        'temp3': round(t3, 2),
        'flow': round(f, 2),
        'power': round(power, 2),
        'pump': cont.pump_on}


cursor.execute('''INSERT INTO solarthermal (timestamp, temp1, temp2, temp3, flow, power, pump)
                VALUES (:timestamp, :temp1, :temp2, :temp3, :flow, :power, :pump)''',
               row)

# Decide if we should turn on or off

conn.commit()
conn.close()

print(row)
