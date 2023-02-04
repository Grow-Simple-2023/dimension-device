import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
no_of_sensors = 3


for i in range(no_of_sensors):
    GPIO.setup(GPIO_ports[i], GPIO.OUT)
    GPIO.output(GPIO_ports[i], GPIO.LOW)
