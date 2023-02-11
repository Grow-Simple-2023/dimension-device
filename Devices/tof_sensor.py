import busio
import board
import numpy as np
from time import sleep
import adafruit_vl53l0x
from time import sleep, time
# from background import reset, init

print("Initializing TOF sensors ...")

i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)
sensor4 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2e)

sleep(0.1)


def get_average(sensor, window_size):
    window = []
    for i in range(window_size):
        window.append(sensor.range)
        sleep(0.01)
    return np.mean(window)


def get_height():
    total1, total2, total3, total4 = 61.388999999999996, 65.233, 63.222, 62.84400000000001
    window_size = 5
    maximum_distance = float('-inf')
    distance1 = total1 - get_average(sensor1, window_size)/10
    distance2 = total2 - get_average(sensor2, window_size)/10
    distance3 = total3 - get_average(sensor3, window_size)/10
    distance4 = total4 - get_average(sensor4, window_size)/10
    print("---------------------------------")
    print("Sensor 1:", distance1, "cm")
    print("Sensor 2:", distance2, "cm")
    print("Sensor 3:", distance3, "cm")
    print("Sensor 4:", distance4, "cm")
    print("---------------------------------")
    maximum_distance = max(
        [distance1, distance2, distance3, distance4, maximum_distance])
    print("Maximum distance:", maximum_distance, "cm")
    return maximum_distance
