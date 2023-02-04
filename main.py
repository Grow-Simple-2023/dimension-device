import time
import board
import busio
import adafruit_vl53l0x

i2c = busio.I2C(board.SCL, board.SDA)

sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)

r1_avg, r2_avg, r3_avg = 0, 0, 0

for _ in range(100):
    r1_avg += sensor1.range/10
    r2_avg += sensor2.range/10
    r3_avg += sensor3.range/10
    # print("Sensor 1:", range1/10, "cm")
    # print("Sensor 2:", range2/10, "cm")
    # print("Sensor 3:", range3/10, "cm")
    time.sleep(0.05)

acch = 57.7

print("Sensor 1:", r1_avg/100, "cm")
print("Sensor 2:", r2_avg/100, "cm")
print("Sensor 3:", r3_avg/100, "cm")
