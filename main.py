from time import sleep, time
import board
import os
import busio
import numpy as np
import adafruit_vl53l0x


def get_average(sensor, window_size):
    window = []
    for i in range(window_size):
        window.append(sensor.range)
        sleep(0.01)
    return np.max(window)


i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)

# off1, off2, off3 = 4.977, 8.135, 5.637
# sensor_height = 57.7

total1, total2, total3 = 50.296, 53.157, 50.341

window_size = 10

max_time = 10
start = time()

maximum_distance = float('-inf')
print("Collecting Data")

while time()-start < max_time:
    distance1 = total1 - get_average(sensor1, window_size)/10
    distance2 = total2 - get_average(sensor2, window_size)/10
    distance3 = total3 - get_average(sensor3, window_size)/10
    print("---------------------------------")
    print("Sensor 1:", distance1, "cm")
    print("Sensor 2:", distance2, "cm")
    print("Sensor 3:", distance3, "cm")
    print("---------------------------------")
    maximum_distance = max([distance1, distance2, distance3, maximum_distance])
    print("Maximum distance:", maximum_distance, "cm")
    sleep(0.1)
    # os.system('cls' if os.name == 'nt' else 'clear')

