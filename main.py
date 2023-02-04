import time
import board
import busio
import adafruit_vl53l0x

i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)

while True:
    range1 = sensor1.range
    range2 = sensor2.range
    range3 = sensor3.range
    print("Sensor 1:", range1/10, "cm")
    print("Sensor 2:", range2/10, "cm")
    print("Sensor 3:", range3/10, "cm")
    time.sleep(1)
