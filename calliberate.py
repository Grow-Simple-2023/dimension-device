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

total1, total2, total3 = 62.74, 65.65, 63.53
window_size = 20


while True:
    distance1 = get_average(sensor1, window_size)
    sleep(0.5)
    distance2 = get_average(sensor2, window_size)
    sleep(0.5)
    distance3 = get_average(sensor3, window_size)
    sleep(0.5)
    print("---------------------------------")
    print("Sensor 1:", total1 - distance1/10, "cm")
    print("Sensor 2:", total2 - distance2/10, "cm")
    print("Sensor 3:", total3 - distance3/10, "cm")
    print("---------------------------------")
    break
    # os.system('cls' if os.name == 'nt' else 'clear')
