import os
from random import randint
from time import sleep, time
import busio
import board
import numpy as np
import adafruit_vl53l0x
import RPi.GPIO as GPIO
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import argparse
import imutils
import cv2
import sys
import requests

# -----------------------CONVEYOR BELT----------------------------------
# CONVEYOR BELT
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
# -------------------------------------------------------------------

# -----------------------TOF SENSORS----------------------------------
# TOF SENSORS
print("Initializing TOF sensors ...")
i2c = busio.I2C(board.SCL, board.SDA)
print("Initializing TOF sensors ...")
sensor1 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2b)
print("Initializing TOF sensors ...")
sensor2 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2c)
print("Initializing TOF sensors ...")
sensor3 = adafruit_vl53l0x.VL53L0X(i2c, address=0x2d)
print("Initializing TOF sensors ...")
total1, total2, total3 = 62.74, 65.65, 63.53
print("Initializing TOF sensors ...")
window_size = 10
print("Initializing TOF sensors ...")
maximum_distance = float('-inf')
print("Initializing TOF sensors ...")
sleep(0.1)
# -------------------------------------------------------------------

# -----------------------LOAD CELL----------------------------------
# LOAD CELL
print("Initializing Load cell ...")
def get_weight():
    return 3.0
sleep(0.1)
# -------------------------------------------------------------------


# -----------------------SEND DATA----------------------------------
# SEND DATA
print("Initializing Send Data ...")
def send_dimensions():
    pass
sleep(0.1)
# -------------------------------------------------------------------



# -----------------------CAMERA----------------------------------
# CAMERA
print("Initializing Camera ...")

sleep(0.1)


def discard_outlier(dimA, dimB) -> bool:
    if dimA > 60 or dimB > 60:
        return True
    if abs(dimA - dimB) >= 0.8 * max(dimA, dimB):
        return True
    return False


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def capture_image():
    cap = cv2.VideoCapture("raspistill -o -")
    if not cap.isOpened():
        print("Error opening camera ...")
        sys.exit(1)
    ret, frame = cap.read()
    if not ret:
        print("Error capturing image...")
        sys.exit(1)
    return frame


def get_object_size(image, distance_bet_cam_obj, height_of_camera, pixel_per_metric):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)

    d0 = height_of_camera
    d1 = distance_bet_cam_obj

    max_dim_A = float('-inf')
    max_dim_B = float('-inf')

    for c in cnts:
        if cv2.contourArea(c) < 100:
            continue

        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        box = perspective.order_points(box)

        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        pixelsPerMetric = round(pixel_per_metric, 4)

        dimA = (dA * d1) / (pixelsPerMetric * d0)
        dimB = (dB * d1) / (pixelsPerMetric * d0)

        if check_outlier(dimA, dimB):
            continue

        max_dim_A = max(max_dim_A, dimA)
        max_dim_B = max(max_dim_B, dimB)

    return {"length": max(max_dim_A, max_dim_B), "breadth": min(max_dim_A, max_dim_B)}


def get_length_width(image, height):

    height_of_camera = 57.7
    object_to_camera = height_of_camera - height
    pixel_per_metric = 45
    object_size = get_object_size(image,
                                  object_to_camera, height_of_camera, pixel_per_metric)
    return object_size["length"], object_size["breadth"]

sleep(0.5)
# -------------------------------------------------------------------


# -----------------------MAIN----------------------------------

print("Stopping Conveyer Belt ...")
stop()

print("<---------------------Welcome To Grow-Simplee Tool------------------------->\n\n")

while True:
    print("Please start inserting Similar Items into the tool\n")
    input("Press Enter to continue...")
    print("Starting Conveyer Belt ...")
    start()
    items_info = []

    if not out_config():
        print("Please Clear the Conveyer Belt ...")
        continue

    while True:

        while not in_config():
            pass

        print("Item Detected ...")
        max_height = float('-inf')
        image = None
        while (max_height <= 0) or (not out_config()):
            if converyer.centre_config() and image is None:
                print("Stopping Conveyer Belt For Image ...")
                stop()
                image = capture_image()
                print("Starting Conveyer Belt after Image ...")
                start()
            max_height = max(max_height, get_height())

        # if max_height <= 0:
        #     print("Error in Height. Please Check the Object ...")
        #     print("Starting Conveyer Belt ...")
        #     start()
        #     continue

        try:
            length, width = get_length_width(image, max_height)
            assert length > 0 and width > 0
        except:
            print("Error in dimensions. Please Check the Object ...")
            print("Starting Conveyer Belt ...")
            start()
            continue

        # Just because we do not have a Bar Code Scanner
        item_id = input("Please Enter Item ID: ")

        item_info = {
            "length": length,
            "breadth": width,
            "height": max_height,
            "weight": get_weight(),
        }

        items_info.append(item_info)

        print("Item Removed ...")
        yes_no = input("1. Continue similar objects (y / n). \n ")
        if yes_no == 'n':
            print("Sending Data to Server ...")
            print(items_info)
            print("Sent info to Server...")
            break

        sleep(0.05)
    sleep(0.05)
