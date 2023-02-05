from time import sleep
import RPi.GPIO as GPIO
print("Initializing Conveyor ...")


sensor_pins = [40, 37]


for pin in sensor_pins:
    print("Setting up pin in sensor: ", pin)
    GPIO.setup(pin, GPIO.IN)

conveyer_ports = [36, 38]
for pin in converyer_ports:
    print("Setting up pin in coveyor: ", pin)
    GPIO.setup(pin, GPIO.OUT)

sleep(0.1)


def in_config() -> bool:
    out_put_array = [GPIO.input(pin) for pin in sensor_pins]
    return out_put_array[0] == 1 and out_put_array[1] == 0


def centre_config() -> bool:
    out_put_array = [GPIO.input(pin) for pin in sensor_pins]
    return out_put_array[1] == 1


def out_config() -> bool:
    out_put_array = [GPIO.input(pin) for pin in sensor_pins]
    return out_put_array[0] == 0 and out_put_array[1] == 0


def start() -> None:
    GPIO.output(conveyer_ports[1], GPIO.LOW)
    GPIO.output(conveyer_ports[0], GPIO.HIGH)
    return


def stop() -> None:
    GPIO.output(conveyer_ports[0], GPIO.LOW)
    GPIO.output(conveyer_ports[1], GPIO.HIGH)
    return
