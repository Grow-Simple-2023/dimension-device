from time import sleep
import RPi.GPIO as GPIO

no_of_sensors = 3
GPIO.setmode(GPIO.BCM)
GPIO_ports = [22, 23, 24, 27, 25]


for i in range(no_of_sensors):
    GPIO.setup(GPIO_ports[i], GPIO.OUT)
    GPIO.output(GPIO_ports[i], GPIO.LOW)
    print(f"Set GPIO {GPIO_ports[i]} to LOW")
    sleep(0.1)
