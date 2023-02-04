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
    GPIO.output(GPIO_ports[i], GPIO.LOW)

for i in range(no_of_sensors):
    GPIO.output(GPIO_ports[i], GPIO.HIGH)
    device.set_address(0x30+i)
    GPIO.output(GPIO_ports[i], GPIO.LOW)
