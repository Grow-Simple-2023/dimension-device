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
sensor4 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2e)

window_size = 20

while True:
    distance1 = get_average(sensor1, window_size)
    sleep(0.2)
    distance2 = get_average(sensor2, window_size)
    sleep(0.2)
    distance3 = get_average(sensor3, window_size)
    sleep(0.2)
    distance4 = get_average(sensor4, window_size)
    sleep(0.2)
    print(f'{distance1/10},{distance2/10},{distance3/10},{distance4/10}')
    # print("---------------------------------")
    # print("Sensor 1:", total1 - distance1/10, "cm")
    # print("Sensor 2:", total2 - distance2/10, "cm")
    # print("Sensor 3:", total3 - distance3/10, "cm")
    # print("---------------------------------")
    break
    # os.system('cls' if os.name == 'nt' else 'clear')

# [0, 5, 10, 15, 20, 25, 30, 57.7, 51.7, 46.7, 41.7, 36.7, 31.7]

# [[-0.024, -0.12, 0.07], [3.985, 2.84, 6.335], [9.155, 7.865, 11.38], [14.545, 14.595, 17.125],
#     [22.89, 20.945, 22.745], [27.78, 26.685, 27.99], [33.4, 32.47, 33.345]]

# [[56.92, 57.035, 57.39], [51.95, 51.51, 51.915], [47.145, 45.815, 46.895],
#     [40.26, 40.29, 40.85], [34.44, 34.025, 34.825], [28.715, 28.16, 29.88]]
