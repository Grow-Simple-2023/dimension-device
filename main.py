from time import sleep
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
    return np.mean(window)


i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)

# off1, off2, off3 = 4.977, 8.135, 5.637
# sensor_height = 57.7

total1, total2, total3 = 50.296, 53.157, 50.341

window_size = 10


while True:
    distance1 = get_average(sensor1, window_size)
    sleep(0.5)
    distance2 = get_average(sensor2, window_size)
    sleep(0.5)
    distance3 = get_average(sensor3, window_size)
    sleep(0.5)
    print("---------------------------------")
    print("Sensor 1:", max(total1 - distance1/10, 0), "cm")
    print("Sensor 2:", max(total2 - distance2/10, 0), "cm")
    print("Sensor 3:", max(total3 - distance3/10, 0), "cm")
    print("---------------------------------")
    # os.system('cls' if os.name == 'nt' else 'clear')
