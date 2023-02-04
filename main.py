import time
import board
import busio
import numpy as np
import adafruit_vl53l0x


def get_average(sensor, window_size):
    window = []
    for i in range(window_size):
        window.append(sensor.range)
        sleep(0.05)
    return np.mean(window)
    

i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)

off1, off2, off3 = 4.977, 8.135, 5.637
sensor_height = 57.7

window_size = 10


while True:
    distance1 = get_average(sensor1, window_size)
    distance2 = get_average(sensor2, window_size)
    distance3 = get_average(sensor3, window_size)

    
    print("Sensor 1:", distance1/10, "cm")
    print("Sensor 2:", distance2/10, "cm")
    print("Sensor 3:", distance3/10, "cm")
    time.sleep(1)
