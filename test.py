from time import sleep
import RPi.GPIO as GPIO

GPIO_ports = [22, 23, 24, 27, 25]

GPIO.setmode(GPIO.BOARD)

for i in range(no_of_sensors):
    GPIO.setup(GPIO_ports[i], GPIO.OUT)
    print(f"Setting GPIO: {GPIO_ports[i]} to low")
    GPIO.output(GPIO_ports[i], GPIO.LOW)
    sleep(0.1)

while True:
    for i in range(no_of_sensors):
        GPIO.output(GPIO_ports[i], GPIO.HIGH)
        print("Port: ", GPIO_ports[i], " is HIGH")
        sleep(1)
        GPIO.output(GPIO_ports[i], GPIO.LOW)
        print("Port: ", GPIO_ports[i], " is LOW")
        sleep(1)
