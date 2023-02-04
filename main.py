import time
import board
import busio
import adafruit_vl53l0x

i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)

off1, off2, off3 = 4.977, 8.135, 5.637


while True:
    range1 = sensor1.range - off1*10
    range2 = sensor2.range - off2*10
    range3 = sensor3.range - off3*10
    print("Sensor 1:", max(range1/10, 0), "cm")
    print("Sensor 2:", max(range2/10, 0), "cm")
    print("Sensor 3:", max(range3/10, 0), "cm")
    time.sleep(1)
