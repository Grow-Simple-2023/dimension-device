import RPi.GPIO as GPIO

sensor_pins = [40, 37]

GPIO.setmode(GPIO.BCM)

for pin in sensor_pins:
    GPIO.setup(sensor_pins[i], GPIO.IN)

conveyer_ports = [36, 38]
for pin in converyer_ports:
    GPIO.setup(sensor_pins[i], GPIO.OUT)


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
    pass


def stop() -> None:
    GPIO.output(conveyer_ports[0], GPIO.LOW)
    GPIO.output(conveyer_ports[1], GPIO.HIGH)
    pass
