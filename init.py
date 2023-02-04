from time import sleep
import board
import RPi.GPIO as GPIO
from adafruit_vl53l0x import VL53L0X

i2c = board.I2C()
device = VL53L0X(i2c)


no_of_sensors = 3
GPIO_ports = [22, 23, 24, 27, 25]

# GPIO.setmode(GPIO.BOARD)

for i in range(no_of_sensors):
    GPIO.setup(GPIO_ports[i], GPIO.OUT)
    print(f"Setting GPIO: {GPIO_ports[i]} to low")
    GPIO.output(GPIO_ports[i], GPIO.LOW)
    sleep(0.1)

for i in range(no_of_sensors):
    GPIO.output(GPIO_ports[i], GPIO.HIGH)
    print(f"Setting Sensor Address to: {0x29+i}")
    device.set_address(0x29+i)
    GPIO.output(GPIO_ports[i], GPIO.LOW)
    sleep(0.1)
