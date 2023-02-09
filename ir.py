from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
print("Initializing Conveyor ...")
sensor_pins = [16, 20, 21, 26, 19]

for pin in sensor_pins:
    print("Setting up pin in sensor: ", pin)
    GPIO.setup(pin, GPIO.IN)


while True:
    out_put_array = [GPIO.input(pin) for pin in sensor_pins]
    print(out_put_array)
    sleep(0.1)